import cv2
from ultralytics import YOLO


MODEL_PATH = "runs/detect/mcqueen/weights/best.pt"

def get_detection(model, cap):
    ret, frame = cap.read()

    if not ret:
        return None, None

    results = model.predict(
        source=frame,
        device=0,
        conf=0.7,
        verbose=False
    )

    result = results[0]

    return frame, result


def main():
    model = YOLO(MODEL_PATH)
    print("Registered Classes:", model.names)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model.predict(
            source=frame, device=0, conf=0.7, verbose=False
        )

        result = results[0]

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            print(f"Class: {class_name} | Confidence: {confidence:.3f}")

        annotated_frame = result.plot()

        cv2.imshow("Lightening McQueen - Gesture Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()