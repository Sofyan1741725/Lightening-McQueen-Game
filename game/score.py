class Score:
    def __init__(self):
        self.score = 0

    def add_nitro(self):
        self.score += 10

    def obstacle_hit(self):
        self.score -= 5

    def reset(self):
        self.score = 0

    def get_score(self):
        return self.score