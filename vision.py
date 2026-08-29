import numpy as np 
import cv2 as cv
import mediapipe as mp
import uuid
import os


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# load a webcam image, load a video capture 
cap = cv.VideoCapture(0,cv.CAP_DSHOW) # zero indicate to number of the webcam

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
# congedence> detection:threshold for initial detection to be successful, trching: threshold for tracking after initial detection 
    while cap.isOpened():

        # firstly we need to get a frame from our video capture device
        ret, frame = cap.read()

        # convert color frame 
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # set flag
        image.flags.writeable = False

        # detection
        results = hands.process(image)

        # set flag to true 
        image.flags.writeable = True

        # convert color again 
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        print(results)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
    
        # now display the frame 
        cv.imshow(r"Hand Tracking", image)

        if cv.waitKey(10) == ord("q"): # to reaf a key pressed and wait one milliesecond to close the camera
            break 

cap.release()
cv.destroyAllWindows()

results.multi_hand_landmarks # output will show x, y, z axis 
mp_hands.HAND_CONNECTIONS # will show you the joints 