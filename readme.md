#AIGENT
AIGENT: Intelligent Document Processing and AI Agent Toolkit


Project Overview

AIGENT is an advanced toolkit designed for AI researchers, developers, and data scientists working on large language models and AI agents. It combines intelligent document processing with dynamic AI agent trait management and prompt generation.


Key Features

1.**Document Conversion**: Convert various document formats (PDF, etc.) to JSONL for AI training.
2.**AI Agent Trait Management**: Hierarchical database for managing AI agent traits and characteristics.
3.**Dynamic Prompt Generation**: Context-aware prompt generation for multiple use cases (solo tasks, agent swarms, user-editable prompts).
4.**Metadata Tagging**: Flexible system for enhanced AI training data.
5.**Intuitive GUI**: Easy management of agent traits and prompt generation.
6.**Extensible Architecture**: Support for future AI development paradigms.

Development Goals

1. Enhance user experience through an intuitive and efficient GUI.
2. Improve data quality and relevance for AI training purposes.
3. Streamline the process of preparing large volumes of document data for AI consumption.
4. Provide flexibility in defining AI agent characteristics and training parameters.
Current Implementation

GUI Components

● General tab: Input/output file selection
● Project Info tab: Project-specific details
● Agent Traits tab: Customizable AI agent characteristics
● Progress bar: Visual representation of conversion progress
● Log viewer: Detailed conversion process information
● Action buttons: Convert, Reset to Defaults, Save Configuration

Core Functionality

● PDF to JSONL conversion
● Data validation using marshmallow schemas
● Configuration file management
● Threaded conversion process for responsive GUI

Todo List

1. Refine and expand agent trait definitions
2. Implement more sophisticated multi-document relationship handling
3. Enhance error handling and user feedback mechanisms
4. Optimize performance for large-scale document processing

Future Developments

1. Adding more detailed error handling and validation feedback
2. Implementing a way to load and switch between different saved configurations
3. Adding tooltips or help text for each input field to guide users
4. Improving the visual design with stylesheets or custom widgets
5. Expanding functionality to convert DOCX documents
6. Developing a prompt engineer that can translate the JSON data into Agent Instruction
markdown files

Prompt Engineer Development

The prompt engineer will be designed to:

● Parse the JSONL output from AIGent
● Extract relevant information about agent traits and project specifics
● Generate structured markdown files containing agent instructions
● Customize instructions based on the defined agent characteristics
● Include specific commands and guidelines as demonstrated in the Browsing Agent

Instructions example
Getting Started
Installation
AIGent can be run either locally or using Docker. Both methods require Python 3.11 or later.

Local Installation

1. Clone this repository
2. Ensure you have Python 3.8 installed:
python --version
3. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
4. Install the required dependencies (packages):
pip install -r requirements.txt

Docker Installation

1. Ensure you have Docker installed on your system.
2. Build the Docker image:
Copy
docker build -t aigent .
3. Run the container:
Copy
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix aigent
Note: Running GUI applications in Docker might require additional setup depending on your operating system.
Usage

Local Usage

1. Run the AIGent GUI:
Copy
python aigent_gui.py

Docker Usage

1. Run the container with GUI support (make sure you've set up X11 forwarding):
Copy
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix aigent
2. Use the GUI to select an input PDF file and specify an output location.

3. Enter project information.

4. Click "Convert PDF to JSONL" to start the conversion process.

Contributing

## Development

To contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit them (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Testing

To run the tests, use the following command:
pytest

We welcome contributions to the AIGent project. Please refer to our contribution guidelines for more information on how to submit pull requests, report issues, or suggest enhancements.

License
[Insert appropriate license information here]
