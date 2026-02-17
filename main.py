# import cv2
# import time
# import tkinter as tk
# from threading import Thread
# import os
# from datetime import datetime
# import winsound

# from face_detection import detect_faces
# from movement_detection import detect_movement
# from audio_detection import detect_audio
# from excel_report import generate_excel

# running = False
# cap = None

# multi_face_count = 0
# audio_count = 0
# movement_count = 0

# # Create folders
# if not os.path.exists("logs"):
#     os.mkdir("logs")

# if not os.path.exists("screenshots"):
#     os.mkdir("screenshots")

# log_file = open(f"logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w")

# def log_event(msg):
#     time_now = datetime.now().strftime("%H:%M:%S")
#     log_file.write(f"{time_now} - {msg}\n")
#     log_file.flush()

# def save_screenshot(frame, reason):
#     filename = f"screenshots/{reason}_{datetime.now().strftime('%H%M%S')}.jpg"
#     cv2.imwrite(filename, frame)

# def beep_alert():
#     winsound.Beep(1200, 300)

# def start_monitoring():
#     global running, cap
#     global multi_face_count, audio_count, movement_count

#     running = True
#     cap = cv2.VideoCapture(0)
#     start_time = time.time()

#     while running:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         faces, face_count = detect_faces(frame)
#         movement = detect_movement(frame)
#         audio_status = detect_audio()

#         suspicious = False

#         if face_count > 1:
#             multi_face_count += 1
#             suspicious = True
#             log_event("Multiple Faces Detected")
#             save_screenshot(frame, "multi_face")

#         if audio_status == "Multiple":
#             audio_count += 1
#             suspicious = True
#             log_event("Multiple Audio Detected")
#             save_screenshot(frame, "multi_audio")

#         if movement:
#             movement_count += 1
#             suspicious = True
#             log_event("Suspicious Movement Detected")
#             save_screenshot(frame, "movement")

#         if suspicious:
#             beep_alert()

#         # Face color
#         if face_count == 0:
#             face_color = (0,255,255)
#         elif face_count == 1:
#             face_color = (0,255,0)
#         else:
#             face_color = (0,0,255)

#         # Audio color
#         if audio_status == "Silent":
#             audio_color = (0,255,255)
#         elif audio_status == "Single":
#             audio_color = (0,255,0)
#         else:
#             audio_color = (0,0,255)

#         movement_color = (0,255,0) if not movement else (0,0,255)

#         elapsed = int(time.time() - start_time)

#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

#         cv2.putText(frame, f"Time: {elapsed}s", (10,25),
#                     cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

#         cv2.putText(frame, f"Faces: {face_count}", (10,60),
#                     cv2.FONT_HERSHEY_SIMPLEX,0.8, face_color, 2)

#         cv2.putText(frame, f"Movement: {movement}", (10,95),
#                     cv2.FONT_HERSHEY_SIMPLEX,0.8, movement_color, 2)

#         cv2.putText(frame, f"Audio: {audio_status}", (10,130),
#                     cv2.FONT_HERSHEY_SIMPLEX,0.8, audio_color, 2)

#         if suspicious:
#             cv2.putText(frame, "WARNING: Suspicious Activity!",
#                         (40,180), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),3)

#         cv2.imshow("Interview Monitoring System - PRO", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             stop_monitoring()

#     cleanup_and_generate_report(start_time)

# def cleanup_and_generate_report(start_time):
#     global cap

#     if cap is not None:
#         cap.release()

#     cv2.destroyAllWindows()

#     total_time = int(time.time() - start_time)
#     generate_excel(total_time, multi_face_count, audio_count, movement_count)

#     log_event("Interview Finished")
#     log_file.close()

#     print("\n✅ Interview Finished Properly")
#     print("📊 Excel Report Generated")
#     print("📝 Log File Generated")
#     print("📸 Screenshots Saved")

# def stop_monitoring():
#     global running
#     running = False

# def gui():
#     root = tk.Tk()
#     root.title("Interview Monitoring System - PRO")
#     root.geometry("330x230")

