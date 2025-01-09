# Load necessary libraries
library(cfbplotR)
library(ggplot2)
library(dplyr)
options(vsc.plot = TRUE)

# Pull team-level stats for the 2023 season
team_stats <- cfbd_stats_season_team(year = 2024)

# Inspect the structure of the team_stats data frame
str(team_stats)

# Check if the 'conference' column exists and is correctly named
if ("conference" %in% colnames(team_stats)) {
  # Filter the data for the specific conferences if 'conference' column is present
  target_conferences <- c("ACC", "Big Ten", "Big 12", "SEC", "Pac-12")
  
  team_stats <- team_stats %>%
    filter(conference %in% target_conferences)
} else {
  # Print a message indicating the absence of the 'conference' column
  print("The 'conference' column is not present in the team_stats data frame.")
}

# Pull play-by-play data with rushing and passing yards for the 2023 season
pbp_data <- cfbd_pbp_data(year = 2024, epa_wpa = TRUE)

# Inspect the structure of the pbp_data data frame
str(pbp_data)

# Continue with the rest of the analysis if the required columns are present
# Calculate explosive plays (10+ yard runs, 15+ yard passes) and success rate
explosive_and_success <- pbp_data %>%
  filter(offense_play %in% team_stats$team) %>%
  mutate(
    explosive = (yards_gained >= 10 & rush == 1) | (yards_gained >= 15 & pass == 1),
    success = (yards_gained >= 0.5 * distance & down == 1) |
              (yards_gained >= 0.7 * distance & down == 2) |
              (yards_gained >= distance & (down == 3 | down == 4))
  ) %>%
  group_by(offense_play) %>%
  summarize(
    explosive_play_pct = mean(explosive, na.rm = TRUE) * 100,
    success_rate = mean(success, na.rm = TRUE) * 100
  )

# Plot Explosive Play Percentage vs Success Rate
explosive_success_plot <- ggplot(explosive_and_success, aes(x = explosive_play_pct, y = success_rate)) +
  geom_cfb_logos(aes(team = offense_play), width = 0.05) +
  labs(
    title = "Explosive Play Percentage vs Success Rate (2024, Selected Conferences)",
    x = "Explosive Play Percentage",
    y = "Success Rate"
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

# Display the plot
print(explosive_success_plot)
