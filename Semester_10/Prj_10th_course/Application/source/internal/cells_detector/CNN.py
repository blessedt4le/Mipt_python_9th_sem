import cv2
from natsort import natsorted
import os
from ultralytics import YOLO

from internal.tools.singleton import singleton

@singleton
class CNN:
  def __init__(self):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    self.__model = YOLO("blood_cells_11n.pt")

  def detect_cells(self, imgs):
    results = []
    for key, elem in imgs.items():
      for img in elem:
        os.chdir(key)
        ress = self.__model(cv2.imread(img), verbose=False, save=False)
        for res in ress:  
          results.append((key + "/" + img, len(res.boxes)))

    return results

if __name__ == "__main__":
  data = dict()
  for root, dirs, files in os.walk("/home/kuliaev_s/Space/Institute/МФТИ/Python/Dev/Mipt_python_9th_sem/Semester_10/Prj_10th_course/images"):
    if len(files) != 0:
      lable = root.replace('\\', '/')
      data[lable] = natsorted(files)

  model = CNN()
  ret = model.detect_cells({list(data.keys())[0]: [list(data.values())[0][0]]})
  print(f"Result 1:")
  print(*ret, sep='\n')
  ret = model.detect_cells(data)
  print(f"Result 2:")
  print(*ret, sep='\n')