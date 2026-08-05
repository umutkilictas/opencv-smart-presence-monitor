# OpenCV Smart Presence Monitor

A real-time user presence monitoring application built with **Python** and **OpenCV**.

The application continuously monitors the webcam feed, detects whether a user is present, and triggers an alarm if no face is detected for a specified period. During an alarm event, the current camera frame is automatically captured and all important events are logged with timestamps.

---

## Project Overview

This project demonstrates how classical computer vision techniques can be used to build a simple real-time presence monitoring system.

Instead of identifying **who** the user is, the application only determines **whether a face is present** in the camera view.

When the user remains absent for a predefined amount of time, the system automatically:

* Triggers an audible alarm
* Captures a screenshot of the current frame
* Records the event in a log file
* Detects when the user returns and logs the event

---

## Features

* ✅ Real-time webcam monitoring
* ✅ Face detection using Haar Cascade Classifier
* ✅ User presence monitoring
* ✅ Configurable absence timeout
* ✅ Audible alarm notification
* ✅ Automatic screenshot capture
* ✅ Timestamped event logging
* ✅ User return detection
* ✅ Live alarm counter
* ✅ Last alarm timestamp
* ✅ Application uptime display
* ✅ Real-time face count display

---

## How It Works

```text
Webcam
   │
   ▼
Capture Frame
   │
   ▼
Convert to Grayscale
   │
   ▼
Histogram Equalization
   │
   ▼
Face Detection
   │
   ▼
Is Face Detected?
   │
 ┌─┴──────────────┐
 │                │
Yes              No
 │                │
 ▼                ▼
Reset Timer    Start Timer
 │                │
 │         Timeout Reached?
 │                │
 │        ┌──────────────┐
 ▼        ▼              ▼
Continue  Alarm     Save Screenshot
                     Write Log
```

---

## Technologies

* Python
* OpenCV
* Haar Cascade Classifier
* Windows Sound API (`winsound`)
* File Handling
* DateTime
* OS Module

---

## OpenCV Concepts Used

This project demonstrates several fundamental OpenCV operations, including:

* Webcam video capture
* Real-time image processing
* Face detection
* Grayscale conversion
* Histogram equalization
* Rectangle drawing
* Text rendering
* Frame saving
* Live video display

---

## Project Structure

```text
opencv-smart-presence-monitor/
│
├── captures/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── .gitignore
├── haarcascade_frontalface_default.xml
├── main.py
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/umutkilictas/opencv-smart-presence-monitor.git
```

Navigate to the project directory:

```bash
cd opencv-smart-presence-monitor
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

Press **Q** to exit the application.

---

## Event Logging

Example log output:

```text
[2026-08-05 16:45:13] APPLICATION STARTED
[2026-08-05 16:46:02] ALARM - User Missing
[2026-08-05 16:46:02] Screenshot Saved
[2026-08-05 16:46:14] USER RETURNED
[2026-08-05 16:48:31] APPLICATION CLOSED
```

---

## Current Limitations

* The application performs **face detection**, not face recognition.
* It cannot identify specific individuals.
* Detection accuracy depends on lighting conditions.
* Haar Cascade performs best with frontal faces.
* Alarm sound currently uses the Windows-specific `winsound` module.

---

## Future Improvements

* Adjustable alarm timeout
* Enable/disable alarm sound
* FPS counter
* MediaPipe face detection support
* Cross-platform alarm system
* Email notifications
* Desktop GUI
* Configuration file support
* Multi-face tracking

---

## License

This project was developed for educational and portfolio purposes.
