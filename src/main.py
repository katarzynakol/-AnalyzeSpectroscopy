import os
import base64
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
import numpy as np
from scipy.signal import savgol_filter, find_peaks

# Konfiguracja ścieżki do folderu uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Konfiguracja bazy danych
DB_USERNAME = 'dsqa_s442846'
DB_PASSWORD = 'adeworapadostri'
DB_HOST = 'psql.wmi.amu.edu.pl'
DB_PORT = '5432'
DB_NAME = 'dsqa_s442846'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model danych dla tabeli `dane_spektroskopowe`
class DaneSpektroskopowe(db.Model):
    __tablename__ = 'dane_spektroskopowe'
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey('zwiazki_chemiczne.id'))
    ppm = db.Column(db.Float)
    hz = db.Column(db.Float)
    intensity = db.Column(db.Float)

# Model danych dla tabeli `zwiazki_chemiczne`
class ZwiazkiChemiczne(db.Model):
    __tablename__ = 'zwiazki_chemiczne'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    formula = db.Column(db.String)

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

    files = request.files.getlist('file')
    uploaded_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(file_path)

    return render_template('index.html', files=uploaded_files)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    roi = data['roi']
    image_data = data['image']

    # Decode the image data
    image_data = base64.b64decode(image_data.split(",")[1])
    image = Image.open(BytesIO(image_data)).convert('L')
    image_array = np.array(image)

    # Extract the region of interest
    roi_image = image_array[roi['startY']:roi['endY'], roi['startX']:roi['endX']]

    # Analyze the ROI
    spectrum = np.sum(roi_image, axis=0)
    spectrum_normalized = 100 * (spectrum - np.min(spectrum)) / (np.max(spectrum) - np.min(spectrum))
    smoothed_spectrum = savgol_filter(spectrum_normalized, window_length=51, polyorder=3)
    inverted_spectrum = np.max(smoothed_spectrum) - smoothed_spectrum
    minima, _ = find_peaks(inverted_spectrum, height=np.max(inverted_spectrum) * 0.1, distance=20)
    boundary_margin = 50
    valid_minima = minima[(minima > boundary_margin) & (minima < (len(spectrum) - boundary_margin))]
    x_values = np.linspace(4000, 400, len(spectrum))
    detected_minima = x_values[valid_minima]
    minima_intensities = smoothed_spectrum[valid_minima]

    result = {
        'minima_positions': detected_minima.tolist(),
        'minima_intensities': minima_intensities.tolist()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
