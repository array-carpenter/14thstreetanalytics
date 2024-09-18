# Load necessary libraries
library(nflfastR)
library(ggplot2)
library(ggimage)

# Load play-by-play data for 2024 season
pbp_data <- load_pbp(2024) 

# Filter data for Week 1 and Week 2
week1_2_data <- pbp_data[pbp_data$week %in% c(1, 2), ]

# Calculate offensive EPA per play
epa_team <- week1_2_data %>%
  dplyr::group_by(posteam) %>%
  dplyr::summarise(epa_per_play = mean(epa, na.rm = TRUE))

# Calculate defensive EPA per play allowed
epa_team_defense <- week1_2_data %>%
  dplyr::group_by(defteam) %>%
  dplyr::summarise(epa_per_play_allowed = mean(epa, na.rm = TRUE))

# Join offensive and defensive data
epa_combined <- dplyr::left_join(epa_team, epa_team_defense, by = c("posteam" = "defteam"))

# Load team logos
team_logos <- nflfastR::teams_colors_logos

# Join combined EPA data with team logos
epa_combined <- dplyr::left_join(epa_combined, team_logos, by = c("posteam" = "team_abbr"))

# Plotting the data
my_plot <- ggplot(epa_combined, aes(x = epa_per_play, y = epa_per_play_allowed)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "black") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "black") +
  geom_image(aes(image = team_logo_wikipedia), size = 0.05) +
  labs(
    title = "NFL Team Offensive and Defensive EPA: Week 1 and Week 2",
    subtitle = "2024 season | Data: nflfastR",
    x = "EPA/Play",
    y = "EPA/Play Allowed"
  ) +
  scale_y_reverse() +  # Flips the y-axis
  theme_minimal() +  # Minimal theme provides white background by default
  theme(
    plot.background = element_rect(fill = "white", color = NA),  # Ensures the background is white
    panel.background = element_rect(fill = "white", color = NA), # Ensures the panel background is white
    panel.grid.major = element_line(color = "grey90"),            # Light grey grid lines
    panel.grid.minor = element_line(color = "grey95")             # Lighter grey for minor grid lines
  )

# Set plot dimensions for landscape (e.g., 12 width x 6 height) and save
ggsave("epa_plot_landscape_white_background.png", my_plot, width = 12, height = 6)
