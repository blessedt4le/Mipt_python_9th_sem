from person import Person
from exception import Except

class City():
  def __init__(self, name, count):
    self.__name = name
    self.__city_curr_pers_cnt = 0
    self.__city_max_pers_cnt = count
    self.__city_residents = list()


  def add_person(self, name, surname, midname):
    pers = None
    
    if self.__city_curr_pers_cnt < self.__city_max_pers_cnt:
      self.__city_curr_pers_cnt += 1
      pers = Person(self.__name, name, surname, midname)
      self.__city_residents.append(pers)
    else:
      raise Except("City overflow!")

    return pers

  def remove_person(self, name, surname, midname):
    pers = None
    
    for pers in self.__city_residents:
      pers = pers.get_person()
      if pers[0] == name and pers[1] == surname and pers[2] == midname:
        self.__city_residents.remove(pers)
        break

    return pers
  
  def get_name(self):
    return self.__name

  def __str__(self):
    info = "\nCity: "
    info += (self.__name + "\n")
    info += ("City persons coutn: " + str(self.__city_max_pers_cnt))
    for pers in self.__city_residents:
      person = pers.get_person()
      info += (person[0] + ' ' + person[1] + ' ' + person[2] + '\n')
    info += '\n'
    return info
  
  def remove_all(self):
    self.__city_residents.clear()
