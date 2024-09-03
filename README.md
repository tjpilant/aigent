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
   python -m aigent.aigent_gui
   ```
3. Use the GUI to:
   - Select an input file (PDF, DOCX, or image)
   - Choose an output location for the converted files
   - Enter project information and agent traits
   - Select OCR options and output formats
   - Convert the document

## Setting Up Google Cloud Credentials

To use AIGENT with Google Cloud services (e.g., Cloud Vision API), follow these steps:

1. Obtain a Google Cloud JSON credentials file:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to "APIs & Services" > "Credentials"
   - Create a new Service Account Key and download the JSON file
2. Place the JSON file in a secure location on your system.
3. Set up the credentials in AIGENT:
   - Create a file named `setup_credentials.py` in your AIGENT project directory
   - Add the following code to the file:
     ```python
     from aigent.api_manager import APIManager

     def setup_google_cloud_credentials():
         api_manager = APIManager()
         credentials_path = '/path/to/your/google_cloud_credentials.json'
         
         if api_manager.set_google_cloud_credentials(credentials_path):
             print(f"Successfully set Google Cloud credentials path: {credentials_path}")
         else:
             print(f"Failed to set Google Cloud credentials. Please check if the file exists: {credentials_path}")

     if __name__ == "__main__":
         setup_google_cloud_credentials()
     ```
   - Replace `/path/to/your/google_cloud_credentials.json` with the actual path to your JSON file
4. Run the setup script:
   ```
   poetry run python setup_credentials.py
   ```
5. Verify the setup:
   - The script will print a success message if the credentials are set correctly
   - You can also check the `.env` file in your project directory to ensure the `GOOGLE_APPLICATION_CREDENTIALS` variable is set

Note: Keep your credentials file secure and never commit it to version control. The `.env` file containing the credentials path should also be in your `.gitignore`.

## Future Directions

AIGENT's roadmap includes:

1. Implementing agent swarm management capabilities for complex tasks.
2. Developing a web interface for broader accessibility.
3. Integrating with APIs like OpenAI and Anthropic for enhanced AI capabilities.
4. Implementing intelligent PDF splitting based on content structure.
5. Developing advanced visualization for document structure and AI agent interactions.

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
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for optical character recognition
- [Google Cloud Vision API](https://cloud.google.com/vision) for advanced OCR capabilities

## Contact

For questions or feedback, please open an issue in the GitHub repository or contact the maintainers at [your-email@example.com](mailto:your-email@example.com).