# File: backend/player_generator.py
import random
import json
import unicodedata

# --- DATA LOADING (No changes here, still loads from external files) ---
def _normalize(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))
def _load_banned_names(filepath="banned_last_names.txt") -> set:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return {_normalize(line.strip()) for line in f if line.strip()}
    except FileNotFoundError: return set()
def _load_name_data(filepath="names.json") -> dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return {}

print("Initializing player generator...")
BANNED_LAST_NAMES_SET = _load_banned_names()
NATIONALITIES_DATA = _load_name_data()
SAFE_NATIONALITIES = {}
for country, names in NATIONALITIES_DATA.items():
    safe_last_names = [name for name in names["last_names"] if _normalize(name) not in BANNED_LAST_NAMES_SET]
    if safe_last_names:
        SAFE_NATIONALITIES[country] = {"first_names": names["first_names"], "last_names": safe_last_names}
print("Player generator initialized successfully.")

ORIGIN_WEIGHTS = {
    "USA": 0.60, "Dominican Republic": 0.104, "Venezuela": 0.050, "Cuba": 0.020,
    "Puerto Rico": 0.020, "Mexico": 0.030, "Colombia": 0.020, "Panama": 0.010,
    "Nicaragua": 0.004, "Curaçao": 0.004, "Aruba": 0.002, "Brazil": 0.016,
    "Japan": 0.035, "South Korea": 0.015, "Canada": 0.035, "Taiwan": 0.010,
    "Australia": 0.010, "Italy": 0.005, "Netherlands": 0.007, "Germany": 0.003,
}
POPULATION = list(SAFE_NATIONALITIES.keys())
WEIGHTS = [ORIGIN_WEIGHTS.get(country, 0) for country in POPULATION]

# ==============================================================================
# == NEW RATING GENERATION LOGIC
# ==============================================================================
def _snap_to_5(rating):
    """Rounds a rating to the nearest 5 (e.g., 53 -> 55, 52 -> 50)."""
    return round(rating / 5) * 5

def generate_ratings(age):
    """Generates a pair of (current, potential) ratings for a single skill."""
    # Extreme variance distribution to create distinct team tiers
    # More scrubs and elites, fewer "average" players to force team separation
    potential_roll = random.random()
    
    if potential_roll < 0.25:  # 25% scrubs/poor players (rebuilding team material)
        potential = _snap_to_5(random.triangular(20, 40, 30))
    elif potential_roll < 0.55:  # 30% below average players  
        potential = _snap_to_5(random.triangular(35, 50, 42))
    elif potential_roll < 0.75:  # 20% average players
        potential = _snap_to_5(random.triangular(45, 60, 52))
    elif potential_roll < 0.92:  # 17% good players
        potential = _snap_to_5(random.triangular(55, 70, 62))
    else:  # 8% elite stars
        potential = _snap_to_5(random.triangular(65, 80, 72))
    
    # Current rating is influenced by age and potential
    # Younger players (18-24) are developing: 65-90% of potential
    # Prime age players (25-30) are at peak: 85-100% of potential  
    # Older players (31+) may decline slightly: 80-95% of potential
    
    if age <= 24:
        # Younger players: more variance in development
        development_factor = random.uniform(0.65, 0.90)
    elif age <= 30:
        # Prime age: at or near peak
        development_factor = random.uniform(0.85, 1.0)
    else:
        # Older players: slight decline possible
        development_factor = random.uniform(0.80, 0.95)
    
    # Calculate current rating
    current = _snap_to_5(potential * development_factor)
    
    # Ensure ratings stay within bounds
    current = max(20, min(current, potential))
    
    return (current, potential)

def generate_player():
    """Generates a complete player with current/potential ratings."""
    player_origin = random.choices(POPULATION, weights=WEIGHTS, k=1)[0]
    first_name = random.choice(SAFE_NATIONALITIES[player_origin]["first_names"])
    last_name = random.choice(SAFE_NATIONALITIES[player_origin]["last_names"])
    
    position = random.choice(["P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"])
    age = random.randint(18, 35)

    contact_c, contact_p = generate_ratings(age)
    power_c, power_p = generate_ratings(age)
    eye_c, eye_p = generate_ratings(age)
    stuff_c, stuff_p = generate_ratings(age)
    movement_c, movement_p = generate_ratings(age)
    control_c, control_p = generate_ratings(age)
    clutchness_c, clutchness_p = generate_ratings(age)

    player_data = {
        "first_name": first_name, "last_name": last_name, "position": position, "age": age,
        "bats": random.choice(["R", "L"]), "throws": random.choice(["R", "L"]),
        "contact_current": contact_c, "contact_potential": contact_p,
        "power_current": power_c, "power_potential": power_p,
        "eye_current": eye_c, "eye_potential": eye_p,
        "stuff_current": stuff_c, "stuff_potential": stuff_p,
        "movement_current": movement_c, "movement_potential": movement_p,
        "control_current": control_c, "control_potential": control_p,
        "clutchness_current": clutchness_c, "clutchness_potential": clutchness_p,
    }

    if position != "P":
        player_data.update({
            "stuff_current": None, "stuff_potential": None,
            "movement_current": None, "movement_potential": None,
            "control_current": None, "control_potential": None
        })
    else:
        player_data.update({
            "contact_current": None, "contact_potential": None,
            "power_current": None, "power_potential": None,
            "eye_current": None, "eye_potential": None
        })
        
    return player_data