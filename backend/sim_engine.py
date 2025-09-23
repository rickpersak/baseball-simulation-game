# File: backend/sim_engine.py
import random

def _calculate_outcome_probability(batter_rating, pitcher_rating, base_chance):
    """Calculates the chance of an event based on the player rating matchup."""
    rating_diff = batter_rating - pitcher_rating
    # A multiplier between ~0.5 (bad matchup) and ~1.5 (good matchup)
    multiplier = 1 + (rating_diff / 100.0) 
    return base_chance * multiplier

def _is_clutch_situation(inning, score_diff, runners_on_base):
    """Determines if the current situation qualifies as a clutch situation."""
    # Late innings (7th inning or later)
    late_inning = inning >= 7
    
    # Close game (within 3 runs)
    close_game = abs(score_diff) <= 3
    
    # Runners in scoring position (2nd or 3rd base)
    risp = runners_on_base >= 2
    
    # Clutch if: (late inning AND close game) OR (runners in scoring position)
    return (late_inning and close_game) or risp

def _apply_clutch_factor(rating, clutchness, is_clutch):
    """Applies clutchness factor to a rating in clutch situations."""
    if not is_clutch:
        return rating
    
    # Clutchness affects performance by up to ±15 points based on clutchness rating
    # Higher clutchness (70+) = boost, Lower clutchness (40-) = penalty
    clutch_modifier = (clutchness - 50) * 0.3  # Scale from -15 to +15
    return max(20, min(80, rating + clutch_modifier))

def simulate_at_bat(batter, pitcher, inning=1, score_diff=0, runners_on_base=0):
    """Determines the outcome of a single at-bat based on current ratings and clutch factors."""
    is_clutch = _is_clutch_situation(inning, score_diff, runners_on_base)
    
    # Apply clutch factors to relevant ratings
    batter_eye = _apply_clutch_factor(batter['eye_current'], batter['clutchness_current'], is_clutch)
    batter_power = _apply_clutch_factor(batter['power_current'], batter['clutchness_current'], is_clutch)
    batter_contact = _apply_clutch_factor(batter['contact_current'], batter['clutchness_current'], is_clutch)
    
    pitcher_stuff = _apply_clutch_factor(pitcher['stuff_current'], pitcher['clutchness_current'], is_clutch)
    pitcher_movement = _apply_clutch_factor(pitcher['movement_current'], pitcher['clutchness_current'], is_clutch)
    pitcher_control = _apply_clutch_factor(pitcher['control_current'], pitcher['clutchness_current'], is_clutch)
    
    # Base probabilities for a league-average matchup
    p_k = _calculate_outcome_probability(30, batter_eye, 0.22) # Pitcher's K chance vs Batter's Eye
    p_bb = _calculate_outcome_probability(batter_eye, pitcher_control, 0.08)
    p_hr = _calculate_outcome_probability(batter_power, pitcher_movement, 0.025)
    p_single = _calculate_outcome_probability(batter_contact, pitcher_stuff, 0.15)
    p_double = _calculate_outcome_probability(batter_contact, pitcher_stuff, 0.04)

    roll = random.random()
    if roll < p_k: return "STRIKEOUT"
    if roll < p_k + p_bb: return "WALK"
    if roll < p_k + p_bb + p_hr: return "HOME RUN"
    if roll < p_k + p_bb + p_hr + p_double: return "DOUBLE"
    if roll < p_k + p_bb + p_hr + p_double + p_single: return "SINGLE"
    return "OUT"

def simulate_game(home_roster, away_roster):
    """Simulates a full 9-inning game using player ratings and clutch factors."""
    home_score = 0
    away_score = 0
    home_pitcher = next(p for p in home_roster if p['position'] == 'P')
    away_pitcher = next(p for p in away_roster if p['position'] == 'P')

    for inning in range(1, 10):
        # Away team bats vs Home pitcher
        outs = 0
        inning_runs = 0
        runners_on_base = 0  # Track runners on base for clutch situations
        
        while outs < 3:
            batter = random.choice([p for p in away_roster if p['position'] != 'P'])
            score_diff = home_score - away_score  # From batting team's perspective
            
            outcome = simulate_at_bat(batter, home_pitcher, inning, score_diff, runners_on_base)
            
            if outcome == "OUT" or outcome == "STRIKEOUT": 
                outs += 1
            elif outcome == "HOME RUN": 
                inning_runs += 1 + min(runners_on_base, 3)  # Score all runners plus batter
                runners_on_base = 0
            elif outcome == "DOUBLE":
                # Runners score from 2nd/3rd, batter goes to 2nd
                runs_scored = min(runners_on_base, 2) if runners_on_base >= 2 else 0
                inning_runs += runs_scored
                runners_on_base = max(1, runners_on_base - runs_scored) + 1  # Batter to 2nd
            elif outcome in ["SINGLE", "WALK"]:
                # Some runners advance and score
                if runners_on_base >= 3:  # Runner on 3rd scores
                    inning_runs += 1
                    runners_on_base = min(3, runners_on_base + 1 - 1)
                else:
                    runners_on_base = min(3, runners_on_base + 1)
                    
        away_score += inning_runs
        
        # Home team bats vs Away pitcher (similar logic)
        outs = 0
        inning_runs = 0
        runners_on_base = 0
        
        while outs < 3:
            batter = random.choice([p for p in home_roster if p['position'] != 'P'])
            score_diff = away_score - home_score  # From batting team's perspective
            
            outcome = simulate_at_bat(batter, away_pitcher, inning, score_diff, runners_on_base)
            
            if outcome == "OUT" or outcome == "STRIKEOUT": 
                outs += 1
            elif outcome == "HOME RUN": 
                inning_runs += 1 + min(runners_on_base, 3)
                runners_on_base = 0
            elif outcome == "DOUBLE":
                runs_scored = min(runners_on_base, 2) if runners_on_base >= 2 else 0
                inning_runs += runs_scored
                runners_on_base = max(1, runners_on_base - runs_scored) + 1
            elif outcome in ["SINGLE", "WALK"]:
                if runners_on_base >= 3:
                    inning_runs += 1
                    runners_on_base = min(3, runners_on_base + 1 - 1)
                else:
                    runners_on_base = min(3, runners_on_base + 1)
                    
        home_score += inning_runs
    
    if home_score == away_score:
        if random.random() < 0.5: home_score += 1
        else: away_score += 1
            
    print(f"Sim Result: Away({away_score}) @ Home({home_score})")
    return {"home_score": home_score, "away_score": away_score}