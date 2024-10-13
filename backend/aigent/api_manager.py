"""
This module manages API keys and credentials for various services.
It provides secure storage and retrieval of API keys, with special
handling for Google Cloud credentials.

Author: Tj Pilant
Date: 2024-07-25
Version: 0.5.1
"""

import json
import os

from cryptography.fernet import Fernet, InvalidToken
from .utils.logger import get_logger

logger = get_logger(__name__)

class APIManager:
    """
    A class to manage API keys and credentials.

    This class provides methods to securely retrieve API keys and credentials
    for various services, including special handling for Google Cloud credentials.
    """

    def __init__(self):
        """
        Initialize the APIManager.
        """
        logger.info("Initializing APIManager")
        self.encryption_key = self.get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        logger.info("APIManager initialized successfully")

    def get_or_create_encryption_key(self):
        """
        Get an existing encryption key or create a new one.

        Returns:
            bytes: The encryption key.
        """
        key_file = '.encryption_key'
        if os.path.exists(key_file):
            logger.debug("Loading existing encryption key")
            with open(key_file, 'rb') as file:
                return file.read()
        else:
            logger.info("Creating new encryption key")
            key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(key)
            return key

    def get_api_key(self, service):
        """
        Retrieve the API key for a specified service.

        Args:
            service (str): The name of the service.

        Returns:
            str or dict: The API key or credentials for the service.
                         Returns None if the key is not found.
        """
        logger.debug(f"Retrieving API key for service: {service}")
        if service.lower() == 'google_cloud':
            return self.get_google_cloud_credentials()

        env_var_name = f"{service.upper()}_KEY"
        key = os.getenv(env_var_name)
        if key:
            try:
                # Attempt to decrypt the key
                decrypted_key = self.fernet.decrypt(key.encode()).decode()
                logger.info(f"API key retrieved successfully for service: {service}")
                return decrypted_key
            except InvalidToken:
                # If decryption fails, assume the key is not encrypted
                logger.warning(f"API key for {service} is not encrypted")
                return key
        logger.warning(f"API key not found for service: {service}")
        return None

    def get_google_cloud_credentials(self):
        """
        Retrieve Google Cloud credentials from the GOOGLE_CLOUD_KEY environment variable.

        Returns:
            dict: The Google Cloud credentials as a dictionary.
                  Returns None if the credentials are not found.
        """
        logger.debug("Retrieving Google Cloud credentials")
        cred_json = os.getenv('GOOGLE_CLOUD_KEY')
        if cred_json:
            try:
                credentials = json.loads(cred_json)
                logger.info("Google Cloud credentials retrieved successfully")
                return credentials
            except json.JSONDecodeError:
                logger.error("Invalid JSON in GOOGLE_CLOUD_KEY environment variable")
        else:
            logger.warning("Google Cloud credentials not found")
        return None

# Usage example
if __name__ == "__main__":
    api_manager = APIManager()

    # Getting Google Cloud credentials
    google_creds = api_manager.get_api_key('google_cloud')
    logger.info("Google Cloud Credentials retrieved")

    # Getting other API keys
    logger.info("OpenAI API Key: %s", api_manager.get_api_key('openai'))
    logger.info("Anthropic API Key: %s", api_manager.get_api_key('anthropic'))
