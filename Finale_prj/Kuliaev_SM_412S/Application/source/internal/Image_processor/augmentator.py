import cv2
import numpy as np

class Noisemaker:
  @staticmethod
  def add_noise(img, mean=0, std=25):
    row, col = img.shape
    gauss = np.random.normal(mean, std, (row, col))
    gauss_noise = gauss.reshape(row, col)
    img_noise = img + gauss_noise
    return img_noise
  
class Augmentator:
  @staticmethod
  def augmentate_img(img, mean=[0, 0], std=[25, 25], out_img_num=1):
    res_imgs = list()
    if out_img_num == 1:
      res_imgs.append(Noisemaker.add_noise(img, mean[0], std[0]))
    else:
      means = np.linspace(mean[0], mean[1], out_img_num, endpoint=True)
      stds = np.linspace(std[0], std[1], out_img_num, endpoint=True)
      for idx in range(out_img_num):
        res_imgs.append(Noisemaker.add_noise(img, means[idx], stds[idx]))
    return res_imgs

if __name__ == "__main__":
  img = cv2.imread("Data/AnnualCrop/AnnualCrop_1.jpg")
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  noise = Noisemaker.add_noise(img_gray)
  cv2.imwrite("test.jpg", noise)
