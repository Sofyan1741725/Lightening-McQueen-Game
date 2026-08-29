# collision.py

def check_collision(item, mcqueen):

    
    # If they are not in the same lane, collision is impossible
    if item.lane_index != mcqueen.lane_index:
        return False
        
    # Calculate top and bottom edges for both objects
    item_top = item.y
    item_bottom = item.y + item.height
    
    mcqueen_top = mcqueen.y
    mcqueen_bottom = mcqueen.y + mcqueen.height
    
    # Collision occurs if item's bottom overlaps McQueen's top, and item's top is above McQueen's bottom
    if item_bottom > mcqueen_top and item_top < mcqueen_bottom:
        return True
        
    return False