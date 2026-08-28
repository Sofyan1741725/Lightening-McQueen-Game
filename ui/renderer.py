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
        

    def render(self, game):
        frame = np.full(
            (self.height, self.width, 3),
            (45, 120, 45),
            dtype=np.uint8
        )

        cv2.rectangle(
            frame,
            (self.road_left, 0),
            (self.road_right, self.height),
            (55, 55, 55),
            -1
        )

        cv2.line(
            frame,
            (self.road_left, 0),
            (self.road_left, self.height),
            (255, 255, 255),
            6
        )

        cv2.line(
            frame,
            (self.road_right, 0),
            (self.road_right, self.height),
            (255, 255, 255),
            6
        )

        for lane in range(1, self.lanes):
            x = self.road_left + lane * self.lane_width
            cv2.line(
                frame,
                (x, 0),
                (x, self.height),
                (255, 255, 255),
                2
            )

        for x in range(self.road_left, self.road_right, 80):
            cv2.rectangle(
                frame,
                (x, 20),
                (x + 40, 60),
                (255, 255, 255),
                -1
            )

            cv2.rectangle(
                frame,
                (x + 40, 20),
                (x + 80, 60),
                (0, 0, 0),
                -1
            )

        cv2.putText(
            frame,
            "LIGHTNING MCQUEEN",
            (430, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        self.draw_image(
            frame,
            self.mcqueen,
            self.lane_x(2) - 50,
            self.height - 120
        )

        self.draw_image(
            frame,
            self.tire,
            self.lane_x(1) - 30,
            200
        )

        self.draw_image(
            frame,
            self.nitro,
            self.lane_x(3) - 30,
            350
        )

        cv2.putText(
            frame,
            "Score: 250",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Lives: 3",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Nitro: 2",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        if game.player.boost_active:
            for y in range(0, self.height, 60):
                cv2.line(
                    frame,
                    (150, y),
                    (180, y),
                    (255, 255, 255),
                    3
                )

                cv2.line(
                    frame,
                    (1100, y),
                    (1130, y),
                    (255, 255, 255),
                    3
                )

        return frame
