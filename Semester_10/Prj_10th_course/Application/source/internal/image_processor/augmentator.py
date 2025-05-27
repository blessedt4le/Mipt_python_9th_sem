import cv2
import numpy as np
import os
import random
import shutil

from internal.tools.save2tmp import Save2tmp
from internal.tools.tmp_if import Tmp_if


class Noisemaker:
  @staticmethod
  def noise(img, noise_param, oni):
    means = np.linspace(noise_param["mean"][0], noise_param["mean"][1], 
                        oni, endpoint=True)
    stds = np.linspace(noise_param["std"][0], noise_param["std"][1], 
                       oni, endpoint=True)
    return [Noisemaker.add_noise2img(img, means[idx], stds[idx]) 
            for idx in range(oni)]

  @staticmethod
  def add_noise2img(img, mean=0, std=25):
    row, col = img.shape
    gauss = np.random.normal(mean, std, (row, col))
    gauss_noise = gauss.reshape(row, col)
    img_noise = img + gauss_noise
    return img_noise
  

class Noisedeleter:
  @staticmethod
  def delete_noise(img, ratio):
    height, width = img.shape[:2]
    kernel_size = int(min(height, width) * ratio)
    if kernel_size % 2 == 0:
      kernel_size += 1
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
  

class Rotator:
  @staticmethod
  def rotate(img, angl_rng, oni):
    angls = np.linspace(angl_rng[0], angl_rng[1], oni, endpoint=True)
    return [Rotator.rotate2angl(img, angls[idx]) for idx in range(oni)]
  
  def rotate2angl(img, angl):
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angl, 1.0)
    return cv2.warpAffine(img, rotation_matrix, (width, height))
  

class Reflector:
  @staticmethod
  def reflect(img):
    return [cv2.flip(img, 1), cv2.flip(img, 0), cv2.flip(img, -1)]
  

class Reshaper:
  @staticmethod
  def reshape(img):
    rsh_coeff = random.randint(1, 20) / 10
    return cv2.resize(img, None, fx=rsh_coeff, fy=rsh_coeff)
  

class Augmentator:
  @staticmethod
  def augmentate(imgs, params):
    os.chdir(Tmp_if().tmp[:Tmp_if().tmp.rfind('/')])
    Tmp_if().clear()
    for key, elem in imgs.items():
      idx = 0
      lable = key[(key.rfind('/') + 1):]
      tmppath = Tmp_if().tmp + '/' + lable
      os.makedirs(tmppath, exist_ok=True)
      for img in elem:
        os.chdir(key)
        src_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        idx = Save2tmp.save2tmp(idx, Augmentator.augmentate_img(src_img, 
                                                                params), 
                                tmppath, lable)

  @staticmethod
  def save_aug2tmp(idx, aug_imgs, tmppath, lable):
    os.chdir(tmppath)

    for elem in aug_imgs:
      cv2.imwrite(lable + '_' + str(idx) + ".jpg", elem)
      idx += 1
    
    return idx

  @staticmethod
  def augmentate_img(src_img, params):
    aug_img = list()
    if "noise" in params.keys():
      aug_img = Noisemaker.noise(src_img, params["noise"], params["oni"])

    if "delete_noise" in params.keys():
      aug_img = Augmentator.delete_noise(src_img, aug_img, params["ratio"],
                                         params["mode"])

    if "angle" in params.keys():
      aug_img = Augmentator.rotate(src_img, aug_img, params["angle"], params["oni"],
                                   params["mode"])

    if "mirror" in params.keys():
      aug_img = Augmentator.reflect(src_img, aug_img, params["mode"])

    if "resize" in params.keys():
      aug_img = Augmentator.reshape(src_img, aug_img, params["mode"])

    aug_img.insert(0, src_img)

    return aug_img
  
  @staticmethod
  def delete_noise(src_img, imgs, ratio, mode):
    aug_img = [Noisedeleter.delete_noise(src_img, ratio)]

    if mode:
      for img in imgs:
        aug_img.append(img)
        aug_img.append(Noisedeleter.delete_noise(img, ratio))
    else:
      aug_img.extend(imgs)

    return aug_img
  
  @staticmethod
  def rotate(src_img, imgs, angl_rng, oni, mode):
    aug_img = [*Rotator.rotate(src_img, angl_rng["angl_rng"], oni)]

    if mode:
      for img in imgs:
        aug_img.append(img)
        aug_img.extend(Rotator.rotate(img, angl_rng["angl_rng"], oni))
    else:
      aug_img.extend(imgs)

    return aug_img
  
  @staticmethod
  def reflect(src_img, imgs, mode):
    aug_img = [*Reflector.reflect(src_img)]

    if mode:
      for img in imgs:
        aug_img.append(img)
        aug_img.extend(Reflector.reflect(img))
    else:
      aug_img.extend(imgs)

    return aug_img
  
  @staticmethod
  def reshape(src_img, imgs, mode):
    aug_img = [Reshaper.reshape(src_img)]
    
    if mode:
      for img in imgs:
        aug_img.append(img)
        aug_img.append(Reshaper.reshape(img))
    else:
      aug_img.extend(imgs)

    return aug_img
