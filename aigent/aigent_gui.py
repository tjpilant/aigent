# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: GUI for the AIGent application
# Version: 0.9.4

import logging
import os
import sys
import sqlite3
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
    QMenuBar,
    QMenu,
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

    def process_documents(self):
        # ... [Keep the existing process_documents method] ...
        # Add the following lines at the end of the method:
        try:
            # Use GPT agents in document processing
            for agent in self.agency.agents:
                agent_result = agent.run({"task": "process_document", "document": "sample_text"})
                logging.info(f"GPT Agent {agent} processed document: {agent_result}")
        except Exception as e:
            QMessageBox.warning(self, "GPT Agent Processing Error", f"Error while using GPT agents: {str(e)}")
            logging.error(f"Error in GPT agent document processing: {str(e)}")

def main():
    logging.info("Starting main application")
    app = QApplication(sys.argv)
    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()