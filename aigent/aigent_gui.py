# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: GUI for the AIGent application
<<<<<<< Updated upstream
# Version: 0.9.4
=======
# Version: 0.9.5
>>>>>>> Stashed changes

import logging
import os
import sys
import sqlite3
<<<<<<< Updated upstream
from PyQt5.QtCore import Qt, QThread, pyqtSignal
=======
from PyQt5.QtCore import QThread, pyqtSignal
>>>>>>> Stashed changes
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QAction,
    QInputDialog,
)

from aigent.ai_service import AIService
from aigent.api_manager import APIManager
from aigent.models import AgentTraits, ProjectInfo
from aigent.aigent_swarm import AIGentSwarm
from aigent.agency_swarm.swarm import Swarm, Agency
from aigent.init_database import init_database

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ... [Keep all the existing thread classes] ...

class AIGentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("Initializing AIGentGUI")
        try:
            # Initialize the database
            init_database()
            logging.info("Database initialized successfully")

            self.api_manager = APIManager()
            self.ai_service = AIService()
            self.aigent_swarm = AIGentSwarm()
            self.swarm = Swarm()
            self.agency = Agency("MainAgency", "agent_descriptors.db")
            self.swarm.add_agency(self.agency)
            logging.info("Services initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing services: {str(e)}")
            QMessageBox.critical(self, "Initialization Error", f"Failed to initialize services: {str(e)}")
            raise
        self.initUI()
        logging.info("AIGentGUI initialized")

    def initUI(self):
<<<<<<< Updated upstream
        # ... [Keep the existing UI setup code] ...

    # ... [Keep all the existing methods] ...

    def create_gpt_agent(self):
        profession, ok = QInputDialog.getText(self, 'Create GPT Agent', 'Enter the profession for the new GPT agent:')
        if ok and profession:
            try:
                new_agent = self.agency.create_gpt_agent(profession)
                QMessageBox.information(self, "Agent Created", f"New GPT agent created for profession: {profession}")
                logging.info(f"Created new GPT agent for profession: {profession}")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", f"An agent for the profession '{profession}' already exists.")
                logging.warning(f"Attempted to create duplicate agent for profession: {profession}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create GPT agent: {str(e)}")
                logging.error(f"Error creating GPT agent: {str(e)}")

    def list_gpt_agents(self):
        try:
            agents = self.agency.agents
            if not agents:
                QMessageBox.information(self, "GPT Agents", "No GPT agents have been created yet.")
            else:
                agent_list = "\n".join([str(agent) for agent in agents])
                QMessageBox.information(self, "GPT Agents", f"Current GPT Agents:\n\n{agent_list}")
            logging.info("Listed all GPT agents")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list GPT agents: {str(e)}")
            logging.error(f"Error listing GPT agents: {str(e)}")
