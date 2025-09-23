# File: backend/world_generator.py
import sqlite3
import random
from player_generator import generate_player

def create_new_world(db_path):
    """
    Creates a new database with a full league, now including players with separate
    current and potential ratings, age, and salary. (Salary calculation is now fixed).
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("Creating database schema with Current/Potential ratings...")
        cursor.execute("""CREATE TABLE "leagues" ( "league_id" INTEGER PRIMARY KEY, "name" TEXT, "abbreviation" TEXT );""")
        cursor.execute("""CREATE TABLE "teams" ( "team_id" INTEGER PRIMARY KEY, "league_id" INTEGER, "city" TEXT, "nickname" TEXT, "abbreviation" TEXT, "budget" INTEGER, "goal" TEXT, FOREIGN KEY("league_id") REFERENCES "leagues"("league_id") );""")
        cursor.execute("""
            CREATE TABLE "players" (
                "player_id" INTEGER PRIMARY KEY, "team_id" INTEGER,
                "first_name" TEXT, "last_name" TEXT, "position" TEXT, "age" INTEGER,
                "bats" TEXT, "throws" TEXT, "salary" INTEGER,
                "contact_current" INTEGER, "contact_potential" INTEGER,
                "power_current" INTEGER, "power_potential" INTEGER,
                "eye_current" INTEGER, "eye_potential" INTEGER,
                "stuff_current" INTEGER, "stuff_potential" INTEGER,
                "movement_current" INTEGER, "movement_potential" INTEGER,
                "control_current" INTEGER, "control_potential" INTEGER,
                "clutchness_current" INTEGER, "clutchness_potential" INTEGER,
                FOREIGN KEY("team_id") REFERENCES "teams"("team_id")
            );
        """)
        cursor.execute("""CREATE TABLE "standings" ( "team_id" INTEGER PRIMARY KEY, "season" INTEGER DEFAULT 1, "wins" INTEGER DEFAULT 0, "losses" INTEGER DEFAULT 0, FOREIGN KEY("team_id") REFERENCES "teams"("team_id") );""")
        cursor.execute("""CREATE TABLE "schedule" ( "game_id" INTEGER PRIMARY KEY, "season" INTEGER DEFAULT 1, "day" INTEGER, "home_team_id" INTEGER, "away_team_id" INTEGER, "home_score" INTEGER, "away_score" INTEGER, "played_status" INTEGER DEFAULT 0, FOREIGN KEY("home_team_id") REFERENCES "teams"("team_id"), FOREIGN KEY("away_team_id") REFERENCES "teams"("team_id") );""")
        cursor.execute("""CREATE TABLE "game_metadata" ( "key" TEXT PRIMARY KEY, "value" TEXT );""")
        print("Schema created successfully.")

        print(f"Generating new world in database: {db_path}...")
        used_full_names = set()
        
        cursor.execute("INSERT INTO leagues (name, abbreviation) VALUES (?, ?);", ("Major Baseball League", "MBL"))
        league_id = cursor.lastrowid

        CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis", "Seattle", "Denver", "Washington", "Boston", "El Paso", "Detroit", "Nashville", "Portland", "Memphis", "Oklahoma City", "Las Vegas", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson"]
        NICKNAMES = ["Dragons", "Wizards", "Golems", "Titans", "Vipers", "Sharks", "Hawks", "Lions", "Bears", "Jets", "Rockets", "Comets", "Stars", "Kings", "Phantoms", "Wolves", "Eagles", "Shoguns", "Samurai", "Ninjas", "Pioneers", "Voyagers", "Explorers", "Captains", "Admirals", "Generals", "Dukes", "Barons", "Counts", "Knights", "Paladins", "Crusaders"]
        GOALS = ["Win Championship", "Make Playoffs", "Finish .500", "Rebuild"]
        random.shuffle(CITIES)
        random.shuffle(NICKNAMES)

        team_ids = []
        team_data = []  # Store team info to assign goals later based on talent
        
        for i in range(32):
            budget = random.randint(150, 250) * 1_000_000
            # Don't assign goal yet - we'll do it after we know team strength
            city, nickname = CITIES[i], NICKNAMES[i]
            abbreviation = (city[:1] + nickname[:2]).upper()
            cursor.execute("INSERT INTO teams (league_id, city, nickname, abbreviation, budget, goal) VALUES (?, ?, ?, ?, ?, ?);",
                           (league_id, city, nickname, abbreviation, budget, "TBD"))
            team_id = cursor.lastrowid
            team_ids.append(team_id)
            team_data.append({'team_id': team_id, 'city': city, 'nickname': nickname})

            for _ in range(26):
                while True:
                    player = generate_player()
                    full_name = f"{player['first_name']} {player['last_name']}"
                    if full_name not in used_full_names:
                        used_full_names.add(full_name)
                        break
                
                # --- THIS IS THE CORRECTED LINE ---
                # Each (player[...] or 0) is now correctly grouped in its own parentheses
                # to ensure it evaluates correctly before the addition.
                avg_current = (
                    (player['contact_current'] or 0) + (player['power_current'] or 0) + (player['eye_current'] or 0) +
                    (player['stuff_current'] or 0) + (player['movement_current'] or 0) + (player['control_current'] or 0) +
                    (player['clutchness_current'] or 0)
                )
                salary = 750_000 + (avg_current - 20) * random.randint(25_000, 60_000)
                if salary < 750_000: salary = 750_000 # Ensure league minimum
                
                cursor.execute("""
                    INSERT INTO players (
                        team_id, first_name, last_name, position, age, bats, throws, salary,
                        contact_current, contact_potential, power_current, power_potential,
                        eye_current, eye_potential, stuff_current, stuff_potential,
                        movement_current, movement_potential, control_current, control_potential,
                        clutchness_current, clutchness_potential
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (team_id, player['first_name'], player['last_name'], player['position'], player['age'],
                      player['bats'], player['throws'], salary,
                      player['contact_current'], player['contact_potential'], player['power_current'], player['power_potential'],
                      player['eye_current'], player['eye_potential'], player['stuff_current'], player['stuff_potential'],
                      player['movement_current'], player['movement_potential'], player['control_current'], player['control_potential'],
                      player['clutchness_current'], player['clutchness_potential']))
        
        print(f"Generated {len(team_ids)} teams and {len(used_full_names)} players.")
        
        # Assign realistic goals based on team talent after all players are generated
        print("Assigning team goals based on talent levels...")
        
        # Calculate each team's average rating
        team_ratings = []
        for team_id in team_ids:
            avg_rating_result = cursor.execute("""
                SELECT AVG(ratings.skill) as avg_rating FROM (
                    SELECT p.contact_current as skill FROM players p WHERE p.team_id = ? AND p.contact_current IS NOT NULL
                    UNION ALL SELECT p.power_current as skill FROM players p WHERE p.team_id = ? AND p.power_current IS NOT NULL
                    UNION ALL SELECT p.eye_current as skill FROM players p WHERE p.team_id = ? AND p.eye_current IS NOT NULL
                    UNION ALL SELECT p.stuff_current as skill FROM players p WHERE p.team_id = ? AND p.stuff_current IS NOT NULL
                    UNION ALL SELECT p.movement_current as skill FROM players p WHERE p.team_id = ? AND p.movement_current IS NOT NULL
                    UNION ALL SELECT p.control_current as skill FROM players p WHERE p.team_id = ? AND p.control_current IS NOT NULL
                    UNION ALL SELECT p.clutchness_current as skill FROM players p WHERE p.team_id = ? AND p.clutchness_current IS NOT NULL
                ) as ratings
            """, (team_id, team_id, team_id, team_id, team_id, team_id, team_id)).fetchone()
            
            avg_rating = avg_rating_result[0] if avg_rating_result[0] else 40
            team_ratings.append((team_id, avg_rating))
        
        # Sort teams by rating to assign appropriate goals
        team_ratings.sort(key=lambda x: x[1], reverse=True)
        
        # Assign goals based on team ranking and strength
        for i, (team_id, avg_rating) in enumerate(team_ratings):
            # Convert rating to team overall using same logic as API
            if avg_rating <= 38.5:
                team_overall = round(((avg_rating - 35) / 3.5) * 10) + 60
            elif avg_rating <= 40.5:
                team_overall = round(((avg_rating - 38.5) / 2) * 10) + 70
            elif avg_rating <= 42:
                team_overall = round(((avg_rating - 40.5) / 1.5) * 8) + 80
            else:
                team_overall = round(((avg_rating - 42) / 3) * 7) + 88
            team_overall = max(55, min(95, team_overall))
            
            # Assign goals based on team strength
            if team_overall >= 90:  # Elite teams (90+)
                goal = "Win Championship"
            elif team_overall >= 83:  # Very good teams (83-89)
                goal = random.choice(["Win Championship", "Make Playoffs"])
            elif team_overall >= 75:  # Good teams (75-82)
                goal = "Make Playoffs"
            elif team_overall >= 68:  # Average teams (68-74)
                goal = random.choice(["Make Playoffs", "Finish .500"])
            else:  # Poor teams (67 and below)
                goal = random.choice(["Finish .500", "Rebuild"])
            
            # Update the goal in database
            cursor.execute("UPDATE teams SET goal = ? WHERE team_id = ?", (goal, team_id))
        
        for t_id in team_ids: cursor.execute("INSERT INTO standings (team_id) VALUES (?);", (t_id,))
        
        print("Generating realistic daily schedule...")
        teams = list(team_ids)
        random.shuffle(teams)
        for day in range(1, 32):
            # This is a simplified round-robin, for 32 teams there are 31 rounds
            for i in range(16):
                home_id = teams[i]
                away_id = teams[len(teams) - 1 - i]
                if random.random() < 0.5:
                    home_id, away_id = away_id, home_id
                cursor.execute("INSERT INTO schedule (day, home_team_id, away_team_id) VALUES (?, ?, ?);", (day, home_id, away_id))

            # Rotate teams for the next day's matchups
            teams.insert(1, teams.pop())

        total_games = cursor.execute("SELECT COUNT(*) FROM schedule").fetchone()[0]
        print(f"Generated a schedule with {total_games} games across {day} days.")
        conn.commit()
        print("World generation complete.")

    except sqlite3.Error as e:
        print(f"An error occurred during world generation: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()