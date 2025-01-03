import facebook as fb

# Facebook Access Token (replace with your valid Page Access Token)
ACCESS_TOKEN = "EAAZAmItlD4Q8BOZCQa54rGrhxGcmhnhGKf9DYmeEUHrm7YgM8N82ZBAH9mX3gtTH7tpquvMfXwPJC19ONbaeFMrg7UwFZCAlVZBaL9xH5hUwThIpkSRiqUQDBjAxI8sKTEp3XB5wtZB5gppviKhIdcrAn0JnyL58AvA3mZCJ9TbXploMDXTdohlLZAyl0jddYmBQl0LuogpFLwDFh9vNTIAZD"

# Initialize the Facebook Graph API
graph = fb.GraphAPI(ACCESS_TOKEN)

# Post a message
try:
    post = graph.put_object(parent_object="me", connection_name="feed", message="This is an automated post!")
    print(f"Successfully posted to Facebook: {post}")
except fb.GraphAPIError as e:
    print(f"Failed to post to Facebook: {e}")

# Post a photo with a caption
try:
    with open("photo.jpg", "rb") as photo:
        photo_post = graph.put_photo(photo, message="Automated photo post with caption!")
        print(f"Successfully posted photo: {photo_post}")
except fb.GraphAPIError as e:
    print(f"Failed to post photo: {e}")
