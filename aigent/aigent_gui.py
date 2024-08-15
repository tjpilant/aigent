# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: GUI for the AIGent application
# Version: 0.4.0

import os
import sys

from PyQt5.QtCore import Qt
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
    QProgressDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .ai_service import AIService
from .api_manager import APIManager
from .file_converter import AgentTraits, FileConverter, ProjectInfo
from .image_converter import ImageConverter


class AIGentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_manager = APIManager()
        self.ai_service = AIService()
        self.file_converter = FileConverter()
        self.image_converter = ImageConverter()
        self.initUI()

    def initUI(self):
        # ... [previous UI setup code] ...

        # OCR options
        ocr_group = QGroupBox("OCR Options")
        ocr_layout = QVBoxLayout()
        self.use_ocr = QCheckBox("Use OCR")
        self.use_ocr.setChecked(True)
        self.ocr_method = QComboBox()
        self.ocr_method.addItems(["Google Cloud Vision", "Tesseract"])
        ocr_layout.addWidget(self.use_ocr)
        ocr_layout.addWidget(QLabel("OCR Method:"))
        ocr_layout.addWidget(self.ocr_method)
        ocr_group.setLayout(ocr_layout)
        layout.addWidget(ocr_group)

        # ... [rest of the UI setup code] ...

    def process_documents(self):
        # ... [previous processing code] ...

        use_cloud_vision = self.ocr_method.currentText() == "Google Cloud Vision"
        self.image_converter.set_ocr_method(use_cloud_vision)

        # ... [rest of the processing code] ...


# ... [rest of the class implementation] ...
