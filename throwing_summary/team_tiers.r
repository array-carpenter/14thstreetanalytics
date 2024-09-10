#install.packages("nflfastR")
#install.packages("ggplot2")
#install.packages("ggimage")

library(nflfastR)
library(ggplot2)
library(ggimage)

pbp_data <- load_pbp(2024) # Load play-by-play data for 2024
week1_data <- pbp_data[pbp_data$week == 1, ]

epa_team <- week1_data %>%
  dplyr::group_by(posteam) %>%
  dplyr::summarise(epa_per_play = mean(epa, na.rm = TRUE))

epa_team_defense <- week1_data %>%
  dplyr::group_by(defteam) %>%
  dplyr::summarise(epa_per_play_allowed = mean(epa, na.rm = TRUE))

# Join offensive and defensive data
epa_combined <- dplyr::left_join(epa_team, epa_team_defense, by = c("posteam" = "defteam"))

team_logos <- nflfastR::teams_colors_logos

epa_combined <- dplyr::left_join(epa_combined, team_logos, by = c("posteam" = "team_abbr"))

my_plot <- ggplot(epa_combined, aes(x = epa_per_play, y = epa_per_play_allowed)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "black") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "black") +
  geom_image(aes(image = team_logo_wikipedia), size = 0.05) +
  labs(
    title = "NFL Team Offensive and Defensive EPA: Week 1",
    subtitle = "2024 season | Data: nflfastR",
    x = "EPA/Play",
    y = "EPA/Play Allowed"
  ) +
  scale_y_reverse() +  # Flips the y-axis
  theme_minimal()

# Print the plot
print(my_plot)

