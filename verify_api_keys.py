# File: aigent/verify_api_keys.py
# Author: Tj Pilant
# Description: This script verifies that the API keys and Google Cloud credentials are properly set.
# Version: 0.2.0

import os

from aigent.api_manager import APIManager


def verify_keys():
    api_manager = APIManager()

    openai_key = api_manager.get_api_key("openai")
    anthropic_key = api_manager.get_api_key("anthropic")
    google_cloud_key_path = api_manager.get_api_key("google_cloud")

    print("OpenAI API Key:", "Set" if openai_key else "Not set")
    print("Anthropic API Key:", "Set" if anthropic_key else "Not set")
    print(
        "Google Cloud Key File Path:",
        google_cloud_key_path if google_cloud_key_path else "Not set",
    )

    google_creds_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    print(
        "GOOGLE_APPLICATION_CREDENTIALS environment variable:",
        google_creds_env if google_creds_env else "Not set",
    )


if __name__ == "__main__":
    verify_keys()
