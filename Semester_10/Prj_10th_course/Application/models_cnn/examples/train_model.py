from ultralytics import YOLO

def main():
    model = YOLO('yolo11m.pt')

    model.train(
        data='dataset/data.yaml',
        epochs=1000,
        imgsz=640, 
        batch=16,
        name='blood_cells_m',
        project='runs/train'
    )

if __name__ == '__main__':
    main()
