import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import pandas as pd

# Function to create football field
def create_football_field(linenumbers=True, endzones=True, figsize=(12, 6.33)):
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1,
                             edgecolor='r', facecolor='darkgreen', zorder=0)
    fig, ax = plt.subplots(1, figsize=figsize)
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1,
                                edgecolor='r',
                                facecolor='blue',
                                alpha=0.2,
                                zorder=0)
        ez2 = patches.Rectangle((110, 0), 10, 53.3,
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
    
    return fig, ax

# Function to animate the play
def animate_play(fig, ax, start_yardline, yards_gained):
    ball = plt.Circle((start_yardline + 10, 26.65), 1, color='brown', zorder=5)
    ax.add_patch(ball)

    def animate(i):
        new_x = start_yardline + 10 + (i / 10) * yards_gained
        ball.set_center((new_x, 26.65))
        return ball,

    anim = FuncAnimation(fig, animate, frames=10, interval=200, blit=True)
    plt.show()

# Example values for play description
start_yardline = 75  # Start at the 25-yard line of the offense
yards_gained = 25  # Example: play gains 25 yards

# Create the football field
fig, ax = create_football_field()

# Animate the play
animate_play(fig, ax, start_yardline, yards_gained)

