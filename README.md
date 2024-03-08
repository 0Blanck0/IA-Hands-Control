# Hand Gesture Control System With IA   

## Introduction   

This project implements a hand gesture control system using computer vision techniques. The system detects hand gestures in real-time using a webcam and performs actions based on the detected gestures.   
It allows users to control various aspects of the computer interface such as mouse movement, media playback, and system volume using hand gestures.   

## Features   

- *Hand Tracking*: Utilizes the MediaPipe library for hand tracking and landmark detection.   
- *Gesture Recognition*: Recognizes hand gestures using landmark positions and finger states.   
- *Mouse Control*: Moves the mouse cursor based on hand movement.   
- *Media Playback Control*: Controls media playback (e.g., play, pause, next track, previous track) based on hand gestures.   
- *Volume Control*: Adjusts the system volume based on hand movements.   
- *User Attention Detection*: Tracks user attention and activates gesture recognition accordingly.   

## Setup   

- *Install Dependencies*: Ensure that you have all the required dependencies installed.   
  You can install them using pip:   
  ```pip install opencv-python mediapipe pyautogui pycaw comtypes```   
  _You can also use the requirements.txt_   
- *Make sure you have a webcam on your device !*   
- *Run the Program*: Execute the `main.py` script to start the hand gesture control system.   

## License   

This project is licensed under the [MIT License](https://fr.wikipedia.org/wiki/Licence_MIT).   