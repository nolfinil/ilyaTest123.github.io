from flask import Flask, request, jsonify
from flask_cors import CORS
import attendance_model  # Replace with the actual name of your model script/module

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Ensure the file is readable
        print("File received:", photo.filename)

        # Predict attendance
        
        attendance_data, _ = attendance_model.predict_children(photo)
        print(attendance_data)
        return jsonify({'attendance': attendance_data}), 200

    except Exception as e:
        print("Error processing the photo:", str(e))
        return jsonify({'error': 'Error processing the photo. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