=======
        self.setWindowTitle("AIGent: Intelligent Document Processor")
        self.setGeometry(100, 100, 600, 500)

        # Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        # Add "Generate Training Data" action
        generate_training_data_action = QAction('Generate Training Data', self)
        generate_training_data_action.triggered.connect(self.generate_training_data)
        file_menu.addAction(generate_training_data_action)

        # Add a new menu for GPT Agent operations
        agent_menu = menubar.addMenu('GPT Agents')

        # Add "Create GPT Agent" action
        create_agent_action = QAction('Create GPT Agent', self)
        create_agent_action.triggered.connect(self.create_gpt_agent)
        agent_menu.addAction(create_agent_action)

        # Add "List GPT Agents" action
        list_agents_action = QAction('List GPT Agents', self)
        list_agents_action.triggered.connect(self.list_gpt_agents)
        agent_menu.addAction(list_agents_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input file/directory selection
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit(self)
        input_file_button = QPushButton("Select Input Files", self)
        input_file_button.clicked.connect(self.select_input_files)
        input_dir_button = QPushButton("Select Input Directory", self)
        input_dir_button.clicked.connect(self.select_input_directory)
        input_layout.addWidget(QLabel("Input:"))
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_file_button)
        input_layout.addWidget(input_dir_button)
        layout.addLayout(input_layout)

        # Output directory selection
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit(self)
        output_button = QPushButton("Select Output Directory", self)
        output_button.clicked.connect(self.select_output_directory)
        output_layout.addWidget(QLabel("Output Directory:"))
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_button)
        layout.addLayout(output_layout)

        # Project Info
        self.project_title = QLineEdit(self)
        layout.addWidget(QLabel("Project Title:"))
        layout.addWidget(self.project_title)

        # Agent Traits
        self.data_purpose = QLineEdit(self)
        layout.addWidget(QLabel("Data Purpose:"))
        layout.addWidget(self.data_purpose)

        # AI Model Selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("AI Model:"))
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(["GPT-3.5", "GPT-4"])
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)

        # OCR options
        ocr_group = QGroupBox("OCR Options")
        ocr_layout = QVBoxLayout()
        self.use_ocr = QCheckBox("Use OCR for PDFs")
        self.use_ocr.setChecked(True)
        self.use_ocr.setToolTip("When checked, OCR will be used for PDFs. If unchecked, text will be extracted directly from the PDF.")
        self.use_cloud_vision = QCheckBox("Use Google Cloud Vision (when applicable)")
        self.use_cloud_vision.setToolTip("Use Google Cloud Vision for OCR when processing images or when OCR is enabled for PDFs.")
        ocr_layout.addWidget(self.use_ocr)
        ocr_layout.addWidget(self.use_cloud_vision)
        ocr_group.setLayout(ocr_layout)
        layout.addWidget(ocr_group)

        # Output format options
        format_group = QGroupBox("Output Formats")
        format_layout = QVBoxLayout()
        self.jsonl_checkbox = QCheckBox("JSONL")
        self.jsonl_checkbox.setChecked(True)
        self.jsonl_checkbox.setEnabled(False)  # JSONL is always selected
        self.txt_checkbox = QCheckBox("TXT")
        self.md_checkbox = QCheckBox("Markdown")
        self.docx_checkbox = QCheckBox("DOCX")
        format_layout.addWidget(self.jsonl_checkbox)
        format_layout.addWidget(self.txt_checkbox)
        format_layout.addWidget(self.md_checkbox)
        format_layout.addWidget(self.docx_checkbox)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Process button
        process_button = QPushButton("Process Documents", self)
        process_button.clicked.connect(self.process_documents)
        layout.addWidget(process_button)

    def select_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Input Files", "", "All Files (*)")
        if files:
            self.input_edit.setText(", ".join(files))

    def select_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if directory:
            self.input_edit.setText(directory)

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_edit.setText(directory)
>>>>>>> Stashed changes

    def create_gpt_agent(self):
        profession, ok = QInputDialog.getText(self, 'Create GPT Agent', 'Enter the profession for the new GPT agent:')
        if ok and profession:
            try:
                self.agency.create_gpt_agent(profession)
                QMessageBox.information(self, "Agent Created", f"New GPT agent created for profession: {profession}")
                logging.info(f"Created new GPT agent for profession: {profession}")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", f"An agent for the profession '{profession}' already exists.")
                logging.warning(f"Attempted to create duplicate agent for profession: {profession}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create GPT agent: {str(e)}")
                logging.error(f"Error creating GPT agent: {str(e)}")

    def list_gpt_agents(self):
        try:
            agents = self.agency.agents
            if not agents:
                QMessageBox.information(self, "GPT Agents", "No GPT agents have been created yet.")
            else:
                agent_list = "\n".join([str(agent) for agent in agents])
                QMessageBox.information(self, "GPT Agents", f"Current GPT Agents:\n\n{agent_list}")
            logging.info("Listed all GPT agents")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list GPT agents: {str(e)}")
            logging.error(f"Error listing GPT agents: {str(e)}")

    def process_documents(self):
<<<<<<< Updated upstream
        # ... [Keep the existing process_documents method] ...
        # Add the following lines at the end of the method:
        try:
            # Use GPT agents in document processing
            for agent in self.agency.agents:
                agent_result = agent.run({"task": "process_document", "document": "sample_text"})
