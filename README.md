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

- *Python version*: This project use python 3.11.7   
- *Install Dependencies*: Ensure that you have all the required dependencies installed.   
  You can install them using pip:   
  ```pip install opencv-python mediapipe pyautogui pycaw comtypes```   
  _You can also use the requirements.txt_   
- *Make sure you have a webcam on your device !*   
- *Run the Program*: Execute the `main.py` script to start the hand gesture control system.   

## Usage   

//Comming soon//

## Additional Notes   

- Ensure that your webcam is properly connected and positioned to capture hand gestures.   
- Adjust the system parameters (e.g., cooldown times, smoothing factor) in the configuration files for optimal performance.   

## Credits   

This project utilizes the following libraries and resources:   

- *OpenCV* for computer vision tasks.   
- *MediaPipe* for hand tracking and gesture recognition.   
- *PyAutoGUI* for GUI automation.   
- *PyCaw* for audio control.   
- *Comtypes* for COM interface access.   

The following videos were used as a basis and/or tutorial:   

- [Gesture Volume Control](https://www.youtube.com/watch?v=9iEPzbG-xLE&t=14s) by [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/@murtazasworkshop)

## License   

This project is licensed under the [MIT License](https://fr.wikipedia.org/wiki/Licence_MIT).   