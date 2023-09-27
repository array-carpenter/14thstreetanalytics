import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

def create_football_field(linenumbers=True,
                          endzones=True,
                          highlight_line=False,
                          highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False,
                          figsize=(12, 6.33)):
    """
    Function that plots the football field for viewing plays.
    Allows for showing or hiding endzones.
    """
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    
    if fifty_is_los:
        plt.plot([60, 60], [0, 53.3], color='gold')
        plt.text(62, 50, '<- Player Yardline at Snap', color='gold')
    
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    
    plt.xlim(0, 120)
    plt.ylim(0, 53.3)
    plt.axis('off')
    
    if linenumbers:
        for x in range(20, 110, 10):
            numb = x
            if x > 50:
                numb = 120 - x
            plt.text(x, 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,
                     color='white')
            plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                     horizontalalignment='center',
                     fontsize=20,
                     color='white', rotation=180)
    
    hash_range = range(11, 110)

    for x in hash_range:
        ax.plot([x, x], [0.4, 0.7], color='white')
        ax.plot([x, x], [53.0, 52.5], color='white')
        ax.plot([x, x], [22.91, 23.57], color='white')
        ax.plot([x, x], [29.73, 30.39], color='white')

    if highlight_line:
        hl = highlight_line_number + 10
        plt.plot([hl, hl], [0, 53.3], color='yellow')
        plt.text(hl + 2, 50, '<- {}'.format(highlighted_name),
                 color='yellow')
    
    return fig, ax

def draw_football_field(team1_name, team2_name, play_description):
    fig, ax = create_football_field(linenumbers=True, endzones=True, highlight_line=False, fifty_is_los=False, figsize=(12, 6.33))
    
    field_length = 120  # Adjusted for the football field's dimensions
    field_width = 53.3
    
    # Set colors based on team names
    if "Eagles" in team1_name:
        endzone1_color = '#004C55'
        text_color1 = 'white'
    else:
        endzone1_color = 'blue'  # Default color
        text_color1 = 'black'
    
    if "Eagles" in team2_name:
        endzone2_color = '#004C55'
        text_color2 = 'white'
    else:
        endzone2_color = 'blue'  # Default color
        text_color2 = 'black'
    
    if "Patriots" in team1_name:
        endzone1_color = '#002244'
        text_color1 = 'white'
    
    if "Patriots" in team2_name:
        endzone2_color = '#002244'
        text_color2 = 'white'
    
    if "Commanders" in team1_name:
        endzone1_color = '#5A1414'
        text_color1 = 'FFB612'
    
    if "Commanders" in team2_name:
        endzone2_color = '#5a1414'
        text_color2 = '#FFB612'
    
    # Draw the colored end zones
    endzone1 = patches.Rectangle((0, 0), 10, field_width, linewidth=0.1, edgecolor='r', facecolor=endzone1_color)
    endzone2 = patches.Rectangle((110, 0), 10, field_width, linewidth=0.1, edgecolor='r', facecolor=endzone2_color)
    ax.add_patch(endzone1)
    ax.add_patch(endzone2)
    
    # Add team names to endzones
    plt.text(5, field_width/2, team1_name, ha='center', va='center', fontsize=12, color=text_color1, rotation='vertical')
    plt.text(115, field_width/2, team2_name, ha='center', va='center', fontsize=12, color=text_color2, rotation='vertical')
    
    # Add play description
    plt.text(field_length/2, -5, play_description, ha='center', va='center', fontsize=12)
    
    # Draw arrow representing the play
    arrow_start_x = 20
    arrow_end_x = 50
    arrow_props = dict(arrowstyle='->', linewidth=2, color='red')
    ax.annotate('', xy=(arrow_end_x, field_width/2), xytext=(arrow_start_x, field_width/2), arrowprops=arrow_props)
    
    # Show the plot
    plt.show()

# Get team names and play description from user input
team1 = input("Enter the name of the first team: ")
team2 = input("Enter the name of the second team: ")
play_desc = input("Enter the play description: ")

# Call the function to draw the football field with
draw_football_field(team1, team2, play_desc)
