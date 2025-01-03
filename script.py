import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Facebook API credentials
ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")  # Your Facebook Page ID

def post_to_facebook(message, link=None):
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    if link:
        payload["link"] = link
    response = requests.post(url, data=payload)
    return response.json()

# Example usage
message = "Check out this week's free games on the Epic Games Store!"
post_to_facebook(message, link="https://store.epicgames.com/")
