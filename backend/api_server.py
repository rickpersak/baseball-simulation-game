# File: backend/api_server.py
import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from world_generator import create_new_world
from sim_engine import simulate_game

SAVES_FOLDER = "saves"
app = Flask(__name__)
CORS(app) 

def get_db_connection(save_name):
    path = os.path.join(SAVES_FOLDER, f"{save_name}.db")
    if not os.path.exists(path): return None
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

# --- Existing Save Management Endpoints (Unchanged) ---
@app.route("/api/saves", methods=['GET'])
def get_save_games():
    try:
        save_files = [f for f in os.listdir(SAVES_FOLDER) if f.endswith(".db")]
        return jsonify(save_files)
    except FileNotFoundError: return jsonify({"error": "Saves directory not found"}), 404
@app.route("/api/new_game", methods=['POST'])
def post_new_game():
    data = request.get_json()
    save_name = data.get('save_name')
    if not save_name or " " in save_name or not save_name.isalnum(): return jsonify({"status": "error", "message": "Invalid save name."}), 400
    try:
        os.makedirs(SAVES_FOLDER, exist_ok=True)
        new_save_path = os.path.join(SAVES_FOLDER, f"{save_name}.db")
        if os.path.exists(new_save_path): return jsonify({"status": "error", "message": "A save file with that name already exists."}), 409
        create_new_world(new_save_path)
        return jsonify({"status": "success", "message": f"Successfully created world in {new_save_path}"})
    except Exception as e: return jsonify({"status": "error", "message": "An internal error occurred."}), 500
@app.route("/api/saves/<save_name>", methods=['DELETE'])
def delete_save_game(save_name):
    if os.path.basename(save_name) != save_name: return jsonify({"status": "error", "message": "Invalid filename."}), 400
    try:
        file_path = os.path.join(SAVES_FOLDER, f"{save_name}.db")
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"status": "success", "message": f"Save file '{save_name}.db' deleted."})
        else:
            return jsonify({"status": "error", "message": "Save file not found."}), 404
    except OSError as e: return jsonify({"status": "error", "message": "Error deleting file on server."}), 500

# ==============================================================================
# == CORRECTED AND OPTIMIZED FRANCHISE ENDPOINTS
# ==============================================================================

@app.route("/api/franchise/<save_name>/teams", methods=['GET'])
def get_all_teams(save_name):
    """
    CORRECTED: Gets a list of all teams with their summary data, including a properly
    calculated 1-100 scale team overall rating.
    """
    try:
        conn = get_db_connection(save_name)
        # --- THIS IS THE NEW, CORRECTED QUERY ---
        # It correctly averages all non-null skill ratings for a team.
        teams_query = """
            SELECT 
                t.team_id, t.city, t.nickname, t.budget, t.goal,
                (
                    SELECT 
                        AVG(ratings.skill)
                    FROM (
                        SELECT p.contact_current as skill FROM players p WHERE p.team_id = t.team_id AND p.contact_current IS NOT NULL
                        UNION ALL
                        SELECT p.power_current as skill FROM players p WHERE p.team_id = t.team_id AND p.power_current IS NOT NULL
                        UNION ALL
                        SELECT p.eye_current as skill FROM players p WHERE p.team_id = t.team_id AND p.eye_current IS NOT NULL
                        UNION ALL
                        SELECT p.stuff_current as skill FROM players p WHERE p.team_id = t.team_id AND p.stuff_current IS NOT NULL
                        UNION ALL
                        SELECT p.movement_current as skill FROM players p WHERE p.team_id = t.team_id AND p.movement_current IS NOT NULL
                        UNION ALL
                        SELECT p.control_current as skill FROM players p WHERE p.team_id = t.team_id AND p.control_current IS NOT NULL
                        UNION ALL
                        SELECT p.clutchness_current as skill FROM players p WHERE p.team_id = t.team_id AND p.clutchness_current IS NOT NULL
                    ) as ratings
                ) as avg_80_scale_rating
            FROM teams t
            ORDER BY t.city;
        """
        teams_raw = conn.execute(teams_query).fetchall()
        conn.close()

        teams = []
        for row in teams_raw:
            team_dict = dict(row)
            avg_80 = team_dict['avg_80_scale_rating'] or 45
            
            # Enhanced team rating conversion to create elite teams in 90s
            # Maps current range to full 60-95 spectrum with some 90+ elites
            if avg_80 <= 38.5:
                # Poor/Rebuilding teams: scale 35-38.5 to 60-70
                team_overall_100 = round(((avg_80 - 35) / 3.5) * 10) + 60
            elif avg_80 <= 40.5:
                # Average teams: scale 38.5-40.5 to 70-80  
                team_overall_100 = round(((avg_80 - 38.5) / 2) * 10) + 70
            elif avg_80 <= 42:
                # Good teams: scale 40.5-42 to 80-88
                team_overall_100 = round(((avg_80 - 40.5) / 1.5) * 8) + 80
            else:
                # Elite teams: scale 42+ to 88-95 (ensures some 90+ teams)
                team_overall_100 = round(((avg_80 - 42) / 3) * 7) + 88
            
            # Ensure realistic bounds with more variety
            team_dict['team_overall'] = max(55, min(95, team_overall_100))
            teams.append(team_dict)

        return jsonify(teams)
    except Exception as e:
        print(f"Error getting all teams: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/franchise/<save_name>/teams/<int:team_id>", methods=['GET'])
