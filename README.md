# AIGENT: Intelligent Document Processing and AI Agent Toolkit

## Project Overview

AIGENT is a comprehensive toolkit for AI development, focusing on document processing, AI agent trait management, dynamic prompt generation, and agent swarm management. The project's concept and agent flow philosophy align with that of Agency Swarm, aiming to streamline the process of creating, managing, and deploying AI agents for various applications. While currently implemented as a desktop application to address specific file handling challenges, AIGENT maintains its vision of facilitating collaborative AI development.

## Key Features

1. **Document Conversion**: Convert PDF, DOCX, and image files to JSONL, TXT, MD, and DOCX formats for AI training.
2. **AI Agent Trait Management**: Integrated system for managing AI agent traits and characteristics, with a vision for a hierarchical database structure.
3. **Dynamic Prompt Generation**: Context-aware prompt generation for multiple use cases, laying the groundwork for sophisticated agent interactions.
4. **PyQt5-based GUI**: User-friendly desktop interface for document conversion and trait management, serving as a foundation for future agent swarm management features.
5. **Configuration Management**: Persistent settings for improved user experience, essential for managing complex AI agent configurations.
6. **Logging System**: Comprehensive logging for better debugging and user support, crucial for monitoring agent activities and interactions.
7. **OCR Integration**: Support for both Tesseract OCR and Google Cloud Vision API for enhanced text extraction from images and PDFs.
8. **Agent Swarm Management**: Implementation of Agency Swarm concepts for collaborative AI agent interactions and task processing.
9. **NLP Document Processing**: Integrated NLP capabilities for generating training data pairs from processed documents.

## Installation

1. Ensure you have Python 3.8+ and Poetry installed on your system.
2. Clone the repository:
   ```
   git clone https://github.com/your-username/aigent.git
   cd aigent
   ```
3. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Usage

### GUI Usage

1. Activate the Poetry shell:
   ```
   poetry shell
   ```
2. Run the AIGENT GUI:
   ```
   python -m aigent.aigent_gui
   ```
3. Use the GUI to:
   - Select input files or a directory (PDF, DOCX, or image)
   - Choose an output location for the converted files
   - Enter project information and agent traits
   - Select OCR options and output formats
   - Process the documents

### AIGentSwarm Usage

The AIGentSwarm functionality is now integrated into the GUI. When you process documents through the GUI, it automatically utilizes the AIGentSwarm for document processing and NLP tasks.

For programmatic usage of AIGentSwarm:

1. Import the AIGentSwarm class:
   ```python
   from aigent.aigent_swarm import AIGentSwarm
   ```

2. Create an instance of AIGentSwarm:
   ```python
   swarm = AIGentSwarm()
   ```

3. Process documents using the swarm:
   ```python
   results = swarm.process_documents(
       input_files,
       output_dir,
       project_info,
       agent_traits,
       output_formats,
       use_ocr,
       use_cloud_vision
   )
   ```

4. The `results` variable will contain the output from each agent in the swarm for each processed document, including both converted data and NLP processing results.

## Agency Swarm Framework Integration

AIGENT now incorporates the Agency Swarm framework, which allows for more flexible and extensible agent-based processing. The integration includes:

1. **BaseTool**: A foundational class for creating specialized tools used by agents.
2. **NLPDocumentsTool**: A tool for processing documents and generating training data pairs.
3. **NLPDocumentsAgent**: An agent that utilizes the NLPDocumentsTool for document processing.
4. **AIGentSwarm**: A class that manages the swarm of agents and coordinates document processing tasks.

This integration allows for easy expansion of AIGENT's capabilities by adding new tools and agents to the swarm.

## Setting Up Google Cloud Credentials

(This section remains unchanged)

## Development Process

(This section remains unchanged)

## Future Directions

AIGENT's roadmap includes:

1. Expanding agent swarm capabilities for more complex tasks and interactions.
2. Developing a web interface for broader accessibility.
3. Integrating with APIs like OpenAI and Anthropic for enhanced AI capabilities.
4. Implementing intelligent PDF splitting based on content structure.
5. Developing advanced visualization for document structure and AI agent interactions.
6. Enhancing the Agency Swarm implementation with more sophisticated agent types and communication protocols.
7. Implementing a plugin system for easy addition of new tools and agents.
8. Developing specialized agents for different types of document analysis and processing.

## Contributing

(This section remains unchanged)

## License

AIGENT is open-source and licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

- [Agency Swarm](https://github.com/VRSEN/agency-swarm) for philosophical alignment in AI agent collaboration concepts and inspiration for our swarm implementation.
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) for PDF manipulation
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for optical character recognition
- [Google Cloud Vision API](https://cloud.google.com/vision) for advanced OCR capabilities

## Contact

For questions or feedback, please open an issue in the GitHub repository or contact the maintainers at [your-email@example.com](mailto:your-email@example.com).