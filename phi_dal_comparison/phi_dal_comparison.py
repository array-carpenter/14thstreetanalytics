import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def create_football_field(ax=None, linenumbers=True, endzones=True,
                          highlight_line=False, highlight_line_number=50,
                          highlighted_name='Line of Scrimmage',
                          fifty_is_los=False, figsize=(12, 6.33)):
    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)
    else:
        fig = ax.figure

    # Set green background
    fig.patch.set_facecolor('darkgreen')
    ax.set_facecolor('darkgreen')

    # Set spines color to white
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    # ... (rest of the function remains unchanged)

    return fig, ax

# Load data
df = pd.read_csv('nfl-team-tendencies.csv')

# Filter data for pass columns
pass_cols = ['go_fourth', 'go_two']

# Melt the dataframe to create a long-form for visualization
df_melted_pass = pd.melt(df, id_vars=['team', 'team_color'], value_vars=pass_cols, var_name='Direction', value_name='Percentage')

# Get data for DAL and PHI
df_dal = df_melted_pass[df_melted_pass['team'] == 'DAL']
df_phi = df_melted_pass[df_melted_pass['team'] == 'PHI']

# Set seaborn style
sns.set(style="whitegrid")

# Create subplots for DAL and PHI
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

# Draw football field for DAL with green background
create_football_field(ax=axes[0])
axes[0].set_title('DAL - Gutsy Play Call Percentages - Through Week 13, 2023', color='white')  # Set title color

# Plot pass percentages by direction for DAL
bars = sns.barplot(x='Direction', y='Percentage', data=df_dal, ax=axes[0], color=df_dal['team_color'].values[0])  # Use team color
axes[0].set_ylabel('Percentage', color='white')  # Set Y-axis label
axes[0].tick_params(axis='both', colors='white')  # Set tick color
axes[0].set_ylim(0, 0.5)  # Set the y-axis limit to 50%
axes[0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y*100:.0f}%'))  # Remove the percentage sign
axes[0].set_xticklabels(['Go for it on 4th Down','Go for Two'])  # Set x-axis labels

# Add bar labels
for bar in bars.patches:
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height()*100:.0f}%',
                ha='center', va='bottom', color='white')

# Draw football field for PHI with green background
create_football_field(ax=axes[1])
axes[1].set_title('PHI - Gutsy Play Call Percentages - Through Week 13, 2023', color='white')  # Set title color

# Plot pass percentages by direction for PHI
bars = sns.barplot(x='Direction', y='Percentage', data=df_phi, ax=axes[1], color=df_phi['team_color'].values[0])  # Use team color
axes[1].set_ylabel('Percentage', color='white')  # Set Y-axis label
axes[1].tick_params(axis='both', colors='white')  # Set tick color
# Set the y-axis limit to 80% for the first subplot (axes[0])
axes[0].set_ylim(0, 0.4)

#0 Set the y-axis limit to 80% for the second subplot (axes[1])
axes[1].set_ylim(0, 0.4)

axes[1].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y*100:.0f}%'))  # Remove the percentage sign
axes[1].set_xticklabels(['Go for it on 4th Down','Go for Two'])  # Set x-axis labels

# Add bar labels
for bar in bars.patches:
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height()*100:.0f}%',
                ha='center', va='bottom', color='white')

# Remove X-axis labels
axes[0].set_xlabel('')
axes[1].set_xlabel('')

# Add text at the bottom with adjusted vertical position
fig.text(0.5, 0.000, 'A viz by Ray Carpenter | 14thstreetanalytics.substack.com | Source: nfeloapp.com', ha='center', color='white')

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
