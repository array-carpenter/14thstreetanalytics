import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'C:/Users/RaymondCarpenter/Documents/GitHub/14thstreetanalytics/EPA 2021-23 and Coaches - Sheet1.csv'
data = pd.read_csv(file_path)

# Coaches to exclude
exclude_coaches = { 'M. Tomlin', 'S. McDermott', 'R. Saleh', 'Ma. LaFleur', 'R. Rivera', 
                   'N. Sirianni', 'B. Staley', 'K. Stefanski', 'M. Vrabel', 'P. Carroll', 'S. Steichen', 
                   'K. Shanahan', 'D. Pederson', 'M. McCarthy', 'B. Callahan', 'Br. Johnson', 'B. Belichick', 
                   'D. Campbell', 'J. Judge', 'U. Meyer', 'D. Allen', 'Z. Taylor', 'K. O\'Connell', 
                   'S. Waldron', 'J. Harbaugh', 'B. Daboll', 'M. Eberflus', 'M. McDaniel', 'Be. Johnson', 
                   'A. Reid', 'S. McVay', 'P. Taylor', 'N. Hackett', 'M. Nagy', 'M. Canada', 'J. McDaniels', 
                   'J. Brady', 'L. Getsy', 'T. Monken', 'J. Gruden','M. Patricia','J. Garrett', 'M. Zimmer', 'A. Tanney', 'T. Bowles', 'B. Schottenheimer','C. O\'Hara', 'P. Taylor',
                   'E. Studesville', 'D. Petzing', 'I. Woolfork', 'P. Shurmur', 'V. Fangio', 'T. Downing', 'D. Webb', 'S. Payton', 'B. Flores','J. Urban','M. Nagy', 'N. Hackett', 'J. Gannon',
                   'D. Nussmeier', 'A. Stenavich', 'P. Carmichael', 'S. Whipple', 'B. Lazor','B. O\'Brien', 'B. Slowik','T Bowles','C. Christensen','D. Ryans', 'D. Ragone','S. Brady','M. Milanovich', 'S. Day',
                   'S. McVay', 'B. Hardegree','M. Lombardi', 'K. Zampese','S. Milanovich','L. Smith','J. McCown','D. Culley'}

# Prepare a DataFrame to store the aggregated data for each coach
coach_data = pd.DataFrame(columns=['Coach', 'Avg CPOE', 'Avg EPA/play'])

# Extracting unique coaches and filtering out the excluded ones
coaches = (set(data['HC'].unique()) | set(data['OC'].dropna().unique()) | set(data['QBC'].dropna().unique())) - exclude_coaches

# Aggregate data for each coach
for coach in coaches:
    coach_rows = data[(data['HC'] == coach) | (data['OC'] == coach) | (data['QBC'] == coach)]
    avg_cpoe = coach_rows['CPOE'].mean()
    avg_epa_play = coach_rows['EPA/play'].mean()

    coach_data = coach_data.append({'Coach': coach, 'Avg CPOE': avg_cpoe, 'Avg EPA/play': avg_epa_play}, ignore_index=True)

# Removing entries with NaN values
coach_data.dropna(inplace=True)

# Define colors for each position
position_colors = {'HC': 'red', 'OC': 'blue', 'QBC': 'green'}

# Plotting
plt.figure(figsize=(15, 10))
sns.set(style="whitegrid")

# Custom offsets for specific coaches to prevent name overlap
custom_offsets = {
    'Coach Name 1': (0.02, 0.02),  # Adjust these values as needed
    'Coach Name 2': (-0.02, -0.02), # Adjust these values as needed
    # Add more coaches here if needed
}

# Plot each coach's average and manually adjust text positions
for _, row in coach_data.iterrows():
    # Determine the color based on the position
    if row['Coach'] in data['HC'].values:
        color = position_colors['HC']
    elif row['Coach'] in data['OC'].values:
        color = position_colors['OC']
    elif row['Coach'] in data['QBC'].values:
        color = position_colors['QBC']
    else:
        color = 'gray'  # Default color if position not found

    # Apply custom offset if the coach is in the custom_offsets dictionary
    x_offset, y_offset = custom_offsets.get(row['Coach'], (0.01, 0.01))
    plt.scatter(row['Avg CPOE'], row['Avg EPA/play'], color=color)
    plt.text(row['Avg CPOE'] + x_offset, row['Avg EPA/play'] + y_offset, row['Coach'], verticalalignment='center', fontsize=12, color='black', ha='right')

# Improving layout
plt.xlabel('Average CPOE', fontsize=14)
plt.ylabel('Average EPA/play', fontsize=14)
plt.title('Average Coach Performance (CPOE vs. EPA/play)', fontsize=16)
plt.grid(True)
plt.tight_layout()

plt.show()
