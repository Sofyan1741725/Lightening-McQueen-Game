import cv2 
import time 

class Effects:
    def __init__(self):
        self.collision_time = 0
        self.boost_duration = 0  

    def collision_effect(self):
        self.collision_time = time.time() #set the time of collision to current time

    def boost_effect(self):
        self.boost_time = time.time() #set the time of boost to current time

    def draw(self, frame): #show the effects on the frame
        t=time.time()

        if t - self.collision_time < 0.5:
            frame[:]=cv2.add(frame, 100) # Increase brightness for collision effect

        if t - self.boost_time < 1.5:
            for y in range(0, frame.shape[0], 50):
                cv2.line(frame, (0, y), (100, y), (0, 255, 255), 2)  # Draw horizontal lines for boost effect
        return frame 
