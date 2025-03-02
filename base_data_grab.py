import pandas as pd
import requests
from io import StringIO

def fetch_torvik_data(year):
    url = f"http://barttorvik.com/{year}_team_results.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Print first few lines of raw data for debugging
        print("Raw data sample:")
        print(response.text[:500])
        
        # Read CSV with explicit parsing parameters
        df = pd.read_csv(
            StringIO(response.text),
            sep=',',              # Explicit comma separator
            quoting=3,            # No special quoting
            skipinitialspace=True # Skip spaces after separators
        )
        
        # Print raw dataframe to verify column alignment
        print("\nRaw DataFrame head:")
        print(df.head())
        
        try:
            # Now process the correctly loaded data
            df['record'] = df['record'].astype(str)
            df[['wins', 'losses']] = df['record'].str.extract(r'(\d+)-(\d+)')
            df['wins'] = pd.to_numeric(df['wins'])
            df['losses'] = pd.to_numeric(df['losses'])
            
            print("\nProcessed data sample:")
            print(df[['rank', 'team', 'conf', 'record', 'wins', 'losses']].head())
            
        except Exception as e:
            print(f"Error processing record data: {e}")
            raise
        
        return df
    
    except requests.RequestException as e:
        print(f"Error fetching data for year {year}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    df = fetch_torvik_data(2025)
    
    if df is not None:
        print("\nSaving data to Excel...")
        output_file = f"torvik_data_2025.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")
        
        # Display final summary
        print("\nFinal data shape:", df.shape)
        print("\nColumns in final dataset:", ', '.join(df.columns))