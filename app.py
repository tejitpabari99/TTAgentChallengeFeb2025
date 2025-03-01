from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from pptx_extractor import PPTXExtractor

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pptx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Check file signature
                with open(filepath, 'rb') as f:
                    magic = f.read(4)
                    if magic != b'PK\x03\x04':
                        if magic == b'\xd0\xcf\x11\xe0':
                            flash('Error: This appears to be an old format PowerPoint file (.ppt). Please save it as .pptx format and try again.')
                        else:
                            flash('Error: Not a valid PowerPoint file')
                        os.remove(filepath)
                        return redirect(request.url)
                
                # Extract content
                extractor = PPTXExtractor(filepath)
                extractor.extract_content()
                
                # Generate summary
                summary = f"""PowerPoint Extraction Summary
{'='*30}

Source File: {filepath}
Text Extractions: {len(extractor.text_content)} slides with text
Notes Extractions: {len(extractor.notes_content)} slides with notes
Media Files: {len(extractor.media_files)} files extracted
"""
                
                # Extract title and description from first slide content
                if extractor.text_content:
                    first_slide_text = extractor.text_content[0].split('\n', 1)[1] if '\n' in extractor.text_content[0] else extractor.text_content[0]
                    
                    # Extract title (first line) and description (rest of content)
                    lines = first_slide_text.split('\n')
                    title = lines[0].strip()
                    description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
                else:
                    title = ""
                    description = ""
                
                # Get remaining text content and notes
                text_content = "\n\n".join(extractor.text_content[1:]) if len(extractor.text_content) > 1 else ""
                notes_content = "\n\n".join(extractor.notes_content) if extractor.notes_content else ""

                # Create JSON structure for slides
                slides_data = {}
                for i, text in enumerate(extractor.text_content):
                    slide_num = i + 1
                    slide_text = text.split('\n', 1)[1] if '\n' in text else text  # Remove "Slide X:" prefix
                    
                    # Find corresponding notes for this slide
                    slide_notes = ""
                    for note in extractor.notes_content:
                        if note.startswith(f"Slide {slide_num} Notes:"):
                            slide_notes = note.split('\n', 1)[1] if '\n' in note else ""
                            break
                    
                    slides_data[f"slide{slide_num}"] = {
                        "text": slide_text,
                        "notes": slide_notes
                    }
                
                # Save to JSON file
                import json
                with open('slides_content.json', 'w', encoding='utf-8') as f:
                    json.dump(slides_data, f, indent=2, ensure_ascii=False)
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return render_template('upload.html', 
                                     summary=summary,
                                     title=title,
                                     description=description,
                                     text_content=text_content,
                                     notes_content=notes_content)
            
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                if os.path.exists(filepath):
                    os.remove(filepath)
                return render_template('upload.html')
        else:
            flash('Only .pptx files are allowed')
            return render_template('upload.html')
    
    return render_template('upload.html', summary=None, title=None, description=None, text_content=None, notes_content=None)

@app.route('/update_presentation_info', methods=['POST'])
def update_presentation_info():
    # Check if the request is JSON
    if request.is_json:
        data = request.get_json()
        title = data.get('title', '')
        description = data.get('description', '')
        intent = data.get('intent', '')
        reviewers = data.get('reviewers', [])
    else:
        # Handle form data for backward compatibility
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        intent = request.form.get('intent', '')
        reviewers = []
    
    # Here you can store the updated info
    # For now, we'll just return it as JSON
    return jsonify({
        'status': 'success', 
        'title': title,
        'description': description,
        'intent': intent,
        'reviewers': reviewers
    })

if __name__ == '__main__':
    app.run(debug=True)
