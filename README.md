# March Madness Data Analysis

This repository contains tools for collecting and analyzing college basketball data, specifically focused on Bart Torvik's college basketball statistics (barttorvik.com) and Evan Miya's Game Analysis data (EvanMiya.com)

## Features

- Fetches current season data from barttorvik.com
- Processes and cleans the data into a usable format
- Extracts key statistics including:
  - Team rankings
  - Win/loss records
  - Conference information
  - Advanced metrics (adjusted offense/defense)
- Exports data to Excel for further analysis
- Predicts head-to-head matchup outcomes with score predictions
- Interactive mode for comparing any two teams (Need to enable by uncommenting code, also possible via adding to matchups.xslx)

## Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

### Usage

#### Data Collection

To fetch the current season's data:

```python
python base_data_grab.py
```

This will:
1. Download the latest data from barttorvik.com
2. Process and clean the data
3. Save it to an Excel file named `torvik_data_2025.xlsx`

In addition, you'll need to download all of Evan Miya's game analysis CSVs to a folder called team_data. Ensure all schools with spaces are seperated by an underscore (i.e. Michigan State -> Michigan_State.csv)

#### Head-to-Head Predictions

To predict matchup outcomes:

```python
python head_to_head.py
```

This will:
1. Load the team data from the Excel files
2. Run predictions for sample matchups
3. Enter interactive mode where you can input any two teams to compare

## Prediction Model

The head-to-head prediction model uses:
- Adjusted offensive efficiency (adjoe)
- Adjusted defensive efficiency (adjde)
- Tempo for # of possesions
- Team power rating (barthag)
- Win-loss record

and some custom calcualted metrics
- `WORTH` (Wins Over Ranked Tournament-Headed Squads)
- `PRIME` (Performance Rating In Major Engagements) 
- `ROAD` (Reliability Outside Accustomed Domain) 
- `NERVE` (Narrow Endgame Resolution and Victory Evaluation)

The model calculates:
- Win probability for each team
- Predicted score based on offensive and defensive efficiencies
- Matchup advantages in key statistical areas

## Data Fields

The exported data includes:
- `rank`: Team's current ranking
- `team`: Team name
- `conf`: Conference affiliation
- `record`: Win-loss record (e.g., "25-4")
- `wins`: Number of wins (extracted from record)
- `losses`: Number of losses (extracted from record)
- `adjoe`: Adjusted offensive efficiency (points per 100 possessions)
- `adjde`: Adjusted defensive efficiency (points allowed per 100 possessions)
- `barthag`: Power rating (probability of beating average team)
- Additional advanced metrics from Torvik's system

## Visualizing your bracket

To showcase your bracket for screenshots and sharing, simply launch the bracket.html file in the browswer of your choice and then load in your results file in the format returned by the head_to_head script. Then hit load file.

## Contributing

Feel free to open issues or submit pull requests with improvements. 

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data sourced from [Bart Torvik's college basketball statistics](http://barttorvik.com) and [Evan Miya's website](https://evanmiya.com). 