import customtkinter as ctk
import tkinter as tk
import os
import cv2
from PIL import Image


class Gallery_win(ctk.CTkToplevel):
  def __init__(self, root, data):
    super().__init__(root)

    self.__data = data
    self.__curr_img_idx = 0
    self.__curr_img_dir = list(self.__data.keys())[0]

    self.__init_win()
    self.__init_combobox()
    self.__init_img_field()
    self.__init_controle_btns()

  def __init_win(self):
    self.title("View images")
    self.minsize(width=900, height=700)
    ctk.set_appearance_mode("system")

  def __init_combobox(self):
    labels = [elem[(elem.rfind('/') + 1):] for elem in self.__data.keys()]
    self.__dir_cmbbx = ctk.CTkComboBox(master=self, values=labels, 
                                       justify="center", command=self.__set_dir)
    self.__dir_cmbbx.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                          ipady=3, expand=False)
    
  def __init_img_field(self):
    self.__name_lbl = ctk.CTkLabel(master=self, 
                                   text=self.__data[self.__curr_img_dir]
                                   [self.__curr_img_idx], justify="center")
    self.__name_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                         ipady=3, expand=False)
    
    self.__img_fld = ctk.CTkLabel(master=self, image=self.__get_img(), text='')
    self.__img_fld.pack(side="top", fill="both", padx=3, pady=3, ipadx=3,
                        ipady=3, expand=True)

  def __init_controle_btns(self):
    btns_frm = ctk.CTkFrame(master=self)
    btns_frm.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                  ipady=3, expand=False)

    prev_btn = ctk.CTkButton(master=btns_frm, text="\u21E6",
                             command=self.__set_prev)
    prev_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                  ipady=3, expand=True)
    
    reduce_btn = ctk.CTkButton(master=btns_frm, 
                               text="Уменьшить изображение",
                               command=self.__reduce)
    reduce_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                    ipady=3, expand=True)
    
    def_btn = ctk.CTkButton(master=btns_frm,
                            text="Вернуть исходный размер",
                            command=self.__set_def_imgsz)
    def_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                 ipady=3, expand=True)
    
    increase_btn = ctk.CTkButton(master=btns_frm, 
                                 text="Увеличить изображение",
                                 command=self.__increase)
    increase_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                      ipady=3, expand=True)
    
    next_btn = ctk.CTkButton(master=btns_frm, text="\u21E8",
                             command=self.__set_next)
    next_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                  ipady=3, expand=True)
    

    self.__setimg_lbl = ctk.CTkLabel(master=self,
                                     text="Всего изображений - "
                                     f"{len(self.__data[self.__curr_img_dir])}."
                                     " перейти к изображению номер:")
    self.__setimg_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                           ipady=3, expand=False)

    chimg_frm = ctk.CTkFrame(master=self)
    chimg_frm.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                   ipady=3, expand=False)
    
    self.__idx_ent = ctk.CTkEntry(master=chimg_frm, 
                                  placeholder_text="Номер изображения", 
                                  text_color="white", justify="center")
    self.__idx_ent.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                        ipady=3, expand=True)
    
    idx_btn = ctk.CTkButton(master=chimg_frm, text="Перейти",
                            command=self.__set_img)
    idx_btn.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                 ipady=3, expand=False)
    
  def __set_dir(self, choice):
    for key in list(self.__data.keys()):
      if choice in key:
        self.__curr_img_dir = key
        break
    self.__curr_img_idx = 0

    self.__setimg_lbl.configure(text="Всего изображений - "
                                     f"{len(self.__data[self.__curr_img_dir])}."
                                     " перейти к изображению номер:")

    self.__name_lbl.configure(text=self.__data[self.__curr_img_dir]
                              [self.__curr_img_idx])
    self.__img_fld.configure(image=self.__get_img())

  def __set_img(self):
    try:
      idx = int(self.__idx_ent.get())

      if idx <= len(self.__data[self.__curr_img_dir]):
        self.__curr_img_idx = idx - 1
        self.__name_lbl.configure(text=self.__data[self.__curr_img_dir]
                                  [self.__curr_img_idx])
        self.__img_fld.configure(image=self.__get_img())
    except ValueError:
      tk.messagebox.showerror(title="Ошибка", 
                              message="Номер изображения должен быть числом!")

  def __get_img(self):
    os.chdir(self.__curr_img_dir)
    img = cv2.imread(self.__data[self.__curr_img_dir][self.__curr_img_idx])
    self.__def_h, self.__def_w = img.shape[:2]
    self.__curr_h, self.__curr_w = self.__def_h, self.__def_w
    pil_img = Image.fromarray(img)
    self.__curr_img = pil_img
    img = ctk.CTkImage(dark_image=pil_img, size=(self.__curr_w,
                                                      self.__curr_h))
    
    return img
    
  def __set_next(self):
    if self.__curr_img_idx < (len(self.__data[self.__curr_img_dir]) - 1):
      self.__curr_img_idx += 1
    else:
      self.__curr_img_idx = 0

    self.__name_lbl.configure(text=self.__data[self.__curr_img_dir]
                              [self.__curr_img_idx])
    self.__img_fld.configure(image=self.__get_img())

  def __set_prev(self):
    if self.__curr_img_idx != 0:
      self.__curr_img_idx -= 1
    else:
      self.__curr_img_idx = len(self.__data[self.__curr_img_dir]) - 1

    self.__name_lbl.configure(text=self.__data[self.__curr_img_dir]
                              [self.__curr_img_idx])
    self.__img_fld.configure(image=self.__get_img())

  def __increase(self):
    self.__curr_h += int(self.__curr_h * 0.5)
    self.__curr_w += int(self.__curr_w * 0.5)
    img = ctk.CTkImage(dark_image=self.__curr_img, size=(self.__curr_w,
                                                         self.__curr_h))
    self.__img_fld.configure(image=img)

  def __reduce(self):
    self.__curr_h -= int(self.__curr_h * 0.5)
    self.__curr_w -= int(self.__curr_w * 0.5)
    img = ctk.CTkImage(dark_image=self.__curr_img, size=(self.__curr_w,
                                                         self.__curr_h))
    self.__img_fld.configure(image=img)

  def __set_def_imgsz(self):
    self.__curr_h = self.__def_h
    self.__curr_w = self.__def_w
    img = ctk.CTkImage(dark_image=self.__curr_img, size=(self.__def_w, 
                                                         self.__def_h))
    self.__img_fld.configure(image=img)


