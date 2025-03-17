import pandas as pd
import os
import re

def load_team_data(file_path='torvik_data_2025.xlsx'):
    """
    Load team data from the Excel file
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded data for {len(df)} teams from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading team data: {e}")
        return None

def get_team_files(directory='team_data'):
    """
    Get list of team files from the team_data directory
    """
    try:
        # Get all CSV files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        
        # Extract team names from file names (remove .csv extension)
        team_names = [os.path.splitext(f)[0] for f in files]
        
        print(f"Found {len(team_names)} team files in {directory}")
        return team_names
    except Exception as e:
        print(f"Error getting team files: {e}")
        return []

def check_team_name_matches():
    """
    Check if every file name in team_data has a match in the team column of torvik_data_2025
    """
    # Load team data from Excel
    df = load_team_data()
    if df is None:
        return
    
    # Get team names from files
    file_team_names = get_team_files()
    if not file_team_names:
        return
    
    # Get team names from Excel
    excel_team_names = df['team'].str.lower().tolist()
    
    # Check for matches
    missing_matches = []
    for file_team in file_team_names:
        # Skip .DS_Store and other non-team files
        if file_team.startswith('.'):
            continue
            
        # Convert to lowercase for case-insensitive comparison
        file_team_lower = file_team.lower()
        
        # Handle special cases (e.g., "Saint" vs "St.")
        file_team_normalized = normalize_team_name(file_team_lower)
        
        # Check if normalized team name exists in Excel data
        match_found = False
        for excel_team in excel_team_names:
            excel_team_normalized = normalize_team_name(excel_team)
            if file_team_normalized == excel_team_normalized:
                match_found = True
                break
        
        if not match_found:
            missing_matches.append(file_team)
    
    # Print results
    if missing_matches:
        print("\nTeam files without matches in torvik_data_2025.xlsx:")
        for team in missing_matches:
            print(f"  - {team}")
        print(f"\nTotal: {len(missing_matches)} teams without matches")
    else:
        print("\nAll team files have matches in torvik_data_2025.xlsx")

def normalize_team_name(name):
    """
    Normalize team names to handle common variations
    """
    # Convert to lowercase
    name = name.lower()
    
    # Handle "Saint" vs "St."
    name = re.sub(r'\bst\.?\s', 'saint ', name)
    
    # Handle "State" vs "St."
    name = re.sub(r'\bst\.?\s', 'state ', name)
    
    # Handle ampersands
    name = name.replace('&', 'and')
    
    # Remove "University", "College", etc.
    name = re.sub(r'\buniversity\b|\bcollege\b|\buniv\b', '', name)
    
    # Remove common suffixes
    name = re.sub(r'\bstate university\b', 'state', name)
    
    # Remove "The" prefix
    name = re.sub(r'^the\s+', '', name)
    
    # Handle hyphens and underscores
    name = name.replace('-', ' ').replace('_', ' ')
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name

if __name__ == "__main__":
    check_team_name_matches() 