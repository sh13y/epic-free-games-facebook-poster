import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

def post_to_facebook(title, description, link, image_url, end_date):
    """Post a notification to the Facebook page."""
    url = f"https://graph.facebook.com/v17.0/{PAGE_ID}/photos"

    # Build the message
    message = (
        f"🎮 **{title}** is now available for FREE on the Epic Games Store! 🎉\n\n"
        f"📝 {description}\n"
        f"📅 Valid until: {end_date}\n"
        f"🔗 Get it here: {link}\n"
    )

    # Prepare payload
    payload = {
        "caption": message,
        "url": image_url,
        "access_token": PAGE_ACCESS_TOKEN,
    }

    # Make the POST request
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Successfully posted to Facebook: {title}")
    else:
        print(f"Failed to post to Facebook. Error: {response.json()}")

def main():
    """Main function to fetch free games and post to Facebook."""
    # Example data for testing
    free_games = [
        {
            "title": "Hell Let Loose",
            "description": "A WW2 platoon-based realistic multiplayer experience.",
            "url": "https://store.epicgames.com/en-US/p/hell-let-loose",
            "image_url": "https://example.com/image.jpg",
            "end_date": "January 9, 2025 at 4:00 PM",
        }
    ]

    print("Posting free games to Facebook...")
    for game in free_games:
        post_to_facebook(
            game["title"],
            game["description"],
            game["url"],
            game["image_url"],
            game["end_date"],
        )

if __name__ == "__main__":
    main()
