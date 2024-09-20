# AIGENT: Intelligent Document Processing and AI Agent Toolkit

## Project Overview

AIGENT is a comprehensive toolkit for AI development, focusing on document processing, AI agent trait management, dynamic prompt generation, and agent swarm management. The project's concept and agent flow philosophy align with that of Agency Swarm, aiming to streamline the process of creating, managing, and deploying AI agents for various applications. AIGENT is now implemented as a web application to provide broader accessibility and easier deployment.

## Key Features

1. **Document Conversion**: Convert PDF, DOCX, and image files to JSONL, TXT, MD, and DOCX formats for AI training.
2. **AI Agent Trait Management**: Integrated system for managing AI agent traits and characteristics, with a vision for a hierarchical database structure.
3. **Dynamic Prompt Generation**: Context-aware prompt generation for multiple use cases, laying the groundwork for sophisticated agent interactions.
4. **Flask-based Web GUI**: User-friendly web interface for document conversion, trait management, and GPT agent creation.
5. **Configuration Management**: Persistent settings for improved user experience, essential for managing complex AI agent configurations.
6. **Logging System**: Comprehensive logging for better debugging and user support, crucial for monitoring agent activities and interactions.
7. **OCR Integration**: Support for both Tesseract OCR and Google Cloud Vision API for enhanced text extraction from images and PDFs.
8. **Agent Swarm Management**: Implementation of Agency Swarm concepts for collaborative AI agent interactions and task processing.
9. **NLP Document Processing**: Integrated NLP capabilities for generating training data pairs from processed documents.
10. **GPT Agent Developer**: Create and manage specialized GPT agents with defined traits and responsibilities.

## Installation

(This section remains unchanged)

## Usage

### Web GUI Usage

1. Activate the Poetry shell:
   ```
   poetry shell
   ```
2. Run the AIGENT Web GUI:
   ```
   python -m aigent.aigent_gui
   ```
3. Open a web browser and navigate to `http://localhost:5000` (or the appropriate address if running on a different host/port).
4. Use the web interface to:
   - Upload input files (PDF, DOCX, or image)
   - Specify an output location for the converted files
   - Enter project information and agent traits
   - Select OCR options and output formats
   - Process the documents
   - Create and manage GPT agents

### AIGentSwarm Usage

(This section remains unchanged)

## Agency Swarm Framework Integration

(This section remains unchanged)

## GPT Agent Developer

The GPT Agent Developer is accessible through the web interface, allowing users to create and manage specialized GPT agents. These agents can be tailored for specific tasks or professions, with defined traits, responsibilities, and interaction styles.

Key capabilities:
- Create new GPT agents with specific professions and traits
- Store agent descriptions in a SQLite database for easy management
- List all created GPT agents
- Utilize created agents in document processing tasks (future development)

To use the GPT Agent Developer:
1. Open the AIGENT Web GUI in your browser
2. Use the "Create GPT Agent" form to define a new agent
3. View the list of created agents on the main page

The GPT Agent Developer lays the groundwork for more sophisticated AI interactions and task-specific processing within the AIGENT ecosystem.

## Setting Up Google Cloud Credentials

(This section remains unchanged)

## Development Process

(This section remains unchanged)

## Future Directions

AIGENT's roadmap includes:

1. Expanding agent swarm capabilities for more complex tasks and interactions.
2. Enhancing the web interface with more advanced features and improved user experience.
3. Integrating with APIs like OpenAI and Anthropic for enhanced AI capabilities.
4. Implementing intelligent PDF splitting based on content structure.
5. Developing advanced visualization for document structure and AI agent interactions.
6. Enhancing the Agency Swarm implementation with more sophisticated agent types and communication protocols.
7. Implementing a plugin system for easy addition of new tools and agents.
8. Developing specialized agents for different types of document analysis and processing.
9. Expanding the GPT Agent Developer to allow for more complex agent interactions and task assignments.
10. Implementing real-time collaboration features in the web interface.

## Contributing

(This section remains unchanged)

## License

AIGENT is open-source and licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

(This section remains unchanged)

## Contact

For questions or feedback, please open an issue in the GitHub repository or contact the maintainers at [your-email@example.com](mailto:your-email@example.com).