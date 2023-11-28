#%%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
from matplotlib import rcParams
import numpy as np
from highlight_text import fig_text
import pandas as pd

from PIL import Image
import urllib
import os

df = pd.read_csv("success_rate_2022_2023.csv", index_col = 0)
df = (
        df
        .sort_values(by = ["variable", "value"], ascending = True)
        .reset_index(drop = True)
)


fig = plt.figure(figsize=(6.5, 10), dpi = 200, facecolor="#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")

# Adjust spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(True, color = "lightgrey", ls = ":")

# Define the series
teams = list(df["team_id"].unique())
Y = np.arange(len(teams))
X_xg = df[df["variable"] == "2022_success_rate"]["value"]
X_goals = df[df["variable"] == "2023_success_rate"]["value"]

# Fix axes limits
ax.set_ylim(-.5, len(teams) - .5)
ax.set_xlim(
    min(X_goals.min(), X_xg.min(), 35), 
    max(X_goals.max(), X_xg.max(), 55)
)

# Scatter plots
ax.scatter(X_xg, Y, color = "#74959A", s = 200, alpha = 1, zorder = 3)
ax.scatter(X_goals, Y, color = "#495371", s = 200, alpha = 1, zorder = 3)
ax.scatter(X_xg, Y, color = "none", ec = "#74959A", s = 180, lw = 2.5, zorder = 3)
ax.scatter(X_goals, Y, color = "none", ec = "#495371", s = 180, lw = 2.5, zorder = 3)


# Add line chart between points and difference annotation
for index in Y:
    difference = X_xg.iloc[index] - X_goals.iloc[index]
    if difference > 0:
        color = "#74959A" 
        x_adj = -1.75
        anot_position = X_xg.iloc[index]
        anot_aux_sign = "-"
    else:
        color = "#495371"
        x_adj = 1.75
        anot_position = X_goals.iloc[index]
        anot_aux_sign = "+"
    
    ax.annotate(
        xy = (anot_position, index),
        text = f"{anot_aux_sign} {abs(difference):.1f}",
        xytext = (13, -2),
        textcoords = "offset points",
        size = 8,
        color = color,
        weight = "bold"
    )
    
    if abs(difference) < 1.3:
        continue
    if abs(difference) < -1.1:
        continue
    ax.plot(
        [X_xg.iloc[index] + x_adj, X_goals.iloc[index] + x_adj*(-1)],
        [index, index],
        lw = 1,
        color = color,
        zorder = 2
    )

DC_to_FC = ax.transData.transform
FC_to_NFC = fig.transFigure.inverted().transform

# Native data to normalized data coordinates
DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

logos_folder = "nfl_logos/"
# Modify the loop to fetch logos from the local folder
for index, team_id in enumerate(teams):
    ax_coords = DC_to_NFC([33, index - 0.55])
    logo_ax = fig.add_axes([ax_coords[0], ax_coords[1], 0.04, 0.04], anchor="C")
    
    # Use the local path to the logos folder
    logo_path = f"{logos_folder}{team_id:.0f}.png"
    
    try:
        # Check if the file exists before opening
        with Image.open(logo_path) as club_icon:
            logo_ax.imshow(club_icon.convert("LA"))
            logo_ax.axis("off")
    except FileNotFoundError:
        print(f"Logo not found for team ID {team_id}")

# Remove tick labels
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
false_ticks = ax.set_yticklabels([])

fig_text(
    x = 0.15, y = .9, 
    s = "Through 10 weeks, only 3 NFL Teams\nhave outperformed their <2022> \noffensive success rate in <2023>",
    highlight_textprops = [
        {"color":"#74959A"},
        {"color": "#495371"}
    ],
    va = "bottom", ha = "left",
    fontsize = 14, color = "black", weight = "bold"
)
fig_text(
	x = 0.15, y = .885, 
    s = "Source: rbsdm.com | Viz by Ray Carpenter | inspired by a viz by @sonofacorner",
	va = "bottom", ha = "left",
	fontsize = 8, color = "#4E616C"
)

# # ---- The League's logo
league_icon = Image.open("nfl_logos/NFL.png")
league_ax = fig.add_axes([0.055, 0.89, 0.065, 0.065], zorder=1)
league_ax.imshow(league_icon)
league_ax.axis("off")

plt.savefig(
	"06202022_bundelsiga_xg.png",
	dpi = 500,
	facecolor = "#EFE9E6",
	bbox_inches="tight",
    edgecolor="none",
	transparent = False
)

plt.savefig(
	"06202022_bundelsiga_xg_tr.png",
	dpi = 500,
	facecolor = "none",
	bbox_inches="tight",
    edgecolor="none",
	transparent = True
)
