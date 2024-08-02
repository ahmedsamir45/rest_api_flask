# Import the requests library to make HTTP requests
import requests

# Define the base URL for the API
BASE = "http://127.0.0.1:5000/"

# Send a PATCH request to update the video with ID 2 and print the response
response = requests.patch(BASE + "video/2", {})
print(response.json())
