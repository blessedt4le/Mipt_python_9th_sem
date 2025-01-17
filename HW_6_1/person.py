class Person:
  def __init__(self, city, name, surname, midname):
    print(f"Creation person with name {name} {surname} {midname} is in process")
    self.__name = name
    self.__surname = surname
    self.__middle_name = midname
    self.__city = city

  def get_person(self):
    return list(self.__name, self.__surname, self.__middle_name)
  
  def get_city_name(self):
    return self.__city

  def __str__(self):
    return f"{self.__name} {self.__surname} {self.__middle_name}"
  
  def __del__(self):
    print(f"Person {self.__name} {self.__surname} {self.__middle_name} was " + 
          "removed")