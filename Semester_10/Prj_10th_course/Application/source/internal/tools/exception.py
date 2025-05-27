class Aug_data_empty(Exception):
  def __init__(self, *args, dirpath=None):
    super().__init__(args)

  def __str__(self):
    return "Отсутствуют аугментированные изображения!"

class Invalid_dirpath(Exception):
  def __init__(self, *args, dirpath=None):
    super().__init__(args)
    self.__dirpath = dirpath

  def __str__(self):
    ret_mess = None
    if self.__dirpath != None:
      ret_mess = f'Директории "{self.__dirpath}" не существует!'
    else:
      ret_mess = super().__str__()
    return ret_mess
  
class Invalid_args_type(Exception):
  def __init__(self, *args, param=None):
    super().__init__(args)
    self.__param = param

  def __str__(self):
    ret_mess = None
    if self.__param != None:
      ret_mess = f'Некорректный тип параметра "{self.__param}"!'
    else:
      ret_mess = super().__str__()
    return ret_mess
  
class Invalid_arg_range(Exception):
  def __init__(self, *args, param=None):
    super().__init__(args)
    self.__param = param

  def __str__(self):
    ret_mess = None
    if self.__param != None:
      ret_mess = f'Некорректный диапазон параметра "{self.__param}"!'
    else:
      ret_mess = super().__str__()
    return ret_mess