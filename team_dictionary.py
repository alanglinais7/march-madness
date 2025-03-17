import os

def get_teams_dictionary():
    """
    Creates a dictionary of all teams that have a file in the team_data directory.
    Returns a dictionary with team names as keys and empty dictionaries as values.
    """
    teams_dict = {}
    
    # Get all CSV files from the team_data directory
    team_files = [f for f in os.listdir('team_data') if f.endswith('.csv') and not f.startswith('.')]
    
    # Create dictionary entries for each team
    for team_file in team_files:
        # Remove the .csv extension to get the team name
        team_name = team_file[:-4]
        teams_dict[team_name] = {}
    
    return teams_dict

# Example usage
if __name__ == "__main__":
    teams = get_teams_dictionary()
    print(f"Found {len(teams)} teams:")
    for i, team in enumerate(sorted(teams.keys()), 1):
        print(f"{i}. {team}")
    
    # Print the full dictionary
    print("\nTeams Dictionary:")
    print(teams) 