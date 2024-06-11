import os
import base64
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
from scipy.signal import savgol_filter, find_peaks
import numpy as np
import cv2

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
    spectrum_type = data['spectrum_type']

    # try:
    #     x_scale_left = int(data['x_scale_left'])
    # except (ValueError, KeyError):
    #     return jsonify({"error": "Invalid or missing value for x_scale_left"}), 400
    #
    # try:
    #     x_scale_right = int(data['x_scale_right'])
    # except (ValueError, KeyError):
    #     return jsonify({"error": "Invalid or missing value for x_scale_right"}), 400
    #
    # y_scale_min = data.get('y_scale_min')
    # y_scale_max = data.get('y_scale_max')
    #
    # if y_scale_min is not None and y_scale_min != '':
    #     try:
    #         y_scale_min = int(y_scale_min)
    #     except ValueError:
    #         return jsonify({"error": "Invalid value for y_scale_min"}), 400
    # else:
    #     y_scale_min = None  # Set to None or a default value if not provided
    #
    # if y_scale_max is not None and y_scale_max != '':
    #     try:
    #         y_scale_max = int(y_scale_max)
    #     except ValueError:
    #         return jsonify({"error": "Invalid value for y_scale_max"}), 400
    # else:
    #     y_scale_max = None  # Set to None or a default value if not provided
    #
    # print("Received ROI:", roi)

    x_scale_left = int(data['x_scale_left'])
    x_scale_right = int(data['x_scale_right'])
    y_scale_min = int(data['y_scale_min'])
    y_scale_max = int(data['y_scale_max'])

    # Decode the image data
    image_data = base64.b64decode(image_data.split(",")[1])
    image = Image.open(BytesIO(image_data)).convert('L')
    image_array = np.array(image)

    # Ensure the ROI coordinates are integers
    startX = int(roi['startX'])
    startY = int(roi['startY'])
    endX = int(roi['endX'])
    endY = int(roi['endY'])

    # Extract the region of interest
    roi_image = image_array[startY:endY, startX:endX]

    if spectrum_type == 'IR':
        result = analyze_ir_spectrum(roi_image, x_scale_left, x_scale_right, y_scale_min, y_scale_max)
    elif spectrum_type == 'NMR':
        result = analyze_nmr_spectrum(roi_image, x_scale_left, x_scale_right)

    return jsonify(result)



def analyze_ir_spectrum(roi_image, x_scale_left, x_scale_right, y_scale_min, y_scale_max):
    height, width = roi_image.shape[0], roi_image.shape[1]
    # rescale
    x_scale_left_ori=0
    x_scale_right_ori=width
    y_scale_min_ori=0
    y_scale_max_ori=height

    image_array = np.array(roi_image).astype(np.uint8)

    if len(image_array.shape) == 2:
        # Obraz jest już w skali szarości
        gray_image = image_array
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        # Obraz jest w formacie RGB/BGR
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGRA2GRAY)
    else:
        print("WARNING!!! Unknown image format")
        gray_image = image_array

    edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
    points = np.column_stack(np.where(edges > 0))
    points = points[np.argsort(points[:, 1])]

    x = points[:, 1]
    y = points[:, 0]

    threshold = 100
    filtered_indices = y > threshold

    # odwrócenie
    inverted_y = -y[filtered_indices]
    peaks, _ = find_peaks(inverted_y)
    original_peaks = np.where(filtered_indices)[0][peaks]

    # grupowanie
    group_distance_threshold = 10
    grouped_minima = []
    current_group = []

    for i in range(len(original_peaks)):
        if i == 0 or (x[original_peaks][i] - x[original_peaks][i - 1]) <= group_distance_threshold:
            current_group.append((x[original_peaks][i], y[original_peaks][i]))
        else:
            grouped_minima.append(current_group)
            current_group = [(x[original_peaks][i], y[original_peaks][i])]

    if current_group:
        grouped_minima.append(current_group)

    # Uśrednianie grupowanych minimów
    averaged_minima = [(int(np.mean([point[0] for point in group])), int(np.max([point[1] for point in group]))) for
                       group in grouped_minima]

    x_values = np.array([point[0] for point in averaged_minima])
    new_x_values = x_scale_left - ((x_values / x_scale_right_ori) * (x_scale_left - x_scale_right))

    y_scale_factor = (y_scale_max-y_scale_min)/(y_scale_max_ori-y_scale_min_ori)
    y_values = np.array([point[1] for point in averaged_minima])
    new_y_values = (y_scale_max_ori-y_values) * y_scale_factor

    scaled_vector = list(zip(new_x_values, new_y_values))

    return scaled_vector

def analyze_nmr_spectrum(roi_image, x_scale_left, x_scale_right):


    image = cv2.imread(roi_image, cv2.IMREAD_GRAYSCALE)

    # Invert the image colors (white to black and black to white)
    inverted_image = cv2.bitwise_not(image)

    # Find the horizontal line
    horizontal_projection = np.sum(inverted_image, axis=1)
    horizontal_line_y = np.argmax(horizontal_projection)

    # Define the ppm range (you need to set this according to your data)
    ppm_min = x_scale_right # Replace with the minimum ppm value
    ppm_max = x_scale_left  # Replace with the maximum ppm value
    image_width = inverted_image.shape[1]

    # Define margins to exclude from analysis
    margin_percentage = 0.05
    start_margin = int(margin_percentage * image_width)
    end_margin = int((1 - margin_percentage) * image_width)

    # Function to convert x-coordinate to ppm value
    def x_to_ppm(x, image_width, ppm_min, ppm_max):
        return ppm_max - (x / image_width) * (ppm_max - ppm_min)

    # Traverse the line from right to left and find the highest peaks, excluding margins
    peak_positions = []
    x_positions = []
    ppm_values = []

    for x in range(end_margin - 1, start_margin - 1, -1):
        column = inverted_image[:, x]
        max_value = column.max()
        peaks = np.where(column == max_value)[0]
        if len(peaks) > 0:
            highest_peak_y = peaks[0]
            peak_positions.append(highest_peak_y)
            x_positions.append(x)
            ppm_values.append(x_to_ppm(x, image_width, ppm_min, ppm_max))

    # Identify the most significant peaks based on y-coordinate differences
    peak_positions = np.array(peak_positions)
    x_positions = np.array(x_positions)
    ppm_values = np.array(ppm_values)

    # Calculate the differences in y-coordinates
    differences = np.abs(np.diff(peak_positions))
    significant_indices = np.where(differences > np.mean(differences))[0]

    # Include the last peak as well, since diff reduces the length by 1
    significant_indices = np.append(significant_indices, significant_indices[-1] + 1)

    # Ensure the longest peak is included and identified as the peak with the highest intensity
    longest_peak_index = np.argmax(peak_positions)
    if longest_peak_index not in significant_indices:
        significant_indices = np.append(significant_indices, longest_peak_index)

    # Calculate intensity
    intensity_values = (1000 * (peak_positions.max() - peak_positions[significant_indices])) // peak_positions.max()
    intensity_values = 1000 - intensity_values  # Adjust to have the longest peak as 1000
    intensity_values[np.argmax(intensity_values)] = 1000  # Ensure the longest peak is set to 1000

    return {"ppm_values": ppm_values.tolist(), "intensity_values": intensity_values.tolist()}


if __name__ == '__main__':
    app.run(debug=True)
