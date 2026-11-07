import os
import time
try:
    import winsound
except ImportError:
    winsound = None
from datetime import datetime

import cv2


# -------------------- SETTINGS --------------------

CAMERA_INDEX = 0
ABSENCE_LIMIT = 5

CAPTURE_FOLDER = "captures"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "events.log")

CASCADE_FILE = "haarcascade_frontalface_default.xml"


# -------------------- DIRECTORIES --------------------

os.makedirs(CAPTURE_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)


# -------------------- FUNCTIONS --------------------

def save_alarm_capture(frame):
    current_time = datetime.now()

    file_name = current_time.strftime(
        "alarm_%Y-%m-%d_%H-%M-%S.jpg"
    )

    file_path = os.path.join(
        CAPTURE_FOLDER,
        file_name
    )

    is_saved = cv2.imwrite(file_path, frame)

    if is_saved:
        print(f"Alarm capture saved: {file_path}")
        return file_path

    print("Failed to save alarm capture.")
    return None


def write_log(event_name, capture_path=None):
    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{current_time}] {event_name}")

        if capture_path is not None:
            log_file.write(
                f" | Capture: {capture_path}"
            )

        log_file.write("\n")


def format_duration(seconds):
    total_seconds = int(seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    remaining_seconds = total_seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining_seconds:02d}"
    )


# -------------------- CAMERA AND MODEL --------------------

camera = cv2.VideoCapture(CAMERA_INDEX)

face_cascade = cv2.CascadeClassifier(
    CASCADE_FILE
)

if not camera.isOpened():
    print("Failed to open camera.")
    raise SystemExit

if face_cascade.empty():
    camera.release()
    print("Failed to load Haar Cascade classifier file.")
    raise SystemExit


# -------------------- STATE VARIABLES --------------------

face_missing_start = None
alarm_active = False
alarm_count = 0
last_alarm_time = None
application_start_time = time.time()

write_log("APPLICATION STARTED")


# -------------------- MAIN LOOP --------------------

try:
    while True:
        success, frame = camera.read()

        if not success:
            print("Failed to read frame from camera.")
            write_log("CAMERA FRAME ERROR")
            break

        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(60, 60)
        )

        # -------------------- PRESENCE CHECK --------------------

        if len(faces) > 0:
            if alarm_active:
                write_log("USER RETURNED")

            face_missing_start = None
            alarm_active = False

            status_text = "User Present"
            status_color = (0, 255, 0)

        else:
            if face_missing_start is None:
                face_missing_start = time.time()

            missing_duration = (
                time.time() - face_missing_start
            )

            remaining_time = max(
                0,
                ABSENCE_LIMIT - missing_duration
            )

            status_text = (
                f"User Missing: {remaining_time:.1f}s"
            )

            status_color = (0, 165, 255)

            if missing_duration >= ABSENCE_LIMIT:
                status_text = "ALARM! USER MISSING"
                status_color = (0, 0, 255)

                if not alarm_active:
                    alarm_count += 1

                    last_alarm_time = (
                        datetime.now().strftime("%H:%M:%S")
                    )

                    capture_path = save_alarm_capture(
                        frame
                    )

                    write_log(
                        "ALARM - User Missing",
                        capture_path
                    )

                    alarm_active = True

                    if winsound is not None:
                        winsound.Beep(
                            1500,
                            1000
                        )
                    else:
                        print("\a[ALARM] User missing threshold exceeded!")

        # -------------------- FACE BOXES --------------------

        for face_x, face_y, face_width, face_height in faces:
            cv2.rectangle(
                frame,
                (face_x, face_y),
                (
                    face_x + face_width,
                    face_y + face_height
                ),
                (0, 255, 0),
                2
            )

        # -------------------- RUNTIME --------------------

        running_seconds = (
            time.time() - application_start_time
        )

        running_time = format_duration(
            running_seconds
        )

        # -------------------- TOP LABELS --------------------

        cv2.putText(
            frame,
            status_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_color,
            2,
            cv2.LINE_AA
        )

        faces_text = f"Faces: {len(faces)}"

        (faces_text_width, _), _ = cv2.getTextSize(
            faces_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            2
        )

        faces_text_x = (
            frame.shape[1]
            - faces_text_width
            - 20
        )

        cv2.putText(
            frame,
            faces_text,
            (faces_text_x, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # -------------------- BOTTOM INFORMATION --------------------

        frame_height = frame.shape[0]

        cv2.putText(
            frame,
            f"Alarm Count: {alarm_count}",
            (20, frame_height - 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        last_alarm_text = (
            last_alarm_time
            if last_alarm_time is not None
            else "None"
        )

        cv2.putText(
            frame,
            f"Last Alarm: {last_alarm_text}",
            (20, frame_height - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        running_text = (
            f"Running: {running_time}"
        )

        (running_text_width, _), _ = cv2.getTextSize(
            running_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2
        )

        running_text_x = (
            frame.shape[1]
            - running_text_width
            - 20
        )

        cv2.putText(
            frame,
            running_text,
            (
                running_text_x,
                frame_height - 30
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # -------------------- DISPLAY --------------------

        cv2.imshow(
            "OpenCV Presence Monitor",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

finally:
    write_log("APPLICATION CLOSED")

    camera.release()
    cv2.destroyAllWindows()
