import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import jwt from 'jsonwebtoken';

const OCR_RESULTS_DIR = process.env.OCR_RESULTS_DIR || path.join(process.cwd(), '..', 'ocr-results');
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Make sure to set this in production

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { token } = req.query;

  if (!token || typeof token !== 'string') {
    return res.status(400).json({ error: 'Invalid token' });
  }

  try {
    const filename = validateToken(token);
    const filePath = path.join(OCR_RESULTS_DIR, filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    const fileContent = await fs.promises.readFile(filePath, 'utf8');
    res.setHeader('Content-Type', 'text/markdown');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.send(fileContent);
  } catch (error) {
    console.error('Error serving OCR result:', error);
    res.status(500).json({ error: 'Error serving OCR result' });
  }
}

function validateToken(token: string): string {
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { filename: string };
    return decoded.filename;
  } catch (error) {
    throw new Error('Invalid token');
  }
}
