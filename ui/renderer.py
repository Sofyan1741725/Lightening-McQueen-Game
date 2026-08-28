import cv2 
import numpy as np
from ui.effects import Effects
from ui.hud import HUD

class Renderer:
    def __init__(self, width=1280, height=720, lanes=5):
        self.width = width
        self.height = height
        self.lanes = lanes
        self.lane_width = self.width // self.lanes
        self.effects = Effects()
        self.hud = HUD()

        self.mcqueen= cv2.imread('assets/images/mcqueen.png', -1)
        self.tire= cv2.imread('assets/images/tire.png', -1)
        self.nitro= cv2.imread('assets/images/nitro.png', -1)

        self.mcqueen= cv2.resize(self.mcqueen, (100, 100))
        self.tire= cv2.resize(self.tire, (60, 60))
        self.nitro= cv2.resize(self.nitro, (60, 60))

    def lane_center(self, lane):
        return (lane * self.lane_width) + (self.lane_width // 2) #lane center calculation

    def draw_image(self, frame, image, x, y):  #draw image on the frame at specified coordinates
        h, w = image.shape[:2]
        frame[y:y+h, x:x+w] = image 
