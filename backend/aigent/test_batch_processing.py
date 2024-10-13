# File: test_batch_processing.py
# Author: Tj Pilant
# Description: Unit tests for batch processing functionality in AIGENT
# Version: 0.1.1

import os
import shutil
import tempfile
import unittest

from .file_converter import FileConverter
from .models import AgentTraits, ProjectInfo
from .utils.logger import get_logger

logger = get_logger(__name__)

class TestBatchProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_converter = FileConverter()
        self.project_info = ProjectInfo(project_title="Test Project")
        self.agent_traits = AgentTraits(data_purpose="Test Purpose")
        logger.info(f"Set up test environment in {self.temp_dir}")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        logger.info(f"Cleaned up test environment in {self.temp_dir}")

    def create_test_file(self, filename, content):
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        logger.debug(f"Created test file: {filepath}")
        return filepath

    def test_batch_convert_files(self):
        logger.info("Starting test_batch_convert_files")
        # Create test files
        file1 = self.create_test_file("test1.txt", "Test content 1")
        file2 = self.create_test_file("test2.txt", "Test content 2")
        file3 = self.create_test_file("test3.txt", "Test content 3")

        input_files = [file1, file2, file3]
        output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Perform batch conversion
        results = self.file_converter.batch_convert_files(
            input_files,
            output_dir,
            self.project_info,
            self.agent_traits,
            output_formats=["jsonl", "txt"],
        )

        # Check results
        self.assertEqual(len(results), 3)
        for input_file in input_files:
            self.assertIn(input_file, results)
            self.assertIsInstance(results[input_file], dict)
            self.assertIn("jsonl", results[input_file])
            self.assertIn("txt", results[input_file])

            # Check if output files exist
            self.assertTrue(os.path.exists(results[input_file]["jsonl"]))
            self.assertTrue(os.path.exists(results[input_file]["txt"]))

        logger.info("test_batch_convert_files completed successfully")

    def test_batch_convert_files_with_error(self):
        logger.info("Starting test_batch_convert_files_with_error")
        # Create test files
        file1 = self.create_test_file("test1.txt", "Test content 1")
        file2 = "non_existent_file.txt"  # This file doesn't exist
        file3 = self.create_test_file("test3.txt", "Test content 3")

        input_files = [file1, file2, file3]
        output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Perform batch conversion
        results = self.file_converter.batch_convert_files(
            input_files,
            output_dir,
            self.project_info,
            self.agent_traits,
            output_formats=["jsonl", "txt"],
        )

        # Check results
        self.assertEqual(len(results), 3)
        self.assertIn(file1, results)
        self.assertIn(file2, results)
        self.assertIn(file3, results)

        # Check if file1 and file3 were processed successfully
        self.assertIsInstance(results[file1], dict)
        self.assertIsInstance(results[file3], dict)

        # Check if file2 resulted in an error
        self.assertIsInstance(results[file2], str)
        self.assertIn("Error", results[file2])

        logger.info("test_batch_convert_files_with_error completed successfully")


if __name__ == "__main__":
    unittest.main()
