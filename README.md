# hand_gesture-Subway_surfers
Control Subway Surfers (or any arrow_key-controlled game) using hand gestures detected through your laptop webcam!

This project uses MediaPipe, OpenCV, and pynput to convert gestures into keyboard events.

🚀 Features

🖐️ Open palm → Jump

🤙 Hang-Loose gesture (Thumb + Pinky) → Duck

👈 Move hand to left side → Move Left

👉 Move hand to right side → Move Right

🎥 Real-time hand tracking with MediaPipe

🎮 Works with Subway Surfers, Temple Run, or any arrow_key-based game

💻 Runs on any laptop webcam

🛠️ Tech Stack

> Python 3

> OpenCV

> MediaPipe

> pynput

📦 Installation

1️⃣ Create Conda environment (recommended)

conda create -n subway python=3.10

conda activate subway

2️⃣ Install dependencies

pip install opencv-python mediapipe pynput

▶️ How to Run

python gesture_subway.py


Make sure your webcam is connected and the Subway Surfers window is focused.

✋ Gestures

Gesture	Action	Description

✋ Open Palm	Jump	All five fingers extended

🤙 Hang Loose	Duck	Only thumb + pinky extended

👉 Hand to Right	Move Right	Move your hand to right zone

👈 Hand to Left	Move Left	Move your hand to left zone

📡 How It Works

The script:

Captures webcam frames

Detects hand landmarks using MediaPipe

Checks:

Finger extension state

Hand’s horizontal positio

Converts gestures into keyboard events using pynput

Sends arrow keys to control the game

Lane Zones:

Left: x < 0.33

Middle: 0.33 ≤ x ≤ 0.60

Right: x > 0.60
