# 😴 Sleep Detection System — MediaPipe + Python

A Python script that uses your webcam to monitor your eyes and plays an alarm if you fall asleep. No extra hardware needed, just your webcam and speakers.

## How It Works

The system uses MediaPipe to track facial landmarks and calculates the Eye Aspect Ratio (EAR). If your eyes remain closed for a specific number of frames, it assumes you are asleep and triggers an audio alarm to wake you up.

### Status Indicators

| State | Condition | Action |
| :--- | :--- | :--- |
| 🟢 **Awake** | Eyes open (EAR > Threshold) | Tracking continues normally |
| 🟡 **Blinking** | Eyes closed briefly | Ignored |
| 🔴 **Asleep** | Eyes closed for extended frames | **Plays `wakeup.mp3` alarm** |

---

## Requirements

* Python 3.7+
* Webcam
* Speakers/Headphones

## Install Dependencies

You can install all the required modules at once using the requirements file:

```bash
pip install -r requirements.txt