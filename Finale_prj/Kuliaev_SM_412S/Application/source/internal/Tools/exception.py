class Invalid_dirpath(Exception):
  def __init__(self, *args, dirpath=None):
    super().__init__(args)
    self.__dirpath = dirpath

  def __str__(self):
    ret_mess = None
    if self.__dirpath is not None:
      ret_mess = f'Директории "{self.__dirpath}" не существует!'
    else:
      ret_mess = super().__str__()
    return ret_mess
  
class Invalid_arg_type(Exception):
  def __init__(self, *args, mess=None):
    super().__init__(args)
    self.__mess = mess

  def __str__(self):
    ret_mess = None
    if self.__mess is not None:
      ret_mess = f'Переменная "{self.__dirpath}" не число!'
    else:
      ret_mess = super().__str__()
    return ret_mess
  
class Invalid_arg_range(Exception):
  def __init__(self, *args, mess=None):
    super().__init__(args)
    self.__mess = mess

  def __str__(self):
    ret_mess = None
    if self.__mess is not None:
      ret_mess = f'Переменная "{self.__dirpath}" имеет не корректный диапазон!'
    else:
      ret_mess = super().__str__()
    return ret_mess
  
if __name__ == "__main__":
  try:
    raise Invalid_dirpath("error")
  except Invalid_dirpath as exc:
    print(exc)