import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Data
weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
passing_grades = [58.0, 74.0, 64.0, 80.4, 79.0, 67.5, 80.5, 69.8, 79.6, 75.2, 74.4, 65.8, 78.0]
pass_attempts = [30, 31, 37, 37, 38, 45, 31, 38, 23, 22, 31, 45, 27]
max_attempts = max(pass_attempts)
circle_sizes = [(attempts / max_attempts) * 500 for attempts in pass_attempts]

# Path to the folder containing logos
logo_folder = "nfl_logos"

# List of logo filenames in the order of the teams played
team_logos = ['8022.png', '8021.png', '8030.png', 
              '8032.png', '8018.png', '8025.png', '8020.png', 
              '8032.png', '8009.png', '8016.png', '8004.png', 
              '8029.png', '8009.png']  # Corrected list with proper commas
# Percentiles
percentiles = {
    "90th": 85,
    "75th": 78,
    "50th": 66,
    "25th": 57,
    "10th": 48
}

circle_sizes = [attempts / max_attempts * 500 for attempts in pass_attempts]
circle_color = '#004C54'
line_color = '#004C54'
# Create the plot
plt.figure(figsize=(15, 10))
plt.plot(weeks, passing_grades, marker='', color=line_color, linestyle='-')

# Add the circles and logos
for i, grade in enumerate(passing_grades):
    plt.scatter(weeks[i], grade, s=circle_sizes[i], color=circle_color,marker='o')
    plt.text(weeks[i], grade, str(passing_grades[i]), color='white', ha='center', va='center',fontweight='bold')

    # Load and add the team logo
    logo_path = f"{logo_folder}\\{team_logos[i]}"
    logo = mpimg.imread(logo_path)
    img_extent = [weeks[i] - 0.3, weeks[i] + 0.3, grade - 6, grade - 3]  # Adjust as needed
    plt.imshow(logo, aspect='auto', extent=img_extent,zorder=5)
for percentile, value in percentiles.items():
    plt.axhline(y=value, color='black', linestyle='--', alpha=0.7)
    plt.text(0.2, value, f'{percentile} percentile', va='center', color='black', fontsize=8,backgroundcolor='white',bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.1'))

# Set the range for y-axis and adjust x-axis intervals
plt.ylim(40, 90)
plt.xticks(np.arange(0, max(weeks)+1, 1))  # Adding a 0 to the x-a
plt.xlabel('Week')
plt.ylabel('PFF Passing Grade')

# Add a title and grid
fig_text(
    x=0.1, y=.965,
    s="Jalen Hurts PFF Passing Grades by Week"
    #,
    #highlight_textprops=[
     #   {"color": colors[0]},
      #  {"color": colors[1]}
    #]
,
    va="bottom", ha="left",
    fontsize=18, color="black", weight="bold"
)
fig_text(
    x=.1, y=.940,
    s="Source: PFF | Viz by Ray Carpenter | Inspired by a viz by @benbbaldwin | 14thstreetanalytics.substack.com",
    va="bottom", ha="left",
    fontsize=12, color="#4E616C"
)
# Show
plt.grid(True, zorder=0)

# Show the plot
plt.show()
