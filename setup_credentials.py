# File: setup_credentials.py

from aigent.api_manager import APIManager


def setup_google_cloud_credentials():
    """
    Set up Google Cloud credentials for the AIGENT project.
    """
    api_manager = APIManager()
    
    credentials_path = ''
    
    if api_manager.set_google_cloud_credentials(credentials_path):
        print(f"Successfully set Google Cloud credentials path: {credentials_path}")
    else:
        print(f"Failed to set Google Cloud credentials. Please check if the file exists: {credentials_path}")

    # Verify the credentials are loaded correctly
    google_creds = api_manager.get_api_key('google_cloud')
    if google_creds:
        print("Google Cloud credentials loaded successfully.")
    else:
        print("Failed to load Google Cloud credentials.")

if __name__ == "__main__":
    setup_google_cloud_credentials()
