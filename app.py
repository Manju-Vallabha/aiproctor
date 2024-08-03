import cv2
import streamlit as st
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(page_title="AI Proctored Exam", page_icon="👁️", layout="wide")

# Function to send email notification
def send_email_notification(snapshot_path, student_name, exam_name, exam_date):
    email_user = '99210041261@klu.ac.in'
    email_password = 'vjub ivne grnh gwfs'
    email_send = 'pmanjuvallabha@gmail.com'

    subject = f'⚠️ Suspicious Activity Detected during {exam_name}'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = (
        f'📚 **Student Name:** {student_name}\n'
        f'📝 **Exam Name:** {exam_name}\n'
        f'📅 **Exam Date:** {exam_date}\n\n'
        '🚨 No motion detected for over 1 minute. Please review the attached snapshot.'
    )
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(snapshot_path, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= ' + snapshot_path)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()

# Function to detect motion
def detect_motion(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        motion_detected = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame1, motion_detected

# Function to save snapshot
def save_snapshot(frame, path='snapshot.png'):
    cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

# Function to log event
def log_event(message, log_file='log.txt'):
    with open(log_file, 'a') as f:
        f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {message}\n')

# Streamlit app
def main():
    st.title('🎓 AI Proctored Exam with Motion Detection 👁️')

    # Sidebar inputs for student details
    student_name = st.sidebar.text_input("Student Name 🧑‍🎓")
    exam_name = st.sidebar.text_input("Exam Name 📝")
    exam_date = st.sidebar.date_input("Exam Date 📅")

    # Display introductory information
    if 'start' not in st.session_state:

        if st.sidebar.button('Start Exam 🚀'):
            st.session_state.start = True
            message = (
                "🎉 **Exam Started Successfully!** 📚\n"
                "The system is now monitoring for suspicious activity. 🚨\n"
                "The video feed will appear below once the exam begins."
            )
            st.success(message)
   
    # Display exam details and video stream after the exam starts
    if 'start' in st.session_state and st.session_state.start:
        col1, col2 = st.columns([1, 2])  # Create two columns, second column wider

        with col1:
            st.write("## Exam Details")
            st.write(f"**Student Name:** {student_name} 🧑‍🎓")
            st.write(f"**Exam Name:** {exam_name} 📝")
            st.write(f"**Exam Date:** {exam_date} 📅")

        with col2:
            st.write("## Video Stream 🎥")
            FRAME_WINDOW = st.image([])

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Failed to open video capture. Please check your camera.")
                return

            ret, frame1 = cap.read()
            if not ret:
                st.error("Failed to read from the video capture.")
                cap.release()
                return

            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

            motion_alerted = False
            no_motion_start_time = None
            warning_displayed = False

            while True:
                ret, frame2 = cap.read()
                if not ret:
                    st.error("Failed to read from the video capture.")
                    break

                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

                frame1_processed, motion_detected = detect_motion(frame1, frame2)

                if motion_detected:
                    motion_alerted = True
                    no_motion_start_time = None
                    warning_displayed = False
                else:
                    if no_motion_start_time is None:
                        no_motion_start_time = time.time()
                    elif time.time() - no_motion_start_time > 5 and not warning_displayed:
                        with col1:
                            st.markdown("<br><br>", unsafe_allow_html=True)
                            st.warning("🚨 The person is copying! Stopping the video. 🚫")
                        warning_displayed = True

                        # Save snapshot
                        snapshot_path = 'snapshot.png'
                        save_snapshot(frame1_processed, snapshot_path)

                        # Log event
                        log_event("No motion detected for over 1 minute.")

                        # Send email notification
                        send_email_notification(snapshot_path, student_name, exam_name, exam_date)

                        # Stop the video feed
                        cap.release()
                        st.stop()

                FRAME_WINDOW.image(frame1_processed)
                frame1 = frame2.copy()

            cap.release()

    else:
        message = (
            "Welcome to the AI Proctored Exam System! 🚀\n"
            "To start the exam, please enter your details on the left sidebar and click the button below."
        )
        st.info(message)

if __name__ == '__main__':
    main()