#     tk.Label(root, text="Interview Monitoring System", font=("Arial",14)).pack(pady=15)

#     tk.Button(root, text="Start Monitoring", width=22,
#               command=lambda: Thread(target=start_monitoring).start()).pack(pady=10)

#     tk.Button(root, text="Exit", width=22, command=lambda: [stop_monitoring(), root.destroy()]).pack(pady=5)

#     root.mainloop()

# if __name__ == "__main__":
#     gui()


# main.py
# Complete updated code with fixes for:
# 1. Audio color logic (Silent=Yellow, Single=Green, Multiple=Red)
# 2. Movement detection improvement
# 3. Face detection color logic (0 face = Yellow)
# 4. Exit button properly closing program
# 5. Excel logging + download
# 6. Alert sound for multiple voices

# import cv2
# import numpy as np
# import pyaudio
# import struct
# import math
# import threading
# import time
# import pandas as pd
# import tkinter as tk
# from tkinter import messagebox
# from datetime import datetime
# import winsound

# # ================== Global Variables ==================
# running = True
# movement_status = False
# face_count = 0
# audio_status = "Silent"

# log_data = []

# # ================== Excel Logging ==================
# def log_to_excel():
#     global log_data
#     if len(log_data) == 0:
#         return
#     df = pd.DataFrame(log_data, columns=["Time", "Faces", "Movement", "Audio"])
#     filename = f"interview_log_{int(time.time())}.xlsx"
#     df.to_excel(filename, index=False)
#     print("Excel saved as:", filename)
#     messagebox.showinfo("Saved", f"Excel file saved as {filename}")

# # ================== Audio Detection ==================
# def audio_detection():
#     global audio_status, running

#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100

#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     while running:
#         data = stream.read(CHUNK, exception_on_overflow=False)
#         rms = audio_rms(data)

#         if rms < 500:
#             audio_status = "Silent"
#         elif rms < 3000:
#             audio_status = "Single"
#         else:
#             audio_status = "Multiple"
#             winsound.Beep(1000, 300)

#         time.sleep(0.3)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()


# def audio_rms(frame):
#     count = len(frame) // 2
#     format = "%dh" % count
#     shorts = struct.unpack(format, frame)

#     sum_squares = 0.0
#     for sample in shorts:
#         n = sample * (1.0 / 32768)
#         sum_squares += n * n
#     return math.sqrt(sum_squares / count) * 10000

# # ================== Main Detection ==================
# def main():
#     global running, movement_status, face_count

#     cap = cv2.VideoCapture(0)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     ret, frame1 = cap.read()
#     ret, frame2 = cap.read()

#     while running:
#         diff = cv2.absdiff(frame1, frame2)
#         gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (5,5), 0)
#         _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#         dilated = cv2.dilate(thresh, None, iterations=3)
#         contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#         movement_status = False
#         for contour in contours:
#             if cv2.contourArea(contour) < 2000:
#                 continue
#             movement_status = True

#         gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
#         face_count = len(faces)

#         # -------- Colors --------
#         # Audio
#         if audio_status == "Silent":
#             audio_color = (0,255,255)   # Yellow
#         elif audio_status == "Single":
#             audio_color = (0,255,0)     # Green
#         else:
#             audio_color = (0,0,255)     # Red

#         # Movement
#         move_color = (0,0,255) if movement_status else (0,255,0)

#         # Face
#         if face_count == 0:
#             face_color = (0,255,255)   # Yellow
#         elif face_count == 1:
#             face_color = (0,255,0)     # Green
#         else:
#             face_color = (0,0,255)     # Red

#         # -------- UI Text --------
#         cv2.putText(frame1, f"Audio: {audio_status}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, audio_color, 2)
#         cv2.putText(frame1, f"Movement: {movement_status}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, move_color, 2)
#         cv2.putText(frame1, f"Faces: {face_count}", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, face_color, 2)

#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame1, (x,y), (x+w,y+h), face_color, 2)

