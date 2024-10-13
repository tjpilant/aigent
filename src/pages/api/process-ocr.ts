import type { NextApiRequest, NextApiResponse } from 'next';
import { IncomingForm, File } from 'formidable';
import fs from 'fs';
import path from 'path';
import jwt from 'jsonwebtoken';
import { GoogleCloudVisionOCRTool } from '../../tools/GoogleCloudVisionOCRTool';

export const config = {
  api: {
    bodyParser: false,
  },
};

const OCR_RESULTS_DIR = process.env.OCR_RESULTS_DIR || path.join(process.cwd(), '..', 'ocr-results');
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Make sure to set this in production

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('OCR processing started');

  if (req.method !== 'POST') {
    console.log('Invalid method:', req.method);
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const uploadDir = path.join(process.cwd(), '..', 'uploads');
  
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

    const ocrMethod = Array.isArray(fields.ocrMethod) ? fields.ocrMethod[0] : fields.ocrMethod;
    const file = Array.isArray(files.file) ? files.file[0] : files.file;

    if (!file || !ocrMethod) {
      console.log('Missing required fields');
      return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
      if (ocrMethod === 'google') {
        console.log('Processing file:', file.originalFilename);
        const inputFilePath = file.filepath;
        const originalFileName = file.originalFilename || 'unnamed';
        const outputFileName = `${path.parse(originalFileName).name}_ocr_result.md`;
        const outputFilePath = path.join(OCR_RESULTS_DIR, outputFileName);

        // Use GitHub secrets for credentials
        const credentials = process.env.GOOGLE_APPLICATION_CREDENTIALS;
        const projectId = process.env.GOOGLE_CLOUD_PROJECT_ID;
        const processorId = process.env.GOOGLE_CLOUD_PROCESSOR_ID;

        if (!credentials || !projectId || !processorId) {
          throw new Error('Missing Google Cloud credentials or configuration');
        }

        const ocrTool = new GoogleCloudVisionOCRTool({
          input_file_path: inputFilePath,
          output_md_file_path: outputFilePath,
          credentials_json: JSON.parse(credentials),
          processor_id: processorId,
          project_id: projectId,
        });

        await ocrTool.run();
        console.log('OCR processing completed for:', originalFileName);
        
        // Clean up the uploaded file
        fs.unlinkSync(inputFilePath);

        // Generate a token for secure file access
        const token = generateToken(outputFileName);

        res.status(200).json({ 
          result: `OCR processing complete for ${originalFileName}`,
          fileToken: token,
          originalFilename: originalFileName
        });
      } else if (ocrMethod === 'tesseract') {
        console.log('Tesseract OCR not implemented for:', file.originalFilename);
        res.status(200).json({ 
          result: `Tesseract OCR not yet implemented for ${file.originalFilename}`,
          fileToken: '',
          originalFilename: file.originalFilename || 'unnamed'
        });
      } else {
        console.log('Invalid OCR method');
        throw new Error('Invalid OCR method');
      }
    } catch (error) {
      console.error('Error processing OCR:', error);
      if (error instanceof Error && error.message.includes('Document exceeds the 15-page limit')) {
        res.status(400).json({ error: 'The document exceeds the 15-page limit for OCR processing. Please upload a smaller document.' });
      } else {
        res.status(500).json({ error: 'Error processing OCR: ' + (error instanceof Error ? error.message : String(error)) });
      }
    }
  });
}

function generateToken(filename: string): string {
  return jwt.sign({ filename }, JWT_SECRET, { expiresIn: '1h' });
}
