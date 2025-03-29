class Imgs_container:
  def __init__(self):
    self.__data = None

  @property
  def imgs(self):
    return self.__data

  @imgs.setter
  def imgs(self, data):
    self.__data = data
