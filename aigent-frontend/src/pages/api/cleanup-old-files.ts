import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const OCR_RESULTS_DIR = process.env.OCR_RESULTS_DIR || path.join(process.cwd(), '..', 'ocr-results');
const UPLOADS_DIR = path.join(process.cwd(), '..', 'uploads');
const MAX_AGE_DAYS = 7; // Files older than this will be deleted

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const secretKey = process.env.CLEANUP_SECRET_KEY;
  const providedKey = req.headers['x-cleanup-key'];

  if (!secretKey || providedKey !== secretKey) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const deletedFiles = [
      ...await cleanupDirectory(OCR_RESULTS_DIR),
      ...await cleanupDirectory(UPLOADS_DIR)
    ];

    res.status(200).json({ message: 'Cleanup completed', deletedFiles });
  } catch (error) {
    console.error('Error during cleanup:', error);
    res.status(500).json({ error: 'Error during cleanup' });
  }
}

async function cleanupDirectory(directory: string): Promise<string[]> {
  const now = new Date();
  const deletedFiles: string[] = [];

  const files = await fs.promises.readdir(directory);

  for (const file of files) {
    const filePath = path.join(directory, file);
    const stats = await fs.promises.stat(filePath);

    if (stats.isFile()) {
      const ageInDays = (now.getTime() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24);

      if (ageInDays > MAX_AGE_DAYS) {
        await fs.promises.unlink(filePath);
        deletedFiles.push(filePath);
      }
    }
  }

  return deletedFiles;
}
