# import cv2
# import numpy as np
# from sklearn.cluster import KMeans
# from scipy.spatial import distance

# # Predefined list of skin-tone-related colors (approximate values)
# COLOR_NAMES = {
#     "Peach": [255, 218, 185],
#     "Beige": [245, 245, 220],
#     "Tan": [210, 180, 140],
#     "Brown": [165, 42, 42],
#     "Chocolate": [210, 105, 30],
#     "Chestnut": [139, 69, 19],
#     "Espresso": [97, 47, 16],
#     "Mocha": [112, 66, 20],
#     "Caramel": [150, 75, 0]
# }

# def calculate_dominant_color(image_path, clusters=3):
#     # Load image
#     image = cv2.imread(image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Convert the image to a 2D array of pixels
#     pixels = image.reshape(-1, 3)

#     # Remove black (non-skin) pixels
#     pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

#     # Apply k-means clustering to find dominant colors
#     kmeans = KMeans(n_clusters=clusters)
#     kmeans.fit(pixels)

#     # Get the most frequent color and round the values to integers
#     dominant_color = kmeans.cluster_centers_[0]
#     dominant_color = np.round(dominant_color).astype(int)

#     return dominant_color

# def get_closest_color_name(rgb_value):
#     # Calculate the Euclidean distance between the rgb_value and each color in COLOR_NAMES
#     min_distance = float('inf')
#     closest_color_name = None

#     for color_name, color_rgb in COLOR_NAMES.items():
#         dist = distance.euclidean(rgb_value, color_rgb)
#         if dist < min_distance:
#             min_distance = dist
#             closest_color_name = color_name

#     return closest_color_name

# # Example usage
# if __name__ == "__main__":
#     image_path = 'chandere.jpg'
#     dominant_color = calculate_dominant_color(image_path)
#     print(f'Dominant Skin Color (RGB): {dominant_color}')
#     closest_color_name = get_closest_color_name(dominant_color)
#     print(f'Closest Skin Tone Description: {closest_color_name}')

import cv2
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import distance

# Predefined list of skin-tone-related colors (approximate values)
COLOR_NAMES = {
    "Peach": [255, 218, 185],
    "Beige": [245, 245, 220],
    "Tan": [210, 180, 140],
    "Brown": [165, 42, 42],
    "Chocolate": [210, 105, 30],
    "Chestnut": [139, 69, 19],
    "Espresso": [97, 47, 16],
    "Mocha": [112, 66, 20],
    "Caramel": [150, 75, 0]
}

def calculate_dominant_color(image, clusters=3):
    """
    Calculate the dominant color in an image using KMeans clustering.
    
    Parameters:
    - image: The uploaded image as a NumPy array.
    - clusters: Number of color clusters to form.
    
    Returns:
    - dominant_color: The most dominant color in the image as an RGB tuple.
    """
    # Convert the image to RGB if it's in BGR format (OpenCV loads in BGR by default)
    if image.shape[-1] == 3:  # If the image has 3 channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Remove black (non-skin) pixels
    pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

    # Apply k-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(pixels)

    # Get the most frequent color and round the values to integers
    dominant_color = kmeans.cluster_centers_[0]
    dominant_color = np.round(dominant_color).astype(int)

    return dominant_color

def get_closest_color_name(rgb_value):
    """
    Get the closest predefined skin tone name by comparing the Euclidean distance.
    
    Parameters:
    - rgb_value: The dominant color in RGB format.
    
    Returns:
    - closest_color_name: The name of the closest predefined skin tone.
    """
    # Calculate the Euclidean distance between the rgb_value and each color in COLOR_NAMES
    min_distance = float('inf')
    closest_color_name = None

    for color_name, color_rgb in COLOR_NAMES.items():
        dist = distance.euclidean(rgb_value, color_rgb)
        if dist < min_distance:
            min_distance = dist
            closest_color_name = color_name

    return closest_color_name


