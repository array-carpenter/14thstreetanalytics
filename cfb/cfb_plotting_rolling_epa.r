# Install necessary packages (if not already installed)
install.packages("httpgd")

# Load the libraries
library(cfbplotR)
library(ggplot2)
library(dplyr)
options(vsc.plot = TRUE)

# Pull team-level stats for the 2023 season
team_stats <- cfbd_stats_season_team(year = 2023)

# Filter the data for the specific conferences
target_conferences <- c("ACC", "Big Ten", "Big 12", "SEC", "Pac-12")

# Filter team stats to include only teams from the selected conferences
team_stats <- team_stats %>%
  filter(conference %in% target_conferences)

# Pull play-by-play data with EPA for the 2023 season
pbp_data <- cfbd_pbp_data(year = 2023, epa_wpa = TRUE)

# Calculate average EPA per play for each team
team_epa <- pbp_data %>%
  filter(pos_team %in% team_stats$team) %>%  # Filter to include only the selected teams
  group_by(pos_team) %>%
  summarize(avg_epa = mean(EPA, na.rm = TRUE))

# Display the first few rows of the extracted data
head(team_epa)

# Plot EPA per Play for each team with spaced-out names
my_plot <- ggplot(team_epa, aes(x = reorder(pos_team, avg_epa), y = avg_epa)) +
  geom_cfb_logos(aes(team = pos_team), width = 0.05) +
  labs(
    title = "Average EPA per Play (2023, Selected Conferences)",
    x = "Team",
    y = "EPA per Play"
  ) +
  theme_minimal() +
  coord_flip() +  # Flip the coordinates for better readability
  theme(
    axis.text.y = element_text(hjust = 0.5),  # Center the text horizontally
    axis.ticks.y = element_blank(),  # Remove y-axis ticks
    panel.grid.major.y = element_blank(),  # Remove major y-axis grid lines
    panel.grid.minor.y = element_blank()  # Remove minor y-axis grid lines
  ) +
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.05)))  # Add space around y-axis limits

# Display the plot
print(my_plot)

# Save the plot
ggsave("epa_per_play_2023_selected_conferences.png", plot = my_plot, width = 10, height = 8)