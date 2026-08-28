import cv2

class HUD:
    def draw(self, frame, score, lives, nitro):
        # Draw score
        cv2.putText(frame, f'Score: {score}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw lives
        cv2.putText(frame, f'Lives: {lives}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw nitro
        cv2.putText(frame, f'Nitro: {nitro}%', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    def boost(self, frame):
        cv2.putText(frame, 'KACHOW BOOST!', (450, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

  
