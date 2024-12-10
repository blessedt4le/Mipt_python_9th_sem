import os

from Image_processor.augmentator import Augmentator
from Load.download_images import Download_data
from Load.upload_images import Upload_images
import Tools.exception as exception
from Tools.imgs_container import Imgs_container
from Tools.singleton import singleton

@singleton
class Command_handler:
  def __init__(self):
    self.__data = Imgs_container()
    self.__aug_data = Imgs_container()
    self.__newdata = False
    self.__dirpath = None

  def download_images(self, dirpath):
    if not os.path.isdir(dirpath):
      raise exception.Invalid_dirpath(dirpath=dirpath)
    elif self.__dirpath != dirpath:
      self.__dirpath = dirpath
      self.__newdata = True
      self.__data.imgs = Download_data.download_images(dirpath)

  def get_images(self):
    return self.__data.imgs
  
  def augmintate_imgs(self, mean=[0, 0], std=[25, 25], out_img_num=1):
    if not isinstance(mean[0], int) or not isinstance(mean[1], int):
      raise exception.Invalid_arg_type(mess="'cеднее значение гауссовского \
                                       распределения'")
    elif not isinstance(std[0], int) or not isinstance(std[1], int):
      raise exception.Invalid_arg_type(mess="'cтандартное отклонение \
                                       гауссовского распределения'")
    elif not isinstance(out_img_num, int):
      raise exception.Invalid_arg_type(mess="'раздутие одного фото'")
    elif not 0 <= mean[0] <= mean[1]:
      raise exception.Invalid_arg_range(mess="'cеднее значение гауссовского \
                                        распределения'")
    elif not 0 <= std[0] <= std[1]:
      raise exception.Invalid_arg_range(mess="'cтандартное отклонение \
                                        гауссовского распределения'")
    elif not out_img_num > 0:
      raise exception.Invalid_arg_range(mess="'раздутие одного фото'")
    else:
      if self.__newdata:
        self.__newdata = False
        self.__augmintate_imgs(mean, std, out_img_num)

  def __augmintate_imgs(self, mean=[0, 0], std=[25, 25], out_img_num=1):
    aug_data = dict()
    for key, elem in self.__data.imgs.items():
      aug_data[key] = list()
      for img in elem:
        aug_data[key].append(img)
        aug_data[key].extend(Augmentator.augmentate_img(img, mean, std, 
                                                        out_img_num))
    self.__aug_data.imgs = aug_data
        
  def get_augmentation_images(self):
    return self.__aug_data.imgs
  
  def upload_images(self, savepath):
    Upload_images.upload_images(self.__aug_data.imgs, savepath)

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
if __name__ == "__main__":
  obj = Command_handler()
  try:
    obj.download_images("C:/Users/looki/Space/Institute/МФТИ/Python/Dev/Finale_prj/Kuliaev_SM_412S/Data")
    obj.augmintate_imgs([0, 0], [25, 50], 3)
    obj.upload_images("C:/Users/looki/Space/Institute/МФТИ/Python/Dev/Finale_prj/Kuliaev_SM_412S/Aug_data")
  except exception.Invalid_dirpath as exc:
    print(exc)
