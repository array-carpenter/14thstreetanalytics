from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, sum, max, first
from pyspark.sql.types import FloatType, TimestampType

# Step 1: Create SparkSession
spark = SparkSession.builder.appName("intense_window").getOrCreate()

# Step 2: Load DataFrame from CSV
# Replace 'your_file_path.csv' with the actual path to your CSV file
df = spark.read.csv("output_tracking.csv", header=True)

# Step 3: Convert timestamp to seconds and cast to TimestampType
df = df.withColumn("timestamp_seconds", col("timestamp").cast(FloatType()))
df = df.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Step 4: Load player DataFrame from CSV
player_df = spark.read.csv("DimPlayer.csv", header=True)

# Step 5: Join the tracking data with player information
joined_df = df.join(player_df, df["trackable_object"] == player_df["trackable_object"])

# Step 6: Aggregate into 5-minute windows, calculating intensity as the sum of distance
intensity_df = joined_df.groupBy("game_id", "short_name", window("timestamp", "5 minutes")).agg(
    sum("x").alias("total_x"),
    sum("y").alias("total_y"),
    sum("z").alias("total_z"),
    window("timestamp", "5 minutes").start.alias("window_start"),
    window("timestamp", "5 minutes").end.alias("window_end")
)

# Calculate overall intensity (you may need to customize this based on your specific metrics)
intensity_df = intensity_df.withColumn("intensity", col("total_x") + col("total_y") + col("total_z"))

# Step 7: Find the 5-minute window with maximum intensity for each player, for each game
max_intensity_per_player = intensity_df.groupBy("game_id", "short_name").agg(
    max("intensity").alias("max_intensity"),
    first("window_start").alias("max_intensity_window_start"),
    first("window_end").alias("max_intensity_window_end")
)

# Display the result
print("Most intense 5-minute window for each player, for each game:")
max_intensity_per_player.show(truncate=False)

# Stop SparkSession
spark.stop()
