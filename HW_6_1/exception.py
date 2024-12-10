class Invalid_dirpath(Exception):
  def __init__(self, *args, dirpath=None):
    super().__init__(args)
    self.__dirpath = dirpath

  def __str__(self):
    ret_mess = None
    if self.__dirpath is not None:
      ret_mess = f"not existed dir {self.__dirpath}"
    else:
      ret_mess = super().__str__()
    return ret_mess
  
if __name__ == "__main__":
  try:
    raise Except("error")
  except Except as exc:
    print(exc)