import os
import zipfile
import xml.etree.ElementTree as ET
import re
import shutil

class PPTXExtractor:
    def __init__(self, pptx_path):
        self.pptx_path = pptx_path
        self.temp_dir = "temp_extraction"
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Initialize content storage
        self.text_content = []
        self.notes_content = []
        self.media_files = []

    def extract_text_from_xml(self, xml_content):
        """Extract text from XML content."""
        try:
            root = ET.fromstring(xml_content)
            # Find all text elements (a:t in PowerPoint XML)
            text_elements = []
            for elem in root.iter():
                if elem.tag.endswith('}t'):  # Text element in any namespace
                    if elem.text and elem.text.strip():
                        text_elements.append(elem.text.strip())
            return '\n'.join(text_elements)
        except ET.ParseError:
            return ""

    def extract_content(self):
        """Extract content from the PowerPoint file."""
        try:
            # Extract the PPTX file (which is a ZIP archive)
            with zipfile.ZipFile(self.pptx_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            # Process slides
            slides_dir = os.path.join(self.temp_dir, 'ppt', 'slides')
            if os.path.exists(slides_dir):
                for slide_file in sorted(os.listdir(slides_dir)):
                    if slide_file.endswith('.xml'):
                        slide_number = re.search(r'slide(\d+)', slide_file).group(1)
                        
                        # Extract slide content
                        with open(os.path.join(slides_dir, slide_file), 'r', encoding='utf-8') as f:
                            slide_content = f.read()
                            text = self.extract_text_from_xml(slide_content)
                            if text:
                                self.text_content.append(f"Slide {slide_number}:\n{text}")
                
                # Extract notes
                notes_dir = os.path.join(self.temp_dir, 'ppt', 'notesSlides')
                if os.path.exists(notes_dir):
                    for notes_file in sorted(os.listdir(notes_dir)):
                        if notes_file.endswith('.xml'):
                            slide_number = re.search(r'notesSlide(\d+)', notes_file).group(1)
                            with open(os.path.join(notes_dir, notes_file), 'r', encoding='utf-8') as f:
                                notes_content = f.read()
                                text = self.extract_text_from_xml(notes_content)
                                if text:
                                    self.notes_content.append(f"Slide {slide_number} Notes:\n{text}")
                
                # Track media files
                media_dir = os.path.join(self.temp_dir, 'ppt', 'media')
                if os.path.exists(media_dir):
                    for media_file in os.listdir(media_dir):
                        self.media_files.append(media_file)
        finally:
            # Clean up temporary directory
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
