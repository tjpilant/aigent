# Description: This script is to set up API keys for the OpenAI, Anthropic, and Google Cloud APIs.
# Usage: Run this script and enter the API keys when prompted.
# Note: This script is not intended to be run multiple times. It is only to be run once to set up the API keys.
#  If you need to update the API keys, you can do so in the .env file directly.
#  If you need to reset the API keys, you can delete the .env file and run this script again.

from aigent.api_manager import APIManager


def setup_keys():
    api_manager = APIManager()

    openai_key = input("Enter your OpenAI API key: ")
    anthropic_key = input("Enter your Anthropic API key: ")
    google_cloud_key = input("Enter your Google Cloud API key: ")

    api_manager.set_api_key("openai", openai_key)
    api_manager.set_api_key("anthropic", anthropic_key)
    api_manager.set_api_key("google_cloud", google_cloud_key)

    print("API keys have been set successfully.")


if __name__ == "__main__":
    # Function to set .env API keys for OpenAI, Anthropic, and Google Cloud APIs.
    setup_keys()
