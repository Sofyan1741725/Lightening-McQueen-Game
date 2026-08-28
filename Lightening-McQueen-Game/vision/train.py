from ultralytics import YOLO


def main():
    model = YOLO("yolo11n.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=100,
        imgsz=640,
        batch=-1,  
        device=0,
        name="mcqueen", 
    )


if __name__ == "__main__":
    main()