import numpy as np
from PIL import Image
import pillow_avif
from exception import Empty_file_path

class Image_container():
  def __init__(self, width, height, img):
    self.__width = width
    self.__height = height
    self.__img = img

  def get_size(self):
    return self.__width, self.__height
  
  def get_img(self):
    return self.__img
  
class Color_image(Image_container):
  def __init__(self, filepath=None):
    if filepath == None:
      raise Empty_file_path("Color_image: empty file path!")
    else:
      with Image.open(filepath, "r") as img:
        w, h = img.size
        Image_container.__init__(self, w, h, img)

class Monochrom_image(Image_container):
  def __init__(self, filepath=None):
    if filepath == None:
      raise Empty_file_path("Monochrom_image: empty file path!")
    else:
      with Image.open(filepath, "r") as img:
        w, h = img.size
        Image_container.__init__(self, w, h, img)

class Black_white_image(Image_container):
  def __init__(self, filepath=None):
    if filepath == None:
      raise Empty_file_path("Black_white_image: empty file path!")
    else:
      with Image.open(filepath, "r") as img:
        w, h = img.size
        Image_container.__init__(self, w, h, img)