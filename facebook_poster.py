import requests
import os
import datetime
import logging
import time
from dotenv import load_dotenv
from dateutil import parser

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Facebook configuration
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")  # Your Facebook API access token
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")  # Your Facebook page ID
POSTED_GAMES_LOG = "posted_games.log"  # Log file to track posted games

def format_date(date_string):
    """Format the date string to a human-friendly international UTC format."""
    try:
        date_obj = parser.isoparse(date_string)
        return date_obj.strftime("%b %d, %Y at %H:%M UTC")
    except ValueError:
        logging.error(f"Error parsing date: {date_string}")
        return date_string

def format_price(price):
    """Format price with dollar sign and two decimal places."""
    if price == 0 or price == "FREE":
        return "Free"
    return f"${price / 100:.2f}"

def enhance_description(description):
    """Make game descriptions more engaging."""
    if not description or description == "No description available.":
        return "An exciting game awaits you! Dive in and explore thrilling adventures."
    return description + "\n\n🔥 Don't miss out on this epic freebie! Grab it now and enjoy!"

def fetch_free_games():
    """Fetch free games from the Epic Games Store."""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching free games: {e}")
        return []
    
    free_games = []
    for game in data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", []):
        if game.get("promotions"):
            for promo in game["promotions"].get("promotionalOffers", []):
                for offer in promo.get("promotionalOffers", []):
                    discounted_price = format_price(game.get("price", {}).get("totalPrice", {}).get("discountPrice", 0))
                    if discounted_price == "Free":  # Check if it's free
                        url_slug = game.get('catalogNs', {}).get('mappings', [{}])[0].get('pageSlug', None)
                        if url_slug:
                            free_games.append({
                                "title": game.get("title"),
                                "description": enhance_description(game.get("description", "No description available.")),
                                "original_price": format_price(game.get("price", {}).get("totalPrice", {}).get("originalPrice", 0)),
                                "discounted_price": discounted_price,
                                "image_url": game.get("keyImages", [{}])[0].get("url", "https://via.placeholder.com/300"),
                                "url": f"https://store.epicgames.com/en-US/p/{url_slug}",
                                "start_date": offer.get("startDate"),
                                "end_date": offer.get("endDate"),
                            })
    return free_games

def read_posted_games():
    """Read the log file and return a set of posted game titles."""
    if not os.path.exists(POSTED_GAMES_LOG):
        return set()
    
    with open(POSTED_GAMES_LOG, 'r') as file:
        return set(line.strip() for line in file)

def write_posted_game(title):
    """Append the title of a posted game to the log file."""
    with open(POSTED_GAMES_LOG, 'a') as file:
        file.write(title + '\n')

def post_to_facebook(free_games):
    """Post free games information to Facebook page."""
    if not free_games:
        logging.info("No free games to post on Facebook.")
        return
    
    posted_games = read_posted_games()
    
    for game in free_games:
        if game['title'] in posted_games:
            logging.info(f"Skipping already posted game: {game['title']}")
            continue
        
        message = (
            f"🎮 Free Game Alert! 🎮\n\n"
            f"🔥 {game['title']} is now available for free! 🔥\n\n"
            f"📝 {game['description']}\n\n"
            f"💰 Original Price: {game['original_price']} → {game['discounted_price']}\n\n"
            f"📅 Available from: {format_date(game['start_date'])} to {format_date(game['end_date'])}\n\n"
            f"🫰 Grab it now 👇 {game['url']}" 
        )

        url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
        payload = {
            "message": message.encode("utf-8").decode("utf-8"),  # Ensure UTF-8 encoding
            "access_token": ACCESS_TOKEN,
            "link": game['url']  # Post with a link preview instead of an image
        }
        
        try:
            response = requests.post(url, json=payload)  # Use JSON instead of form-data
            response.raise_for_status()
            logging.info(f"Post published successfully for {game['title']}! Response: {response.json()}")
            write_posted_game(game['title'])  # Log the posted game title
        except requests.RequestException as e:
            logging.error(f"Failed to publish post for {game['title']}: {e}")
        
        time.sleep(5)  # Prevent hitting rate limits

def validate_environment_variables():
    """Validate required environment variables."""
    if not ACCESS_TOKEN or not PAGE_ID:
        logging.error("Environment variables for Facebook API are not set.")
        raise EnvironmentError("Please set FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID in your .env file.")

def main():
    """Main function to fetch games and send notifications."""
    validate_environment_variables()
    
    logging.info("Fetching free games...")
    free_games = fetch_free_games()
    
    if free_games:
        logging.info(f"{len(free_games)} free games found! Posting to Facebook...")
        post_to_facebook(free_games)
    else:
        logging.info("No free games available at the moment.")

if __name__ == "__main__":
    main()
