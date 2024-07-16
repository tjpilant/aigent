import pytest
from pdf_converter import ProjectInfo, start_conversion

def test_project_info_creation():
    project_info = ProjectInfo(project_title="Test Project")
    assert project_info.project_title == "Test Project"

def test_start_conversion(tmp_path):
    # Create a dummy PDF file
    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.5")  # Minimal valid PDF content
    
    output_file = tmp_path / "output.jsonl"
    project_info = ProjectInfo(project_title="Test Project")
    
    start_conversion(str(dummy_pdf), str(output_file), project_info)
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "Test Project" in content