# Technology Stack

## Backend
- Python: The project is primarily Python-based.
- AI/ML Services:
  - Google Cloud Document AI: Used for advanced Optical Character Recognition (OCR)
  - OpenAI API: Used for text generation (GPT-3.5 and GPT-4 models)
  - Anthropic API: Used for text generation (alternative to OpenAI)
- Natural Language Processing (NLP): Custom NLP processing for documents

## Frontend (Planned)
- Next.js: React framework for building server-side rendered and static web applications
- React: JavaScript library for building user interfaces
- TypeScript: Typed superset of JavaScript for improved developer experience and code quality
- Tailwind CSS: Utility-first CSS framework for rapid UI development
- Formik: Form library for React, used for form management and validation
- Yup: JavaScript schema builder for value parsing and validation

## AI Architecture
- Agent-based Architecture: Uses a flexible agent system for AI processing
  - Abstract Base Class: Defines a common interface for all agents
  - Pydantic Integration: Uses Pydantic for data validation and settings management
- Swarm Intelligence:
  - Agency: Manages groups of agents, supporting addition, removal, and creation of agents
  - Swarm: Orchestrates multiple agencies, enabling complex multi-agent systems
  - Task Distribution: Supports distributing tasks across multiple agents and agencies
  - Result Aggregation: Implements logic for combining results from multiple agents/agencies
- Inter-agency Communication: Implemented for communication between agencies

## OCR Tools
- Google Cloud Vision AI: Implemented as GoogleCloudVisionOCRTool for high-accuracy OCR
- Tesseract: Implemented as an alternative OCR option

## File Processing
- OpenCV: Used for image preprocessing in OCR operations
- Pillow: Python Imaging Library for image processing tasks
- PyPDF2: Used for PDF processing

## Data Storage
- SQLite: Used for local database operations

## Security
- Cryptography: Used for encrypting and decrypting API keys

## Cloud Services
- Google Cloud Platform: Used for Document AI and Vision AI services

## DevOps
- Docker: Used for containerization (Dockerfile present in the project)
- Poetry: Used for Python dependency management and packaging

## Testing
- pytest: Framework for writing and running Python tests
- unittest: Python's built-in testing framework, used alongside pytest
- (Frontend testing frameworks to be determined during implementation)

## Additional Tools and Libraries
- Logging: Custom logging module built on top of Python's built-in logging module
- JSON: Used for structured data handling
- os: Used for file and directory operations
- dotenv: Used for loading environment variables from .env file

## Output Formats
- Markdown: OCR results are saved in Markdown format for easy readability and further processing
- JSONL: Used for storing structured data, especially for training data generation

## Architecture Decisions
- Modular Design: The project follows a modular architecture, with separate classes for different functionalities.
- Swarm Architecture: Implements a swarm of AI agents for distributed processing of documents.
- Service-Oriented: The AI functionality is encapsulated in service classes that can be easily integrated and extended.
- Extensibility: The system is designed to easily add new agent types and processing capabilities.
- Error Handling and Logging: Comprehensive error handling and logging implemented across the codebase.
- Test-Driven Development: Emphasis on unit testing for core components to ensure reliability and ease of maintenance.

## Security Considerations
- API keys are encrypted before storage and decrypted when retrieved.
- Google Cloud credentials are stored securely and loaded at runtime.
- Environment variables are used to minimize exposure of sensitive information in code.
- GitHub Secrets: Used for managing sensitive credentials in the CI/CD pipeline

Note: This document will be updated as the project evolves and new technologies or architectural decisions are made.
