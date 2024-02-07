# Unzip Folder
import zipfile
import os
import pandas as pd
import json
import csv
from io import StringIO

def unzip_folder(zip_file_path, extract_to):
    if not zipfile.is_zipfile(zip_file_path):
        print("Invalid zip file.")
        return
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract all contents to the specified directory
        zip_ref.extractall(extract_to)
        print("Folder successfully unzipped to:", extract_to)

if __name__ == "__main__":
    zip_file_path = "/PATH.zip" 
    extract_to = "/EXTRACT_PATH"

    unzip_folder(zip_file_path, extract_to)

# List of match files in unzipped folder
json_files = ['10000_metadata.json', '10017_metadata.json', 
              '10013_metadata.json', '100094_metadata.json',
              '10009_metadata.json']


# Create empty df to enter parsed json into
all_data = pd.DataFrame()

# loop for loading each json
for json_file in json_files:
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    # flatten
    flat_data = pd.json_normalize(json_data)

    # more granular flattening for players fields
    players_data = pd.json_normalize(json_data['players'])
    flat_data = pd.concat([flat_data, players_data], axis=1).drop('players', axis=1)

    # append game id to every row
    flat_data['game_id'] = json_data['id']

    # put all data in df
    all_data = all_data.append(flat_data, ignore_index=True)

# Save the combined data to a CSV file
all_csv_path = 'combined_metadata.csv'
all_data.to_csv(all_csv_path, index=False)

print(f'All CSV files have been combined into: {all_csv_path}')

# Transform tracking txt files into a df
tracking_files = ['10000_tracking.txt', '10017_tracking.txt', 
              '10013_tracking.txt', '100094_tracking.txt',
              '10009_tracking.txt']
for txt_file in tracking_files:
    with open(txt_file, 'r') as file:
        lines = txt_file.readlines()
# Output CSV file path
    output_csv_path = 'output.csv'

# Open the CSV file for writing
    with open(output_csv_path, 'w', newline='') as output_csv:
    # Create a CSV writer object
        csv_writer = csv.writer(output_csv)

    # Write header to CSV
        csv_writer.writerow(["track_id", "trackable_object", "is_visible", "x", "y", "z", "frame", "timestamp"])

    # Iterate through each line in the input file
        for line in lines:
        # Load JSON data from the line
            data = json.loads(line)

        # Extract relevant information
            frame = data.get("frame")
            timestamp = data.get("timestamp")

            for item in data.get("data", []):
                track_id = item.get("track_id")
                trackable_object = item.get("trackable_object")
                is_visible = item.get("is_visible")
                x = item.get("x", 0.0)
                y = item.get("y", 0.0)
                z = item.get("z", 0.0)

            # Write the extracted data to CSV
                csv_writer.writerow([track_id, trackable_object, is_visible, x, y, z, frame, timestamp])

print(f'CSV file created successfully at: {output_csv_path}')

# Read transformed metadata CSV and divide into snowflake schema
df = pd.read_csv('combined_metadata.csv')

DimStadium = df[['stadium.id', 'stadium.name', 'stadium.city', 'stadium.capacity','pitch_length','pitch_width']]
DimTeam = df[['home_team.id', 'home_team.name', 'home_team.short_name', 'home_team.acronym',
                   'away_team.id', 'away_team.name', 'away_team.short_name', 'away_team.acronym']]
DimKit = df[['home_team_kit.id', 'home_team_kit.team_id', 'home_team_kit.season.id',
                  'home_team_kit.season.start_year', 'home_team_kit.season.end_year',
                  'home_team_kit.season.name', 'home_team_kit.name', 'home_team_kit.jersey_color',
                  'home_team_kit.number_color', 'away_team_kit.id', 'away_team_kit.team_id',
                  'away_team_kit.season.id', 'away_team_kit.season.start_year',
                  'away_team_kit.season.end_year', 'away_team_kit.season.name',
                  'away_team_kit.name', 'away_team_kit.jersey_color', 'away_team_kit.number_color']]
DimSeason = df[['competition_edition.season.id','competition_edition.season.start_year','competition_edition.season.end_year']]
DimCoach = df[['home_team_coach.id', 'home_team_coach.first_name', 'home_team_coach.last_name',
                    'away_team_coach.id', 'away_team_coach.first_name', 'away_team_coach.last_name']]
DimCompetition = df[['competition_edition.id', 'competition_edition.competition.id',
                          'competition_edition.competition.area', 'competition_edition.competition.name',
                          'competition_edition.season.id', 'competition_edition.season.start_year',
                          'competition_edition.season.end_year', 'competition_edition.season.name',
                          'competition_edition.name', 'competition_round.id', 'competition_round.name',
                          'competition_round.round_number', 'competition_round.potential_overtime']]
DimCompetitionRound = df[['competition_round.id','competition_edition.name','competition_round.round_number','competition_round.potential_overtime']]
DimCompetionEdition = df[['competition_edition.id','competition_edition.competition.id','competition_edition.competition.area','competition_edition.competition.name','competition_edition.season.id']]
DimPlayer = df[['id.1', 'first_name', 'last_name', 'short_name', 'birthday', 'trackable_object',
                     'gender', 'player_role.id', 'player_role.name', 'player_role.acronym']]
DimPlayerRole = df[['player_role.id','player_role.name','player_role.acronym']]
FactMatch = df[['id', 'home_team_score','away_team_score','date_time','referees','status','home_team_side','stadium.id','home_team.id','away_team.id','competition_edition.season.id','home_team_coach.id','away_team_coach.id','competition_edition.id',
                'competition_edition.competition.id','competition_round.id','start_time','end_time','away_team_kit.id','ball.trackable_object',
                'yellow_card','red_card','goal','own_goal','injured']]

# Save each schema to a separate CSV file
DimStadium.to_csv('DimStadium.csv', index=False)
DimTeam.to_csv('DimTeam.csv', index=False)
DimKit.to_csv('DimKit.csv', index=False)
DimCoach.to_csv('DimCoach.csv', index=False)
DimCompetition.to_csv('DimCompetition.csv', index=False)
DimPlayer.to_csv('DimPlayer.csv', index=False)
DimCompetionEdition.to_csv('DimCompetitionEdition.csv',index=False)
DimCompetitionRound.to_csv('DimCompetitionRound.csv',index=False)
DimSeason.to_csv('DimSeason.csv',index=False)
DimPlayerRole.to_csv('DimPlayerRole.csv',index=False)
FactMatch.to_csv('FactMatch.csv',index=False)
# Would move csvs into cloud storage folders at this point

