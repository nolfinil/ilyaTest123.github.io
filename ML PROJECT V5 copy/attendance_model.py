import pickle
import face_recognition
import os
import cv2
import numpy as np

TRAINED_DATA_PATH = "/Users/nolfinil/Projects/ML PROJECT V5/static/results/trained_data.pkl"   # Path to the pre-saved trained data

def load_saved_training_data():
    """
    Load the pre-saved training data from the pickle file.
    """
    if os.path.exists(TRAINED_DATA_PATH):
        with open(TRAINED_DATA_PATH, 'rb') as f:
            known_names, known_name_encodings = pickle.load(f)
        print("Loaded saved training data.")
        return known_names, known_name_encodings
    else:
        raise FileNotFoundError(f"Trained data file not found at {TRAINED_DATA_PATH}. Please run the training script first.")

def capitalize_surname(name):
    """
    Capitalize the first letter of the surname (last name).
    """
    # Split the full name into first and last name
    name_parts = name.split()
    if len(name_parts) > 1:
        # Capitalize the first letter of the surname (last name)
        name_parts[-1] = name_parts[-1].capitalize()
        # Rejoin the name with the capitalized surname
        return " ".join(name_parts)
    else:
        return name.capitalize()  # In case the name has no surname, just capitalize the whole name

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

    # Prepare attendance data for display with capitalized surname
    attendance_data = [{"name": capitalize_surname(name), "present": status == "Present"} for name, status in attendance.items()]

    return attendance_data, image



# def predict_attendance(photo, known_names, known_name_encodings):
#     """
#     Predict attendance from a test image using preloaded training data.
#     """
#     # Convert the uploaded photo to an OpenCV image
#     np_image = np.frombuffer(photo.read(), np.uint8)
#     image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Detect faces and encode them
#     face_locations = face_recognition.face_locations(image)
#     face_encodings = face_recognition.face_encodings(image, face_locations)

#     recognized_names = []
#     attendance = {}

#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         matches = face_recognition.compare_faces(known_name_encodings, face_encoding)
#         name = ""

#         face_distances = face_recognition.face_distance(known_name_encodings, face_encoding)
#         best_match = np.argmin(face_distances)

#         if matches[best_match]:
#             name = known_names[best_match]

#         attendance[name] = "Present"
#         recognized_names.append(name)

#         # Draw rectangles and labels for visualization (Optional)
#         cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
#         cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#     # Fill absent students' attendance as "Absent"
#     for name in known_names:
#         if name not in recognized_names:
#             attendance[name] = "Absent"

#     # Prepare attendance data for display
#     attendance_data = [{"name": name, "present": status == "Present"} for name, status in attendance.items()]

#     return attendance_data, image

def predict_children(image_file):
    known_names, known_name_encodings = load_saved_training_data()

    # Process the uploaded image to predict attendance
    attendance_data, processed_image = predict_attendance(image_file, known_names, known_name_encodings)
    return attendance_data, processed_image

# Example usage
if __name__ == "__main__":
    # Load saved training data and run prediction on a test image
    with open("test_image.jpg", "rb") as test_image_file:
        attendance_data, processed_image = predict_children(test_image_file)

    # Print the attendance data
    print(attendance_data)
