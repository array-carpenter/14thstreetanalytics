import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
import requests
from io import BytesIO
from PIL import Image

# Define the year and load the data
YEAR = 2024
url = f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{YEAR}.csv.gz'
data = pd.read_csv(url, compression='gzip', low_memory=False)

# Set options for displaying dataframes
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 400)


# Function to get an image from ESPN based on player_id
def get_espn_headshot(player_id: str):
    url = f'https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/{player_id}.png'
    response = requests.get(url)
    
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Could not retrieve headshot for player {player_id}")
        return None

def player_headshot(player_id: str, ax: plt.Axes):
    # Fetch the headshot using the player_id
    headshot = get_espn_headshot(player_id)
    
    if headshot:
        # Display the image on the axis
        ax.imshow(headshot)
        ax.axis('off')  # Hide the axis
    else:
        # Placeholder in case the headshot can't be retrieved
        ax.text(0.5, 0.5, 'No Image', ha='center', va='center', fontsize=12)
        ax.axis('off')

# Load the quarterback information (including player_id) from qb_info.csv
qb_info = pd.read_csv('C:/Users/RaymondCarpenter/Documents/GitHub/14thstreetanalytics/throwing_summary/qb_info.csv')

# Retrieve player info based on player name
player_name = 'Brock Purdy'  # Make sure this matches the format in the CSV
player_info = qb_info[qb_info['Name'] == player_name].iloc[0]

# Get the player ID from the CSV and use it to fetch the headshot
player_id = player_info['player_id']
headshot = get_espn_headshot(player_id)

# Manual filters start here
filtered_df = data[(data['home_team'] == 'SF') | (data['away_team'] == 'SF')] ### change team RAMS are LA Chargers are LAC

# Separate filters for passing and rushing plays
passing_plays = filtered_df[filtered_df['passer_player_name'] == 'B.Purdy'] ### change qb
rushing_plays = filtered_df[filtered_df['rusher_player_name'] == 'B/Purdy'] ### change qb

# Filter game data by game id
game_data_passing = passing_plays[passing_plays['game_id'] == '2024_01_NYJ_SF'] ### follow format YEAR_WEEK_AWAY_HOME 2023_12_BUF_PHI
game_data_rushing = rushing_plays[rushing_plays['game_id'] == '2024_01_NYJ_SF']

# Calculate cumulative completions and attempts for passing plays
game_data_passing['cumulative_completions'] = game_data_passing['complete_pass'].cumsum()
game_data_passing['cumulative_attempts'] = game_data_passing['pass_attempt'].cumsum()
game_data_passing['cumulative_completion_percentage'] = (
    game_data_passing['cumulative_completions'] / game_data_passing['cumulative_attempts']
) * 100

# Sum EPA for both passing and rushing plays
total_passing_epa = game_data_passing['epa'].sum()
total_rushing_epa = game_data_rushing['epa'].sum() 
total_epa = total_passing_epa + total_rushing_epa

# Sum the total number of plays (passing attempts + rushing attempts)
total_plays = game_data_passing['pass_attempt'].sum() + game_data_rushing['rush_attempt'].sum()

# Calculate EPA per play
epa_per_play = round(total_epa / total_plays, 3)

air_yards_per_attempt = round(
    game_data_passing['air_yards'].sum() / game_data_passing['pass_attempt'].sum(), 2
)
success_rate = round(
    game_data_passing[game_data_passing['epa'] > 0].shape[0] / game_data_passing.shape[0] * 100, 1
)

# Calculate passer rating
completions = game_data_passing['complete_pass'].sum()
attempts = game_data_passing['pass_attempt'].sum()
yards = game_data_passing['passing_yards'].sum()
touchdowns = game_data_passing['pass_touchdown'].sum()
interceptions = game_data_passing['interception'].sum()

if attempts > 0:
    comp_pct = completions / attempts
    avg_yards = yards / attempts
    td_pct = touchdowns / attempts
    int_pct = interceptions / attempts

    passer_rating = (comp_pct * 5 + avg_yards * 0.25 + td_pct * 20 - int_pct * 25) / 6 * 100
    passer_rating = round(passer_rating, 1)
else:
    passer_rating = 0

