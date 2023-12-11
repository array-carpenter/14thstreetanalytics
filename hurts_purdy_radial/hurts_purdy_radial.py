# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from highlight_text import fig_text
# Set data
df = pd.DataFrame({
'group': ['Jalen Hurts','Brock Purdy'],
'EPA+CPOE Comp.': [6,1],
'Adj. EPA/play': [7,1],
'EPA/Play': [7,1],
'Success Rate': [9,1],
'Cmp%': [3,2],
'Expected Cmp%': [23,25],
'CPOE': [3,2],
'Air Yards': [5,12],
'QBR': [6,1],
'PAA': [6,5],
'RTG': [12,1]
})
 
# number of variable
categories=list(df)[1:]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
fig, ax = plt.subplots(figsize=(10,10),subplot_kw=dict(polar=True))
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([10,20,30], [], color="grey", size=7)
plt.ylim(35,0)
 
# Ind1
values=df.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid',color='#004C54', label="Jalen Hurts")
ax.fill(angles, values, 'b', alpha=0.1)
 
# Ind2
values=df.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid',color="#AA0000", label="Brock Purdy")
ax.fill(angles, values, 'r', alpha=0.1)
 
# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

fig_text(
    x = 0.02, y = .965, 
    s = "Comparing the Rankings \nof <Jalen Hurts> and <Brock Purdy> \nThrough 12 Weeks of the 2023 Season",
    highlight_textprops = [
        {"color":"#004C54"},
        {"color": "#AA0000"}
    ],
    va = "bottom", ha = "left",
    fontsize = 18, color = "black", weight = "bold"
)
fig_text(
	x = 0.02, y = .920, 
    s = "Source: rbsdm.com | Viz by Ray Carpenter | 14thstreetanalytics.substack.com \nThe further out the radial extends, the higher the league rank for the QB.",
	va = "bottom", ha = "left",
	fontsize = 12, color = "#4E616C"
)
# Show the graph
plt.show()