import os
import requests
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# Facebook API credentials
ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

def fetch_free_games():
    """Fetch free games from the Epic Games Store."""
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Error fetching free games: {e}"

    free_games = []
    for game in data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", []):
        if game.get("promotions"):
            for promo in game["promotions"].get("promotionalOffers", []):
                for offer in promo.get("promotionalOffers", []):
                    original_price = game.get("price", {}).get("totalPrice", {}).get("originalPrice", 0)
                    discounted_price = game.get("price", {}).get("totalPrice", {}).get("discountPrice", 0)
                    if original_price == 0 and discounted_price == 0:
                        free_games.append({
                            "title": game.get("title"),
                            "url": f"https://store.epicgames.com/en-US/p/{game.get('productSlug')}",
                            "end_date": offer.get("endDate")
                        })
    return free_games

def check_facebook_permissions():
    """Check if the required Facebook permissions are granted."""
    url = f"https://graph.facebook.com/me/permissions"
    params = {
        "access_token": ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "data" in data:
        permissions = {item["permission"]: item["status"] for item in data["data"]}
        required_permissions = ["pages_read_engagement", "pages_manage_posts"]
        for perm in required_permissions:
            if permissions.get(perm) != "granted":
                print(f"Missing required permission: {perm}")
                return False, f"Missing required permission: {perm}"
        print("All required permissions are granted.")
        return True, "All required permissions are granted."
    print(f"Error checking permissions: {data}")
    return False, "Error checking permissions."

def post_to_facebook(message, link=None):
    """Post a message to the Facebook page."""
    has_permissions, permission_message = check_facebook_permissions()
    if not has_permissions:
        return {"error": {"message": permission_message}}

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    if link:
        payload["link"] = link
    response = requests.post(url, data=payload)
    return response.json()

def format_date(date_string):
    """Format the ISO date string to a human-readable format."""
    try:
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_obj.strftime("%B %d, %Y at %I:%M %p")
    except ValueError:
        return date_string

def main():
    free_games = fetch_free_games()
    if isinstance(free_games, str):  # Error message
        print(free_games)
        return

    if free_games:
        for game in free_games:
            end_date = format_date(game["end_date"])
            message = (
                f"🎮 *{game['title']}* is now FREE on the Epic Games Store!\n\n"
                f"Offer valid until: {end_date}\n\n"
                f"Claim it here: {game['url']}"
            )
            response = post_to_facebook(message, link=game["url"])
            if "error" in response:
                print(f"Failed to post to Facebook: {response['error']['message']}")
            else:
                print(f"Posted to Facebook: {response}")
    else:
        print("No free games available at the moment.")

if __name__ == "__main__":
    main()
