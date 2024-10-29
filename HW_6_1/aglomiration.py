from city import City

class Aglomiration:
  def __init__(self, name, count):
    self.__name = name
    self.__resids_max_count = count
    self.__resids_curr_count = 0
    self.__agl_citys = list()
    self.__agl_residents = list()

  def add_city(self, name, count):
    if (self.__resids_curr_count + count) > self.__resids_max_count:
      city = City(name, count)
      self.__agl_citys.append(city)
    else:
      pass

  def add_person(self, city_name, name, surname, midname):
    for city in self.__agl_citys:
      if city_name == city.get_name():
        pers = city.add_person(name, surname, midname)
        if pers != None:
          self.__agl_residents.append(pers)
        break

  def remove_person(self, name, surname, midname):
    for city in self.__agl_citys:
      pers = city.remove_person(name, surname, midname)
      if pers != None:
        self.__agl_residents.remove(pers)
      break
