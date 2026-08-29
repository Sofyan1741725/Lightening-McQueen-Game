import cv2

class Nitro:
    def __init__(self, lane_index, lane_width, speed):
        self.lane_index = lane_index
        self.type = "nitro"
        self.speed = speed
        
        # Set size slightly smaller than obstacles (e.g., 50% of lane width)
        self.width = int(lane_width * 0.5)
        self.height = self.width  
        
        # Calculate X coordinate to center it in the lane
        self.x = int((lane_index * lane_width) + (lane_width / 2) - (self.width / 2))
        
        # Start above the screen bounds
        self.y = -self.height 
        
        # Load the nitro image
        raw_img = cv2.imread("assets/nitro.png")
        self.img = cv2.resize(raw_img, (self.width, self.height))

    def update(self, speed_multiplier=1.0):
        # Scroll downward towards McQueen
        self.y += int(self.speed * speed_multiplier)

    def draw(self, canvas):
        screen_height = canvas.shape[0]
        
        # Draw the image only if it's fully inside the screen to prevent errors
        if self.y >= 0 and (self.y + self.height) < screen_height:
            canvas[self.y : self.y + self.height, self.x : self.x + self.width] = self.img