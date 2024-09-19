# File: aigent/aigent_gui.py
# Author: Tj Pilant
# Description: Web GUI for the AIGent application
# Version: 1.1.7

import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename

from aigent.ai_service import AIService
from aigent.api_manager import APIManager
from aigent.aigent_swarm import AIGentSwarm
from aigent.agency_swarm.swarm import Swarm, Agency
from aigent.init_database import init_database

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'
BASE_OUTPUT_DIR = os.environ.get('BASE_OUTPUT_DIR', '/safe/output/directory')

# Ensure the UPLOAD_FOLDER exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class ProcessingForm(FlaskForm):
    input_files = MultipleFileField('Select Input Files', validators=[DataRequired()])
    output_directory = StringField('Output Directory', validators=[DataRequired()])
    submit = SubmitField('Process Files')

    def validate_output_directory(self, field):
        full_path = os.path.abspath(field.data)
        if not full_path.startswith(BASE_OUTPUT_DIR):
            raise ValidationError('Invalid output directory')
        if not os.path.isdir(full_path):
            raise ValidationError('Output directory does not exist')

    def validate_input_files(self, field):
        if not field.data:
            raise ValidationError('At least one file must be selected')


class AIGentGUI:
    def __init__(self):
        logging.info("AIGentGUI __init__ started")
        try:
            init_database()
            logging.info("Database initialized successfully")

            self.api_manager = APIManager()
            self.ai_service = AIService()
            self.aigent_swarm = AIGentSwarm()
            self.swarm = Swarm()
            self.agency = Agency("MainAgency", "agent_descriptors.db")
            self.swarm.add_agency(self.agency)
            logging.info("Services initialized successfully")
        except (OSError, IOError) as e:
            logging.error("Error initializing services: %s", str(e))
            raise
        except Exception as e:
            logging.error("Unexpected error initializing services: %s", str(e))
            raise

        logging.info("AIGentGUI __init__ completed")

    def process_documents(self, file_paths):
        results = []
        for file_path in file_paths:
            try:
                # Process the document (implementation needed)
                result = f"Processed {file_path}"
                results.append(result)
                logging.info(result)
            except (FileNotFoundError, PermissionError) as e:
                error_msg = f"Error accessing {file_path}: {str(e)}"
                results.append(error_msg)
                logging.error(error_msg)
            except (IOError, ValueError) as e:
                error_msg = f"Error processing {file_path}: {str(e)}"
                results.append(error_msg)
                logging.error(error_msg)
        return results

    def create_gpt_agent(self, profession):
        return self.agency.create_gpt_agent(profession)

    def get_gpt_agents(self):
        return self.agency.get_gpt_agents()


aigent_gui = AIGentGUI()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ProcessingForm()
    if form.validate_on_submit():
        input_files = request.files.getlist('input_files')
        output_directory = form.output_directory.data

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Save uploaded files
        file_paths = []
        for file in input_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_paths.append(file_path)

        # Process files
        try:
            results = aigent_gui.process_documents(file_paths)
        except (IOError, ValueError, FileNotFoundError, PermissionError) as e:
            logging.error("Error processing documents: %s", str(e))
            results = [f"Error processing documents: {str(e)}"]
        except Exception as e:
            logging.exception("Unexpected error during processing: %s", str(e))
            results = ["An unexpected error occurred during processing"]

        return render_template('results.html', results=results)

    return render_template('index.html', form=form)


@app.route('/create_gpt_agent', methods=['POST'])
def create_gpt_agent():
    profession = request.json.get('profession')
    if not profession:
        return jsonify({"error": "No profession provided"}), 400

    try:
        aigent_gui.create_gpt_agent(profession)
        return jsonify({
            "message": f"New GPT agent created for profession: {profession}"
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (IOError, RuntimeError) as e:
        logging.error("Error creating GPT agent: %s", str(e))
        return jsonify({"error": f"Error creating GPT agent: {str(e)}"}), 500
    except Exception as e:
        logging.exception("Unexpected error creating GPT agent: %s", str(e))
        return jsonify({
            "error": "An unexpected error occurred while creating the agent"
        }), 500


@app.route('/list_gpt_agents', methods=['GET'])
def list_gpt_agents():
    try:
        agents = aigent_gui.get_gpt_agents()
        agent_list = [str(agent) for agent in agents]
        return jsonify({"agents": agent_list}), 200
    except (IOError, ValueError) as e:
        logging.error("Error listing GPT agents: %s", str(e))
        return jsonify({"error": f"Error listing GPT agents: {str(e)}"}), 500
    except Exception as e:
        logging.exception("Unexpected error listing GPT agents: %s", str(e))
        return jsonify({"error": "An unexpected error occurred while listing agents"}), 500


def main():
    logging.info("Starting main application")
    app.run(debug=False, host='0.0.0.0')


if __name__ == "__main__":
    main()
    