# Include 'game_seconds_remaining' when combining passing and rushing plays
combined_plays = pd.concat([
    game_data_passing[['play_id', 'epa', 'game_seconds_remaining']],
    game_data_rushing[['play_id', 'epa', 'game_seconds_remaining']]
])
combined_plays.sort_values('play_id', inplace=True)
combined_plays['rolling_total_epa'] = combined_plays['epa'].cumsum()
combined_plays['rolling_play_count'] = range(1, len(combined_plays) + 1)
combined_plays['rolling_epa_per_play'] = combined_plays['rolling_total_epa'] / combined_plays['rolling_play_count']

# Determine play IDs for quarter lines using game_seconds_remaining
quarter_end_times = [3600, 2700, 1800, 900]  # Remove the 0 for overtime unless it's a known OT game ,0
quarter_positions = []

# Use a boolean flag to control the inclusion of the overtime line
overtime = False

for end_time in quarter_end_times:
    try:
        # Only append play_id if it uniquely identifies the end of a quarter
        play_id = combined_plays[combined_plays['game_seconds_remaining'] <= end_time].iloc[0]['play_id']
        if play_id not in quarter_positions:
            quarter_positions.append(play_id)
    except IndexError:
        continue

# If the last quarter position is 0, it's mistakenly identifying overtime, remove it
if overtime or (len(quarter_positions) > 0 and quarter_positions[-1] == 0):
    quarter_positions = quarter_positions[:-1]


# Create bins for pass distances
bins = [-np.inf, 1, 10, 25, np.inf]
labels = ['Screen', 'Short', 'Medium', 'Deep']
game_data_passing['pass_distance_category'] = pd.cut(game_data_passing['air_yards'], bins=bins, labels=labels)

# Calculate success rate, EPA/play, attempts, and completions for each category
pass_distance_summary = game_data_passing.groupby('pass_distance_category').agg({
    'pass_attempt': 'sum',
    'complete_pass': 'sum',
    'epa': 'sum'  # Sum EPA for each category
}).reset_index()

# Convert the categorical column to a regular object type to avoid issues with setting NaN
pass_distance_summary['pass_distance_category'] = pass_distance_summary['pass_distance_category'].astype(object)

# Calculate EPA per play for each category by dividing total EPA by total pass attempts
pass_distance_summary['EPA/Play'] = (pass_distance_summary['epa'] / pass_distance_summary['pass_attempt']).round(2)

pass_distance_summary['Success Rate'] = (pass_distance_summary['complete_pass'] / pass_distance_summary['pass_attempt']) * 100

# Replace NaN values with 0
pass_distance_summary.fillna(0, inplace=True)

pass_distance_summary = pass_distance_summary[['pass_distance_category', 'pass_attempt', 'complete_pass', 'Success Rate', 'EPA/Play']]

pass_distance_summary.columns = ['Distance', 'Att', 'Completions', 'Success Rate', 'EPA/Play']

# Format numbers without decimal points in the tables
pass_distance_summary['Att'] = pass_distance_summary['Att'].astype(int)
pass_distance_summary['Completions'] = pass_distance_summary['Completions'].astype(int)
pass_distance_summary['Success Rate'] = pass_distance_summary['Success Rate'].apply(lambda x: f"{x:.1f}%")

# Check for non-null rush attempts and rushing yards to avoid issues with missing data
game_data_rushing = game_data_rushing.dropna(subset=['rush_attempt', 'rushing_yards', 'rush_touchdown'])

# Calculate rushing statistics
rush_attempts = game_data_rushing['rush_attempt'].sum()
rush_yards = game_data_rushing['rushing_yards'].sum()
rush_touchdowns = game_data_rushing['rush_touchdown'].sum()

# Handle cases where there might be no rushing stats available
if rush_attempts == 0:
    rush_yards = 0
    rush_touchdowns = 0

# Update the summary table with passing and rushing stats
summary_table = {
    'Att': [int(game_data_passing['pass_attempt'].sum())],
    'Cmp': [int(game_data_passing['complete_pass'].sum())],
    'Yds': [int(game_data_passing['passing_yards'].sum())],
    'TD': [int(game_data_passing['pass_touchdown'].sum())],
    'Int': [int(game_data_passing['interception'].sum())],
    'Sck': [int(game_data_passing['sack'].sum())],
    'Rush Att': [int(rush_attempts)],        
    'Rush Yds': [int(rush_yards)],           
    'Rush TD': [int(rush_touchdowns)],       
    'Passer Rtg': [passer_rating],
    'EPA/Play': [epa_per_play],              
    'AY/A': [air_yards_per_attempt],
    'Success Rate': [f"{success_rate}%"]
}

