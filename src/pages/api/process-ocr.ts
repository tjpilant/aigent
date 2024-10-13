import type { NextApiRequest, NextApiResponse } from 'next';
import { IncomingForm, File } from 'formidable';
import fs from 'fs';
import path from 'path';
import { GoogleCloudVisionOCRTool } from '../../tools/GoogleCloudVisionOCRTool';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('OCR processing started');

  if (req.method !== 'POST') {
    console.log('Invalid method:', req.method);
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const uploadDir = path.join(process.cwd(), 'uploads');
  const outputDir = path.join(process.cwd(), 'public', 'ocr-results');
  
  // Create directories if they don't exist
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
  }
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const form = new IncomingForm({
    uploadDir: uploadDir,
    keepExtensions: true,
    multiples: true,
  });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error('Error parsing form:', err);
      return res.status(500).json({ error: 'Error processing file upload' });
    }

    console.log('Fields:', fields);
    console.log('Files:', files);

    const ocrMethod = Array.isArray(fields.ocrMethod) ? fields.ocrMethod[0] : fields.ocrMethod;

    if (!files || !ocrMethod) {
      console.log('Missing required fields');
      return res.status(400).json({ error: 'Missing required fields' });
    }

    try {
      const results: string[] = [];
      const downloadUrls: string[] = [];
      const originalFilenames: string[] = [];

      const fileArray = Object.values(files).flat();
      console.log('Number of files to process:', fileArray.length);

      for (const file of fileArray) {
        if (file && ocrMethod === 'google') {
          console.log('Processing file:', file.originalFilename);
          const inputFilePath = file.filepath;
          const originalFileName = file.originalFilename || 'unnamed';
          const outputFileName = `${path.parse(originalFileName).name}_ocr_result.md`;
          const outputFilePath = path.join(outputDir, outputFileName);

          // Use the credentials file directly
          const credentialsPath = '/home/tjpilant/aiengineers/aigent/aiocr-gcv-api.json';
          
          if (!fs.existsSync(credentialsPath)) {
            throw new Error('Google Cloud credentials file not found');
          }

          const credentialsContent = fs.readFileSync(credentialsPath, 'utf8');
          const credentialsJson = JSON.parse(credentialsContent);

          if (!credentialsJson.client_email) {
            throw new Error('Invalid Google Cloud credentials: missing client_email');
          }

          const projectId = credentialsJson.project_id;
          const processorId = "cdbb7ba4f9c316d0";

          if (!projectId) {
            throw new Error('Google Cloud project ID not found in credentials');
          }

          const ocrTool = new GoogleCloudVisionOCRTool({
            input_file_path: inputFilePath,
            output_md_file_path: outputFilePath,
            credentials_json: credentialsJson,
            processor_id: processorId,
            project_id: projectId,
          });

          await ocrTool.run();
          console.log('OCR processing completed for:', originalFileName);
          
          // Clean up the uploaded file
          fs.unlinkSync(inputFilePath);

          // Generate download URL
          const downloadUrl = `/ocr-results/${outputFileName}`;

          results.push(`OCR processing complete for ${originalFileName}`);
          downloadUrls.push(downloadUrl);
          originalFilenames.push(originalFileName);
        } else if (file && ocrMethod === 'tesseract') {
          // TODO: Implement Tesseract OCR processing
          console.log('Tesseract OCR not implemented for:', file.originalFilename);
          results.push(`Tesseract OCR not yet implemented for ${file.originalFilename}`);
          downloadUrls.push('');
          originalFilenames.push(file.originalFilename || 'unnamed');
        } else {
          console.log('Invalid OCR method or file');
          throw new Error('Invalid OCR method or file');
        }
      }

      console.log('OCR processing completed for all files');
      res.status(200).json({ results, downloadUrls, originalFilenames });
    } catch (error) {
      console.error('Error processing OCR:', error);
      if (error instanceof Error && error.message.includes('Document exceeds the 15-page limit')) {
        res.status(400).json({ error: 'One or more documents exceed the 15-page limit for OCR processing. Please upload smaller documents.' });
      } else {
        res.status(500).json({ error: 'Error processing OCR: ' + (error instanceof Error ? error.message : String(error)) });
      }
    }
  });
}
