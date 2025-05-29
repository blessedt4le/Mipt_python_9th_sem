import cv2
from ultralytics import YOLO

model = YOLO(r"C:\Files\VSC\proj\models\yolo\blood_cells_11m.pt")

img = cv2.imread(r"C:\Files\VSC\proj\data\test_simple_val.png")

results = model(img)

for result in results:
    boxes = result.boxes
    print(f"Объектов найдено: {len(boxes)}")

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0].item()
        cls = int(box.cls[0].item())

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'{cls} {conf:.2f}', (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()