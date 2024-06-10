# nmr_analysis.py

import cv2
import numpy as np
from scipy.signal import find_peaks


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

def compare_with_database(peaks_ppm, peaks_hz, intensity, database):
    matches = []
    for entry in database:
        for ppm, hz, intensity_value in zip(peaks_ppm, peaks_hz, intensity):
            if np.isclose(ppm, entry['ppm'], atol=0.1) and np.isclose(hz, entry['hz'], atol=10):
                matches.append(entry)
    return matches