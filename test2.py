from PIL import Image
import numpy as np
from deepface import DeepFace

# Load the two images to compare
image1 = Image.open(r'C:\Users\sahil\Documents\repos\facerecoglogin\Face-Recognition-GUI-Login\face\0.jpg')
image2 = Image.open(r'C:\Users\sahil\Documents\repos\facerecoglogin\Face-Recognition-GUI-Login\face\rihanna20gala%202023.jpg')

# Convert the images to NumPy arrays
array1 = np.array(image1)
array2 = np.array(image2)

# Use DeepFace to compare the two images
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
result = DeepFace.verify(array1, array2, detector_backend=backends[0], enforce_detection=False)

# Print the similarity score
print("Similarity score:", result['verified'])
