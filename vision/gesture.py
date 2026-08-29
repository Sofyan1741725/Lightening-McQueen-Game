class Gesture:

    def __init__(self, model):
        self.model = model

    def process(self, result):

        gesture = None
        x_position = None
        detections = []

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Center X of the hand
            center_x = int((x1 + x2) / 2)

            detections.append({
                "class_id": class_id,
                "confidence": confidence,
                "x": center_x,
                "box": (
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                )
            })

            # 0 = Open Palm → steering
            if class_id == 0:
                gesture = 0
                x_position = center_x

            # 1 = Peace → boost
            elif class_id == 1:
                gesture = 1

        return gesture, x_position, detections