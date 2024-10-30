class Except(BaseException):
  def __init__(self, message):
    self.__msg = message

  def get_message(self):
    return self.__msg