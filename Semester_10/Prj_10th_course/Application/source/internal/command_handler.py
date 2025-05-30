import os
from pathlib import Path
import threading
import tkinter as tk

from internal.cells_detector.CNN import CNN
from internal.cells_detector.ml_search_cells import MlSearchCells
from internal.cells_detector.simple_search_cells import SimpleSearchCells

from internal.db.db import DB

from internal.image_processor.augmentator import Augmentator
from internal.image_processor.generator import Image_generator

from internal.load.download_images import Download_data
from internal.load.upload_images import Upload_images

import internal.tools.exception as exception
from internal.tools.imgs_container import Imgs_container
from internal.tools.singleton import singleton
from internal.tools.tmp_if import Tmp_if

@singleton
class Command_handler:
  def __init__(self, logbox=None):
    self.__logbox = logbox
    self.__data = Imgs_container()
    self.__aug_data = Imgs_container()
    self.__tmp_if = Tmp_if()
    self.__dirpath = None
    self.__algorithms = [SimpleSearchCells(), MlSearchCells(), CNN()]
    DB()
  
  def download(self, dirpath):
    if not os.path.isdir(dirpath):
      raise exception.Invalid_dirpath(dirpath=dirpath)
    elif self.__dirpath != dirpath:
      self.__dirpath = dirpath
      download = threading.Thread(target=self.__download, args=(dirpath,))
      download.start()
      
  def __download(self, dirpath):
    self.__data.imgs = Download_data.download_images(dirpath)

    mess = f"Загружено из директории: \"{dirpath}\"\n" + \
      self.__get_data_info(self.__data.imgs) + '\n'
    self.__update_logbox(mess)

    tk.messagebox.showinfo("Информация", "Загрузка завершена!")

  def generate(self, img_size, nof_imgs, nof_cells):
    err = 0
    try:
      img_size = (int(img_size[0]), int(img_size[1]))
    except ValueError:
      err = 1
      raise exception.Invalid_args_type(param="размер изображения")
    
    if (err == 0):
      try:
        nof_imgs = int(nof_imgs)
      except ValueError:
        err = 1
        raise exception.Invalid_args_type(param="количество изображений")
      
    if (err == 0):
      try:
        nof_cells = int(nof_cells)
      except ValueError:
        err = 1
        raise exception.Invalid_args_type(param="количество клеток")
      
    if err == 0:
      generate = threading.Thread(target=self.__generate, args=(img_size, 
                                                                nof_imgs, 
                                                                nof_cells,))
      generate.start()

  def __generate(self, img_size, nof_imgs, nof_cells):
    Image_generator().generate(img_size, nof_imgs, nof_cells)

    mess = f"Сгенерированы изображения:\n  количество - {nof_imgs}\n" \
       f"  размер - {img_size[0]}x{img_size[1]}\n  количество клеток на " \
       f"изображение - от {nof_cells - 10 if (nof_cells - 10) > 0 else 0} " \
       f"до {nof_cells}\n\n"
    self.__update_logbox(mess)
    tk.messagebox.showinfo("Информация", "Генерация завершена!")

  def detect(self, img_type, methods):
    err = 0
    try:
      img_type = int(img_type)
    except ValueError:
      err = 1
      raise exception.Invalid_args_type(param="размер изображения")
    
    for idx in range(len(methods)):
      try:
        methods[idx] = int(methods[idx])
      except ValueError:
        print(idx)
        err = 1
        raise exception.Invalid_args_type(param="размер изображения")
      
    if err == 0:
      detect = threading.Thread(target=self.__detect, args=(img_type, methods,))
      detect.start()

  def __detect(self, img_type, methods):
    if img_type == 0 and self.__data.imgs != None:
      self.__use_algorithms(self.__data.imgs, methods)
    elif img_type == 1 and Image_generator().get_gens() != None:
      self.__use_algorithms(Image_generator().get_gens(), methods)

  def __use_algorithms(self, imgs, methods):
    res = [None] * 3
    for method in methods:
      res[method] = self.__algorithms[method].detect_cells(imgs)
    print(res)
    DB().update(res)

  def open_db(self):
    open_db = threading.Thread(target=self.__open_db)
    open_db.start()

  def __open_db(self):
    DB().open()

  def copy_db(self, dst_dir):
    copy_db = threading.Thread(target=self.__copy_db, args=(dst_dir,))
    copy_db.start()

  def __copy_db(self, dst_dir):
    print("copy 1")
    DB().copy(dst_dir)

  def get_images(self):
    return self.__data.imgs
  
  def get_generated_images(self):
    return Image_generator().get_gens()
  
  def augmentate(self, **kwargs):
    aug_params = dict()
    err = 0

    if "oni" in kwargs.keys():
      try:
        aug_params["oni"] = int(kwargs["oni"])
        aug_params["mode"] = kwargs["mode"]
      except ValueError:
        err = 1
        raise exception.Invalid_args_type(param="коэффициент аугментации")

    if err == 0 and "noise" in kwargs.keys() and kwargs["noise"]:
      err, aug_params["noise"] = self.__handle_noise(kwargs)

    if err == 0 and "angle" in kwargs.keys() and kwargs["angle"]:
      err, aug_params["angle"] = self.__handle_angle(kwargs["angl_rng"])

    if "delete_noise" in kwargs.keys() and kwargs["delete_noise"]:
      aug_params["delete_noise"] = True
      try:
        aug_params["ratio"] = float(kwargs["ratio"])
      except ValueError:
        err = 1
        raise exception.Invalid_args_type(param="коэффициент размера ядра "
                                          "размытия")

    if "mirror" in kwargs.keys() and kwargs["mirror"]:
      aug_params["mirror"] = True

    if "resize" in kwargs.keys() and kwargs["resize"]:
      aug_params["resize"] = True

    if err == 0 and self.__data.imgs != None \
      and ("mirror" in aug_params or "noise" in aug_params 
           or "angle" in aug_params or "delete_noise" in aug_params
           or "resize" in aug_params):
      augmentate = threading.Thread(target=self.__augmentate, 
                                    args=(aug_params,))
      augmentate.start()
  
  def __handle_noise(self, noise):
    noise_param = dict()
    err = 0

    try:
      noise_param["mean"] = [float(noise["mean"][0]), 
                             float(noise["mean"][1])]
      if not 0 <= noise_param["mean"][0] <= noise_param["mean"][1]:
        err = 1
        raise exception.Invalid_arg_range(param="распределение")
    except ValueError:
      err = 1
      raise exception.Invalid_args_type(param="распределение")
    
    if err == 0:
      try:
        noise_param["std"] = [float(noise["std"][0]), float(noise["std"][1])]
        if not 0 <= noise_param["std"][0] <= noise_param["std"][1]:
          err = 1
          raise exception.Invalid_arg_range(param="отклонение")
      except ValueError:
        err = 1
        raise exception.Invalid_args_type(param="отклонение")
    
    return err, noise_param
  
  def __handle_angle(self, angle):
    angle_param = dict()
    err = 0

    try:
      angle_param["angl_rng"] = [float(angle[0]), 
                                 float(angle[1])]
      if not 0 <= angle_param["angl_rng"][0] <= angle_param["angl_rng"][1]:
        err = 1
        raise exception.Invalid_arg_range(param="распределение")
    except ValueError:
      err = 1
      raise exception.Invalid_args_type(param="распределение")
    
    return err, angle_param
  
  def __augmentate(self, params):
    Augmentator.augmentate(self.__data.imgs, params)
    self.__aug_data.imgs = Download_data.download_images(Tmp_if().tmp)
    mess = f"Результат аугментации:\n" + \
      self.__get_data_info(self.__aug_data.imgs) + '\n'
    self.__update_logbox(mess)

    tk.messagebox.showinfo("Информация", "Аугментация завершена!")

  def get_augmentation_images(self):
    return self.__aug_data.imgs
  
  def upload(self, savepath):
    if savepath == "" or not os.path.isdir(savepath):
      raise exception.Invalid_dirpath(savepath)
    elif not any(Path(self.__tmp_if.tmp).iterdir()):
      raise exception.Aug_data_empty()
    else:
      upload = threading.Thread(target=self.__upload, args=(savepath,))
      upload.start()

  def __upload(self, savepath):
    Upload_images.upload_images(savepath)
    
    mess = f"Сохранено в директорию: \"{savepath}\"\n" + \
      self.__get_data_info(self.__aug_data.imgs) + '\n'
    self.__update_logbox(mess)

    tk.messagebox.showinfo("Информация", "Сохранение завершено!")

  def __get_data_info(self, data):
    imgs_info = ""
    imgs_cnt = 0
    for key, elem in data.items():
      imgs_cnt += len(elem)
      imgs_info += f"  Название лейбла: \"{key[(key.rfind('/') + 1):]}\" - " \
        f"кол-во изображений: {len(elem)}\n"

    mess = f"Всего изображений: {imgs_cnt}\n" + imgs_info
    return mess
  
  def __update_logbox(self, mess):
    self.__logbox.configure(state="normal")
    self.__logbox.insert(tk.END, mess)
    self.__logbox.configure(state="normal")
