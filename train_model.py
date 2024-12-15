import os
import pickle
import face_recognition

TRAIN_PATH = "/Users/nolfinil/Downloads/newTrainData" # Path to your training images
TRAINED_DATA_PATH = "/Users/nolfinil/Projects/ML PROJECT V5/templates/trained_data.pkl"   # Path to save the trained data

def load_and_train_model(path=TRAIN_PATH):
    """
    Load training data from the given path, encode faces, and store student names.
    Then save the trained data to a pickle file.
    """
    known_names = []
    known_name_encodings = []

    # Load and encode faces from training images
    images = os.listdir(path)
    print("pochti start")
    for image_name in images:
        image_path = os.path.join(path, image_name)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:  # Checks if the list is not empty
            encoding = encodings[0]
                
        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())
        
    print("pochti finished")
    # Save the encoded faces and student names to a pickle file
    with open(TRAINED_DATA_PATH, 'wb') as f:
        pickle.dump((known_names, known_name_encodings), f)
    
    print(f"Training data saved to {TRAINED_DATA_PATH}. Students: {known_names}")
    return known_names, known_name_encodings

if __name__ == "__main__":
    load_and_train_model()
