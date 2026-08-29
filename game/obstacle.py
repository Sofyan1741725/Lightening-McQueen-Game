import cv2

class Obstacle:
    def __init__(self, lane_index, lane_width, speed, obs_type="tire"):
        self.lane_index = lane_index
        self.type = obs_type
        self.speed = speed
        
        # Set size and starting position
        self.width = int(lane_width * 0.6)
        self.height = self.width  
        self.x = int((lane_index * lane_width) + (lane_width / 2) - (self.width / 2))
        self.y = -self.height 
        
        # Load the image 
        if self.type == "tire":
            raw_img = cv2.imread("assets/tires.png")
        else:
            raw_img = cv2.imread("assets/stain.png")
            
        self.img = cv2.resize(raw_img, (self.width, self.height))

    def update(self, speed_multiplier=1.0):
        # Scroll downward
        self.y += int(self.speed * speed_multiplier)

    def draw(self, canvas):
        screen_height = canvas.shape[0]

        # Only draw if fully inside the screen bounds
        if self.y >= 0 and (self.y + self.height) < screen_height:
            # Paste the image directly into the numpy array
            canvas[self.y : self.y + self.height, self.x : self.x + self.width] = self.img