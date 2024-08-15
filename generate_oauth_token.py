import json

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
# for the OAuth 2.0 client, which you configured in the API Console.
flow.redirect_uri = "http://localhost"

# Generate URL for request to Google's OAuth 2.0 server.
auth_url, _ = flow.authorization_url(prompt="consent")

print(f"Please go to this URL to authorize the application: {auth_url}")

# Wait for user to enter the authorization code
auth_code = input("Enter the authorization code: ")

# Exchange auth code for access token
flow.fetch_token(code=auth_code)

# Get the access token
token = flow.credentials.token

print(f"Access token: {token}")
