from aglomiration import Aglomiration

if __name__ == "__main__":
  inp = input("Enter aglomiration name and residents count: ").split()
  agl = Aglomiration(inp[0], int(inp[1]))
  while True:
    inp = input("Enter city name and residents count: ")

    if inp == "end":
      break

    inp = inp.split()
    city_name = inp[0]
    agl.add_city(inp[0], int(inp[1]))

    while True:
      inp = input("Enter resident info: ")
      if inp == "end":
        break
      else:
        inp = inp.split()
        agl.add_person(city_name, inp[0], inp[1], inp[2])
    
    