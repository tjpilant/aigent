import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const OCR_RESULTS_DIR = process.env.OCR_RESULTS_DIR || path.join(process.cwd(), '..', 'ocr-results');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { filename } = req.query;

  if (!filename || typeof filename !== 'string') {
    return res.status(400).json({ error: 'Invalid filename' });
  }

  try {
    // Prevent directory traversal
    const sanitizedFilename = path.basename(filename);
    const filePath = path.join(OCR_RESULTS_DIR, sanitizedFilename);

    // Check if file exists and is within the OCR_RESULTS_DIR
    if (!fs.existsSync(filePath) || !filePath.startsWith(OCR_RESULTS_DIR)) {
      return res.status(404).json({ error: 'File not found' });
    }

    const fileContent = await fs.promises.readFile(filePath, 'utf8');
    res.setHeader('Content-Type', 'text/markdown');
    res.setHeader('Content-Disposition', `attachment; filename="${sanitizedFilename}"`);
    res.send(fileContent);
  } catch (error) {
    console.error('Error serving OCR result:', error);
    res.status(500).json({ error: 'Error serving OCR result' });
  }
}
