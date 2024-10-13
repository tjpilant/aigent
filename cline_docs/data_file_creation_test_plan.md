# Data File Creation Page Test Plan

## UI Verification
1. Verify that the page title "Data File Creation" is displayed correctly.
2. Confirm that the file upload section is present with the label "Google AI OCR Upload Files (max 15 pages per file)".
3. Check that the "Choose Files" button is visible and indicates multiple file selection.
4. Ensure the note about file size limits (20MB for images and 2GB for PDFs) is displayed.
5. Verify that OCR Method selection is available with options for Google Cloud Vision OCR and Tesseract OCR.
6. Confirm that the "Process Files" button is present and initially disabled.

## File Upload Testing
1. Select multiple valid image files (e.g., JPEG, PNG) under 20MB each
   - Verify that all file names appear in the UI
   - Confirm that the "Process Files" button becomes enabled
2. Select multiple valid PDF files under 2GB each
   - Verify that all file names appear in the UI
   - Confirm that the "Process Files" button becomes enabled
3. Select a mix of valid image and PDF files
   - Verify that all file names appear in the UI
   - Confirm that the "Process Files" button becomes enabled
4. Attempt to upload an image file over 20MB
   - Verify that an error message is displayed and the file is not added to the selection
5. Attempt to upload a PDF file over 2GB
   - Verify that an error message is displayed and the file is not added to the selection
6. Attempt to upload an unsupported file type (e.g., .txt, .docx)
   - Verify that an error message is displayed or the file is not accepted
7. Test removing individual files from the selection
   - Verify that files can be removed and the list updates correctly

## OCR Method Selection
1. Select Google Cloud Vision OCR
   - Verify that it can be selected and remains selected after choosing multiple files
2. Select Tesseract OCR
   - Verify that it can be selected and remains selected after choosing multiple files
3. Switch between OCR methods multiple times
   - Verify that the selection changes correctly each time

## File Processing (Mock testing due to credential issues)
1. Select multiple valid files and click "Process Files"
   - Verify that the UI indicates processing has begun (e.g., loading spinner, disabled buttons)
   - Confirm that the UI handles the error response gracefully (since actual processing will fail due to missing credentials)

## Error Handling
1. Verify that appropriate error messages are displayed for various error scenarios (e.g., file too large, unsupported file type)
2. Confirm that error messages are clear and informative

## Accessibility
1. Navigate the page using only the keyboard
   - Verify that all interactive elements can be accessed and used
2. Use a screen reader to navigate the page
   - Verify that all important information is read out correctly, including the list of selected files

Please document any issues encountered during testing, including steps to reproduce, expected behavior, and actual behavior.
