from game.player import Player
from game.lane import get_lane_from_x
from game.obstacle import Obstacle
from game.nitro import Nitro
from game.collision import check_collision

import time
import random

class Game:

    # initialize game objects and game state
    def __init__(self, lane_width, num_lanes, screen_width, y_position):
        self.player = Player(lane_width, num_lanes, y_position)
        self.obstacles = []
        self.nitros = []   
        self.lanes = num_lanes
        self.screen = screen_width
        self.last_obstacle_spawn = time.perf_counter()
        self.last_nitro_spawn = time.perf_counter()
        self.obstacle_spawn_interval = 1.0
        self.nitro_spawn_interval = 2.5

    # reset lives, score, objects, boost, etc.
    def reset(self):
        pass

    # main game logic for ONE frame
    def update(self, gesture , x_position):
       self.handle_gesture(gesture, x_position)
       self.update_items()
       self.handle_collisions()
       self.update_difficulty()


    # decide what to do with OPEN_PALM / PEACE
    def handle_gesture(self, gesture, x_position):
        if(gesture == "open_palm"):
            lane_index = get_lane_from_x(x_position, self.screen , self.lanes)
            self.player.move_to_lane(lane_index)
        elif(gesture == "peace"):
            self.player.activate_boost()
            self.player.update()

            

    

    # decide when to spawn obstacles/nitro
    def spawn_items(self):
        lane_index = random.randint(0, self.player.num_lanes - 1)
        if(time.perf_counter() - self.last_obstacle_spawn > self.obstacle_spawn_interval):
            obstacle = Obstacle(lane_index, self.player.lane_width, speed)
            self.obstacles.append(obstacle)

        elif(time.perf_counter() - self.last_nitro_spawn > self.nitro_spawn_interval):
            nitro = Nitro(lane_index, self.player.lane_width, speed)
            self.nitros.append(nitro)


    # move obstacles and nitro downward
    def update_items(self):
        for obstacle in self.obstacles:
            obstacle.update()
        for nitro in self.nitros:
            nitro.update()


    # ask collision system what happened
    def handle_collisions(self):
        pass
        

    # increase difficulty over time
    def update_difficulty(self):
        pass
        
    # return True/False
    def is_game_over(self):
        pass
    
    # main game loop
    def run(self):
        pass