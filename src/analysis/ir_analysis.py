import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from PIL import Image
import cv2

# Load the image
image_path = '../upload/Ethanol_IR_wyciete.png'
image = Image.open(image_path)

# Convert image to numpy array
image_array = np.array(image).astype(np.uint8)

# rescale
x_scale_left_ori = 0
x_scale_right_ori = image.width
y_scale_min_ori = 0
y_scale_max_ori = image.height

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

# x_values = np.array([point[0] for point in averaged_minima])
# new_x_values = x_scale_left - ((x_values / x_scale_right_ori) * (x_scale_left - x_scale_right))
#
# y_scale_factor = (y_scale_max - y_scale_min) / (y_scale_max_ori - y_scale_min_ori)
# y_values = np.array([point[1] for point in averaged_minima])
# new_y_values = y_values * y_scale_factor

# scaled_vector = list(zip(new_x_values, new_y_values))

# Wyświetlenie wyników
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Function')
plt.plot([point[0] for point in averaged_minima], [point[1] for point in averaged_minima], 'ro', label='Grouped Local Minima')
plt.legend()
plt.title("Grouped Local Minima Detection")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().invert_yaxis()  # Odwrócenie osi y dla poprawnego wyświetlenia
plt.show()

# Zwrócenie grupowanych minimów lokalnych
print("Grouped Local Minima (x, y):", averaged_minima)