import requests

# Define the URL
url = 'http://localhost:8000/user/update_name'

# Your access token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGluIiwiaWQiOiIyYjM2MDRmYy0xYjc3LTRmNWItYWQ3MC0wZTVmOWMzNDExMjciLCJleHAiOjE3NDE4NzAzNjh9.qveZL3VGDJc5pQHiE7yzGLV5L9PSJehfhKGmb5qEVWM"

# Set up headers with Bearer Token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"  # Ensures proper request format
}

# Make a GET request (change method if necessary)
response = requests.patch(url, headers=headers)

# Print response
print(f"Status Code: {response.status_code}")
print("Response JSON:", response.json())
