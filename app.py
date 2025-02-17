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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
                
                # Extract first slide content separately
                first_slide_content = extractor.text_content[0].split('\n', 1)[1] if extractor.text_content else ""
                
                # Get remaining text content and notes
                text_content = "\n\n".join(extractor.text_content[1:]) if len(extractor.text_content) > 1 else ""
                notes_content = "\n\n".join(extractor.notes_content) if extractor.notes_content else ""
                
                # Clean up uploaded file
                os.remove(filepath)
                
                return render_template('upload.html', 
                                     summary=summary,
                                     first_slide_content=first_slide_content,
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
    
    return render_template('upload.html', summary=None, first_slide_content=None, text_content=None, notes_content=None)

@app.route('/update_context', methods=['POST'])
def update_context():
    context = request.form.get('context', '')
    # Here you can store or process the updated context
    # For now, we'll just return it as JSON
    return jsonify({'status': 'success', 'context': context})

if __name__ == '__main__':
    app.run(debug=True)
