import csv
from datetime import datetime
import os
import platform
import shutil
import subprocess

from internal.tools.singleton import singleton

@singleton
class DB():
  __columns = ["№", "Дата", "Путь к изображению", "Результат алгоритма 1", 
               "Результат алгоритма 2", "Результат алгоритма 3"]
  __db_name = "results.csv"

  def __init__(self):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    exist = True if os.path.exists(self.__db_name) else False
    if exist:
      with open(self.__db_name, 'r', newline='', encoding='utf-8') as rcsv:
        reader = csv.reader(rcsv)
        headers = next(reader, None)

        last_row = None
        for row in reader:
          if row:
            last_row = row
        
        if last_row and last_row[0].strip():
          self.__curr_experiment = int(last_row[0]) + 1
        else:
          self.__curr_experiment = 1
    else:
      self.__curr_experiment = 1

    mode = 'a' if exist else 'w'
    self.__wcsv = open(self.__db_name, mode, newline='', encoding='utf-8')
    self.__writer = csv.DictWriter(self.__wcsv, fieldnames=self.__columns)

    if not exist:
      self.__writer.writeheader()
      
  def update(self, results):
    ptrn = dict.fromkeys(self.__columns)

    nof_ress = len(results[0]) if results[0] != None else \
      len(results[1]) if results[1] != None else len(results[2])

    new_rows = []
    for idx in range(nof_ress):
      ptrn["№"] = self.__curr_experiment
      self.__curr_experiment += 1

      ptrn["Дата"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

      ptrn["Путь к изображению"] = results[0][idx][0] if results[0] != None \
        else results[1][idx][0] if results[1] != None else results[2][idx][0]
      
      if results[0] != None:
        ptrn["Результат алгоритма 1"] = results[0][idx][1]
      else:
        ptrn["Результат алгоритма 1"] = "NaN"

      if results[1] != None:
        ptrn["Результат алгоритма 2"] = results[1][idx][1]
      else:
        ptrn["Результат алгоритма 2"] = "NaN"

      if results[2] != None:
        ptrn["Результат алгоритма 3"] = results[2][idx][1]
      else:
        ptrn["Результат алгоритма 3"] = "NaN"

      new_rows.append(ptrn.copy())

    self.__writer.writerows(new_rows)

  def open(self):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    self.__wcsv.close()
    system = platform.system()
    if system == "Windows":
      os.startfile(self.__db_name)
    elif system == "Linux":
      subprocess.run(["xdg-open", self.__db_name])
    self.__wcsv = open(self.__db_name, 'a', newline='', encoding='utf-8')
    self.__writer = csv.DictWriter(self.__wcsv, fieldnames=self.__columns)

  def copy(self, dst_dir):
    if not os.path.exists(dst_dir):
      os.makedirs(dst_dir)
    
    self.__wcsv.close()
    shutil.copy2(os.path.dirname(os.path.abspath(__file__)) + '/' + 
                 self.__db_name, dst_dir)
    self.__wcsv = open(self.__db_name, 'a', newline='', encoding='utf-8')
    self.__writer = csv.DictWriter(self.__wcsv, fieldnames=self.__columns)

  def __del__(self):
    self.__wcsv.close()

if __name__ == "__main__":
  db = DB()
  db.update([[('a', 1), ('b', 10)], [('a', 15), ('b', 35)], None])
  db.copy("/home/kuliaev_s/Space/Institute/МФТИ/Python/Dev/"
          "Mipt_python_9th_sem/Semester_10")