import type { NextApiRequest, NextApiResponse } from 'next';
import { IncomingForm } from 'formidable';
import fs from 'fs';
import path from 'path';
import { TesseractOCRTool } from '../../tools/TesseractOCRTool';

export const config = {
  api: {
    bodyParser: false,
  },
};

const OCR_RESULTS_DIR = process.env.OCR_RESULTS_DIR || path.join(process.cwd(), '..', 'ocr-results');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('Tesseract OCR processing started');

  if (req.method !== 'POST') {
    console.log('Invalid method:', req.method);
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const uploadDir = path.join(process.cwd(), 'uploads');
  
  // Create directories if they don't exist
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
  }
  if (!fs.existsSync(OCR_RESULTS_DIR)) {
    fs.mkdirSync(OCR_RESULTS_DIR, { recursive: true });
  }

  const form = new IncomingForm({
    uploadDir: uploadDir,
    keepExtensions: true,
    multiples: false,
  });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error('Error parsing form:', err);
      return res.status(500).json({ error: 'Error processing file upload' });
    }

    console.log('Fields:', fields);
    console.log('Files:', files);

    const file = Array.isArray(files.file) ? files.file[0] : files.file;

    if (!file) {
      console.error('No file uploaded');
      return res.status(400).json({ error: 'No file uploaded' });
    }

    try {
      console.log('Processing file:', file.originalFilename);
      const outputFileName = `${path.parse(file.originalFilename || '').name}_ocr_result.md`;
      const outputFilePath = path.join(OCR_RESULTS_DIR, outputFileName);

      console.log('Output file path:', outputFilePath);

      const tesseractTool = new TesseractOCRTool();
      const result = await tesseractTool.processFile(file.filepath, outputFilePath);

      console.log('OCR result:', result);

      // Clean up the uploaded file
      fs.unlinkSync(file.filepath);

      const downloadUrl = `/api/serve-ocr-result?filename=${encodeURIComponent(outputFileName)}`;

      res.status(200).json({
        result: `OCR processing complete for ${file.originalFilename}`,
        downloadUrl,
        originalFilename: file.originalFilename || 'unnamed'
      });
    } catch (error: unknown) {
      console.error('Error processing OCR:', error);
      res.status(500).json({ error: 'Error processing OCR: ' + (error instanceof Error ? error.message : String(error)) });
    }
  });
}
