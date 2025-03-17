import pandas as pd
import numpy as np
from team_dictionary import get_teams_dictionary
from datetime import datetime
import os

def load_team_data(file_path='torvik_data_2025.xlsx'):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None

def grab_team_info(team_name):
    """
    Grabs Miya data from the team_data folder for the team name after changing it to the right format
    """
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

def calc_TEMPO(team_name):
    """
    TO-DO: Calc tempo info from Miya
    """
    pass

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
        torvik_data (pd.DataFrame, optional): DataFrame containing team data
        miya_data (dict, optional): Dictionary containing MIYA metrics for teams
    Returns:
        dict: Dictionary containing prediction results
    """
    # Load data if not provided
    if torvik_data is None:
        torvik_data = load_team_data()
        if torvik_data is None and miya_data is None:
            return {"error": "Could not load team data"}
    
    # Find teams in data
    team1_df = torvik_data[torvik_data['team'].str.lower() == team1_name.lower()]
    team2_df = torvik_data[torvik_data['team'].str.lower() == team2_name.lower()]
    
    # Check if teams were found
    if len(team1_df) == 0:
        return {"error": f"Team '{team1_name}' not found in data"}
    if len(team2_df) == 0:
        return {"error": f"Team '{team2_name}' not found in data"}
    
    # Extract team data
    team1 = team1_df.iloc[0]
    team2 = team2_df.iloc[0]
    
    # Calculate win percentage
    team1_win_pct = team1['wins'] / (team1['wins'] + team1['losses'])
    team2_win_pct = team2['wins'] / (team2['wins'] + team2['losses'])
    
    # Calculate offensive and defensive advantages
    team1_offense = team1['adjoe']
    team1_defense = team1['adjde']
    team2_offense = team2['adjoe']
    team2_defense = team2['adjde']
    
    # Calculate overall power rating advantage
    team1_power = team1['barthag']
    team2_power = team2['barthag']
    power_diff = team1_power - team2_power
    
    # Get MIYA metrics if available
    team1_worth = 0
    team1_prime = 0
    team1_road = 0
    team1_nerve = 0
    
    team2_worth = 0
    team2_prime = 0
    team2_road = 0
    team2_nerve = 0
    
    if miya_data is not None:
        if team1_name in miya_data:
            team1_worth = miya_data[team1_name].get('WORTH', 0)
            team1_prime = miya_data[team1_name].get('PRIME', 0)
            team1_road = miya_data[team1_name].get('ROAD', 0)
            team1_nerve = miya_data[team1_name].get('NERVE', 0)
        
        if team2_name in miya_data:
            team2_worth = miya_data[team2_name].get('WORTH', 0)
            team2_prime = miya_data[team2_name].get('PRIME', 0)
            team2_road = miya_data[team2_name].get('ROAD', 0)
            team2_nerve = miya_data[team2_name].get('NERVE', 0)
    
    # Calculate win probability using absolute metrics instead of advantages
    # This makes the model symmetric regardless of team order
    win_prob = 0.5 + (
        0.05 * (team1_win_pct - team2_win_pct) +
        0.1 * ((team1_offense - team2_defense) / 100) +
        0.1 * ((team2_offense - team1_defense) / -100) +
        0.25 * power_diff +
        0.05 * (team1_worth - team2_worth) +
        0.15 * (team1_prime - team2_prime) +
        0.05 * (team1_road - team2_road) +
        0.05 * (team1_nerve - team2_nerve)
    )
    
    # Ensure probability is between 0 and 1
    win_prob = max(0.01, min(0.99, win_prob))
    
    # Calculate predicted scores
    team1_predicted_score = round(team1_offense * 0.01 * 70 * (100 / team2_defense))
    team2_predicted_score = round(team2_offense * 0.01 * 70 * (100 / team1_defense))
    
    # Ensure different scores (no ties)
    if team1_predicted_score == team2_predicted_score:
        if win_prob > 0.5:
            team1_predicted_score += 1
        else:
            team2_predicted_score += 1
    
    # For close games (win probability between 40% and 60%)
    if win_prob > .4 and win_prob < .6:
        # Calculate how close the game is (0 = exactly 50%, 1 = at 40% or 60%)
        closeness = 1 - abs(win_prob - 0.5) / 0.1
        
        # Get advantage values
        worth_advantage = team1_worth - team2_worth
        prime_advantage = team1_prime - team2_prime
        road_advantage = team1_road - team2_road
        nerve_advantage = team1_nerve - team2_nerve
        
        # Apply WORTH adjustment - scale based on magnitude (max adjustment of 0.04)
        worth_magnitude = min(abs(worth_advantage), 0.5)  # Cap at 0.5 difference
        worth_adjustment = worth_magnitude * 0.08  # Scale to max of 0.04
        if worth_advantage > 0:
            win_prob += worth_adjustment
        else:
            win_prob -= worth_adjustment
            
        # Apply PRIME adjustment
        prime_magnitude = min(abs(prime_advantage), 0.5)
        prime_adjustment = prime_magnitude * 0.08
        if prime_advantage > 0:
            win_prob += prime_adjustment
        else:
            win_prob -= prime_adjustment
            
        # Apply NERVE adjustment
        nerve_magnitude = min(abs(nerve_advantage), 0.5)
        base_nerve_adjustment = 0.03 + (0.04 * closeness)
        nerve_adjustment = base_nerve_adjustment * (0.5 + nerve_magnitude)
        
        if nerve_advantage > 0:
            win_prob += nerve_adjustment
        else:
            win_prob -= nerve_adjustment

    # Determine winner
    winner = team1_name if win_prob > 0.5 else team2_name
    
    # Determine which team's win probability to report
    reported_win_prob = win_prob if winner == team1_name else 1 - win_prob
    
    # Format the score with winner first
    predicted_score = f"{team1_predicted_score}-{team2_predicted_score}" if winner == team1_name else f"{team2_predicted_score}-{team1_predicted_score}"
    
    # Build the result dictionary
    result = {
        "team1": {
            "name": team1_name,
            "rank": team1['rank'],
            "record": team1['record'],
            "win_pct": team1_win_pct,
            "adjoe": team1['adjoe'],
            "adjde": team1['adjde'],
            "barthag": team1['barthag'],
            "predicted_score": team1_predicted_score
        },
        "team2": {
            "name": team2_name,
            "rank": team2['rank'],
            "record": team2['record'],
            "win_pct": team2_win_pct,
            "adjoe": team2['adjoe'],
            "adjde": team2['adjde'],
            "barthag": team2['barthag'],
            "predicted_score": team2_predicted_score
        },
        "prediction": {
            "winner": winner,
            "win_probability": reported_win_prob,
            "score": predicted_score,
            "team1_win_probability": win_prob
        }
    }
    
    # Add MIYA metrics if available
    if miya_data is not None:
        if team1_name in miya_data:
            result["team1"]["WORTH"] = team1_worth
            result["team1"]["PRIME"] = team1_prime
            result["team1"]["ROAD"] = team1_road
            result["team1"]["NERVE"] = team1_nerve
        
        if team2_name in miya_data:
            result["team2"]["WORTH"] = team2_worth
            result["team2"]["PRIME"] = team2_prime
            result["team2"]["ROAD"] = team2_road
            result["team2"]["NERVE"] = team2_nerve
    
    return result

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

    #torvik data that feeds traditional metrics
    data = load_team_data()

    #tournament teams stored in list and dict format (to add metrics to them)
    teams_dict = get_teams_dictionary()
    team_names = list(teams_dict.keys())
    teams_dict = load_miya_data(team_names, teams_dict)

    #grab matchups to parse
    matchups_df = pd.read_excel('matchups.xlsx')
    results_df = matchups_df.copy()
    
    # Add columns for predicted winner, confidence, scores and MIYA metrics
    results_df['predicted_winner'] = None
    results_df['confidence'] = None
    results_df['predicted_score'] = None
    
    # Add columns for Team 1 MIYA metrics
    results_df['team1_WORTH'] = None
    results_df['team1_PRIME'] = None
    results_df['team1_ROAD'] = None
    results_df['team1_NERVE'] = None
    
    # Add columns for Team 2 MIYA metrics
    results_df['team2_WORTH'] = None
    results_df['team2_PRIME'] = None
    results_df['team2_ROAD'] = None
    results_df['team2_NERVE'] = None
    
    # Add advantage columns
    results_df['WORTH_advantage'] = None
    results_df['PRIME_advantage'] = None
    results_df['ROAD_advantage'] = None
    results_df['NERVE_advantage'] = None

    for index, row in matchups_df.iterrows():
        team1 = row['team_1']
        team2 = row['team_2']
        seed1 = row['seed_1']
        seed2 = row['seed_2']
        
        # Call the predict_winner function for each matchup
        try:
            prediction = predict_winner(team1, team2, data, teams_dict)
            
            # Store the prediction results
            results_df.at[index, 'predicted_winner'] = prediction['prediction']['winner']
            results_df.at[index, 'confidence'] = prediction['prediction']['win_probability']
            results_df.at[index, 'predicted_score'] = prediction['prediction']['score']
            
            # Store MIYA metrics for team 1 if available
            if 'WORTH' in prediction['team1']:
                results_df.at[index, 'team1_WORTH'] = prediction['team1']['WORTH']
                results_df.at[index, 'team1_PRIME'] = prediction['team1']['PRIME']
                results_df.at[index, 'team1_ROAD'] = prediction['team1']['ROAD']
                results_df.at[index, 'team1_NERVE'] = prediction['team1']['NERVE']
            
            # Store MIYA metrics for team 2 if available
            if 'WORTH' in prediction['team2']:
                results_df.at[index, 'team2_WORTH'] = prediction['team2']['WORTH']
                results_df.at[index, 'team2_PRIME'] = prediction['team2']['PRIME']
                results_df.at[index, 'team2_ROAD'] = prediction['team2']['ROAD']
                results_df.at[index, 'team2_NERVE'] = prediction['team2']['NERVE']
            
            # Calculate and store advantages (team1 - team2)
            if 'WORTH' in prediction['team1'] and 'WORTH' in prediction['team2']:
                results_df.at[index, 'WORTH_advantage'] = prediction['team1']['WORTH'] - prediction['team2']['WORTH']
                results_df.at[index, 'PRIME_advantage'] = prediction['team1']['PRIME'] - prediction['team2']['PRIME']
                results_df.at[index, 'ROAD_advantage'] = prediction['team1']['ROAD'] - prediction['team2']['ROAD']
                results_df.at[index, 'NERVE_advantage'] = prediction['team1']['NERVE'] - prediction['team2']['NERVE']
            
            # Print progress
            print(f"Processed matchup {index+1}/{len(matchups_df)}: {team1} ({seed1}) vs {team2} ({seed2})")
            print(f"  Predicted winner: {prediction['prediction']['winner']} with {prediction['prediction']['win_probability']:.2%} confidence")
            print_matchup_results(prediction)
        except Exception as e:
            print(f"Error processing matchup {index+1}: {e}")

    # Save the results to an Excel file in the predictions folder
    # Create predictions directory if it doesn't exist
    predictions_dir = "predictions"
    if not os.path.exists(predictions_dir):
        os.makedirs(predictions_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(predictions_dir, f'prediction_results_{timestamp}.xlsx')
    
    # Save the file
    results_df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")

    #optional interactive mode
    # if data is not None:
    #     print(team_names)
    #     print("\nEnter team names to predict a matchup (or 'quit' to exit):")
    #     while True:
    #         team1 = input("Team 1: ")
    #         if team1.lower() == 'quit':
    #             break
                
    #         team2 = input("Team 2: ")
    #         if team2.lower() == 'quit':
    #             break
                
    #         results = predict_winner(team1, team2, data)
    #         print_matchup_results(results)
