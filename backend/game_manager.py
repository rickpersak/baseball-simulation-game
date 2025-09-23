import os
import sqlite3
from world_generator import create_new_world

# --- SETTINGS ---
SAVES_FOLDER = "saves"

# --- CORE FUNCTIONS ---

def create_new_game():
    """
    Handles the logic for creating a new save game by calling the world generator.
    """
    save_name = input("Enter a name for your new game (no spaces): ")
    if not save_name or " " in save_name or not save_name.isalnum():
        print("\nInvalid save name. Please use only letters and numbers with no spaces.\n")
        return

    # Ensure the 'saves' directory exists
    try:
        os.makedirs(SAVES_FOLDER, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create the saves directory: {e}")
        return

    new_save_path = os.path.join(SAVES_FOLDER, f"{save_name}.db")

    if os.path.exists(new_save_path):
        print(f"\nError: A save file named '{save_name}.db' already exists.\n")
        return

    # --- NEW LOGIC ---
    # Call the world generator to create and populate the new database file.
    create_new_world(new_save_path)
    
    print("\n--- New Game World Created! ---")
    print(f"Successfully created save file: {new_save_path}\n")


def load_game():
    """
    Handles the logic for listing and loading an existing save game.
    """
    try:
        save_files = [f for f in os.listdir(SAVES_FOLDER) if f.endswith(".db")]
    except FileNotFoundError:
        print(f"\nError: The '{SAVES_FOLDER}' directory does not exist. No games to load.\n")
        return

    if not save_files:
        print("\nThere are no saved games to load.\n")
        return

    print("\n--- Load Game ---")
    for i, file_name in enumerate(save_files):
        print(f"  {i + 1}: {file_name}")
    print("-------------------")

    try:
        choice = int(input("Enter the number of the game to load: "))
        if not (1 <= choice <= len(save_files)):
            print("\nInvalid number. Please try again.\n")
            return
    except ValueError:
        print("\nInvalid input. Please enter a number.\n")
        return

    selected_file = save_files[choice - 1]
    db_path = os.path.join(SAVES_FOLDER, selected_file)
    
    print(f"\n...Loading game from '{db_path}'...")
    display_rosters_from_db(db_path)

def display_rosters_from_db(db_path):
    """
    Connects to a specific database file and prints its team rosters.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("\n--- ROSTER REPORT (First 2 Teams) ---")
        # Limit to 2 teams for a cleaner display
        cursor.execute("SELECT team_id, city, nickname FROM teams ORDER BY city LIMIT 2;")
        all_teams = cursor.fetchall()

        for team in all_teams:
            print(f"\nTeam: {team['city']} {team['nickname']}")
            cursor.execute("SELECT * FROM players WHERE team_id = ? ORDER BY last_name;", (team['team_id'],))
            players_on_team = cursor.fetchall()
            for player in players_on_team:
                print(f"  - {player['first_name']} {player['last_name']} ({player['position']})")
        print("\n--- End of Report ---\n")

    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    finally:
        if conn:
            conn.close()

# --- MAIN MENU ---

def main():
    """ The main loop for the game manager application. """
    while True:
        print("====== Baseball Game Manager ======")
        print("  1. Start a New Game")
        print("  2. Load an Existing Game")
        print("  3. Exit")
        print("=================================")
        
        choice = input("Please enter your choice (1-3): ")

        if choice == '1':
            create_new_game()
        elif choice == '2':
            load_game()
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.\n")

if __name__ == "__main__":
    main()