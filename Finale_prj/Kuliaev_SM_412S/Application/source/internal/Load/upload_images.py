import cv2
import os

class Upload_images:
  @staticmethod
  def upload_images(images, savepath):
    for key, val in images.items():
      save_dir = savepath + "/" + key
      os.makedirs(save_dir, exist_ok=True)
      cnt = 0
      for img in val:
        os.chdir(save_dir)
        save_path = key + '_' + str(cnt) + ".jpg"
        cv2.imwrite(save_path, img)
        cnt += 1