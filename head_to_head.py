import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from team_dictionary import get_teams_dictionary

def load_team_data(file_path='torvik_data_2025.xlsx'):
    try:
        df = pd.read_excel(file_path)
        # print(f"Loaded data for {len(df)} teams")
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None

def grab_team_info(team_name):
    try:
        # Convert team name to filename format (replace spaces with underscores)
        filename = team_name.replace(" ", "_") + ".csv"
        file_path = f"team_data/{filename}"
        
        # Load the CSV file
        df = pd.read_csv(file_path)
        # print(f"Loaded team data for {team_name} from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Team data file not found for {team_name} at team_data/{filename}")
        return None
    except Exception as e:
        print(f"Error loading team data for {team_name}: {e}")
        return None

   
def calc_WORTH(team_name, tourney_teams):
    """
    Calcs: WORTH (Wins Over Ranked Tournament-Headed Squads 
    Returns:
    float: Winning percentage against tournament teams (0 if no games played)
    """
    df = grab_team_info(team_name)
    
    # Filter for games against tournament teams
    tournament_games = df[df['opponent'].isin(tourney_teams)]
    
    # If no games against tournament teams, return 0
    if len(tournament_games) == 0:
        return 0.0
    
    wins = len(tournament_games[tournament_games['result'] == 'W'])
    total_games = len(tournament_games)
    
    # Calculate and return winning percentage
    return wins / total_games

def calc_PRIME(team_name):
    """
    Calcs: PRIME (Performance Rating In Major Engagements)

    Returns:
    float: Winning percentage against top five ranked opponents (0 if fewer than 5 games played)
    """
    df = grab_team_info(team_name)
    ranked_games = df[df['opp_rank'].notna()]
    
    # Sort by opponent rank (ascending) and take top 5
    top_games = ranked_games.sort_values('opp_rank').head(5)
    
    # Count wins against top 5 opponents
    wins = len(top_games[top_games['result'] == 'W'])
    
    # Calculate and return winning percentage
    return wins / 5

def calc_ROAD(team_name):
   """
   Calcs: ROAD (Reliability Outside Accustomed Domain)
   
   Returns:
   float: Road/neutral win percentage minus home win percentage
   """
   df = grab_team_info(team_name)
   
   away_games = df[(df['venue'] == 'away') | (df['venue'] == 'neutral')]
   home_games = df[df['venue'] == 'home']
   
   away_wins = len(away_games[away_games['result'] == 'W'])
   home_wins = len(home_games[home_games['result'] == 'W'])
   
   away_win_pct = away_wins / len(away_games) if len(away_games) > 0 else 0
   home_win_pct = home_wins / len(home_games) if len(home_games) > 0 else 0
   
   return away_win_pct - home_win_pct

def calc_NERVE(team_name):
   """
   Calcs: NERVE (Narrow Endgame Resolution and Victory Evaluation)
   
   Returns:
   float: Winning percentage in close games (4 points or less difference)
   """
   df = grab_team_info(team_name)
   
   close_games = df[abs(df['t_score_t'] - df['t_score_o']) <= 4]
   
   if len(close_games) == 0:
       return 0.0
   
   wins = len(close_games[close_games['result'] == 'W'])
   
   return wins / len(close_games)

def load_miya_data(team_names, teams_dict):
    for team in team_names:
        try:
            worth_value = calc_WORTH(team, team_names)
            prime_value = calc_PRIME(team)
            road_value = calc_ROAD(team)
            nerve_value = calc_NERVE(team)

            teams_dict[team]['WORTH'] = worth_value
            teams_dict[team]['PRIME'] = prime_value
            teams_dict[team]['ROAD'] = road_value
            teams_dict[team]['NERVE'] = nerve_value
        except Exception as e:
            print(f"Error calculating metrics for {team}: {e}")
    return teams_dict


