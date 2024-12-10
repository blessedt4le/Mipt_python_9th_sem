import cv2
import os
import numpy as np

from Tools.exception import Invalid_dirpath

class Download_data:
  @staticmethod
  def download_images(dirpath):
    data = dict()
    for root, dirs, files in os.walk(dirpath):
      if len(files) != 0:
        label = root[(root.rfind('\\') + 1):]
        data[label] = list()
      for file in files:
        os.chdir(root)
        src_image = cv2.imread(file)
        gray_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
        data[label].append(gray_image)

    return data