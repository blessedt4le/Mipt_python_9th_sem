import cv2
import os

def generate_yolo_annotations(image_path, mask_path, output_path, class_id=0):
    img = cv2.imread(image_path)
    mask = cv2.imread(mask_path, 0)

    height, width = mask.shape

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    lines = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_center = (x + w / 2) / width
        y_center = (y + h / 2) / height
        norm_w = w / width
        norm_h = h / height

        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

generate_yolo_annotations(
    "original.png",
    "mask.png",
    "label.txt"
)

def draw_yolo_boxes(image_path, label_path, output_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue

        class_id, x_center, y_center, w, h = map(float, parts)
        x_center *= width
        y_center *= height
        w *= width
        h *= height

        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        x2 = int(x_center + w / 2)
        y2 = int(y_center + h / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(int(class_id)), (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imwrite(output_path, image)
    print(f"Saved debug image to {output_path}")

draw_yolo_boxes(
    "original.png",
    "label.txt",
    "debug.png"
)