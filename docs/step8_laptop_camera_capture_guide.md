# Step 8 Guide: Laptop Camera Image Capture

This step documents the laptop camera input added to the AI skin disease screening project.

Current project already supports:

```text
Patient login
Patient details form
Image upload from file
FastAPI /predict endpoint
Image storage in backend/uploads
TensorFlow/Keras model prediction
Doctor dashboard review
Voice report
```

The patient image input now supports both existing image upload and laptop webcam capture. Since this is an AI skin diagnosis project, this makes the system closer to real-world sensing/capture. For the current local version, we use the laptop webcam to capture a skin image. Later, after hosting, we can extend this to mobile camera usage.

## Goal Of This Step

Use a laptop camera capture option in the Patient App.

The patient should be able to:

```text
1. Open the patient form.
2. Start the laptop camera.
3. Position the affected skin area in front of the camera.
4. Capture one photo.
5. Preview the captured image.
6. Submit the same captured image to the backend for prediction.
```

Important:

```text
The backend does not need a new prediction endpoint.
The captured camera image will be converted into a normal image File object.
Then it will be sent through the existing POST /predict API exactly like uploaded images.
```

## Why Camera Capture Fits

Camera capture supports the project by letting patients create image input directly in the browser.

In this project, the camera acts as the sensing/input device.

Current input:

```text
Manual image upload from laptop storage
```

Next input:

```text
Live laptop camera capture
```

Future input after hosting:

```text
Mobile phone camera capture
mobile camera capture
Remote health kiosk camera
```

This step makes the project more practical because the system can capture live patient image data instead of only selecting an existing file.

## Current Flow Before Camera

Current patient image flow:

```text
Patient chooses JPG/PNG file
        |
React stores selected file in form.image
        |
React shows image preview using URL.createObjectURL()
        |
Patient clicks Submit For Screening
        |
React creates FormData
        |
FormData includes image file
        |
Frontend sends POST /predict
        |
Backend saves image in backend/uploads
        |
Backend sends image to prediction.py
        |
Model returns disease prediction
```

Current relevant frontend file:

```text
frontend/src/main.jsx
```

Current relevant backend files:

```text
backend/app/main.py
backend/app/services/storage.py
backend/app/services/prediction.py
```

## New Flow After Camera Capture

New patient image flow:

```text
Patient clicks Start Camera
        |
Browser asks camera permission
        |
Camera stream appears in video preview
        |
Patient clicks Capture Photo
        |
Frontend draws video frame to hidden canvas
        |
Canvas image is converted into Blob/File
        |
React stores captured File in form.image
        |
Existing image preview shows captured photo
        |
Patient clicks Submit For Screening
        |
Existing POST /predict API receives image
        |
Backend prediction flow remains same
```

Main point:

```text
Only frontend image input changes.
Backend prediction logic remains the same.
```

## Technology Used For Camera

### Browser MediaDevices API

Definition:

```text
The MediaDevices API lets a web page request access to camera and microphone devices.
```

Function we will use:

```javascript
navigator.mediaDevices.getUserMedia()
```

Purpose:

```text
Starts the laptop camera and gives the browser a live video stream.
```

Example concept:

```javascript
navigator.mediaDevices.getUserMedia({ video: true })
```

### HTML video element

Purpose:

```text
Displays the live camera stream in the frontend.
```

Concept:

```text
video.srcObject = cameraStream
```

### HTML canvas element

Purpose:

```text
Captures one frame from the video stream and converts it into an image.
```

Concept:

```text
canvas draws the current video frame
canvas converts the frame into Blob/File
```

### Blob/File object

Definition:

```text
A Blob is raw file-like data in the browser.
A File is a Blob with a filename and file type.
```

Why needed:

```text
Our backend already expects image as UploadFile.
So the captured camera photo must become a File object before adding it to FormData.
```

## Files Modified

### 1. frontend/src/main.jsx

Added:

```text
camera state
video reference
canvas reference
startCamera()
stopCamera()
capturePhoto()
camera preview UI
capture button
retake/stop button
```

Existing function that will still work:

```text
submitCase()
```

Why:

```text
submitCase() already sends form.image to backend.
The captured camera image will be stored in form.image, same as uploaded file.
```

### 2. frontend/src/styles.css

Added styles for:

```text
camera panel
video preview
camera action buttons
captured image state
mobile responsive camera layout
```

### 3. README.md

Added a short note:

```text
Patient can either upload a skin image or capture one using laptop camera.
```

### 4. docs/step8_laptop_camera_capture_guide.md

This file documents the implementation and test process.

## Files We Do Not Need To Modify

### backend/app/main.py

No change needed.

Reason:

```text
POST /predict already accepts image: UploadFile.
```

### backend/app/services/storage.py

No change needed.

Reason:

```text
It already saves JPG, JPEG, and PNG files.
```

### backend/app/services/prediction.py

No change needed.

Reason:

```text
The model receives the saved image path.
It does not care whether image came from file upload or camera capture.
```

### backend/app/database.py

No change needed.

Reason:

```text
The saved case structure remains same.
```

## Planned UI Changes