# Create the updated summary DataFrame
summary_df = pd.DataFrame.from_dict(summary_table)

player_name = 'Brock Purdy' 
player_info = qb_info[qb_info['Name'] == player_name].iloc[0]

# Get the player ID from the CSV and fetch the headshot
player_id = player_info['player_id']
headshot = get_espn_headshot(player_id)

logo_path = '/Users/raymondcarpenter/Documents/GitHub/14thstreetanalytics/throwing_summary/niners_logo.png' # manually find logo path
logo = Image.open(logo_path)

def qb_dashboard(game_data_passing: pd.DataFrame, headshot: Image, logo: Image, summary_df: pd.DataFrame, pass_distance_summary: pd.DataFrame, quarter_positions, save_path: str = None):
    # Create a more compact figure
    fig = plt.figure(figsize=(18, 14))  

    # Create a gridspec layout with adjusted settings for alignment and spacing
    gs = gridspec.GridSpec(6, 20, 
                           height_ratios=[2, 4, 4, 25, 10, 5],  
                           width_ratios=[1, 3, 1, 4, 1, 3, 1, 3, 1, 3, 1, 4, 1, 3, 1, 3, 1, 3, 1, 1])  # Equal width for plots and tables

    # Define the positions of each subplot in the grid
    ax_headshot = fig.add_subplot(gs[1, 2:4])  # Positioned headshot
    ax_bio = fig.add_subplot(gs[1, 5:13])  # Centered bio text more
    ax_logo = fig.add_subplot(gs[1, 14:16])  # Positioned logo

    ax_summary_table = fig.add_subplot(gs[2, 1:19])

    # Adjust plot positions for compactness
    ax_rolling_epa = fig.add_subplot(gs[3, 1:7])  # Rolling EPA
    ax_yards_dist = fig.add_subplot(gs[3, 7:13])  # Yards Distribution
    ax_passing_chart = fig.add_subplot(gs[3, 13:19])  # Pass Location Chart

    ax_pass_distance = fig.add_subplot(gs[4, 1:19])  # Pass Distance Table

    ax_footer = fig.add_subplot(gs[-1, 1:19])  # Footer
    ax_left = fig.add_subplot(gs[:, 0])
    ax_right = fig.add_subplot(gs[:, -1])

    # Hide axes for footer, left, and right
    ax_footer.axis('off')
    ax_left.axis('off')
    ax_right.axis('off')

# Use the player_headshot function to display the headshot
    player_headshot(player_id, ax_headshot)

