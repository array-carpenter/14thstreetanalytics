import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

def draw_football_field(team1_name, team2_name, play_description):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    field_width = 160
    field_length = 360
    
    # Draw the field outline
    field_outline = patches.Rectangle((0, 0), field_length, field_width, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(field_outline)
    
    # Draw the midfield line
    midfield_line = patches.ConnectionPatch((field_length/2, 0), (field_length/2, field_width), "data", "data", linewidth=2, edgecolor='black')
    ax.add_patch(midfield_line)
    
    # Draw the yard lines and labels
    for yard in range(0, 101):
        if yard % 10 == 0:
            yard_line = patches.ConnectionPatch((yard * field_length/100, 0), (yard * field_length/100, field_width), "data", "data", linewidth=2, edgecolor='black')
            ax.add_patch(yard_line)
            plt.text(yard * field_length/100, field_width + 8, str(yard), ha='center', va='center', fontsize=10)
    
    # Draw the hashes
    hash_distance = 5.33
    for yard in range(0, 101):
        if yard % 10 != 0:
            hash_line = patches.ConnectionPatch((yard * field_length/100, 0), (yard * field_length/100, hash_distance), "data", "data", linewidth=1, edgecolor='black')
            ax.add_patch(hash_line)
    
    goal_line1 = patches.ConnectionPatch((0, 0), (0, field_width), "data", "data", linewidth=2, edgecolor='black')
    goal_line2 = patches.ConnectionPatch((field_length, 0), (field_length, field_width), "data", "data", linewidth=2, edgecolor='black')
    ax.add_patch(goal_line1)
    ax.add_patch(goal_line2)
    
    # Set colors based on team names
    if "Eagles" in team1_name:
        endzone1_color = '#004C55'
        text_color1 = 'white'
    else:
        endzone1_color = 'none'
        text_color1 = 'black'
    
    if "Eagles" in team2_name:
        endzone2_color = '#004C55'
        text_color2 = 'white'
    else:
        endzone2_color = 'none'
        text_color2 = 'black'
    
    if "Patriots" in team1_name:
        endzone1_color = '#002244'
        text_color1='white'
    
    if "Patriots" in team2_name:
        endzone2_color = '#002244'
        text_color2= 'white'
    
    
    endzone1 = patches.Rectangle((0, 0), 30, field_width, linewidth=2, edgecolor='black', facecolor=endzone1_color)
    endzone2 = patches.Rectangle((field_length - 30, 0), 30, field_width, linewidth=2, edgecolor='black', facecolor=endzone2_color)
    ax.add_patch(endzone1)
    ax.add_patch(endzone2)
    
    # Add team names to endzones
    plt.text(15, field_width/2, team1_name, ha='center', va='center', fontsize=12, color=text_color1, rotation='vertical')
    plt.text(field_length - 15, field_width/2, team2_name, ha='center', va='center', fontsize=12, color=text_color2, rotation='vertical')
    
    # Add play description
    plt.text(field_length/2, -15, play_description, ha='center', va='center', fontsize=12)
    
    # Draw arrow representing the play
    arrow_start_x = 20 * field_length / 100
    arrow_end_x = 50 * field_length / 100
    arrow_props = dict(arrowstyle='->', linewidth=2, color='red')
    ax.annotate('', xy=(arrow_end_x, field_width/2), xytext=(arrow_start_x, field_width/2), arrowprops=arrow_props)
    
    # Set plot limits and aspect ratio
    ax.set_xlim(0, field_length)
    ax.set_ylim(0, field_width)
    ax.set_aspect('equal', adjustable='box')
    
    # Remove axes
    ax.axis('off')
    
    # Show the plot
    plt.show()

# Get team names and play description from user input
team1 = input("Enter the name of the first team: ")
team2 = input("Enter the name of the second team: ")
play_desc = input("Enter the play description: ")

# Call the function to draw the football field with customized endzone colors and play arrow
draw_football_field(team1, team2, play_desc)
