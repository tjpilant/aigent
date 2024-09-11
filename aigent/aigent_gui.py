# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: GUI for the AIGent application
# Version: 0.7.1

import logging
import os
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
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
)

from aigent.ai_service import AIService
from aigent.api_manager import APIManager
from aigent.file_converter import FileConverter
from aigent.models import AgentTraits, ProjectInfo

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessingThread(QThread):
    progress_update = pyqtSignal(int, int)
    processing_complete = pyqtSignal(dict, dict)
    
    def __init__(self, file_converter, input_files, output_dir, project_info, agent_traits, output_formats, use_ocr, use_cloud_vision):
        super().__init__()
        self.file_converter = file_converter
        self.input_files = input_files
        self.output_dir = output_dir
        self.project_info = project_info
        self.agent_traits = agent_traits
        self.output_formats = output_formats
        self.use_ocr = use_ocr
        self.use_cloud_vision = use_cloud_vision

    def run(self):
        results = {}
        errors = {}
        total_files = len(self.input_files)
        
        for i, input_file in enumerate(self.input_files, 1):
            try:
                result = self.file_converter.convert_file(
                    input_file,
                    self.output_dir,
                    self.project_info,
                    self.agent_traits,
                    self.output_formats,
                    self.use_ocr,
                    self.use_cloud_vision
                )
                results[input_file] = result
            except Exception as e:
                errors[input_file] = str(e)
            
            self.progress_update.emit(i, total_files)
        
        self.processing_complete.emit(results, errors)

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
        self.setGeometry(100, 100, 600, 500)

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

    def process_documents(self):
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
            self.file_converter,
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

    def update_progress(self, current, total):
        self.progress_bar.setValue(int((current / total) * 100))

    def processing_finished(self, results, errors):
        message = "Processing complete.\n\n"
        message += self.generate_summary(results)
        message += "\nOutput files:\n"
        for input_file, output_files in results.items():
            message += f"Processed {input_file}:\n"
            for format, file_path in output_files.items():
                message += f"  {format.upper()}: {file_path}\n"

        if errors:
            message += "\nErrors encountered:\n"
            for input_file, error in errors.items():
                message += f"Error processing {input_file}: {error}\n"

        QMessageBox.information(self, "Processing Complete", message)
        logging.info("Document processing completed successfully")

        # Option to open output directory
        reply = QMessageBox.question(self, "Open Output Directory", 
                                     "Do you want to open the output directory?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.startfile(self.output_edit.text())

    def generate_summary(self, results):
        total_files = len(results)
        total_pages = sum(len(output_files) for output_files in results.values())
        
        summary = f"Total files processed: {total_files}\n"
        summary += f"Total pages processed: {total_pages}\n"
        
        return summary

def main():
    logging.info("Starting main application")
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()