import os
from natsort import natsorted

class Download_data:
  @staticmethod
  def download_images(dirpath):
    data = dict()
    for root, dirs, files in os.walk(dirpath):
      if len(files) != 0:
        lable = root.replace('\\', '/')
        data[lable] = natsorted(files)

    return data