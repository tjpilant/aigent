"""
This module manages API keys and credentials for various services.
It provides secure storage and retrieval of API keys, with special
handling for Google Cloud credentials.

Author: Tj Pilant
Date: 2024-07-25
Version: 0.2.0
"""

import json
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


class APIManager:
    """
    A class to manage API keys and credentials.

    This class provides methods to securely store, retrieve, and manage
    API keys and credentials for various services, including special
    handling for Google Cloud credentials.
    """

    def __init__(self):
        """
        Initialize the APIManager.

        Loads environment variables and sets up encryption for secure
        storage of API keys.
        """
        load_dotenv()  # This loads the variables from .env
        self.encryption_key = self.get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)

    def get_or_create_encryption_key(self):
        """
        Get an existing encryption key or create a new one.

        Returns:
            bytes: The encryption key.
        """
        key_file = '.encryption_key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                return file.read()
        else:
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
        if service == 'google_cloud':
            return self.get_google_cloud_credentials()
        
        encrypted_key = os.getenv(f"{service.upper()}_API_KEY")
        if encrypted_key:
            return self.fernet.decrypt(encrypted_key.encode()).decode()
        return None

    def set_api_key(self, service, api_key):
        """
        Set the API key for a specified service.

        Args:
            service (str): The name of the service.
            api_key (str): The API key to be stored.
        """
        encrypted_key = self.fernet.encrypt(api_key.encode()).decode()
        os.environ[f"{service.upper()}_API_KEY"] = encrypted_key
        self.update_env_file(f"{service.upper()}_API_KEY", encrypted_key)

    def update_env_file(self, key, value):
        """
        Update the .env file with a new or updated key-value pair.

        Args:
            key (str): The key to be updated or added.
            value (str): The value to be set for the key.
        """
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as file:
                lines = file.readlines()
            
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    updated = True
                    break
            
            if not updated:
                lines.append(f"{key}={value}\n")
            
            with open(env_path, 'w') as file:
                file.writelines(lines)
        else:
            with open(env_path, 'w') as file:
                file.write(f"{key}={value}\n")

    def get_google_cloud_credentials(self):
        """
        Retrieve Google Cloud credentials from the specified JSON file.

        Returns:
            dict: The Google Cloud credentials as a dictionary.
                  Returns None if the credentials file is not found.
        """
        cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if cred_path and os.path.exists(cred_path):
            with open(cred_path, 'r') as cred_file:
                return json.load(cred_file)
        return None

    def set_google_cloud_credentials(self, cred_path):
        """
        Set the path to the Google Cloud credentials JSON file.

        Args:
            cred_path (str): The file path to the Google Cloud credentials JSON file.

        Returns:
            bool: True if the credentials file was successfully set, False otherwise.
        """
        if os.path.exists(cred_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
            self.update_env_file('GOOGLE_APPLICATION_CREDENTIALS', cred_path)
            return True
        return False

# Usage example
if __name__ == "__main__":
    api_manager = APIManager()
    
    # Setting Google Cloud credentials
    api_manager.set_google_cloud_credentials('/path/to/your/google_cloud_credentials.json')
    
    # Getting Google Cloud credentials
    google_creds = api_manager.get_api_key('google_cloud')
    print("Google Cloud Credentials:", google_creds)
    
    # Setting and getting other API keys
    api_manager.set_api_key('openai', 'your-openai-api-key')
    print("OpenAI API Key:", api_manager.get_api_key('openai'))