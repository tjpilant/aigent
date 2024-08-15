import os
import sys

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv


class APIManager:
    def __init__(self):
        load_dotenv()  # This loads the variables from .env
        self.encryption_key = self.get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)

    def get_or_create_encryption_key(self):
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
        encrypted_key = os.getenv(f"{service.upper()}_API_KEY")
        if encrypted_key:
            try:
                return self.fernet.decrypt(encrypted_key.encode()).decode()
            except InvalidToken:
                print(f"Warning: Stored {service} API key is not properly encrypted. Please set it again.")
                return None
        return None

    def set_api_key(self, service, api_key):
        encrypted_key = self.fernet.encrypt(api_key.encode()).decode()
        os.environ[f"{service.upper()}_API_KEY"] = encrypted_key
        # Update the .env file
        self.update_env_file(f"{service.upper()}_API_KEY", encrypted_key)

    def update_env_file(self, key, value):
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

# Usage example:
if __name__ == "__main__":
    api_manager = APIManager()
    
    # Setting API keys
    api_manager.set_api_key('openai', 'your-openai-api-key')
    api_manager.set_api_key('anthropic', 'your-anthropic-api-key')
    
    # Getting API keys
    print("OpenAI API Key:", api_manager.get_api_key('openai'))
    print("Anthropic API Key:", api_manager.get_api_key('anthropic'))