import cv2
import os
import shutil

from internal.tools.tmp_if import Tmp_if

class Upload_images:
  @staticmethod
  def upload_images(savepath):
    if os.path.isdir(savepath):
      shutil.rmtree(savepath)
    shutil.copytree(Tmp_if().tmp, savepath)