#         # -------- Logging --------
#         log_data.append([
#             datetime.now().strftime("%H:%M:%S"),
#             face_count,
#             movement_status,
#             audio_status
#         ])

#         cv2.imshow("Interview Monitoring", frame1)

#         frame1 = frame2
#         ret, frame2 = cap.read()

#         if cv2.waitKey(1) & 0xFF == 27:
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # ================== GUI ==================
# def exit_program():
#     global running
#     running = False
#     time.sleep(1)
#     log_to_excel()
#     root.destroy()

# root = tk.Tk()
# root.title("Interview Monitoring System")
# root.geometry("300x150")

# btn_start = tk.Button(root, text="Start Monitoring", command=lambda: threading.Thread(target=main).start(), width=25)
# btn_start.pack(pady=10)

# btn_exit = tk.Button(root, text="Exit & Save", command=exit_program, width=25)
# btn_exit.pack(pady=10)

# threading.Thread(target=audio_detection, daemon=True).start()

# root.mainloop()

# import cv2
# import time
# import os
# import winsound
# from datetime import datetime
# import tkinter as tk
# from threading import Thread

# from face_detection import detect_faces
# from movement_detection import detect_movement
# from audio_detection import detect_audio
# from excel_report import generate_excel

# running = False

# multi_face_count = 0
# audio_count = 0
# movement_count = 0

# log_file = "interview_log.txt"
# screenshot_dir = "screenshots"

# if not os.path.exists(screenshot_dir):
#     os.makedirs(screenshot_dir)

# def log_event(msg):
#     with open(log_file, "a") as f:
#         f.write(f"{datetime.now()} : {msg}\n")

# def capture_screenshot(frame, reason):
#     filename = f"{screenshot_dir}/{reason}_{int(time.time())}.jpg"
#     cv2.imwrite(filename, frame)
#     log_event(f"Screenshot captured: {filename}")

# def start_monitoring():
#     global running, multi_face_count, audio_count, movement_count
#     running = True

#     cap = cv2.VideoCapture(0)
#     start_time = time.time()

#     while running:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         faces, face_count = detect_faces(frame)
#         movement = detect_movement(frame)
#         audio = detect_audio()

#         elapsed_time = int(time.time() - start_time)

#         # FACE LOGIC
#         if face_count == 0:
#             face_color = (0,255,255)
#             face_status = "No Face"
#         elif face_count == 1:
#             face_color = (0,255,0)
#             face_status = "Single Face"
#         else:
#             face_color = (0,0,255)
#             face_status = "Multiple Faces"
#             multi_face_count += 1
#             log_event("Multiple faces detected")
#             capture_screenshot(frame, "multiple_faces")

#         # AUDIO LOGIC
#         if audio == False:
#             audio_color = (0,255,255)
#             audio_status = "Silent"
#         else:
#             audio_color = (0,0,255)
#             audio_status = "Multiple"
#             audio_count += 1
#             winsound.Beep(1000,200)
#             log_event("Multiple voice detected")
#             capture_screenshot(frame, "multiple_audio")

#         # MOVEMENT LOGIC
#         if movement:
#             move_color = (0,0,255)
#             movement_count += 1
#             log_event("Suspicious movement detected")
#             capture_screenshot(frame, "movement")
#         else:
#             move_color = (0,255,0)

#         # DRAW BOXES
#         for (x,y,w,h) in faces:
#             cv2.rectangle(frame,(x,y),(x+w,y+h),face_color,2)

#         # DISPLAY TEXT
#         cv2.putText(frame, f"Time: {elapsed_time}s", (10,30),
#                     cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

#         cv2.putText(frame, f"Face: {face_status}", (10,70),
#                     cv2.FONT_HERSHEY_SIMPLEX,1,face_color,2)

#         cv2.putText(frame, f"Movement: {movement}", (10,110),
#                     cv2.FONT_HERSHEY_SIMPLEX,1,move_color,2)

#         cv2.putText(frame, f"Audio: {audio_status}", (10,150),
#                     cv2.FONT_HERSHEY_SIMPLEX,1,audio_color,2)

