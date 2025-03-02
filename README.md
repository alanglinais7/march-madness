# March Madness Data Analysis

This repository contains tools for collecting and analyzing college basketball data, specifically focused on Bart Torvik's college basketball statistics (barttorvik.com).

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
- Interactive mode for comparing any two teams

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

#### Head-to-Head Predictions

To predict matchup outcomes:

```python
python head_to_head.py
```

This will:
1. Load the team data from the Excel file
2. Run predictions for sample matchups
3. Enter interactive mode where you can input any two teams to compare

## Prediction Model

The head-to-head prediction model uses:
- Adjusted offensive efficiency (adjoe)
- Adjusted defensive efficiency (adjde)
- Team power rating (barthag)
- Win-loss record

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

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data sourced from [Bart Torvik's college basketball statistics](http://barttorvik.com) 