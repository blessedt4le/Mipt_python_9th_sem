import os
import shutil

from internal.tools.singleton import singleton

@singleton
class Tmp_if:
  __dir_name = "tmp_aug"

  def __init__(self):
    self.__tmp_dir = os.path.dirname(os.path.abspath(__file__)) \
      .replace('\\', '/') + '/' + self.__dir_name
    os.makedirs(self.__tmp_dir, exist_ok=True)

  @property
  def tmp(self):
    return self.__tmp_dir
  
  def clear(self):
    for item in os.listdir(self.__tmp_dir):
      item_path = os.path.join(self.__tmp_dir, item)
      if os.path.isfile(item_path) or os.path.islink(item_path):
        os.unlink(item_path)
      elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

  def __del__(self):
    if os.path.isdir(self.__tmp_dir):
      shutil.rmtree(self.__tmp_dir)

if __name__ == "__main__":
  Tmp_if()