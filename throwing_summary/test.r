# Load required packages
install.packages("kableExtra")

library(cfbfastR)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(grid)
library(knitr)
library(kableExtra)

# Define constants for the year, week, and player
YEAR <- 2024
WEEK <- 1
PLAYER_NAME <- 'Grayson McCall'

# Fetch play-by-play data for the specific game using cfbfastR
pbp_data <- cfbd_pbp_data(year = YEAR, week = WEEK)

# Check if data was retrieved successfully
if (is.null(pbp_data) || nrow(pbp_data) == 0) {
  stop("No play-by-play data returned for the specified criteria. Check if the game occurred and the parameters are correct.")
}

# Filter data by play_text containing the player's name
filtered_df <- pbp_data %>%
  filter(str_detect(play_text, PLAYER_NAME))

# Check the structure of the dataset to see available columns
str(filtered_df)

# Correct the touchdown logic and other stats
player_stats <- filtered_df %>%
  summarise(
    completions = sum(str_detect(play_text, "(?i)complete")),
    incompletions = sum(str_detect(play_text, "(?i)incomplete")),
    touchdowns = sum(str_detect(play_text, "(?i)touchdown")),
    interceptions = sum(str_detect(play_text, "(?i)interception")),
    sacks = sum(str_detect(play_text, "(?i)sack")),
    total_yards = sum(yards_gained, na.rm = TRUE),
    pass_attempts = n()  # Total number of pass plays
  )

# Create a summary stats table using kable
stats_table <- data.frame(
  Cmp = player_stats$completions,
  Att = player_stats$pass_attempts,
  Yds = player_stats$total_yards,
  TD = player_stats$touchdowns,
  Int = player_stats$interceptions,
  Sck = player_stats$sacks
)

# Create kable for neat display
stats_kable <- kable(stats_table, format = "html") %>%
  kable_styling(bootstrap_options = c("striped", "hover", "condensed"))

# Create Rolling EPA plot (assuming EPA is available in the dataset)
rolling_epa_plot <- ggplot(filtered_df, aes(x = play_id, y = epa)) +
  geom_line(color = "green") +
  labs(title = "Rolling EPA/Play Throughout Game", x = "Play ID", y = "Rolling EPA/Play") +
  theme_minimal()

# Create Distribution of Yards Gained Plot
yards_dist_plot <- ggplot(filtered_df, aes(x = yards_gained)) +
  geom_histogram(binwidth = 5, fill = "blue", color = "black", alpha = 0.7) +
  labs(title = "Distribution of Yards Gained", x = "Yards Gained", y = "Frequency") +
  theme_minimal()

# Create Pass Location Scatter Plot
pass_location_plot <- ggplot(filtered_df, aes(x = pass_location, y = yards_gained)) +
  geom_point(aes(shape = pass_result, color = pass_result), size = 4) +
  scale_shape_manual(values = c("Complete" = 16, "Incomplete" = 4, "INT" = 18, "TD" = 21)) +
  scale_color_manual(values = c("Complete" = "green", "Incomplete" = "red", "INT" = "purple", "TD" = "gold")) +
  labs(title = "Pass Locations", x = "Horizontal Placement", y = "Depth of Target (yards)") +
  theme_minimal()

# Arrange all the plots and tables in a grid layout
grid.arrange(
  tableGrob(stats_table),  # Stats table at the top
  rolling_epa_plot,  # Rolling EPA plot
  yards_dist_plot,   # Distribution of Yards plot
  pass_location_plot,  # Pass location scatter plot
  nrow = 3, ncol = 2  # Arrange in 3 rows and 2 columns
)
