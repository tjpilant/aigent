# AIGENT: Intelligent Document Processing and AI Agent Toolkit

## Project Overview

AIGENT is a comprehensive toolkit for AI development, focusing on document processing, AI agent trait management, dynamic prompt generation, and agent swarm management. The project's concept and agent flow philosophy align with that of Agency Swarm, aiming to streamline the process of creating, managing, and deploying AI agents for various applications. While currently implemented as a desktop application to address specific file handling challenges, AIGENT maintains its vision of facilitating collaborative AI development.

## Key Features

1. **Document Conversion**: Convert PDF documents to JSONL format for AI training, with future plans to support various document formats (DOCX, TXT).
2. **AI Agent Trait Management**: Integrated system for managing AI agent traits and characteristics, with a vision for a hierarchical database structure.
3. **Dynamic Prompt Generation**: Context-aware prompt generation for multiple use cases, laying the groundwork for sophisticated agent interactions.
4. **PyQt5-based GUI**: User-friendly desktop interface for document conversion and trait management, serving as a foundation for future agent swarm management features.
5. **Configuration Management**: Persistent settings for improved user experience, essential for managing complex AI agent configurations.
6. **Logging System**: Comprehensive logging for better debugging and user support, crucial for monitoring agent activities and interactions.

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

1. Activate the Poetry shell:
   ```
   poetry shell
   ```
2. Run the AIGENT GUI:
   ```
   python aigent_gui.py
   ```
3. Use the GUI to:
   - Select an input PDF file
   - Choose an output location for the JSONL file
   - Enter project information and agent traits
   - Convert the PDF to JSONL

## Future Directions

While currently focused on robust PDF to JSONL conversion and trait management, AIGENT's roadmap includes:

1. Implementing agent swarm management capabilities for complex tasks.
2. Expanding document conversion to support various formats.
3. Developing a web interface for broader accessibility.
4. Integrating with APIs like OpenAI and Anthropic for enhanced AI capabilities.
5. Implementing intelligent PDF splitting based on content structure.
6. Developing advanced visualization for document structure and AI agent interactions.

## Contributing

We welcome contributions to AIGENT! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## License

AIGENT is open-source and licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

- [Agency Swarm](https://github.com/VRSEN/agency-swarm) for philosophical alignment in AI agent collaboration concepts.
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) for PDF manipulation

## Contact

For questions or feedback, please open an issue in the GitHub repository or contact the maintainers at [your-email@example.com](mailto:your-email@example.com).