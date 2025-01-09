# Install and load necessary packages
if (!requireNamespace('pacman', quietly = TRUE)){
  install.packages('pacman')
}
pacman::p_load(tidyverse, cfbfastR, tictoc, progressr)

# Load play-by-play data for seasons 2014-2020
tictoc::tic()
pbp <- data.frame()
seasons <- 2023
progressr::with_progress({
  pbp <- cfbfastR::load_cfb_pbp(seasons)
})
tictoc::toc()

# Get coaching information for the same seasons
coaches <- purrr::map_dfr(seasons, function(x) {
  cfbfastR::cfbd_coaches(year = x)
})

# Get school conference information and join with coaches data
team_info <- cfbfastR::cfbd_team_info()
coaches <- coaches %>%
  dplyr::left_join(team_info, by = "school") %>%
  dplyr::mutate(coach = paste(first_name, last_name, sep = " ")) %>%
  dplyr::filter(games >= 6) %>%
  dplyr::select(coach, school, year, conference)

# Add coaches data to the play-by-play dataframe
pbp <- pbp %>%
  dplyr::inner_join(coaches, by = c("offense_play" = "school", "year" = "year"))

# Filter down to fourth down plays and categorize them
down4 <- pbp %>%
  dplyr::filter(down == 4) %>%
  dplyr::mutate(fga = ifelse(str_detect(play_type, "Field Goal"), 1, 0),
                punt = ifelse(play_type == "Punt", 1, 0),
                attempt = ifelse(rush == 1 | pass == 1, 1, 0),
                play = dplyr::case_when(fga == 1 ~ "FG Attempt",
                                        punt == 1 ~ "Punt",
                                        attempt == 1 ~ "Go"))

# Create the plot for selected head coaches
down4 %>%
  dplyr::filter(!is.na(play)) %>%
  dplyr::filter(coach %in% c("Jim Harbaugh", "Steve Sarkisian", "Lincoln Riley", "Brian Kelly", 
                             "Ryan Day", "Kalen DeBoer", "Lane Kiffine", "Mike Gundy", 
                             "Kirby Smart", "Nick Saban")) %>%
  dplyr::filter(distance <= 5, distance > 0) %>%
  ggplot(aes(x = distance, y = 100 - yards_to_goal, color = play)) +
  geom_jitter() +
  facet_wrap(. ~ coach) +
  theme_bw() +
  labs(x = "Yards to Go",
       title = "College Coaches's Fourth Down Tendencies | 2023 Season",
       subtitle = "Data from @cfbfastR, Viz by Ray Carpenter (@array_carpenter), inspired by a viz by Michael Egle (@deceptivespeed_)",
       color = "Decision") +
  scale_y_continuous(labels = c("Own 20", "Own 40", "Opp 40",
                                "Opp 20", "Endzone"),
                     breaks = c(20, 40, 60, 80, 100)) +
  theme(axis.title.y = element_blank())


# Create the plot for selected head coaches
plot <- down4 %>%
  dplyr::filter(!is.na(play)) %>%
  dplyr::filter(coach %in% c("Jim Harbaugh", "Steve Sarkisian", "Lincoln Riley", "Brian Kelly", 
                             "Ryan Day", "Kalen DeBoer", "Lane Kiffin", "Mike Gundy", 
                             "Kirby Smart", "Nick Saban","Dan Lanning","Marcus Freeman")) %>%
  dplyr::filter(distance <= 5, distance > 0) %>%
  ggplot(aes(x = distance, y = 100 - yards_to_goal, color = play)) +
  geom_jitter() +
  facet_wrap(. ~ coach) +
  theme_bw() +
  labs(x = "Yards to Go",
       title = "Top AP Ranked Coach 4th Down Tendencies | 2023 Season",
       subtitle = "Data from @cfbfastR",
       caption = "Viz by Ray Carpenter (@array_carpenter), inspired by Michael Egle (@deceptivespeed_)",
       color = "Decision") +
  scale_y_continuous(labels = c("Own 20", "Own 40", "Opp 40",
                                "Opp 20", "Endzone"),
                     breaks = c(20, 40, 60, 80, 100)) +
  theme(axis.title.y = element_blank())

# Print the plot to display it
print(plot)

# Calculate the proportion of "Go" plays for each coach
go_attempts <- down4 %>%
  dplyr::filter(!is.na(play)) %>%
  dplyr::filter(coach %in% c("Jim Harbaugh", "Steve Sarkisian", "Lincoln Riley", "Brian Kelly", 
                             "Ryan Day", "Kalen DeBoer", "Lane Kiffin", "Mike Gundy", 
                             "Kirby Smart", "Nick Saban","Dan Lanning","Marcus Freeman")) %>%
  dplyr::filter(distance <= 5, distance > 0) %>%
  dplyr::group_by(coach) %>%
  dplyr::summarize(
    total_plays = n(),
    go_attempts = sum(play == "Go"),
    go_percentage = (go_attempts / total_plays) * 100
  ) %>%
  arrange(desc(go_percentage))

# Print the results
print(go_attempts)
