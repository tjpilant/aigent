import json
import webbrowser
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow

# Load client secrets
client_secret_file = "client_secret_997980018332-v1pnpb3gm94i8u4dqm3fg29jfb84dai4.apps.googleusercontent.com.json"
with open(client_secret_file, "r") as f:
    client_config = json.load(f)

# Create flow instance
flow = Flow.from_client_config(
    client_config, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# The redirect URI must match one of the authorized redirect URIs
flow.redirect_uri = "http://localhost"

# Generate URL for request to Google's OAuth 2.0 server.
auth_url, _ = flow.authorization_url(prompt="consent")

# Open the authorization URL in the default web browser
print(f"Opening browser to authorize the application...")
webbrowser.open(auth_url)

# Wait for user to enter the full redirect URL
redirect_url = input("Please paste the full redirect URL here: ")

# Parse the authorization code from the redirect URL
parsed_url = urlparse(redirect_url)
auth_code = parse_qs(parsed_url.query)["code"][0]

# Exchange auth code for access token
flow.fetch_token(code=auth_code)

# Get the access token
token = flow.credentials.token

print(f"Access token: {token}")

# Optional: Print additional information
print(f"Expiry: {flow.credentials.expiry}")

# Save the token to a file for later use
with open("access_token.txt", "w") as f:
    f.write(token)
print("Access token has been saved to 'access_token.txt'")
