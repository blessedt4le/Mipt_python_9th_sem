import cv2
import os
from ultralytics import YOLO

class CNN:
  def __init__(self):
    os.path.abspath(__file__)
    self.__model = YOLO(r"blood_cells_11n.pt")

  def detect_cells(self):
    pass