Inside the Patient Details form, the image section should support two options:

```text
Upload Skin Image
Start Camera
```

Camera mode should show:

```text
live video preview
Capture Photo button
Stop Camera button
```

After capture:

```text
captured photo appears in existing result preview area
file name can show something like camera-capture.jpg
patient can submit normally
```

Suggested button labels:

```text
Start Camera
Capture Photo
Stop Camera
Retake Photo
Upload Skin Image
```

## Implementation Summary

### Step 1: Add React Imports

Current import:

```javascript
import React, { useMemo, useState } from "react";
```

Will become:

```javascript
import React, { useEffect, useMemo, useRef, useState } from "react";
```

Why:

```text
useRef is needed to access video/canvas DOM elements.
useEffect can clean up camera stream when component unmounts.
```

### Step 2: Add Camera State

Add states like:

```javascript
const [cameraStream, setCameraStream] = useState(null);
const [cameraError, setCameraError] = useState("");
const [isCameraOpen, setIsCameraOpen] = useState(false);
```

Add refs:

```javascript
const videoRef = useRef(null);
const canvasRef = useRef(null);
```

### Step 3: Start Camera

Function:

```javascript
async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" },
    audio: false,
  });
}
```

For laptop:

```text
Browser will use available webcam.
```

For mobile later:

```text
facingMode: "environment" tries to use rear camera.
```

### Step 4: Show Video Stream

Attach stream:

```javascript
videoRef.current.srcObject = stream;
```

The UI will show:

```html
<video ref={videoRef} autoPlay playsInline />
```

### Step 5: Capture Photo

Process:

```text
Read video width and height
Set canvas size
Draw video frame into canvas
Convert canvas to Blob
Create File from Blob
Store File in form.image
Stop camera if desired
```

The key result:

```javascript
updateField("image", capturedFile);
```

After this, the existing submit function works.

### Step 6: Stop Camera

Process:

```text
Loop through stream tracks
Stop each track
Clear video srcObject
Reset camera state
```

Why:

```text
This releases the laptop camera and turns off the webcam indicator.
```

### Step 7: Rebuild Frontend

After editing frontend:

```powershell
cd "<project-root>\frontend"
npm.cmd run build
```

### Step 8: Test

Start backend:

```powershell
cd "<project-root>\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

Test:

```text
Login as patient
Click Start Camera
Allow browser camera permission
Capture photo
Check preview appears
Submit for screening
Check result appears
Login as doctor
Refresh dashboard
Check captured image appears in case card
```

## Browser Permission Notes

The browser will ask:

```text
Allow camera access?
```

The user must click:

```text
Allow
```

If denied:

```text
Camera preview will not start.
Show a clear error message.
User can enable camera permission from browser settings.
```

## Localhost And HTTPS Note

Camera access usually works on:

```text
http://127.0.0.1
http://localhost
```

For hosted websites, camera access generally requires:

```text
HTTPS
```

So later, when hosting the project, the deployed site should use HTTPS for mobile/laptop camera access.

## Privacy And Safety

Camera privacy rules:

```text
Camera starts only after patient clicks Start Camera.
Browser asks permission.
Only captured image is submitted.
Live video stream is not saved.
Camera stream is stopped after capture or when user clicks Stop Camera.
Uploaded/captured image is saved only in backend/uploads on the machine/server running backend.
```

Medical safety reminder:

```text
Image quality affects prediction quality.
The patient should capture a clear, well-lit, focused image.
The result is only screening support and must be reviewed by a doctor.
```

## Good Camera Capture Guidelines For Patient

Tell patient/user:

```text
Use good lighting.
Keep the camera steady.
Keep the affected area clearly visible.
Avoid blurry image.
Avoid too much zoom or too much distance.
Do not include unnecessary personal/face details if not needed.
Capture only the affected skin area.
```

## Future Mobile Camera Plan

After hosting:

```text
Open hosted app on mobile browser
Use same getUserMedia camera API
Prefer rear camera using facingMode: "environment"
Capture skin image from phone camera
Submit to hosted backend
Doctor can review remotely
```

Mobile camera requirements:

```text
HTTPS hosting
Responsive camera UI
Rear camera support
Image compression if needed
Hosted backend storage
Cloud database if multiple users are expected
```

## Success Criteria

This step is complete when:

```text
Patient can start laptop camera
Camera permission works
Live preview appears
Patient can capture photo
Captured image becomes form.image
Existing preview displays captured image
Submit For Screening works with captured image
Backend saves captured image in backend/uploads
Model prediction runs successfully
Doctor dashboard displays captured image
Camera stops properly after use
```

## Short Explanation For Viva

Use this answer:

```text
Earlier our system accepted skin images only through file upload. Since this is an AI skin diagnosis project, we planned a live sensing input using the laptop camera. The frontend will use the browser MediaDevices API to access the webcam, show a live video preview, capture one frame using canvas, convert that frame into a File object, and send it to the existing FastAPI /predict endpoint through FormData. The backend does not need changes because it already accepts image files. Later, after hosting with HTTPS, the same camera flow can work on mobile phones using the rear camera.
```