# Plot logo as before
    ax_logo.imshow(logo)    
    ax_logo.axis('off')

    # Biographical Information with adjusted horizontal and vertical space
    ax_bio.text(0.5, 0.95, 'Brock Purdy', fontsize=22, ha='center', fontweight='bold')  # manual
    ax_bio.text(0.5, 0.50, 'RHQB, Age: 24, 6\'1/220', fontsize=18, ha='center')  # manual
    ax_bio.text(0.5, 0.1, '2024 Week 1 Throwing Summary vs. New York Jets', fontsize=18, ha='center', fontstyle='italic')  # manual
    ax_bio.axis('off')

    # Summary Table Plot - Adjusted for more compact cells
    ax_summary_table.axis('off')
    table = ax_summary_table.table(cellText=summary_df.values,
                                   colLabels=summary_df.columns,
                                   cellLoc='center',
                                   loc='center',
                                   colColours=['#f2f2f2'] * len(summary_df.columns),
                                   colWidths=[0.1] * len(summary_df.columns))  # Reduced column width
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # Set a smaller font size for compactness
    table.scale(0.8, 1.5)  # Reduced scale for compactness

    # Rolling Total EPA/Play Plot
    ax_rolling_epa.plot(combined_plays['play_id'], combined_plays['rolling_epa_per_play'], marker='o', linestyle='-', color='green')
    for pos in quarter_positions:
        ax_rolling_epa.axvline(x=pos, color='red', linestyle='--', linewidth=1)
    ax_rolling_epa.set_xlabel('Play ID', fontdict={'size': 14})
    ax_rolling_epa.set_ylabel('Rolling EPA/Play', fontdict={'size': 14})
    ax_rolling_epa.set_title('Rolling Total EPA/Play Throughout Game', fontdict={'size': 18})
    ax_rolling_epa.grid(True)

    # Yards Gained Distribution Plot
    sns.histplot(game_data_passing['yards_gained'], bins=10, kde=True, color='blue', ax=ax_yards_dist)
    ax_yards_dist.set_xlabel('Yards Gained', fontdict={'size': 14})
    ax_yards_dist.set_ylabel('Frequency', fontdict={'size': 14})
    ax_yards_dist.set_title('Distribution of Yards Gained', fontdict={'size': 18})

    # Pass Location Chart Plot
    game_data_passing['x'] = game_data_passing['pass_location'].replace({'left': -1, 'middle': 0, 'right': 1})
    game_data_passing['y'] = game_data_passing['air_yards']

    complete = game_data_passing[game_data_passing['complete_pass'] == 1]
    incomplete = game_data_passing[game_data_passing['complete_pass'] == 0]
    interceptions = game_data_passing[game_data_passing['interception'] == 1]
    touchdowns = game_data_passing[game_data_passing['pass_touchdown'] == 1]

    ax_passing_chart.scatter(complete['x'], complete['y'], color='green', label='Complete', s=80, edgecolor='black')
    ax_passing_chart.scatter(incomplete['x'], incomplete['y'], color='red', marker='x', label='Incomplete', s=80)
    ax_passing_chart.scatter(interceptions['x'], interceptions['y'], color='purple', marker='D', label='INT', s=80)
    ax_passing_chart.scatter(touchdowns['x'], touchdowns['y'], color='gold', marker='o', label='TD', s=80, edgecolor='black')

    # Add horizontal dotted lines every 10 yards
    for y in range(0, 51, 10):
        ax_passing_chart.axhline(y, color='gray', linestyle=':', linewidth=1)

    # Formatting
    ax_passing_chart.axhline(0, color='black', linewidth=2)  # Line of scrimmage
    ax_passing_chart.set_xlim(-1.5, 1.5)
    ax_passing_chart.set_ylim(-10, 50)
    ax_passing_chart.set_xticks([-1, 0, 1])
    ax_passing_chart.set_xticklabels(['Left', 'Middle', 'Right'], fontsize=12)
    ax_passing_chart.set_yticks(range(0, 51, 10))
    ax_passing_chart.set_xlabel('Horizontal Placement', fontsize=12)
    ax_passing_chart.set_ylabel('Depth of Target (yards)', fontsize=12)

    # Set legend as the title, placed on top
    ax_passing_chart.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=4, fontsize=10, frameon=False)

    # Pass Distance Table
    ax_pass_distance.axis('off')
    pass_distance_table = ax_pass_distance.table(
        cellText=pass_distance_summary.values,
        colLabels=pass_distance_summary.columns,
        cellLoc='center',
        loc='center',
        colColours=['#f2f2f2'] * len(pass_distance_summary.columns),
        colWidths=[0.18] * len(pass_distance_summary.columns)  # Column width adjustment
    )
    pass_distance_table.auto_set_font_size(False)
    pass_distance_table.set_fontsize(12)  # Font size adjustment
    pass_distance_table.scale(.8, 1.5)  # Scaling adjustment

    # Footer
    ax_footer.text(0.5, 0.5, 'By Ray Carpenter | 14thstreetanalytics.substack.com | Inspired by a viz by Thomas Nestico | Data from NFLverse | Images from NFL.com', 
                   ha='center', va='center', fontsize=18)

    # Adjust the spacing between subplots with increased padding
    plt.tight_layout(pad=1.5) 

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show the figure
    plt.show()

save_path = '/Users/raymondcarpenter/Documents/GitHub/14thstreetanalytics/throwing_summary/qb_dashboard.png'

qb_dashboard(game_data_passing, headshot, logo, summary_df, pass_distance_summary, quarter_positions, save_path=save_path)

