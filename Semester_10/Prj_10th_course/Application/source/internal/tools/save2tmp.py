import os
import cv2

class Save2tmp:
  @staticmethod
  def save2tmp(idx, imgs, tmppath, lable=None):
    os.chdir(tmppath)

    for elem in imgs:
      cv2.imwrite((lable + '_') if lable != None else "" + str(idx) + ".jpg", elem)
      idx += 1
    
    return idx