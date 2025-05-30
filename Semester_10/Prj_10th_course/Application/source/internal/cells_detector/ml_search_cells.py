import os
import cv2
import numpy as np
import warnings
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import sobel

class MlSearchCells:
    def __init__(self,
                 patch_size=20,
                 step=8,
                 n_clusters=2,
                 min_cell_area=160,
                 debug=False):
        self.patch_size = patch_size
        self.step = step
        self.n_clusters = n_clusters
        self.min_cell_area = min_cell_area
        self.debug = debug

    def __glcm_features(self, patch):
        glcm = graycomatrix(patch, distances=[1], angles=[0], symmetric=True, normed=True)
        return [
            graycoprops(glcm, 'contrast')[0, 0],
            graycoprops(glcm, 'homogeneity')[0, 0],
            graycoprops(glcm, 'energy')[0, 0]
        ]

    def __histogram_features(self, patch, bins=8):
        hist = cv2.calcHist([patch], [0], None, [bins], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist.tolist()

    def __gradient_feature(self, patch):
        grad = sobel(patch)
        return [np.mean(grad), np.std(grad)]

    def __extract_all_features(self, patch):
        feats = []
        feats.extend(self.__glcm_features(patch))
        feats.extend(self.__histogram_features(patch))
        feats.extend(self.__gradient_feature(patch))
        return feats

    def __sliding_window_features(self, img):
        h, w = img.shape[:2]
        X, positions = [], []
        for i in range(0, h - self.patch_size + 1, self.step):
            for j in range(0, w - self.patch_size + 1, self.step):
                patch = img[i:i+self.patch_size, j:j+self.patch_size]
                feats = self.__extract_all_features(patch)
                X.append(feats)
                positions.append((i, j))
        return np.array(X), positions

    def __create_cluster_mask(self, shape, positions, labels, target_label):
        mask = np.zeros(shape, dtype=np.uint8)
        for (i, j), lbl in zip(positions, labels):
            if lbl == target_label:
                mask[i:i+self.patch_size, j:j+self.patch_size] = 1
        return mask

    def __preprocess_mask(self, mask):
        ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        cleaned = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, ker, iterations=2)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, ker, iterations=1)
        return cleaned

    def __count_cells(self, mask):
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
        final_mask = np.zeros_like(labels, dtype=np.uint8)
        count = 0
        for lbl in range(1, num_labels):
            area = stats[lbl, cv2.CC_STAT_AREA]
            if area >= self.min_cell_area:
                final_mask[labels == lbl] = lbl
                count += 1
        return final_mask, count

    def detect_cells(self, imgs):
        print("MlSearchCells start!")
        if not isinstance(imgs, dict):
            raise TypeError(f"Expected dict, got {type(imgs).__name__}")

        results = []
        orig_cwd = os.getcwd()
        for path, files in imgs.items():
            if not isinstance(path, str):
                warnings.warn(f"Skipping non-string directory: {path}")
                continue
            if not os.path.isdir(path):
                warnings.warn(f"Directory does not exist: {path}")
                continue
            if not isinstance(files, (list, tuple)):
                warnings.warn(f"Expected list of filenames for {path}")
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

                    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        warnings.warn(f"Failed to load image: {full_path}")
                        continue

                    # Pipeline
                    feats, positions = self.__sliding_window_features(img)
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(feats)
                    kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10).fit(X_scaled)
                    labels = kmeans.labels_
                    unique, counts = np.unique(labels, return_counts=True)
                    target = unique[np.argmin(counts)]

                    mask = self.__create_cluster_mask(img.shape, positions, labels, target)
                    mask = self.__preprocess_mask(mask)
                    final_mask, cell_count = self.__count_cells(mask)

                    results.append((full_path, cell_count, final_mask))

                    if self.debug:
                        plt.figure(figsize=(12, 4))
                        plt.subplot(1, 3, 1); plt.title("Original"); plt.imshow(img, cmap="gray")
                        plt.subplot(1, 3, 2); plt.title("Mask"); plt.imshow(mask, cmap="gray")
                        plt.subplot(1, 3, 3); plt.title(f"Count: {cell_count}"); plt.imshow(final_mask, cmap="nipy_spectral")
                        plt.tight_layout(); plt.show()

            finally:
                os.chdir(orig_cwd)

        print("MlSearchCells end!")
        return results

if __name__ == "__main__":
    counter = MlSearchCells(debug=False)
    inputs = {r"C:\Files\VSC\proj\data": ["test_simple_val.png", "test_val.png"]}
    results = counter.detect_cells(inputs)
    for path, cnt, mask in results:
        print(f"{path}: найдено клеток: {cnt}")