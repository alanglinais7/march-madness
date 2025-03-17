import os

def rename_team_files():
    """
    Renames all files in the team_data directory by replacing spaces with underscores.
    Returns a dictionary mapping original filenames to new filenames.
    """
    # Define the directory path
    team_data_dir = "team_data"
    
    # Dictionary to store the mapping of original to new filenames
    renamed_files = {}
    
    # Check if the directory exists
    if not os.path.isdir(team_data_dir):
        print(f"Error: Directory '{team_data_dir}' not found.")
        return renamed_files
    
    # Iterate through all files in the directory
    for filename in os.listdir(team_data_dir):
        # Check if the file is a CSV and contains spaces
        if filename.endswith('.csv') and ' ' in filename:
            # Create the new filename by replacing spaces with underscores
            new_filename = filename.replace(' ', '_')
            
            # Get the full paths
            original_path = os.path.join(team_data_dir, filename)
            new_path = os.path.join(team_data_dir, new_filename)
            
            # Rename the file
            try:
                os.rename(original_path, new_path)
                renamed_files[filename] = new_filename
                print(f"Renamed: '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")
    
    # Return the mapping of renamed files
    return renamed_files

# Example usage
if __name__ == "__main__":
    renamed = rename_team_files()
    
    if renamed:
        print("\nSummary of renamed files:")
        for old, new in renamed.items():
            print(f"  {old} → {new}")
    else:
        print("No files were renamed.")

