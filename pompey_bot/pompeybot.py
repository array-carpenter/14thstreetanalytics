import csv
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Read player names from the CSV file
with open('pompey_bot\eligibledraftplayers.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    player_names = [row['PLAYER'] for row in reader]
# Create tweet image
def generate_tweet_image(text):
    img = Image.new('RGB', (600, 200), color='white')
    d = ImageDraw.Draw(img)

    # Grab Pompey profile picture
    profile_pic = Image.open('pompey_bot\profile_picture.png') 
    profile_pic = profile_pic.resize((50, 50))

    # Circular Crop
    mask = Image.new('L', (50, 50), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 50, 50), fill=255)
    profile_pic.putalpha(mask)

    # Add profile picture
    img.paste(profile_pic, (10, 10), profile_pic)

    # Add account name and handle
    font = ImageFont.truetype('arial.ttf', 12)
    d.text((70, 10), "Keith Pompey", fill=(29, 161, 242), font=font)  # Adjust the account name and handle
    d.text((70, 30), "@PompeyOnSixers", fill='gray', font=font)  # Adjust the account name and handle

    # Add the tweet text
    tweet_font = ImageFont.truetype('arial.ttf', 14)
    d.text((70, 70), text, fill='black', font=tweet_font)

    # Save
    img.save('tweet_image.png')
    img.show()

# Pompey phrases
phrases = [
    "The hustle that {player_name} brings to the court is unparalleled. A true game-changer.",
    "Don't underestimate the impact of {player_name} in the next match. They're a force to be reckoned with.",
    "Mark my words, {player_name} is going to be the standout performer of this season.",
    "The synergy between {player_name} and the rest of the team is what's setting them apart this year.",
    "Keep an eye on {player_name}. Their work ethic is inspirational, and it's reflecting in their performance.",
    "It's not just about the numbers. {player_name} brings an intangible energy that drives the team forward.",
        "I would consider picking {player1} over {player2} in this round. Their recent form is impressive.",
    "Keep an eye on {player1} as a sleeper pick. They might surprise everyone this season.",
    "The stats show that {player1} has a slight edge over {player2}. Consider them for a strategic advantage.",
    "If you're looking for consistent performance, {player1} is your best bet compared to {player2}.",
    "{player1} has been a solid performer throughout the season, making them a reliable choice over {player2}.",
    "Considering the matchup, {player1} seems to have an advantage over {player2} in this round."
]

# Generate random phrase
def generate_reply():
    chosen_phrase = random.choice(phrases)
    return chosen_phrase.format(
        player_name=random.choice(player_names),
        team_name="TeamY",
        team1="TeamA",
        team2="TeamB",
        player1=random.choice(player_names),
        player2=random.choice(player_names),
    )

# Generate entire image
def generate_tweet_image(text):
    # Create a blank image with a white background
    img = Image.new('RGB', (600, 200), color='white')
    d = ImageDraw.Draw(img)

    # Load a Twitter profile picture and resize it
    profile_pic = Image.open('pompey_bot\profile_picture.png')
    profile_pic = profile_pic.resize((50, 50))

    # Create a circular mask
    mask = Image.new('L', (50, 50), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 50, 50), fill=255)
    profile_pic.putalpha(mask)
    img.paste(profile_pic, (10, 10), profile_pic)
    font = ImageFont.truetype('arial.ttf', 12)
    d.text((70, 10), "Keith Pompey", fill=(29, 161, 242), font=font)
    d.text((70, 30), "@PompeyOnSixers", fill='gray', font=font) 

    # Wrap the text
    tweet_font = ImageFont.truetype('arial.ttf', 14)
    lines = textwrap.wrap(text, width=40)
    y_text = 70
    for line in lines:
        d.text((70, y_text), line, fill='black', font=tweet_font)
        y_text += 20

    # Save
    img.save('pompey_bot/tweet_image.png')
    img.show()

reply = generate_reply()
generate_tweet_image(reply)
