import os
import shutil

from internal.tools.singleton import singleton

@singleton
class Tmp_if:
  def __init__(self):
    self.__tmp_dir = os.path.dirname(os.path.abspath(__file__)) \
      .replace('\\', '/') + '/' + "tmp"
    os.makedirs(self.__tmp_dir, exist_ok=True)

  @property
  def tmp(self):
    return self.__tmp_dir

  def __del__(self):
    if os.path.isdir(self.__tmp_dir):
      os.chdir(os.path.dirname(os.path.abspath(__file__)))
      shutil.rmtree(self.__tmp_dir)

if __name__ == "__main__":
  Tmp_if()