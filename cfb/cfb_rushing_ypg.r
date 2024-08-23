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

# Pull play-by-play data with rushing yards for the 2023 season
pbp_data <- cfbd_pbp_data(year = 2023, epa_wpa = TRUE)

# Calculate total rushing yards and games played for each team
team_rushing <- pbp_data %>%
  filter(offense_play %in% team_stats$team, rush == 1) %>%  # Use the correct column name
  group_by(offense_play) %>%
  summarize(
    total_rushing_yards = sum(yards_gained, na.rm = TRUE),
    games_played = n_distinct(game_id)
  ) %>%
  mutate(rushing_yards_per_game = total_rushing_yards / games_played)

# Plot Rushing Yards per Game for each team with spaced-out names
my_rushing_plot <- ggplot(team_rushing, aes(x = reorder(offense_play, rushing_yards_per_game), y = rushing_yards_per_game)) +
  geom_cfb_logos(aes(team = offense_play), width = 0.05) +
  labs(
    title = "Rushing Yards per Game (2023, Selected Conferences)",
    x = "Team",
    y = "Rushing Yards per Game"
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
print(my_rushing_plot)

# Save the plot
ggsave("rushing_yards_per_game_2023_selected_conferences.png", plot = my_rushing_plot, width = 10, height = 8)
