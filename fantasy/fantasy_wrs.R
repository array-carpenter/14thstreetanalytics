# Set the API key
Sys.setenv(CFBD_API_KEY = "--")

# Load the cfbfastR package
library(cfbfastR)

# Pull game data for a specific year
year <- 2023
games <- cfbfastR::cfbd_game_info(year = year)

# Display the data
print(games)