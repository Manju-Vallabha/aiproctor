# AI Proctored Exam with Motion Detection

## Overview

The AI Proctored Exam application is a web-based tool designed to monitor exam sessions using motion detection. The system captures video from the user's webcam, detects any motion, and alerts if no motion is detected for over a minute. The application also sends an email notification if suspicious activity is detected during the exam.

## Features

- Real-time video streaming and motion detection
- Email notification for suspicious activity
- User-friendly interface with Streamlit
- Configurable exam details

## Prerequisites

- Python 3.7 or later
- Required Python packages

## Installation

1. **Clone the repository:**
   
   Clone the repository from GitHub and navigate into the project directory.

2. **Install required packages:**

   Create a virtual environment (optional but recommended) and install the required packages.




## Usage

1. **Run the Streamlit app:**

Execute the Streamlit app using the provided command.

2. **Access the application:**

Open your web browser and go to `http://localhost:8501` to access the application.

3. **Fill in the details in the sidebar:**

- Student Name
- Exam Name
- Exam Date

4. **Click 'Start Exam' to begin monitoring.**

The system will display the exam details and start streaming video from the webcam. It will detect motion and alert if no motion is detected for over a minute.

## How Motion Detection Works

1. **Capture Video Frames**: The system captures consecutive frames from the webcam.

2. **Calculate Frame Difference**: The difference between two consecutive frames is computed to identify changes. This difference highlights areas where motion has occurred.

3. **Convert to Grayscale**: The difference frame is converted to grayscale to simplify the detection process.

4. **Apply Gaussian Blur**: A Gaussian blur is applied to reduce noise and smooth the image.

5. **Thresholding**: The blurred grayscale image is thresholded to create a binary image where white areas represent potential motion.

6. **Dilate the Image**: Dilation is used to fill in small holes in the binary image, making it easier to detect larger contours.

7. **Find Contours**: Contours are identified in the binary image. Each contour represents a detected region of motion.

8. **Filter Contours**: Contours that are too small are filtered out. Only larger contours are considered as significant motion.

9. **Draw Bounding Rectangles**: Bounding rectangles are drawn around detected contours on the original frame to visualize the motion.

10. **Determine Motion Detection**: If any significant contours are detected, motion is considered present. If no significant motion is detected for over a minute, an alert is triggered.

## Code Overview

- **Imports**: Required libraries are imported including `cv2`, `streamlit`, `numpy`, `smtplib`, and `email` modules.
- **Functions**:
- `send_email_notification(snapshot_path, student_name, exam_name, exam_date)`: Sends an email notification with the attached snapshot if suspicious activity is detected.
- `detect_motion(frame1, frame2)`: Detects motion by comparing two consecutive video frames.
- `save_snapshot(frame, path)`: Saves a snapshot of the current frame.
- `log_event(message, log_file)`: Logs events to a text file.
- **Streamlit App**:
- Configures the Streamlit layout and handles user inputs.
- Displays introductory information and video stream.
- Monitors the video feed for motion and sends alerts if necessary.

## Troubleshooting

- **Camera not working**: Ensure the camera is properly connected and accessible.
- **Email issues**: Check SMTP server settings and ensure the email credentials are correct.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for providing an easy-to-use framework for building web applications.
- [OpenCV](https://opencv.org/) for video processing and motion detection.