def predict_winner(team1_name, team2_name, torvik_data=None, miya_data=None):
    """
    Args:
        team1_name (str): Name of the first team
        team2_name (str): Name of the second team
        data (pd.DataFrame, optional): DataFrame containing team data     
    Returns:
        dict: Dictionary containing prediction results
    """
    # Load data if not provided
    if torvik_data is None:
        torvik_data = load_team_data()
        if torvik_data is None or miya_data is None:
            return {"error": "Could not load team data"}
    
    # Find teams in data
    team1 = torvik_data[torvik_data['team'].str.lower() == team1_name.lower()]
    team2 = torvik_data[torvik_data['team'].str.lower() == team2_name.lower()]
    
    # Check if teams were found
    if len(team1) == 0:
        return {"error": f"Team '{team1_name}' not found in data"}
    if len(team2) == 0:
        return {"error": f"Team '{team2_name}' not found in data"}
    
    # Extract team data
    team1 = team1.iloc[0]
    team2 = team2.iloc[0]
    
    # Calculate win probability using a simple model
    # This model uses adjusted offensive and defensive efficiency, plus win percentage
    
    # Feature extraction
    features = ['adjoe', 'adjde', 'barthag']
    
    # Check if all features are available
    for feature in features:
        if feature not in torvik_data.columns:
            return {"error": f"Required feature '{feature}' not found in data"}
    
    # Calculate win percentage
    team1_win_pct = team1['wins'] / (team1['wins'] + team1['losses'])
    team2_win_pct = team2['wins'] / (team2['wins'] + team2['losses'])
    
    # Calculate offensive and defensive advantages
    # Higher offensive efficiency is better, lower defensive efficiency is better
    offensive_advantage = team1['adjoe'] - team2['adjde']
    defensive_advantage = team2['adjoe'] - team1['adjde']
    
    # Calculate overall advantage using Barthag (power rating)
    barthag_advantage = team1['barthag'] - team2['barthag']
    
    # Calculate win probability using a weighted model
    # This is a simplified model for demonstration
    win_prob = 0.5 + (
        0.2 * (team1_win_pct - team2_win_pct) +
        0.3 * (offensive_advantage / 100) +
        0.3 * (defensive_advantage / 100) +
        0.2 * barthag_advantage
    )
    
    # Ensure probability is between 0 and 1
    win_prob = max(0.01, min(0.99, win_prob))
    
    # Determine predicted score (simplified)
    avg_team1_score = team1['adjoe'] * 0.01 * 70  # Assuming 70 possessions
    avg_team2_score = team2['adjoe'] * 0.01 * 70
    
    # Adjust scores based on defensive ratings
    team1_predicted_score = avg_team1_score * (100 / team2['adjde'])
    team2_predicted_score = avg_team2_score * (100 / team1['adjde'])
    
    # Round scores to integers
    team1_score = round(team1_predicted_score)
    team2_score = round(team2_predicted_score)
    
    # Ensure different scores (no ties)
    if team1_score == team2_score:
        if win_prob > 0.5:
            team1_score += 1
        else:
            team2_score += 1
    
    # Determine winner
    winner = team1_name if win_prob > 0.5 else team2_name
    
    # Return results
    return {
        "team1": {
            "name": team1_name,
            "rank": team1['rank'],
            "record": team1['record'],
            "win_pct": team1_win_pct,
            "adjoe": team1['adjoe'],
            "adjde": team1['adjde'],
            "barthag": team1['barthag'],
            "predicted_score": team1_score
        },
        "team2": {
            "name": team2_name,
            "rank": team2['rank'],
            "record": team2['record'],
            "win_pct": team2_win_pct,
            "adjoe": team2['adjoe'],
            "adjde": team2['adjde'],
            "barthag": team2['barthag'],
            "predicted_score": team2_score
        },
        "prediction": {
            "winner": winner,
            "win_probability": win_prob if winner == team1_name else 1 - win_prob,
            "score": f"{team1_score}-{team2_score}" if winner == team1_name else f"{team2_score}-{team1_score}"
        }
    }

def print_matchup_results(results):
    """
    Print the results of a matchup prediction in a readable format
    
    Args:
        results (dict): Dictionary containing prediction results
    """
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    team1 = results["team1"]
    team2 = results["team2"]
    prediction = results["prediction"]
    
    print("\n" + "="*50)
    print(f"MATCHUP: #{team1['rank']} {team1['name']} ({team1['record']}) vs #{team2['rank']} {team2['name']} ({team2['record']})")
    print("="*50)
    
    print(f"\nTeam Stats:")
    print(f"{'':20} {'Adj. OE':10} {'Adj. DE':10} {'Power':10}")
    print(f"{team1['name']:20} {team1['adjoe']:<10.1f} {team1['adjde']:<10.1f} {team1['barthag']:<10.3f}")
    print(f"{team2['name']:20} {team2['adjoe']:<10.1f} {team2['adjde']:<10.1f} {team2['barthag']:<10.3f}")
    
    print(f"\nPREDICTION:")
    print(f"Winner: {prediction['winner']} ({prediction['win_probability']:.1%} probability)")
    print(f"Predicted Score: {prediction['score']}")
    print("="*50 + "\n")

# Example usage
if __name__ == "__main__":
    # Load data
    data = load_team_data()
    teams_dict = get_teams_dictionary()
    team_names = list(teams_dict.keys())
    teams_dict = load_miya_data(team_names, teams_dict)


    if data is not None:

        print(team_names)
        print("\nEnter team names to predict a matchup (or 'quit' to exit):")
        while True:
            team1 = input("Team 1: ")
            if team1.lower() == 'quit':
                break
                
            team2 = input("Team 2: ")
            if team2.lower() == 'quit':
                break
                
            results = predict_winner(team1, team2, data)
            print_matchup_results(results)



        # Example matchups
        # matchups = [
        #     ("Houston", "Duke"),
        #     ("Gonzaga", "Auburn"),
        #     ("Alabama", "Purdue")
        # ]
        
        # for team1, team2 in matchups:
        #     results = predict_winner(team1, team2, data)
        #     print_matchup_results(results)
        
        # Interactive mode