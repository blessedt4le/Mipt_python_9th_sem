import os
import cv2
import random
import numpy as np

from internal.load.download_images import Download_data
from internal.tools.imgs_container import Imgs_container
from internal.tools.save2tmp import Save2tmp
from internal.tools.singleton import singleton
from internal.tools.tmp_gen_if import Tmp_gen_if

@singleton
class Image_generator:
  __dir_name = "Patterns"

  def __init__(self):
    self.__patterns = Download_data.download_images(os.path.dirname(
      os.path.abspath(__file__)).replace('\\', '/') + '/' + self.__dir_name)
    
    self.__ptrns_data = Imgs_container()
    Tmp_gen_if()

  def get_gens(self):
    return self.__ptrns_data.imgs
  
  def clear(self):
    self.__ptrns_data.imgs = None
  
  def generate(self, img_size=(400, 600), nof_imgs=1, nof_cells=50):
    Tmp_gen_if().clear()
    idx = 0
    for _ in range(nof_imgs):
      res_img = self.__generate_img(img_size, nof_cells)
      idx = Save2tmp.save2tmp(idx, [res_img], Tmp_gen_if().tmp)

    self.__ptrns_data.imgs = Download_data.download_images(Tmp_gen_if().tmp)

  
  def __generate_img(self, img_size, nof_cells):
    cells_coords = self.__gen_cells_coords(img_size, random.randint(nof_cells - 10 if (nof_cells - 10) > 0 else 0, 
                                                                    nof_cells))

    os.chdir(list(self.__patterns.keys())[0])
    back_img = cv2.imread(random.choice(self.__patterns[list(self.__patterns.keys())[0]]))

    os.chdir(list(self.__patterns.keys())[1])
    cell_img = cv2.imread(random.choice(self.__patterns[list(self.__patterns.keys())[1]]),
                          cv2.IMREAD_UNCHANGED)

    for idx in range(len(cells_coords)):
      back_img = self.__overlay(img_size, back_img, cell_img, 
                                {"h": cells_coords["h"][idx], 
                                 "w": cells_coords["w"][idx]})
      
    return back_img

  def __gen_cells_coords(self, img_size, nof_cells):
    coords = {"h": [], "w": []}

    for _ in range(nof_cells):
      coords["h"].append(random.randint(0, img_size[0] -
                                        int(img_size[0] * 0.01)))
      coords["w"].append(random.randint(0, img_size[1] -
                                        int(img_size[1] * 0.01)))
      
    return coords
  
  def __overlay(self, img_size, back_img, cell_img, coord):
    scale_coef = round(random.uniform(0.20, 0.05), 2)

    back_img = cv2.resize(back_img, dsize=(img_size[1], 
                                           img_size[0]), 
                          interpolation=cv2.INTER_CUBIC)
    
    size_min = min(img_size)
    cell_h = int(size_min * scale_coef)
    cell_w = int(size_min * scale_coef)
    cell_img = cv2.resize(cell_img, dsize=(cell_w, cell_h),
                          interpolation=cv2.INTER_CUBIC)
    
    cell_img, cell_h, cell_w = self.__rotate_cell(cell_img, cell_h, cell_w)

    down_shift = 0
    if coord["h"] + cell_h > back_img.shape[0]:
      down_shift = coord["h"] + cell_h - back_img.shape[0]
    right_shift = 0
    if coord["w"] + cell_w > back_img.shape[1]:
      right_shift = coord["w"] + cell_w - back_img.shape[1]
    cell_img = cell_img[:cell_h - down_shift, :cell_w - right_shift]
    
    cell_img_rgb = cell_img[:, :, :3]
    cell_img_alpha = cell_img[:, :, 3] / 255.0
    region = back_img[coord["h"]:coord["h"] + cell_h - down_shift, 
                      coord["w"]:coord["w"] + cell_w - right_shift]
    
    for chnl in range(3):
      region[:, :, chnl] = (1.0 - cell_img_alpha) * region[:, :, chnl] + \
        cell_img_alpha * cell_img_rgb[:, :, chnl]
    
    back_img[coord["h"]:coord["h"] + cell_h - down_shift, 
             coord["w"]:coord["w"] + cell_w - right_shift] = region
      
    return back_img
  
  def __rotate_cell(self, cell_img, cell_h, cell_w):
    img_center = (cell_w // 2, cell_h // 2)
    rotate_angle = random.randint(0, 90)
    rotation_matrix = cv2.getRotationMatrix2D(img_center, rotate_angle, 1.0)

    cell_w = int((cell_h * np.abs(rotation_matrix[0, 1])) + \
                 (cell_w * np.abs(rotation_matrix[0, 0])))
    cell_h = int((cell_h * np.abs(rotation_matrix[0, 0])) + \
                 (cell_w * np.abs(rotation_matrix[0, 1])))
    
    rotation_matrix[0, 2] += (cell_w / 2) - img_center[0]
    rotation_matrix[1, 2] += (cell_h / 2) - img_center[1]

    cell_img = cv2.warpAffine(cell_img, rotation_matrix, (cell_w, cell_h))

    return cell_img, cell_h, cell_w