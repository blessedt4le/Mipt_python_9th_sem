import cv2
import numpy as np
import math
from typing import Tuple, List

class SimpleSearchCells:
    def __init__(self,
                 blur_ksize: Tuple[int,int]=(5,5),
                 morph_kernel: Tuple[int,int]=(3,3),
                 min_area: float=100.0,
                 max_area: float=20000.0,
                 min_circularity: float=0.5,
                 debug: bool=False):
        self.blur_ksize = blur_ksize
        self.morph_ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_kernel)
        self.min_area = min_area
        self.max_area = max_area
        self.min_circ = min_circularity
        self.debug = debug

    def preprocess(self, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, self.blur_ksize, 0)
        if self.debug:
            cv2.imshow("1_gray_blur", blur)
        return blur

    def segment(self, gray: np.ndarray) -> np.ndarray:
        _, binar = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )

        ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        clean = cv2.morphologyEx(binar, cv2.MORPH_OPEN, ker, iterations=1)
        clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, ker, iterations=2)
        clean = self.remove_small_objects(clean, min_size=80)

        if self.debug:
            cv2.imshow("2_binar", binar)
            cv2.imshow("3_morph_clean", clean)
        return clean

    @staticmethod
    def remove_small_objects(mask: np.ndarray, min_size: int) -> np.ndarray:
        nb, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
        out = np.zeros_like(mask)
        for i in range(1, nb):
            if stats[i, cv2.CC_STAT_AREA] >= min_size:
                out[labels == i] = 255
        return out

    def find_and_filter(self, mask: np.ndarray) -> List[np.ndarray]:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # TODO: fix the filtering algorithm
        # good = []
        # for cnt in contours:
        #     area = cv2.contourArea(cnt)
        #     if area < self.min_area or area > self.max_area:
        #         continue
        #     peri = cv2.arcLength(cnt, True)
        #     if peri <= 0:
        #         continue
        #     circ = 4 * math.pi * area / (peri * peri)
        #     if circ < self.min_circ:
        #         continue
        #     good.append(cnt)
        # if self.debug:
        #     print(f"Всего контуров: {len(contours)}, отфильтровано: {len(good)}")

        return contours

    def annotate(self, img: np.ndarray, contours: List[np.ndarray]) -> np.ndarray:
        out = img.copy()
        for i, cnt in enumerate(contours, 1):
            (x,y), r = cv2.minEnclosingCircle(cnt)
            c = (int(x), int(y))
            cv2.circle(out, c, int(r), (0,255,0), 2)
            cv2.putText(out, str(i), (c[0]-10, c[1]+int(r)+12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        return out

    def get(self, img: np.ndarray) -> Tuple[int, np.ndarray]:
        pre = self.preprocess(img)
        mask = self.segment(pre)
        good = self.find_and_filter(mask)
        vis = self.annotate(img, good)
        if self.debug:
            cv2.imshow("4_result", vis)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return len(good), vis

if __name__ == "__main__":
    counter = SimpleSearchCells(
        blur_ksize=(5,5),
        morph_kernel=(5,5),
        min_area=100,
        max_area=8000,
        min_circularity=0.3,
        debug=True
    )
    img = cv2.imread(r"C:\Files\VSC\proj\data\test_simple_val.png")
    count, vis = counter.get(img)
    print(f"Найдено объектов: {count}")