import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QSpinBox, QComboBox
from pdf_converter import ProjectInfo, AgentTraits, start_conversion, split_large_pdf, load_config, save_config

class AIGentGUI(QMainWindow):
    """
    Main GUI class for the AIGent PDF to JSONL converter.
    This class creates the main window and handles user interactions.
    """
    def __init__(self):
        super().__init__()
        self.config = load_config('config.json')  # Specify the config file name
        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle('AIGent: PDF to JSONL Converter')
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input file selection
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit(self)
        input_button = QPushButton('Select Input File', self)
        input_button.clicked.connect(self.select_input_file)
        input_layout.addWidget(QLabel('Input File:'))
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_button)
        layout.addLayout(input_layout)

        # Output folder and file selection
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit(self)
        output_folder_button = QPushButton('Select Output Folder', self)
        output_folder_button.clicked.connect(self.select_output_folder)
        output_layout.addWidget(QLabel('Output File:'))
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_folder_button)
        layout.addLayout(output_layout)

        # Project Info
        self.project_title = QLineEdit(self.config.get('project_title', ''))
        layout.addWidget(QLabel('Project Title:'))
        layout.addWidget(self.project_title)

        # Agent Traits
        self.data_purpose = QLineEdit(self.config.get('data_purpose', ''))
        layout.addWidget(QLabel('Data Purpose:'))
        layout.addWidget(self.data_purpose)

        # Large PDF handling
        self.pages_per_file = QSpinBox(self)
        self.pages_per_file.setMinimum(1)
        self.pages_per_file.setMaximum(1000)
        self.pages_per_file.setValue(self.config.get('pages_per_file', 500))
        layout.addWidget(QLabel('Pages per file:'))
        layout.addWidget(self.pages_per_file)

        self.output_format = QComboBox(self)
        self.output_format.addItems(['JSONL', 'PDF'])
        self.output_format.setCurrentText(self.config.get('output_format', 'JSONL'))
        layout.addWidget(QLabel('Output format:'))
        layout.addWidget(self.output_format)

        # Convert buttons
        convert_button = QPushButton('Convert PDF to JSONL', self)
        convert_button.clicked.connect(self.convert_pdf)
        layout.addWidget(convert_button)

        process_large_button = QPushButton('Process Large PDF', self)
        process_large_button.clicked.connect(self.process_large_pdf)
        layout.addWidget(process_large_button)

    def select_input_file(self):
        """
        Open a file dialog for selecting the input PDF file.
        Also generates a default output filename based on the input file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Input PDF File", 
            "", 
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )
        if file:
            self.input_edit.setText(file)
            # Automatically generate output filename
            input_filename = os.path.basename(file)
            output_filename = os.path.splitext(input_filename)[0] + '.jsonl'
            self.output_edit.setText(output_filename)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            current_filename = os.path.basename(self.output_edit.text())
            full_path = os.path.join(folder, current_filename)
            self.output_edit.setText(full_path)

    def validate_inputs(self):
        if not self.input_edit.text():
            QMessageBox.warning(self, "Error", "Please select an input file.")
            return False
        if not self.output_edit.text():
            QMessageBox.warning(self, "Error", "Please specify an output file.")
            return False
        if not self.project_title.text():
            QMessageBox.warning(self, "Error", "Please enter a project title.")
            return False
        return True

    def convert_pdf(self):
        if not self.validate_inputs():
            return
        
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()
        project_title = self.project_title.text()
        data_purpose = self.data_purpose.text()

        project_info = ProjectInfo(project_title=project_title)
        agent_traits = AgentTraits(data_purpose=data_purpose)

        try:
            start_conversion(input_file, output_file, project_info, agent_traits)
            QMessageBox.information(self, "Success", f"Conversion complete. Output saved to {output_file}")
            
            # Update and save config
            self.config.update({
                'project_title': project_title,
                'data_purpose': data_purpose,
            })
            save_config(self.config, 'config.json')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during conversion: {str(e)}")

    def process_large_pdf(self):
        if not self.validate_inputs():
            return
        
        input_file = self.input_edit.text()
        output_prefix = os.path.splitext(self.output_edit.text())[0]
        project_title = self.project_title.text()
        data_purpose = self.data_purpose.text()
        pages_per_file = self.pages_per_file.value()
        output_format = self.output_format.currentText().lower()

        project_info = ProjectInfo(project_title=project_title)
        agent_traits = AgentTraits(data_purpose=data_purpose)

        try:
            split_large_pdf(input_file, output_prefix, pages_per_file, output_format, project_info, agent_traits)
            QMessageBox.information(self, "Success", f"Large PDF processed. Output files saved with prefix: {output_prefix}")
            
            # Update and save config
            self.config.update({
                'project_title': project_title,
                'data_purpose': data_purpose,
                'pages_per_file': pages_per_file,
                'output_format': output_format,
            })
            save_config(self.config, 'config.json')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during processing: {str(e)}")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()