from city import City
from family import Family
from exception import Except

class Aglomiration:
  def __init__(self, name, count):
    self.__name = name
    self.__resids_max_count = count
    self.__resids_curr_count = 0
    self.__agl_citys = list()
    self.__agl_residents = list()
    self.__familys = list()

  def add_city(self, name, count):
    if (self.__resids_curr_count + count) < self.__resids_max_count:
      city = City(name, count)
      self.__agl_citys.append(city)
    else:
      raise Except("Aglomiration overflow!")

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

  def add_family(self, husband, wife, city_n=''):
    husband_ = None
    wife_ = None
    for pers in self.__agl_residents:
      if husband == pers.__str__():
        husband_ = pers
      elif wife == pers.__str__():
        wife_ = pers

    if husband_ != None and wife_ != None:
      family = Family(husband_.__str__(), wife_.__str__())
      self.__familys.append(family)
    elif husband_ != None:
      city_name = husband_.get_city_name()
      for city in self.__agl_citys:
        if city_name == city.get_name():
          person = wife.split()
          pers = city.add_person(person[0], person[1], person[2])
          if pers != None:
            self.__agl_residents.append(pers)
            family = Family(husband_.__str__(), wife)
            self.__familys.append(family)
          break
    elif wife_ != None:
      city_name = wife_.get_city_name()
      for city in self.__agl_citys:
        if city_name == city.get_name():
          person = husband.split()
          pers = city.add_person(person[0], person[1], person[2])
          if pers != None:
            self.__agl_residents.append(pers)
            family = Family(husband, wife_.__str__())
            self.__familys.append(family)
          break
    else:
      if city_n == '':
        raise Except("For family with new persons need hometown!")
      else:
        for city in self.__agl_citys:
          if city_n == city.get_name():
            wife_ = wife.split()
            wife_ = city.add_person(wife_[0], wife_[1], wife_[2])
            if wife_ != None:
              husband_ = husband.split()
              husband_ = city.add_person(husband_[0], husband_[1], husband_[2])
              if husband_ != None:
                self.__agl_residents.append(husband_)
                self.__agl_residents.append(wife_)
                family = Family(husband_.__str__(), wife_.__str__())
                self.__familys.append(family)
              else:
                pers = wife_.get_person()
                pers = city.remove_person(pers[0], pers[1], pers[2])
                self.__agl_residents.remove(pers)
                raise Except("City overflow!")
            else:
              raise Except("City overflow!")
            break
  
  def add_child(self, family_name, child):
    flag = False

    for family in self.__familys:
      if family_name == family.get_name():
        family.add_child(child)
        flag = True

    if not flag:
      raise Except("Incorrect data!")

  def __del__(self):
    for city in self.__agl_citys:
      city.remove_all()
    self.__agl_residents.clear()