=======
        logging.info("Starting document processing")
        input_path = self.input_edit.text()
        output_dir = self.output_edit.text()
        project_title = self.project_title.text()
        data_purpose = self.data_purpose.text()

        if not input_path or not output_dir or not project_title:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        input_files = []
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    input_files.append(os.path.join(root, file))
        else:
            input_files = input_path.split(", ")

        logging.debug(f"Input files: {input_files}")
        logging.debug(f"Output directory: {output_dir}")
        logging.debug(f"Project title: {project_title}")
        logging.debug(f"Data purpose: {data_purpose}")

        project_info = ProjectInfo(project_title=project_title)
        agent_traits = AgentTraits(data_purpose=data_purpose)

        output_formats = ["jsonl"]
        if self.txt_checkbox.isChecked():
            output_formats.append("txt")
        if self.md_checkbox.isChecked():
            output_formats.append("md")
        if self.docx_checkbox.isChecked():
            output_formats.append("docx")

        use_ocr = self.use_ocr.isChecked()
        use_cloud_vision = self.use_cloud_vision.isChecked()

        ai_model = self.model_combo.currentText()
        agent_traits.add_trait("ai_model", ai_model)

        self.processing_thread = ProcessingThread(
            self.aigent_swarm,
            input_files,
            output_dir,
            project_info,
            agent_traits,
            output_formats,
            use_ocr,
            use_cloud_vision
        )
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.processing_complete.connect(self.processing_finished)
        self.processing_thread.start()

        try:
            # Use GPT agents in document processing
            for agent in self.agency.agents:
                agent_result = agent.process({"task": "process_document", "document": "sample_text"})
>>>>>>> Stashed changes
                logging.info(f"GPT Agent {agent} processed document: {agent_result}")
        except Exception as e:
            QMessageBox.warning(self, "GPT Agent Processing Error", f"Error while using GPT agents: {str(e)}")
            logging.error(f"Error in GPT agent document processing: {str(e)}")
<<<<<<< Updated upstream
=======

    def generate_training_data(self):
        logging.info("Starting training data generation")
        input_path = self.input_edit.text()
        output_dir = self.output_edit.text()

        if not input_path or not output_dir:
            QMessageBox.warning(self, "Error", "Please select input files/directory and output directory.")
            return

        input_files = []
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    input_files.append(os.path.join(root, file))
        else:
            input_files = input_path.split(", ")

        logging.debug(f"Input files for training data: {input_files}")
        logging.debug(f"Output directory for training data: {output_dir}")

        self.training_data_thread = TrainingDataThread(
            self.aigent_swarm,
            input_files,
            output_dir
        )
        self.training_data_thread.progress_update.connect(self.update_progress)
        self.training_data_thread.processing_complete.connect(self.training_data_finished)
        self.training_data_thread.start()

    def update_progress(self, current, total):
        self.progress_bar.setValue(int((current / total) * 100))

    def processing_finished(self, results, errors):
        message = "Processing complete.\n\n"
        message += self.generate_summary(results)
        message += "\nOutput files:\n"
        for result in results:
            input_file = result['input_file']
            converted_data = result['converted_data']
            nlp_result = result['nlp_result']
            message += f"Processed {input_file}:\n"
            for format, file_path in converted_data.items():
                message += f"  {format.upper()}: {file_path}\n"
            message += f"  NLP Result: {nlp_result}\n"

        if errors:
            message += "\nErrors encountered:\n"
            for error_type, error_message in errors.items():
                message += f"Error in {error_type}: {error_message}\n"

        QMessageBox.information(self, "Processing Complete", message)
        logging.info("Document processing completed successfully")

        # Option to open output directory
        reply = QMessageBox.question(self, "Open Output Directory", 
                                     "Do you want to open the output directory?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.startfile(self.output_edit.text())

    def training_data_finished(self, results, errors):
        message = "Training data generation complete.\n\n"
        message += f"Total files processed: {len(results)}\n"
        message += "\nOutput files:\n"
        for result in results:
            input_file = result['input_file']
            output_dir = result['output_dir']
            message += f"Processed {input_file}:\n"
            message += f"  Output directory: {output_dir}\n"
            message += "  Generated files:\n"
            message += "    pc_training_data.jsonl\n"
            message += "    qa_training_data.jsonl\n"

        if errors:
            message += "\nErrors encountered:\n"
            for error_type, error_message in errors.items():
                message += f"Error in {error_type}: {error_message}\n"

        QMessageBox.information(self, "Training Data Generation Complete", message)
        logging.info("Training data generation completed successfully")

        # Option to open output directory
        reply = QMessageBox.question(self, "Open Output Directory", 
                                     "Do you want to open the output directory?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.startfile(self.output_edit.text())

    def generate_summary(self, results):
        total_files = len(results)
        total_pages = sum(len(result['converted_data']) for result in results)
        
        summary = f"Total files processed: {total_files}\n"
        summary += f"Total pages processed: {total_pages}\n"
        
        return summary
>>>>>>> Stashed changes

def main():
    logging.info("Starting main application")
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()