document.getElementById('upload-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the form from reloading the page

    const photoInput = document.getElementById('photo');
    if (!photoInput.files.length) {
        alert('Please select a photo to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('photo', photoInput.files[0]);

    try {
        // Ensure the fetch URL matches your Flask server's base URL and port
        const response = await fetch('https://afb2-5-76-252-129.ngrok-free.app/upload', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Server response:", data);
            updateAttendanceTable(data.attendance);
        } else {
            const errorData = await response.json();
            console.error("Error from server:", errorData);
            alert(`Error: ${errorData.error || 'Unable to process the photo.'}`);
        }
    } catch (error) {
        console.error('Error during fetch:', error);
        alert('An error occurred while communicating with the server. Please try again.');
    }       
});

function updateAttendanceTable(attendance) {
    const tableBody = document.querySelector('#attendance-table tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    attendance.forEach(student => {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        const statusCell = document.createElement('td');

        nameCell.textContent = student.name;
        statusCell.textContent = student.present ? '✅' : '❌';

        row.appendChild(nameCell);
        row.appendChild(statusCell);
        tableBody.appendChild(row);
    });
}

//
const realTimePreview = document.getElementById('real-time-preview');
const startRealTimeButton = document.getElementById('start-real-time');
const stopRealTimeButton = document.getElementById('stop-real-time');

let realTimeStream;
let realTimeInterval;

// Start real-time video stream
async function startRealTimeVideo() {
    try {
        realTimeStream = await navigator.mediaDevices.getUserMedia({ video: true });
        realTimePreview.srcObject = realTimeStream;
        startRealTimeButton.disabled = true;
        stopRealTimeButton.disabled = false;

        // Start sending frames every 5 seconds
        realTimeInterval = setInterval(captureAndSendFrame, 5000);
    } catch (error) {
        console.error('Error accessing real-time camera:', error);
        alert('Unable to access the camera for real-time attendance.');
    }
}
//a
function updateDetectedNames(attendance) {
    const namesContainer = document.getElementById('detected-names');
    console.log('Updating detected names...');
    console.log('Attendance data received:', attendance);
    console.log('Ilya')
    // Check if the container exists
    if (!namesContainer) {
        console.error('Element with ID "detected-names" not found.');
        return;
    }

    // Clear the existing content
    namesContainer.innerHTML = '';

    // Check if there are any "present" students
    const presentStudents = attendance.filter(student => student.present);

    if (presentStudents.length === 0) {
        // Replace the placeholder text ONLY when no faces are detected
        console.log('No faces detected.');
        namesContainer.innerHTML = '<div style="color: red;">No faces detected.</div>';
    } else {
        console.log('Present students:', presentStudents);

        // Append recognized names
        presentStudents.forEach((student, index) => {
            const nameLine = document.createElement('div');
            nameLine.style.font = '18px Arial';
            nameLine.style.color = 'green';
            nameLine.textContent = `${index + 1}. ${student.name}`;
            namesContainer.appendChild(nameLine);
        });
    }
}

//a

// Stop real-time video stream
function stopRealTimeVideo() {
    if (realTimeStream) {
        const tracks = realTimeStream.getTracks();
        tracks.forEach(track => track.stop());
    }
    clearInterval(realTimeInterval);
    startRealTimeButton.disabled = false;
    stopRealTimeButton.disabled = true;
}

// Capture and send a frame from the video stream
async function captureAndSendFrame() {
    const canvas = document.createElement('canvas');
    const video = realTimePreview;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageDataUrl = canvas.toDataURL('image/jpeg');

    // Convert the base64 image to a Blob for uploading
    const response = await fetch(imageDataUrl);
    const blob = await response.blob();

    const formData = new FormData();
    formData.append('photo', blob, 'real_time_frame.jpg');

    try {
        const uploadResponse = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        });
    
        if (uploadResponse.ok) {
            const data = await uploadResponse.json();
            console.log('Attendance response:', data);
    
            // Update recognized names
            updateDetectedNames(data.attendance);
    
            // Optionally update attendance table
            updateAttendanceTable(data.attendance);
        } else {
            console.error('Server error:', await uploadResponse.text());
        }
    } catch (error) {
        console.error('Error during real-time frame upload:', error);
    }    
}

startRealTimeButton.addEventListener('click', startRealTimeVideo);
stopRealTimeButton.addEventListener('click', stopRealTimeVideo);

//
const cameraPreview = document.getElementById('camera-preview');
const takePictureButton = document.getElementById('take-picture');

let cameraStream;

// Access the camera
async function startCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraPreview.srcObject = cameraStream;
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Unable to access the camera. Please check your device settings.');
    }
}

// Capture an image from the video stream
function captureImage() {
    const canvas = document.createElement('canvas');
    const video = cameraPreview;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    return canvas.toDataURL('image/jpeg');
}

// Handle the "Take Picture" button click
takePictureButton.addEventListener('click', async function () {
    const imageDataUrl = captureImage();

    // Convert the base64 image to a Blob for uploading
    const response = await fetch(imageDataUrl);
    const blob = await response.blob();

    const formData = new FormData();
    formData.append('photo', blob, 'capture.jpg');

    try {
        const uploadResponse = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        });

        if (uploadResponse.ok) {
            const data = await uploadResponse.json();
            console.log("Server response:", data);
            updateAttendanceTable(data.attendance);
        } else {
            const errorData = await uploadResponse.json();
            console.error("Error from server:", errorData);
            alert(`Error: ${errorData.error || 'Unable to process the photo.'}`);
        }
    } catch (error) {
        console.error('Error during upload:', error);
        alert('An error occurred while communicating with the server. Please try again.');
    }
});

// Start the camera when the page loads
window.addEventListener('load', startCamera);
