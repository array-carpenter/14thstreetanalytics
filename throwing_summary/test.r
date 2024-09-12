# Load required packages
library(cfbfastR)
library(dplyr)
library(ggplot2)
library(grid)
library(gridExtra)
library(png)
library(stringr)

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

# Filter data by play_text containing Jalen Milroe
filtered_df <- pbp_data %>%
  filter(str_detect(play_text, PLAYER_NAME))

# Print the filtered data to inspect it
print(filtered_df, n = Inf)