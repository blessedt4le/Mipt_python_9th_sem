import os
import cv2
import shutil

def generate_yolo_annotations(mask_path, image_size, class_id=0):
    mask = cv2.imread(mask_path, 0)
    height, width = image_size

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    lines = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_center = (x + w / 2) / width
        y_center = (y + h / 2) / height
        norm_w = w / width
        norm_h = h / height

        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}")
    return lines

def draw_debug_image(image_path, label_path, output_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

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

def prepare_dataset(train_dir="train", output_dir="dataset"):
    original_dir = os.path.join(train_dir, "original")
    mask_dir = os.path.join(train_dir, "mask")
    images_out_dir = os.path.join(output_dir, "images")
    labels_out_dir = os.path.join(output_dir, "labels")
    debug_out_dir = os.path.join(output_dir, "debug")

    if not os.path.isdir(original_dir):
        print(f"[!] Каталог не найден: {original_dir}")
        return
    if not os.path.isdir(mask_dir):
        print(f"[!] Каталог не найден: {mask_dir}")
        return

    os.makedirs(images_out_dir, exist_ok=True)
    os.makedirs(labels_out_dir, exist_ok=True)
    os.makedirs(debug_out_dir, exist_ok=True)

    for filename in os.listdir(original_dir):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        name, _ = os.path.splitext(filename)
        original_path = os.path.join(original_dir, filename)
        mask_path = os.path.join(mask_dir, f"{name}.png")

        if not os.path.exists(mask_path):
            print(f"[!] Пропущено — нет маски: {filename}")
            continue

        image_out_path = os.path.join(images_out_dir, filename)
        label_out_path = os.path.join(labels_out_dir, f"{name}.txt")
        debug_out_path = os.path.join(debug_out_dir, filename)

        shutil.copy2(original_path, image_out_path)

        img = cv2.imread(original_path)
        image_size = img.shape[:2]
        lines = generate_yolo_annotations(mask_path, image_size)

        with open(label_out_path, "w") as f:
            f.write("\n".join(lines))

        draw_debug_image(image_out_path, label_out_path, debug_out_path)

        print(f"Обработано и отрисовано: {filename}")

prepare_dataset(
    r"C:\Users\kosit\Downloads\blood_cells_dataset\BCCD Dataset with mask\test",
    r"C:\Files\VSC\proj\dataset_val"
)