#         cv2.imshow("Interview Monitoring System", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     total_time = int(time.time() - start_time)
#     generate_excel(total_time, multi_face_count, audio_count, movement_count)
#     log_event("Interview Finished")
#     running = False

# def stop_monitoring():
#     global running
#     running = False
#     root.destroy()

# def gui():
#     global root
#     root = tk.Tk()
#     root.title("Interview Monitoring System")
#     root.geometry("300x200")

#     tk.Label(root, text="Interview Monitoring System", font=("Arial",14)).pack(pady=20)

#     tk.Button(root, text="Start Monitoring", width=20,
#               command=lambda: Thread(target=start_monitoring).start()).pack(pady=10)

#     tk.Button(root, text="Exit", width=20, command=stop_monitoring).pack()

#     root.mainloop()

# if __name__ == "__main__":
#     gui()


import cv2
import time
import os
import winsound
from datetime import datetime
import tkinter as tk
from threading import Thread

from face_detection import detect_faces
from movement_detection import detect_movement
from audio_detection import detect_audio
from excel_report import generate_excel

running = False

multi_face_count = 0
audio_count = 0
movement_count = 0

log_file = "interview_log.txt"
screenshot_dir = "screenshots"

if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def log_event(msg):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} : {msg}\n")

def capture_screenshot(frame, reason):
    filename = f"{screenshot_dir}/{reason}_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    log_event(f"Screenshot captured: {filename}")

def start_monitoring():
    global running, multi_face_count, audio_count, movement_count
    running = True

    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        faces, face_count = detect_faces(frame)
        movement = detect_movement(frame)
        audio_status = detect_audio()

        elapsed_time = int(time.time() - start_time)

        # FACE LOGIC
        if face_count == 0:
            face_color = (0,255,255)
            face_status = "No Face"
        elif face_count == 1:
            face_color = (0,255,0)
            face_status = "Single Face"
        else:
            face_color = (0,0,255)
            face_status = "Multiple Faces"
            multi_face_count += 1
            log_event("Multiple faces detected")
            capture_screenshot(frame, "multiple_faces")

        # AUDIO LOGIC
        if audio_status == "silent":
            audio_color = (0,0,255)
        elif audio_status == "single":
            audio_color = (0,255,0)
        else:
            audio_color = (0,0,255)
            audio_count = audio_count + 1
            winsound.Beep(1000,200)
            log_event("Multiple voice detected")
            capture_screenshot(frame, "multiple_audio")

        # MOVEMENT LOGIC
        if movement:
            move_color = (0,0,255)
            movement_count += 1
            log_event("Suspicious movement detected")
            capture_screenshot(frame, "movement")
        else:
            move_color = (0,255,0)

        # DRAW FACE BOX
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),face_color,2)

        # DISPLAY TEXT
        cv2.putText(frame, f"Time: {elapsed_time}s", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        cv2.putText(frame, f"Face: {face_status}", (10,70),
                    cv2.FONT_HERSHEY_SIMPLEX,1,face_color,2)

        cv2.putText(frame, f"Movement: {movement}", (10,110),
                    cv2.FONT_HERSHEY_SIMPLEX,1,move_color,2)

        cv2.putText(frame, f"Audio: {audio_status.upper()}", (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX,1,audio_color,2)

        cv2.imshow("Interview Monitoring System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    total_time = int(time.time() - start_time)
    generate_excel(total_time, multi_face_count, audio_count, movement_count)
    log_event("Interview Finished")
    running = False

def stop_monitoring():
    global running
    running = False
    root.destroy()

def gui():
    global root
    root = tk.Tk()
    root.title("Interview Monitoring System")
    root.geometry("300x200")

    tk.Label(root, text="Interview Monitoring System", font=("Arial",14)).pack(pady=20)

    tk.Button(root, text="Start Monitoring", width=20,
              command=lambda: Thread(target=start_monitoring).start()).pack(pady=10)

    tk.Button(root, text="Exit", width=20, command=stop_monitoring).pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
