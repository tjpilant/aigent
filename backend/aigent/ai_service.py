# File: aigent/ai_service.py
# Author: Tj Pilant
# Description: Handles AI service integrations for AIGENT, focusing on API calls for the swarm agency
# Version: 0.7.0

import json
import os
from typing import Optional, Dict, Any

import openai
from anthropic import Anthropic
from google.cloud import documentai
from google.oauth2 import service_account

from aigent.api_manager import APIManager
from aigent.utils.logger import get_logger

logger = get_logger(__name__)

class AIService:
    def __init__(self):
        logger.info("Initializing AIService")
        self.api_manager = APIManager()
        self.openai_api_key = self.api_manager.get_api_key("openai")
        self.anthropic_api_key = self.api_manager.get_api_key("anthropic")

        self.openai_client: Optional[openai.OpenAI] = None
        self.anthropic_client: Optional[Anthropic] = None

        self._initialize_clients()
        logger.info("AIService initialized successfully")

    def _initialize_clients(self):
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not found. OpenAI services will not be available.")

        if self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
            logger.info("Anthropic client initialized")
        else:
            logger.warning("Anthropic API key not found. Anthropic services will not be available.")

    def generate_openai_response(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        if not self.openai_client:
            logger.error("OpenAI client is not initialized")
            raise ValueError("OpenAI client is not initialized. Cannot generate response.")

        try:
            logger.info("Generating OpenAI response", extra={"model": model, "prompt_length": len(prompt)})
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("OpenAI response generated successfully", extra={"response_length": len(response.choices[0].message.content)})
            return response.choices[0].message.content
        except Exception as e:
            logger.error("Error generating OpenAI response", extra={"error": str(e), "model": model})
            raise

    def generate_anthropic_response(self, prompt: str, model: str = "claude-2") -> str:
        if not self.anthropic_client:
            logger.error("Anthropic client is not initialized")
            raise ValueError("Anthropic client is not initialized. Cannot generate response.")

        try:
            logger.info("Generating Anthropic response", extra={"model": model, "prompt_length": len(prompt)})
            response = self.anthropic_client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens_to_sample=300
            )
            logger.info("Anthropic response generated successfully", extra={"response_length": len(response.completion)})
            return response.completion
        except Exception as e:
            logger.error("Error generating Anthropic response", extra={"error": str(e), "model": model})
            raise

    def make_api_call(self, api_name: str, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generic method to make API calls for the swarm agency.
        """
        try:
            logger.info(f"Making API call to {api_name}", extra={"endpoint": endpoint, "method": method})
            # Implement the actual API call logic here
            # This is a placeholder and should be replaced with actual API call implementation
            response = {"status": "success", "data": "API call result"}
            logger.info(f"API call to {api_name} completed successfully")
            return response
        except Exception as e:
            logger.error(f"Error making API call to {api_name}", extra={"error": str(e), "endpoint": endpoint})
            raise

# Usage example
if __name__ == "__main__":
    ai_service = AIService()

    # Example OpenAI response
    try:
        openai_response = ai_service.generate_openai_response("Tell me a joke")
        print("OpenAI Response:", openai_response)
    except Exception as e:
        logger.error("OpenAI Error", extra={"error": str(e)})

    # Example Anthropic response
    try:
        anthropic_response = ai_service.generate_anthropic_response("Tell me a joke")
        print("Anthropic Response:", anthropic_response)
    except Exception as e:
        logger.error("Anthropic Error", extra={"error": str(e)})

    # Example API call
    try:
        api_response = ai_service.make_api_call("ExampleAPI", "/example/endpoint", method="POST", data={"key": "value"})
        print("API Response:", api_response)
    except Exception as e:
        logger.error("API Call Error", extra={"error": str(e)})
