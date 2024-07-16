import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
from pdf_converter import ProjectInfo, start_conversion, load_config, save_config

class AIGentGUI(QMainWindow):
    """
    Main GUI class for the AIGent PDF to JSONL converter.
    This class creates the main window and handles user interactions.
    """
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle('AIGent: PDF to JSONL Converter')
        self.setGeometry(100, 100, 600, 400)

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
        self.project_title = QLineEdit(self)
        layout.addWidget(QLabel('Project Title:'))
        layout.addWidget(self.project_title)

        # Data Purpose (we'll keep this for now, but it's not used in conversion yet)
        self.data_purpose = QLineEdit(self)
        layout.addWidget(QLabel('Data Purpose:'))
        layout.addWidget(self.data_purpose)

        # Convert button
        convert_button = QPushButton('Convert PDF to JSONL', self)
        convert_button.clicked.connect(self.convert_pdf)
        layout.addWidget(convert_button)

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

    def convert_pdf(self):
        input_file = self.input_edit.text()
        output_file = self.output_edit.text()
        project_title = self.project_title.text()

        if not input_file or not output_file:
            QMessageBox.warning(self, "Error", "Please select both input file and output file.")
            return

        project_info = ProjectInfo(project_title=project_title)

        try:
            start_conversion(input_file, output_file, project_info)
            QMessageBox.information(self, "Success", f"Conversion complete. Output saved to {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during conversion: {str(e)}")

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()