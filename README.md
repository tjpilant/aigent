# AIGENT Project

AIGENT is an AI-powered document processing and analysis system that utilizes advanced OCR techniques and a swarm of AI agents for distributed processing.

## Project Structure

The project is organized into the following main components:

- `backend/`: Contains the Python-based backend code
  - `aigent/`: Main application code
    - `agency_swarm/`: Implementation of the swarm intelligence architecture
    - `utils/`: Utility functions and helpers
  - `tests/`: Unit and integration tests

- `frontend/`: (To be implemented) Will contain the Next.js-based frontend code

- `cline_docs/`: Project documentation and guidelines

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Poetry (for Python dependency management)
- Google Cloud account with Document AI and Vision AI enabled
- OpenAI API key
- Anthropic API key

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/aigent.git
   cd aigent
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   GOOGLE_CLOUD_KEY=path/to/your/google-cloud-credentials.json
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

4. Initialize the database:
   ```
   poetry run python backend/aigent/init_database.py
   ```

5. Run the backend tests:
   ```
   poetry run pytest
   ```

### Running the Application

Currently, the application is backend-only. To run specific components or tests, use the following commands:

- Run the AI service:
  ```
  poetry run python backend/aigent/ai_service.py
  ```

- Process a document using the swarm:
  ```
  poetry run python backend/aigent/aigent_swarm.py
  ```

## Documentation

For more detailed information about the project, refer to the following documentation:

- [Codebase Summary](cline_docs/codebaseSummary.md)
- [Technology Stack](cline_docs/techStack.md)
- [Error Handling and Logging Guidelines](cline_docs/error_handling_and_logging_guidelines.md)

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
