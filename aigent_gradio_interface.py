import os

import gradio as gr

from pdf_converter import AgentTraits, ProjectInfo, start_conversion


def update_output_file(input_file, output_dir):
    if input_file and output_dir:
        input_filename = os.path.basename(input_file.name)
        output_filename = os.path.splitext(input_filename)[0] + '.jsonl'
        return os.path.normpath(os.path.join(output_dir, output_filename))
    return ""

def convert_pdf(input_file, output_dir, project_title, data_purpose):
    if not input_file or not output_dir or not project_title:
        return "Error: Please fill in all required fields."
    
    # Normalize the output directory path
    output_dir = os.path.normpath(output_dir)
    
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the input filename and create the output filename
    input_filename = os.path.basename(input_file.name)
    output_filename = os.path.splitext(input_filename)[0] + '.jsonl'
    
    # Combine the output directory and filename
    output_file = os.path.normpath(os.path.join(output_dir, output_filename))
    
    project_info = ProjectInfo(project_title=project_title)
    agent_traits = AgentTraits(data_purpose=data_purpose)

    try:
        # Ensure the input file exists
        if not os.path.exists(input_file.name):
            return f"Error: Input file not found: {input_file.name}"
        
        start_conversion(input_file.name, output_file, project_info, agent_traits)
        
        # Check if the output file was created
        if os.path.exists(output_file):
            return f"Conversion complete. Output saved to {output_file}"
        else:
            return f"Error: Output file was not created at {output_file}"
    except PermissionError:
        return f"Error: Permission denied. Unable to write to {output_dir}"
    except Exception as e:
        return f"An error occurred during conversion: {str(e)}"

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# AIGent: PDF to JSONL Converter")
    
    input_file = gr.File(label="Select Input PDF File")
    output_dir = gr.Textbox(label="Output Directory", placeholder="Enter the full path to the output directory")
    output_file = gr.Textbox(label="Output File (auto-generated)", interactive=False)
    
    project_title = gr.Textbox(label="Project Title")
    data_purpose = gr.Textbox(label="Data Purpose")
    
    convert_btn = gr.Button("Convert PDF to JSONL")
    
    result = gr.Textbox(label="Result")
    
    input_file.change(update_output_file, inputs=[input_file, output_dir], outputs=output_file)
    output_dir.change(update_output_file, inputs=[input_file, output_dir], outputs=output_file)
    convert_btn.click(convert_pdf, inputs=[input_file, output_dir, project_title, data_purpose], outputs=result)

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(share=True)