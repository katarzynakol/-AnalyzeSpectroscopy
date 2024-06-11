import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread(roi_image, cv2.IMREAD_GRAYSCALE)

# Invert the image colors (white to black and black to white)
inverted_image = cv2.bitwise_not(image)

# Find the horizontal line
horizontal_projection = np.sum(inverted_image, axis=1)
horizontal_line_y = np.argmax(horizontal_projection)

# Define the ppm range (you need to set this according to your data)
ppm_min = x_scale_right  # Replace with the minimum ppm value
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

# Print the values of the significant peaks
print("Significant peaks:")
for ppm, intensity in zip(ppm_values[significant_indices], intensity_values):
    print(f"PPM: {ppm:.2f}, Intensity: {intensity}")




