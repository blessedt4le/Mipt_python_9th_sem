from aglomiration import Aglomiration
from exception import Except

if __name__ == "__main__":
  inp = input("Enter aglomiration name and residents count: ").split()
  agl = Aglomiration(inp[0], int(inp[1]))
  while True:
    inp = input("Enter city name and residents count: ")

    if inp == "end":
      break

    inp = inp.split()
    city_name = inp[0]
    try:
      agl.add_city(inp[0], int(inp[1]))
    except Except as error:
      print(error.get_message())
      continue

    while True:
      inp = input("Enter resident info: ")
      if inp == "end":
        break
      else:
        inp = inp.split()
        
        try:
          agl.add_person(inp[0], inp[1], inp[2], inp[3])
        except Except as error:
          print(error.get_message())
          continue

  while True:
    husbend = input("Enter husbend: ")
    wife = input("Enter wife: ")
    city = input("Enter city: ")

    if husbend == "end" or wife == "end" or city == "end":
      break

    try:
      agl.add_family(husbend, wife, city)
    except Except as error:
      print(error.get_message())

  while True:
    family_surname = input("Enter family surname: ")
    child = input("Enter child: ")

    if child == "end" or family_surname == "end":
      break

    try:
      agl.add_child(family_surname, child)
    except Except as error:
      print(error.get_message())