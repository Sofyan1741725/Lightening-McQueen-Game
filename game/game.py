from game.player import Player
from game.lane import get_lane_from_x
from game.obstacle import Obstacle
from game.nitro import Nitro
from game.collision import check_collision
from game.difficulty import Difficulty
from game.score import Score
from vision.camera import get_detection
from vision.gesture import Gesture

import cv2 as cv
from ultralytics import YOLO

import time
import random

class Game:

    # initialize game objects and game state
    def __init__(self, lane_width, num_lanes, screen_width, screen_height, y_position , game_duration):
        self.player = Player(lane_width, num_lanes, y_position)
        self.score = Score()
        self.difficulty = Difficulty()
        self.last_difficulty_update = time.perf_counter()
        self.obstacles = []
        self.nitros = []   
        self.lanes = num_lanes
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_obstacle_spawn = time.perf_counter()
        self.last_nitro_spawn = time.perf_counter()
        self.obstacle_spawn_interval = 1.0
        self.nitro_spawn_interval = 2.5
        self.game_duration = game_duration
        self.timer = time.perf_counter()

    # reset lives, score, objects, boost, etc.
    def reset(self):
        self.player.reset()
        self.score.reset()
        self.difficulty = Difficulty()
        self.last_difficulty_update = time.perf_counter()
        self.obstacles.clear()
        self.nitros.clear() 
        self.last_obstacle_spawn = time.perf_counter()
        self.last_nitro_spawn = time.perf_counter()
        self.timer = time.perf_counter()

    # main game logic for ONE frame
    def update(self, gesture , x_position):
       self.handle_gesture(gesture, x_position)
       self.player.update()
       self.spawn_items()
       self.update_items()
       self.handle_collisions()
       self.update_difficulty()


    # decide what to do with OPEN_PALM / PEACE
    def handle_gesture(self, gesture, x_position):
        if(gesture == 0): # 0 means open palm
            lane_index = get_lane_from_x(x_position, self.screen_width , self.lanes)
            self.player.move_to_lane(lane_index)
        elif(gesture == 1): # 1 means peace sign
            self.player.activate_boost()

            

    

    # decide when to spawn obstacles/nitro
    def spawn_items(self):
        lane_index_obstacle = random.randint(0, self.player.num_lanes - 1)
        lane_index_nitro = random.randint(0, self.player.num_lanes - 1)
        if(time.perf_counter() - self.last_obstacle_spawn >= self.obstacle_spawn_interval):
            obstacle = Obstacle(lane_index_obstacle, self.player.lane_width, self.difficulty.scroll_speed)
            self.obstacles.append(obstacle)
            self.last_obstacle_spawn = time.perf_counter()

        if(time.perf_counter() - self.last_nitro_spawn >= self.nitro_spawn_interval):
            nitro = Nitro(lane_index_nitro, self.player.lane_width, self.difficulty.scroll_speed)
            self.nitros.append(nitro)
            self.last_nitro_spawn = time.perf_counter()


    # move obstacles and nitro downward
    def update_items(self):
        for obstacle in self.obstacles[:]:
            obstacle.update(self.difficulty.speed_multiplier)
            if(obstacle.y > self.screen_height):
                self.obstacles.remove(obstacle)
        for nitro in self.nitros[:]:
            nitro.update(self.difficulty.speed_multiplier)
            if(nitro.y > self.screen_height):
                self.nitros.remove(nitro)


    # ask collision system what happened
    def handle_collisions(self):
        for obstacle in self.obstacles[:]:
            if check_collision(obstacle, self.player):
                if not self.player.boost_active:
                    self.player.lives -= 1
                    self.score.obstacle_hit()
                self.obstacles.remove(obstacle)
        for nitro in self.nitros[:]:
            if check_collision(nitro, self.player):
                self.player.nitro_points += 1
                self.score.add_nitro()
                self.nitros.remove(nitro)
        
        

    # increase difficulty over time
    def update_difficulty(self):
        current_time = time.perf_counter()
        if current_time - self.last_difficulty_update >= 10:
           self.difficulty.speed_multiplier += 0.2
           self.last_difficulty_update = current_time
    
        
    # return True/False
    def is_game_over(self):
        elapsed_time = time.perf_counter() - self.timer
        if(self.player.lives <= 0 or elapsed_time >= self.game_duration):
            return True
        else:
            return False
    
    # main game loop
    def main(self):
        model = YOLO("runs/detect/mcqueen/weights/best.pt")
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        gesture_detector = Gesture(model)
        while not self.is_game_over():
            frame, result = get_detection(model, cap)
            if frame is None:
                break
            gesture, x_position = gesture_detector.process(result)
            self.update(gesture,x_position)
            game_frame = self.renderer.render(self)
            cv.imshow("McQueen Hand Gesture Game",game_frame)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv.destroyAllWindows()




if __name__ == "main":
    Game.main()