def get_team_details(save_name, team_id):
    # This endpoint is now slightly redundant for team_overall, but we keep it
    # for the other details. We can add the 1-100 overall here too for consistency.
    try:
        conn = get_db_connection(save_name)
        payroll_q = conn.execute("SELECT SUM(salary) as total_payroll FROM players WHERE team_id = ?", (team_id,)).fetchone()
        top_players = conn.execute("SELECT * FROM players WHERE team_id = ? ORDER BY (IFNULL(contact_potential,0) + IFNULL(power_potential,0) + IFNULL(stuff_potential,0) + IFNULL(movement_potential,0)) DESC LIMIT 3", (team_id,)).fetchall()
        conn.close()
        return jsonify({
            "payroll": payroll_q['total_payroll'] if payroll_q else 0,
            "top_players": [dict(p) for p in top_players]
        })
    except Exception as e:
        print(f"Error getting team details: {e}")
        return jsonify({"error": str(e)}), 500

# --- The rest of the endpoints are unchanged ---
@app.route("/api/franchise/<save_name>/select_team", methods=['POST'])
def post_select_team(save_name):
    # ... (code is unchanged)
    data = request.get_json()
    team_id = data.get('team_id')
    try:
        conn = get_db_connection(save_name)
        conn.execute("REPLACE INTO game_metadata (key, value) VALUES (?, ?)", ("player_team_id", team_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Team {team_id} selected."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/franchise/<save_name>", methods=['GET'])
def get_franchise_data(save_name):
    # ... (code is unchanged)
    try:
        conn = get_db_connection(save_name)
        player_team_id_q = conn.execute("SELECT value FROM game_metadata WHERE key = 'player_team_id'").fetchone()
        if not player_team_id_q: return jsonify({"error": "Player team not set."}), 404
        player_team_id = player_team_id_q['value']
        team = conn.execute("SELECT * FROM teams WHERE team_id = ?", (player_team_id,)).fetchone()
        standings = conn.execute("SELECT t.city, t.nickname, s.wins, s.losses FROM standings s JOIN teams t ON s.team_id = t.team_id ORDER BY s.wins DESC, s.losses ASC").fetchall()
        next_game_q = conn.execute("SELECT g.*, ht.city as home_city, ht.nickname as home_nickname, awt.city as away_city, awt.nickname as away_nickname FROM schedule g JOIN teams ht ON g.home_team_id = ht.team_id JOIN teams awt ON g.away_team_id = awt.team_id WHERE g.played_status = 0 AND (g.home_team_id = ? OR g.away_team_id = ?) ORDER BY g.day, g.game_id LIMIT 1", (player_team_id, player_team_id)).fetchone()
        conn.close()
        return jsonify({"team": dict(team) if team else None, "standings": [dict(row) for row in standings], "next_game": dict(next_game_q) if next_game_q else None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/franchise/<save_name>/simulate", methods=['POST'])
def post_simulate_game(save_name):
    # ... (code is unchanged)
    try:
        conn = get_db_connection(save_name)
        player_team_id = conn.execute("SELECT value FROM game_metadata WHERE key = 'player_team_id'").fetchone()['value']
        next_game = conn.execute("SELECT * FROM schedule WHERE played_status = 0 AND (home_team_id = ? OR away_team_id = ?) ORDER BY day, game_id LIMIT 1", (player_team_id, player_team_id)).fetchone()
        if not next_game: return jsonify({"status": "complete", "message": "No more games!"})
        home_roster_q = conn.execute("SELECT * FROM players WHERE team_id = ?", (next_game['home_team_id'],)).fetchall()
        away_roster_q = conn.execute("SELECT * FROM players WHERE team_id = ?", (next_game['away_team_id'],)).fetchall()
        home_roster = [dict(p) for p in home_roster_q]
        away_roster = [dict(p) for p in away_roster_q]
        result = simulate_game(home_roster, away_roster)
        cursor = conn.cursor()
        cursor.execute("UPDATE schedule SET home_score = ?, away_score = ?, played_status = 1 WHERE game_id = ?", (result['home_score'], result['away_score'], next_game['game_id']))
        winner_id, loser_id = (next_game['home_team_id'], next_game['away_team_id']) if result['home_score'] > result['away_score'] else (next_game['away_team_id'], next_game['home_team_id'])
        cursor.execute("UPDATE standings SET wins = wins + 1 WHERE team_id = ?", (winner_id,))
        cursor.execute("UPDATE standings SET losses = losses + 1 WHERE team_id = ?", (loser_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Game simulated.", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)