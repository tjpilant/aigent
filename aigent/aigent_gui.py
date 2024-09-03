# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: GUI for the AIGent application
# Version: 0.6.2

import logging
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from aigent.ai_service import AIService
from aigent.api_manager import APIManager
from aigent.file_converter import FileConverter
from aigent.models import AgentTraits, ProjectInfo

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AIGentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("Initializing AIGentGUI")
        try:
            self.api_manager = APIManager()
            self.ai_service = AIService()
            self.file_converter = FileConverter()
            logging.info("Services initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing services: {str(e)}")
            raise
        self.initUI()
        logging.info("AIGentGUI initialized")

    def initUI(self):
        self.setWindowTitle("AIGent: Intelligent Document Processor")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input file selection
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit(self)
        input_button = QPushButton("Select Input Files", self)
        input_button.clicked.connect(self.select_input_files)
        input_layout.addWidget(QLabel("Input Files:"))
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_button)
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

        # OCR options
        ocr_group = QGroupBox("OCR Options")
        ocr_layout = QVBoxLayout()
        self.use_ocr = QCheckBox("Use OCR")
        self.use_ocr.setChecked(True)
        self.use_cloud_vision = QCheckBox("Use Google Cloud Vision (when applicable)")
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

        # Process button
        process_button = QPushButton("Process Documents", self)
        process_button.clicked.connect(self.process_documents)
        layout.addWidget(process_button)

    def select_input_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Input Files", "", "All Files (*)")
        if files:
            if len(files) > 10:
                QMessageBox.warning(self, "Warning", "Maximum 10 files can be selected for batch processing. Only the first 10 files will be processed.")
                files = files[:10]
            self.input_edit.setText(", ".join(files))

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_edit.setText(directory)

    def process_documents(self):
        logging.info("Starting document processing")
        input_files = self.input_edit.text().split(", ")
        output_dir = self.output_edit.text()
        project_title = self.project_title.text()
        data_purpose = self.data_purpose.text()

        logging.debug(f"Input files: {input_files}")
        logging.debug(f"Output directory: {output_dir}")
        logging.debug(f"Project title: {project_title}")
        logging.debug(f"Data purpose: {data_purpose}")

        if not input_files or not output_dir or not project_title:
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        project_info = ProjectInfo(project_title=project_title)
        agent_traits = AgentTraits(data_purpose=data_purpose)

        logging.debug(f"Created ProjectInfo: {project_info}")
        logging.debug(f"Type of ProjectInfo: {type(project_info)}")
        logging.debug(f"Created AgentTraits: {agent_traits}")
        logging.debug(f"Type of AgentTraits: {type(agent_traits)}")

        output_formats = ["jsonl"]
        if self.txt_checkbox.isChecked():
            output_formats.append("txt")
        if self.md_checkbox.isChecked():
            output_formats.append("md")
        if self.docx_checkbox.isChecked():
            output_formats.append("docx")

        logging.debug(f"Output formats: {output_formats}")

        use_ocr = self.use_ocr.isChecked()
        use_cloud_vision = self.use_cloud_vision.isChecked()

        logging.debug(f"Use OCR: {use_ocr}")
        logging.debug(f"Use Cloud Vision: {use_cloud_vision}")

        try:
            progress = QProgressDialog("Processing documents...", "Cancel", 0, len(input_files), self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()

            logging.info(f"Calling batch_convert_files with {len(input_files)} files")
            results, errors = self.file_converter.batch_convert_files(
                input_files,
                output_dir,
                project_info,
                agent_traits,
                output_formats=output_formats,
                use_ocr=use_ocr,
                use_cloud_vision=use_cloud_vision
            )

            progress.close()

            message = "Processing complete. Output files:\n"
            for input_file, output_files in results.items():
                message += f"Processed {input_file}:\n"
                for format, file_path in output_files.items():
                    message += f"  {format.upper()}: {file_path}\n"

            if errors:
                message += "\nErrors encountered:\n"
                for input_file, error in errors.items():
                    message += f"Error processing {input_file}: {error}\n"

            QMessageBox.information(self, "Success", message)
            logging.info("Document processing completed successfully")
        except Exception as e:
            logging.error(f"Error during document processing: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Error", f"An error occurred during processing: {str(e)}")

def main():
    logging.info("Starting main application")
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()