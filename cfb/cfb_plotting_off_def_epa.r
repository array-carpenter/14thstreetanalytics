# Install necessary packages (if not already installed)
install.packages("httpgd")

# Load the libraries
library(cfbplotR)
library(ggplot2)
library(dplyr)
options(vsc.plot = TRUE)

# Pull team-level stats for the 2023 season
team_stats <- cfbd_stats_season_team(year = 2023)

# Define the target conferences
target_conferences <- c("ACC", "Big Ten", "Big 12", "SEC", "Pac-12")

# Filter the team stats for the target conferences
team_stats <- team_stats %>%
  filter(conference %in% target_conferences)

# Pull play-by-play data with EPA for the 2023 season
pbp_data <- cfbd_pbp_data(year = 2023, epa_wpa = TRUE)

# Filter pbp_data to include only the teams from the selected conferences
pbp_data <- pbp_data %>%
  filter(pos_team %in% team_stats$team)

# Calculate Offensive and Defensive EPA per play for each team
team_epa <- pbp_data %>%
  group_by(pos_team) %>%
  summarize(
    off_epa_per_play = mean(EPA[offense_score_play == 1], na.rm = TRUE),
    def_epa_per_play = mean(-EPA[defense_score_play == 1], na.rm = TRUE)
  )

# Check if the team names match valid team logos
team_epa <- team_epa %>%
  mutate(pos_team = if_else(pos_team %in% valid_team_names(), pos_team, NA_character_)) %>%
  drop_na(pos_team)

# Display the first few rows of the extracted data
head(team_epa)

# Create the plot
tier_plot <- ggplot(team_epa, aes(x = off_epa_per_play, y = def_epa_per_play)) +
  geom_cfb_logos(aes(team = pos_team), width = 0.08) +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +  # Horizontal line at y=0
  geom_vline(xintercept = 0, color = "red", linetype = "dashed") +  # Vertical line at x=0
  labs(
    title = "College Football Team Tiers, 2023 (Selected Conferences)",
    x = "Offensive EPA/play",
    y = "Defensive EPA/play",
    caption = "Data from CollegeFootballData.com"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    plot.caption = element_text(hjust = 0.5)
  )

# Display the plot
print(tier_plot)

# Save the plot
ggsave("cfb_team_tiers_2023_selected_conferences.png", plot = tier_plot, width = 12, height = 8)
