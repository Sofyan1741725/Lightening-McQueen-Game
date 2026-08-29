# lane.py

def get_lane_from_x(x, screen_width, num_lanes):
    lane_width = screen_width / num_lanes
    return int(x // lane_width)

