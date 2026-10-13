"""Resume processing module - handles file uploads and text extraction"""

import tempfile
import os
from pathlib import Path
from utils.helpers import extract_text, extract_emails, extract_phone_numbers, tokenize_text
from utils.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


class ResumeProcessor:
    """Process and extract information from uploaded resume files."""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.resume_text = None
        self.file_name = None
        self.file_path = None
    
    def process_file(self, uploaded_file):
        """
        Process uploaded file and extract text.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            dict: Extracted resume text and metadata
        """
        try:
            # Check file size
            if uploaded_file.size > MAX_FILE_SIZE:
                return {
                    'success': False,
                    'error': f'File size exceeds {MAX_FILE_SIZE / (1024*1024):.1f}MB limit'
                }
            
            # Check file extension
            file_ext = Path(uploaded_file.name).suffix[1:].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                return {
                    'success': False,
                    'error': f'File type .{file_ext} not supported. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
                }
            
            # Save file temporarily
            file_path = os.path.join(self.temp_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract text
            self.resume_text = extract_text(file_path)
            
            if not self.resume_text:
                return {
                    'success': False,
                    'error': 'Could not extract text from file'
                }
            
            self.file_name = uploaded_file.name
            self.file_path = file_path
            
            # Extract contact info
            emails = extract_emails(self.resume_text)
            phones = extract_phone_numbers(self.resume_text)
            
            return {
                'success': True,
                'text': self.resume_text,
                'file_name': self.file_name,
                'file_size': len(self.resume_text),
                'email': emails[0] if emails else 'Not found',
                'phone': f"{phones[0][0]}-{phones[0][1]}-{phones[0][2]}" if phones else 'Not found'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing file: {str(e)}'
            }
    
    def get_text(self):
        """Get extracted resume text."""
        return self.resume_text
    
    def get_word_count(self):
        """Get word count of resume."""
        if not self.resume_text:
            return 0
        return len(tokenize_text(self.resume_text))
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
            except:
                pass
