# Load necessary libraries
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

# Pull play-by-play data with rushing and passing yards for the 2023 season
pbp_data <- cfbd_pbp_data(year = 2023, epa_wpa = TRUE)

# Calculate total passing and rushing yards allowed and games played for each team
defensive_stats <- pbp_data %>%
  filter(defense_play %in% team_stats$team) %>%
  group_by(defense_play) %>%
  summarize(
    total_passing_yards_allowed = sum(yards_gained[pass == 1], na.rm = TRUE),
    total_rushing_yards_allowed = sum(yards_gained[rush == 1], na.rm = TRUE),
    games_played = n_distinct(game_id)
  ) %>%
  mutate(
    passing_yards_allowed_per_game = total_passing_yards_allowed / games_played,
    rushing_yards_allowed_per_game = total_rushing_yards_allowed / games_played
  )

# Plot Passing Yards Allowed vs Rushing Yards Allowed per Game
defense_plot <- ggplot(defensive_stats, aes(x = passing_yards_allowed_per_game, y = rushing_yards_allowed_per_game)) +
  geom_cfb_logos(aes(team = defense_play), width = 0.05) +
  labs(
    title = "Passing vs Rushing Yards Allowed per Game (2023 Season, 2024 Power 5)",
    x = "Passing Yards Allowed per Game",
    y = "Rushing Yards Allowed per Game"
  ) +
  theme_minimal() +
  theme(
    panel.grid.major = element_line(color = "gray", size = 0.5),  # Add major grid lines
    panel.grid.minor = element_blank(),  # Remove minor grid lines
    axis.title = element_text(size = 14, face = "bold"),  # Axis title style
    axis.text = element_text(size = 12)  # Axis text style
  ) +
  scale_x_continuous(expand = expansion(mult = c(0.05, 0.05))) +  # Add space around x-axis limits
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.05)))  # Add space around y-axis limits

# Set the plot display dimensions
options(repr.plot.width = 16, repr.plot.height = 4)

# Print the plot
print(defense_plot)

# Save the plot with an even wider and shorter aspect ratio
ggsave("passing_vs_rushing_yards_allowed_2023_selected_conferences.png", plot = defense_plot, width = 16, height = 4)
