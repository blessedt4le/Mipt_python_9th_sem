import os
import cv2
import numpy as np
import warnings

from internal.tools.singleton import singleton

@singleton
class SimpleSearchCells:
    def __init__(self,
                 blur_ksize=(5, 5),
                 morph_kernel=(3, 3),
                 min_area=100.0,
                 max_area=20000.0,
                 min_circularity=0.5,
                 debug=False):
        self.blur_ksize = blur_ksize
        self.morph_ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_kernel)
        self.min_area = min_area
        self.max_area = max_area
        self.min_circ = min_circularity
        self.debug = debug

    def __preprocess(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, self.blur_ksize, 0)
        if self.debug:
            cv2.imshow("Gray-Blur", blur)
        return blur

    def __segment(self, gray):
        _, binar = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        clean = cv2.morphologyEx(binar, cv2.MORPH_OPEN, kernel, iterations=1)
        clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel, iterations=2)
        clean = self.__remove_small_objects(clean, min_size=80)
        if self.debug:
            cv2.imshow("Binary", binar)
            cv2.imshow("Morph-Clean", clean)
        return clean

    def __remove_small_objects(self, mask, min_size):
        components, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        out = np.zeros_like(mask)
        for i in range(1, components):
            if stats[i, cv2.CC_STAT_AREA] >= min_size:
                out[labels == i] = 255
        return out

    def __annotate(self, img, contours):
        output = img.copy()
        for idx, cnt in enumerate(contours, start=1):
            (x, y), r = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            cv2.circle(output, center, int(r), (0, 255, 0), 2)
            cv2.putText(output, str(idx), (center[0] - 10, center[1] + int(r) + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        return output

    def detect_cells(self, imgs):
        print("SimpleSearchCells start!")
        if not isinstance(imgs, dict):
            raise TypeError(f"Expected dict, got {type(imgs).__name__}")

        results = []
        orig_cwd = os.getcwd()
        for path, files in imgs.items():
            if not isinstance(path, str):
                warnings.warn(f"Skipping non-string path key: {path}")
                continue
            if not os.path.isdir(path):
                warnings.warn(f"Directory does not exist: {path}")
                continue
            if not isinstance(files, (list, tuple)):
                warnings.warn(f"Expected list of files for path {path}, got {type(files).__name__}")
                continue

            try:
                os.chdir(path)
                for fname in files:
                    if not isinstance(fname, str):
                        warnings.warn(f"Skipping non-string filename: {fname}")
                        continue
                    full_path = os.path.join(path, fname)
                    if not os.path.isfile(full_path):
                        warnings.warn(f"File not found: {full_path}")
                        continue

                    img = cv2.imread(full_path)
                    if img is None:
                        warnings.warn(f"Failed to load image: {full_path}")
                        continue

                    processed = self.__preprocess(img)
                    mask = self.__segment(processed)
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    annotated = self.__annotate(img, contours)
                    count = len(contours)
                    results.append((full_path, count, annotated))

                    if self.debug:
                        cv2.imshow("Result", annotated)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
            finally:
                os.chdir(orig_cwd)

        print("SimpleSearchCells end!")
        return results


if __name__ == "__main__":
    counter = SimpleSearchCells(
        blur_ksize=(5, 5),
        morph_kernel=(5, 5),
        min_area=100,
        max_area=8000,
        min_circularity=0.3,
        debug=True
    )
    inputs = {r"C:\Files\VSC\proj\data": ["test_simple_val.png", "test_val.png"]}
    results = counter.detect_cells(inputs)
    for path, (cnt, vis) in results:
        print(f"{path}: найдено объектов: {cnt}")