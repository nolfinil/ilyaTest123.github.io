import cv2
import numpy as np
import os
import face_recognition
import pandas as pd
import matplotlib.pyplot as plt

# Path to training images
TRAIN_PATH = "/Users/nolfinil/Downloads/newTrainData"

def load_training_data(path=TRAIN_PATH):
    """
    Load training data from the given path, encode faces, and store student names.
    """
    known_names = []
    known_name_encodings = []

    images = os.listdir(path)
    for image_name in images:
        image_path = os.path.join(path, image_name)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]

        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

    print("Training data loaded. Students:", known_names)
    return known_names, known_name_encodings

def predict_attendance(photo, known_names, known_name_encodings):
    """
    Predict attendance from a test image using preloaded training data.
    """
    # Convert the uploaded photo to an OpenCV image
    np_image = np.frombuffer(photo.read(), np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    recognized_names = []
    attendance = {}

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = face_recognition.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]

        attendance[name] = "Present"
        recognized_names.append(name)

        # Draw rectangles and labels for visualization (Optional)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Fill absent students' attendance as "Absent"
    for name in known_names:
        if name not in recognized_names:
            attendance[name] = "Absent"

    # Prepare attendance data for display
    attendance_data = [{"name": name, "present": status == "Present"} for name, status in attendance.items()]

    return attendance_data, image

def save_attendance_to_csv(attendance_data, output_path="attendance.csv"):
    """
    Save attendance data to a CSV file.
    """
    df = pd.DataFrame(attendance_data)
    df.to_csv(output_path, index=False)
    print(f"Attendance saved to {output_path}")

def visualize_image(image):
    """
    Display the processed image with bounding boxes and names.
    """
    plt.imshow(image, aspect='auto')
    plt.axis("off")
    plt.show()

def predict_children(image_file):
    known_names, known_name_encodings = load_training_data()

    # with open(image_file, "rb") as test_image_file:
    attendance_data, processed_image = predict_attendance(image_file, known_names, known_name_encodings)
    return attendance_data,processed_image

# Example Usage
if __name__ == "__main__":
    known_names, known_name_encodings = load_training_data()

    test_image_path = "/Users/nolfinil/Projects/Automated-Attendance-System-using-Computer-Vision/test/test4.png"
    with open(test_image_path, "rb") as test_image_file:
        attendance_data, processed_image = predict_attendance(test_image_file, known_names, known_name_encodings)

    save_attendance_to_csv(attendance_data)
    visualize_image(processed_image)
