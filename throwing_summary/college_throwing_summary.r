# Load required packages
library(cfbfastR)
library(dplyr)
library(ggplot2)
library(grid)
library(gridExtra)
library(png)
library(stringr)

# Set the API key for cfbfastR
Sys.setenv(CFBD_API_KEY = "ykUQNUFlwhEFpeeB1mBdAM86qgZiENgq3hYGFj8HRl1j47ZlhKMQv0czdY0fxena")

# Define constants for the year, week, and player
YEAR <- 2024
WEEK <- 1
PLAYER_NAME <- 'Jalen Milroe'

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

# Identify passing and rushing plays using play_text
passing_plays <- filtered_df %>%
  filter(str_detect(play_text, paste0(PLAYER_NAME, " pass")))

rushing_plays <- filtered_df %>%
  filter(str_detect(play_text, paste0(PLAYER_NAME, " run")))

# Calculate cumulative completions and attempts for passing plays
passing_plays <- passing_plays %>%
  mutate(
    cumulative_completions = cumsum(str_detect(play_text, "complete")),
    cumulative_attempts = cumsum(str_detect(play_text, "pass")),
    cumulative_completion_percentage = (cumulative_completions / cumulative_attempts) * 100
  )

# Sum the total number of plays (passing attempts + rushing attempts)
total_plays <- nrow(passing_plays) + nrow(rushing_plays)

# Calculate passing statistics
completions <- sum(str_detect(passing_plays$play_text, "complete"), na.rm = TRUE)
attempts <- nrow(passing_plays)
yards <- sum(passing_plays$yards_gained, na.rm = TRUE)
touchdowns <- sum(str_detect(passing_plays$play_text, "touchdown"), na.rm = TRUE)
interceptions <- sum(str_detect(passing_plays$play_text, "intercepted"), na.rm = TRUE)

# Calculate passer rating
if (attempts > 0) {
  comp_pct <- completions / attempts
  avg_yards <- yards / attempts
  td_pct <- touchdowns / attempts
  int_pct <- interceptions / attempts
  
  passer_rating <- (comp_pct * 5 + avg_yards * 0.25 + td_pct * 20 - int_pct * 25) / 6 * 100
  passer_rating <- round(passer_rating, 1)
} else {
  passer_rating <- 0
}

# Calculate rushing statistics for Jalen Milroe
rush_attempts <- nrow(rushing_plays)
rush_yards <- sum(rushing_plays$yards_gained, na.rm = TRUE)
rush_touchdowns <- sum(str_detect(rushing_plays$play_text, "touchdown"))

# Update the summary table with passing and rushing stats
summary_table <- data.frame(
  Att = attempts,
  Cmp = completions,
  Yds = yards,
  TD = touchdowns,
  Int = interceptions,
  `Rush Att` = rush_attempts,
  `Rush Yds` = rush_yards,
  `Rush TD` = rush_touchdowns,
  `Passer Rtg` = passer_rating
)

# Load images
headshot_path <- 'path/to/jalen_milroe_headshot.png'
logo_path <- 'path/to/team_logo.png'
headshot <- readPNG(headshot_path)
logo <- readPNG(logo_path)

# Create the dashboard plot
jalen_milroe_dashboard <- function(headshot, logo, summary_df) {
  
  # Define the layout
  layout_matrix <- rbind(
    c(1, 2, 3),
    c(4, 4, 4),
    c(5, 6, 7),
    c(8, 8, 8),
    c(9, 9, 9)
  )
  
  grid.newpage()
  pushViewport(viewport(layout = grid.layout(nrow(layout_matrix), ncol(layout_matrix))))
  
  # Define viewport function for each plot
  vplayout <- function(x, y) viewport(layout.pos.row = x, layout.pos.col = y)
  
  # Headshot
  pushViewport(vplayout(1, 1))
  grid.raster(headshot)
  upViewport()
  
  # Logo
  pushViewport(vplayout(1, 3))
  grid.raster(logo)
  upViewport()
  
  # Bio
  pushViewport(vplayout(1, 2))
  grid.text("Jalen Milroe\nQB, Age: 22, 6'3/210\n2024 Week 1 Summary", 
            gp = gpar(fontsize = 16), just = "center")
  upViewport()
  
  # Summary Table
  pushViewport(vplayout(2, 1:3))
  grid.table(summary_df)
  upViewport()
  
  # Yards Gained Distribution
  pushViewport(vplayout(3, 1))
  ggplot(passing_plays, aes(x = yards_gained)) +
    geom_histogram(bins = 10, fill = "blue", color = "black") +
    labs(x = "Yards Gained", y = "Frequency", title = "Distribution of Yards Gained") +
    theme_minimal()
  upViewport()
  
  # Pass Location Chart
  pushViewport(vplayout(3, 2))
  ggplot(passing_plays, aes(x = as.factor(play_number), y = yards_gained)) +
    geom_point(aes(color = as.factor(str_detect(play_text, "complete")), size = 3)) +
    scale_color_manual(values = c("FALSE" = "red", "TRUE" = "green")) +
    labs(x = "Play Number", y = "Yards Gained", title = "Pass Location Chart") +
    theme_minimal()
  upViewport()
  
  # Footer
  pushViewport(vplayout(5, 1:3))
  grid.text("By Ray Carpenter | 14thstreetanalytics.substack.com | Inspired by a viz by Thomas Nestico | Data from cfbfastR | Images from College Football Resources", 
            gp = gpar(fontsize = 10), just = "center")
  upViewport()
}

# Call the modified dashboard function
jalen_milroe_dashboard(headshot, logo, summary_table)
