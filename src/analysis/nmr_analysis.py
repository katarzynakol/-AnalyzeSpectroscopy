# nmr_analysis.py

import cv2
import numpy as np
from scipy.signal import find_peaks
from sqlalchemy import create_engine, text
import ast  # Moduł do parsowania listy z postaci tekstowej na obiekt Pythona

# Tworzenie połączenia z bazą danych
engine = create_engine('postgresql://dsqa_s442846:adeworapadostri@psql.wmi.amu.edu.pl:5432/dsqa_s442846')

def analyse_nmr_image(image_path):
    # Wczytanie obrazu
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Odwrócenie kolorów
    inverted_image = cv2.bitwise_not(image)

    # Sumowanie wartości pikseli wzdłuż osi Y
    signal = np.sum(inverted_image, axis=0)

    # Znajdowanie pików
    peaks, _ = find_peaks(signal, height=np.max(signal) * 0.3)

    # Skala ppm
    max_ppm = 10
    ppm_scale = np.linspace(0, max_ppm, inverted_image.shape[1])
    peaks_ppm = ppm_scale[peaks]

    # Skala Hz
    hz_per_ppm = 400
    peaks_hz = peaks_ppm * hz_per_ppm

    # Intensywność
    intensity = signal[peaks]

    return peaks_ppm, peaks_hz, intensity

def compare_with_database(ppm, hz, intensity):
    # Łączymy dane ppm, hz i intensity w postać, która odpowiada danym w bazie
    data_str = f"[{ppm}, {hz}, {intensity}]"

    # Zapytanie SQL do pobrania danych z bazy
    query = text("SELECT * FROM dane_spektroskopowe")

    # Wykonanie zapytania
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.fetchall()  # Pobranie wszystkich wierszy z bazy danych

    # Lista dopasowanych wyników
    matches = []

    # Porównanie danych ze zdjęcia z danymi w bazie
    for row in rows:
        # Sprawdzenie, czy dane nie są puste
        if all(row):
            # Parsowanie listy z postaci tekstowej na obiekt Pythona
            ppm_db = ast.literal_eval(row[0])
            hz_db = ast.literal_eval(row[1])
            intensity_db = ast.literal_eval(row[2])

            # Porównanie danych
            if ppm_db == ppm and hz_db == hz and intensity_db == intensity:
                matches.append(row)

    return matches

