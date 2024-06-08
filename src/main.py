import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from src.analysis.nmr_analysis import analyse_nmr_image, compare_with_database

# Konfiguracja ścieżki do folderu uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upewnij się, że folder istnieje
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist('file')  # Wczytaj wszystkie pliki
    uploaded_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(file_path)

    # Przekażemy pliki bezpośrednio do funkcji analizy
    return render_template('analyse.html', files=uploaded_files)
@app.route('/analysis', methods=['POST'])
def analyse_files():
    file_paths = request.form.getlist('file')
    results = []

    for file_path in file_paths:
        peaks_ppm, peaks_hz, intensity = analyse_nmr_image(file_path)
        results.append({
            'file': file_path,
            'peaks_ppm': peaks_ppm,
            'peaks_hz': peaks_hz,
            'intensity': intensity
        })

    # Przykładowa baza danych
    database = [
        {'compound': 'Substancja A', 'ppm': 1.0, 'hz': 400, 'intensity': 100},
        {'compound': 'Substancja B', 'ppm': 2.0, 'hz': 800, 'intensity': 150},
    ]

    matches = []
    for result in results:
        match = compare_with_database(result['peaks_ppm'], result['peaks_hz'], result['intensity'], database)
        matches.extend(match)

    return render_template('results.html', results=results, matches=matches)

if __name__ == '__main__':
    app.run(debug=True)

