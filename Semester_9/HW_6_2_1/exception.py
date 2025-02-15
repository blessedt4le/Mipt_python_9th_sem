class Empty_file_path(BaseException):
  def __init__(self, err_mess):
    self.__err_msg = err_mess

  def get_err_mess(self):
    return self.__err_msg