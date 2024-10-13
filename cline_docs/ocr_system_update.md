# OCR System Update Documentation

## Overview
This document outlines the changes made to improve the security and maintainability of the OCR system.

## Changes Implemented

1. **External File Storage**
   - OCR results and uploads are now stored outside the project directory.
   - New locations: `../ocr-results` and `../uploads` relative to the project root.

2. **Token-based File Access**
   - Implemented JWT for secure access to OCR result files.
   - Updated `process-ocr.ts` to generate tokens.
   - Created `serve-ocr-result.ts` to validate tokens and serve files.

3. **Frontend Updates**
   - Modified `data-file-creation.tsx` to use the new token-based system.

4. **File Cleanup Mechanism**
   - Created `cleanup-old-files.ts` to periodically remove old files.

5. **Security Enhancements**
   - Added `JWT_SECRET` for token encryption.
   - Implemented `CLEANUP_SECRET_KEY` for authenticating cleanup requests.

## New Environment Variables
- `OCR_RESULTS_DIR`: Path to OCR results directory
- `JWT_SECRET`: Secret key for JWT tokens
- `CLEANUP_SECRET_KEY`: Secret key for cleanup authentication

## Deployment Instructions
1. Set the above environment variables in the production environment.
2. Ensure the external directories (`ocr-results` and `uploads`) exist and have proper permissions.
3. Set up a daily cron job to call the cleanup API:
   ```
   curl -X POST -H "X-Cleanup-Key: YOUR_CLEANUP_SECRET_KEY" https://your-domain.com/api/cleanup-old-files
   ```

## Maintenance Tasks
- Regularly rotate `JWT_SECRET` and `CLEANUP_SECRET_KEY`.
- Monitor disk usage of external directories.
- Review and adjust the `MAX_AGE_DAYS` in `cleanup-old-files.ts` as needed.
