class Family:
  def __init__(self, husband, wife):
    print(f"Family {husband} {wife} create!")
    self.__family = husband.split()[1]
    self.__husband = husband
    self.__wife = wife
    self.__childs = list()

  def add_child(self, child):
    print(f"Child {child} add!")
    self.__childs.append(child)

  def get_name(self):
    return self.__family