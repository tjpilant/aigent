import { Tool } from './Tool';
import fs from 'fs/promises';
import sharp from 'sharp';
import { createWorker } from 'tesseract.js';
import pdfParse from 'pdf-parse';

export class TesseractOCRTool implements Tool {
  name = 'TesseractOCRTool';
  description = 'Performs OCR on images and PDFs using Tesseract.js';

  async run(): Promise<string> {
    return "TesseractOCRTool run method called";
  }

  async processFile(inputFilePath: string, outputFilePath: string): Promise<string> {
    try {
      let text: string;

      if (inputFilePath.toLowerCase().endsWith('.pdf')) {
        text = await this.processPdf(inputFilePath);
      } else {
        text = await this.processImage(inputFilePath);
      }

      await this.saveAsMarkdown(text, outputFilePath);
      return `Markdown file created at: ${outputFilePath}`;
    } catch (error) {
      console.error(`Error in TesseractOCRTool: ${error}`);
      throw error;
    }
  }

  private async processPdf(filePath: string): Promise<string> {
    try {
      console.log(`Processing PDF: ${filePath}`);
      const dataBuffer = await fs.readFile(filePath);
      console.log(`PDF file read, size: ${dataBuffer.length} bytes`);
      const data = await pdfParse(dataBuffer);
      console.log(`PDF parsed, extracted text length: ${data.text.length}`);
      return data.text;
    } catch (error: unknown) {
      console.error(`Error processing PDF: ${error}`);
      if (error instanceof Error) {
        throw new Error(`Failed to process PDF: ${error.message}`);
      } else {
        throw new Error(`Failed to process PDF: Unknown error`);
      }
    }
  }

  private async processImage(filePath: string): Promise<string> {
    try {
      console.log(`Processing image: ${filePath}`);
      // Convert image to PNG using sharp
      const pngBuffer = await sharp(filePath).png().toBuffer();
      console.log(`Image converted to PNG, size: ${pngBuffer.length} bytes`);

      const worker = await createWorker('eng');
      const { data: { text } } = await worker.recognize(pngBuffer);
      await worker.terminate();

      console.log(`OCR completed, extracted text length: ${text.length}`);
      return text;
    } catch (error: unknown) {
      console.error(`Error processing image: ${error}`);
      if (error instanceof Error) {
        throw new Error(`Failed to process image: ${error.message}`);
      } else {
        throw new Error(`Failed to process image: Unknown error`);
      }
    }
  }

  private async saveAsMarkdown(text: string, outputPath: string): Promise<void> {
    const markdown = `# OCR Extracted Text\n\n${text}`;
    await fs.writeFile(outputPath, markdown);
    console.log(`Markdown file saved at: ${outputPath}`);
  }
}
