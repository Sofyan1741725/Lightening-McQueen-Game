import cv2 as cv
import time

class Player:

    def __init__(self, lane_width, num_lanes, y_position):
        #Lane info
        self.lane = num_lanes // 2
        self.num_lanes = num_lanes
        self.lane_width = lane_width

        #Player dimensions and coordinates
        self.width = int(lane_width * 0.3)
        self.height = self.width * 2
        self.x = int((self.lane * lane_width) + (lane_width / 2) - (self.width / 2))
        self.y = y_position

        #Player game info
        self.lives = 3
        self.nitro_points = 0
        self.boost_active = False
        self.start_boost = 0

        #Player image
        originalImage = cv.imread("assets/mcqueen.png")
        self.img = cv.resize(originalImage, (self.width, self.height))

    def move_left(self):
        if(self.lane != 0):
            self.x -= self.lane_width
            self.lane -= 1
        else:
            return

    def move_right(self):
        if(self.lane != (self.num_lanes - 1)):
            self.x += self.lane_width
            self.lane +=1
        else:
            return


    def move_to_lane(self, lane_index):
        if(lane_index > self.lane):
            steps = lane_index - self.lane
            for step in range(steps):
                 self.move_right()
        elif(lane_index < self.lane):
             steps = self.lane - lane_index
             for step in range(steps):
                 self.move_left()
        else:
            return


    def activate_boost(self):
        if(self.nitro_points > 0 and not self.boost_active):
            self.nitro_points -= 1
            self.boost_active = True
            self.start_boost = time.perf_counter()
        


    def update(self):
        if self.boost_active:
            if time.perf_counter() - self.start_boost >= 2:
                self.boost_active = False
                self.start_boost = 0

    def reset(self):
        self.lane = self.num_lanes // 2
        self.x = int((self.lane * self.lane_width) + (self.lane_width / 2) - (self.width / 2))
        self.lives = 3
        self.nitro_points = 0
        self.boost_active = False
        self.start_boost = 0
