from ultralytics import YOLO

def evaluate_models(models, data_path, imgsz=640):
    for name, path in models.items():
        print(f"\nEvaluating {name}...")
        model = YOLO(path)
        metrics = model.val(data=data_path, imgsz=imgsz)

        print(f"{name} results:")
        print(f"-mAP50-95:  {metrics.box.map}")
        print(f"-mAP50:     {metrics.box.map50}")
        print(f"-mAP75:     {metrics.box.map75}")
        print(f"-Precision: {metrics.box.p}")
        print(f"-Recall:    {metrics.box.r}")

def main():
    base_dir = r"C:\Files\VSC\proj\models\yolo"
    data_yaml = r"C:\Files\VSC\proj\dataset\data.yaml"

    models = {
        "YOLOv8n": f"{base_dir}\\blood_cells_8n.pt",
        "YOLOv8m": f"{base_dir}\\blood_cells_8m.pt",
        "YOLOv8x": f"{base_dir}\\blood_cells_8x.pt",
        "YOLOv11n": f"{base_dir}\\blood_cells_11n.pt",
        "YOLOv11m": f"{base_dir}\\blood_cells_11m.pt",
    }

    evaluate_models(models, data_yaml)

if __name__ == '__main__':
    main()