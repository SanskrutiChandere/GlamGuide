# import cv2
# import mediapipe as mp
# import numpy as np

# # Initialize Mediapipe Face Mesh
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# # Define face shape categories
# FACE_SHAPES = {
#     "Oval": "Oval",
#     "Round": "Round",
#     "Square": "Square",
#     "Heart": "Heart",
#     "Diamond": "Diamond",
#     "Rectangle": "Rectangle"
# }

# def calculate_face_shape(landmarks):
#     # Calculate facial proportions based on landmarks
#     jaw_width = np.linalg.norm(landmarks[234] - landmarks[454])
#     cheek_width = np.linalg.norm(landmarks[93] - landmarks[323])
#     face_length = np.linalg.norm(landmarks[10] - landmarks[152])

#     # Determine face shape based on proportions
#     if face_length > jaw_width * 1.2:
#         if cheek_width > jaw_width:
#             return FACE_SHAPES["Oval"]
#         else:
#             return FACE_SHAPES["Rectangle"]
#     elif face_length <= jaw_width * 1.2:
#         if jaw_width == cheek_width:
#             return FACE_SHAPES["Square"]
#         elif jaw_width > cheek_width:
#             return FACE_SHAPES["Round"]
#         else:
#             return FACE_SHAPES["Heart"]
#     else:
#         return FACE_SHAPES["Diamond"]

# def detect_face_shape(image_path):
#     # Load image and convert to RGB
#     image = cv2.imread(image_path)
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Process the image to find face landmarks
#     results = face_mesh.process(rgb_image)
    
#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             landmarks = np.array([(lm.x * image.shape[1], lm.y * image.shape[0]) for lm in face_landmarks.landmark])

#             # Calculate and return face shape
#             face_shape = calculate_face_shape(landmarks)
#             return face_shape

#     return "Face not detected"

# # Example usage
# if __name__ == "__main__":
#     image_path = 'chandere.jpg'
#     face_shape = detect_face_shape(image_path)
#     print(f'Detected Face Shape: {face_shape}')


import cv2
import numpy as np
import io
from PIL import Image
import mediapipe as mp

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# Define face shape categories
FACE_SHAPES = {
    "Oval": "Oval",
    "Round": "Round",
    "Square": "Square",
    "Heart": "Heart",
    "Diamond": "Diamond",
    "Rectangle": "Rectangle"
}

def calculate_face_shape(landmarks):
    # Calculate key facial proportions based on specific landmark indices
    jaw_width = np.linalg.norm(landmarks[234] - landmarks[454])
    cheek_width = np.linalg.norm(landmarks[93] - landmarks[323])
    face_length = np.linalg.norm(landmarks[10] - landmarks[152])

    # Determine face shape based on proportions
    if face_length > jaw_width * 1.2:
        if cheek_width > jaw_width:
            return FACE_SHAPES["Oval"]
        else:
            return FACE_SHAPES["Rectangle"]
    elif face_length <= jaw_width * 1.2:
        if jaw_width == cheek_width:
            return FACE_SHAPES["Square"]
        elif jaw_width > cheek_width:
            return FACE_SHAPES["Round"]
        else:
            return FACE_SHAPES["Heart"]
    else:
        return FACE_SHAPES["Diamond"]

def detect_face_shape(image):
    # Convert image to RGB if it's in BGR format (OpenCV loads in BGR by default)
    if image.shape[-1] == 3:  # Ensure the image has 3 channels (BGR)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to find face landmarks
    results = face_mesh.process(rgb_image)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Convert landmarks into an array of (x, y) coordinates relative to the image size
            landmarks = np.array([(lm.x * image.shape[1], lm.y * image.shape[0]) for lm in face_landmarks.landmark])

            # Calculate and return face shape
            face_shape = calculate_face_shape(landmarks)
            return face_shape

    return "Face not detected"

def process_uploaded_image(uploaded_image):
    """
    Convert an uploaded image (FileStorage object) to a NumPy array usable by OpenCV.
    
    Parameters:
    - uploaded_image: The uploaded image as a FileStorage object.
    
    Returns:
    - image: The image as a NumPy array.
    """
    # Convert the FileStorage object (uploaded image) to bytes, then to a PIL image
    image_stream = io.BytesIO(uploaded_image.read())
    pil_image = Image.open(image_stream)

    # Convert the PIL image to a NumPy array
    open_cv_image = np.array(pil_image)

    # If the image has an alpha channel (transparency), remove it
    if open_cv_image.shape[-1] == 4:
        open_cv_image = open_cv_image[:, :, :3]

    return open_cv_image
