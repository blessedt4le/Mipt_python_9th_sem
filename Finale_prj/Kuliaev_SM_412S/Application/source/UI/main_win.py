import tkinter as tk
import customtkinter as ctk

from internal.command_handler import Command_handler
from internal.tools.singleton import singleton
from internal.tools import exception

from ui.augmentation_win import Augmentation_win
from ui.gallery_win import Gallery_win

@singleton
class Main_win(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.__init_win()
    self.__init_btns()
    self.__init_textbox()

    Command_handler(logbox=self.__textbox)

  def __init_win(self):
    self.title("Augmintation app")
    self.minsize(width=800, height=50)
    ctk.set_appearance_mode("system")

  def __init_btns(self):
    btn_frm = ctk.CTkFrame(master=self)
    btn_frm.pack(side="top", fill="both", padx=3, pady=3, expand=False)
    self.__init_download(btn_frm)
    self.__init_aug(btn_frm)

  def __init_download(self, src_frm):
    right_btns = ctk.CTkFrame(master=src_frm)
    right_btns.pack(side="left", fill="both", padx=3, pady=3, expand=True)
    
    self.__download_btn = ctk.CTkButton(master=right_btns, 
                                        text="Загрузить изображения",
                                        command=self.__download_data)
    self.__download_btn.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                             ipady=3, expand=True)

    self.__srcshow_btn = ctk.CTkButton(master=right_btns, 
                                       text="Просмотреть исходные изображения",
                                       command=self.__show_data)
    self.__srcshow_btn.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)

  def __init_aug(self, src_frm):
    left_btns = ctk.CTkFrame(master=src_frm)
    left_btns.pack(side="right", fill="both", padx=3, pady=3, expand=True)
    
    self.__aug_btn = ctk.CTkButton(master=left_btns, 
                                   text="Аугментировать изображения",
                                   command=self.__call_aug_win)
    self.__aug_btn.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                        ipady=3, expand=True)

    self.__augshow_btn = ctk.CTkButton(master=left_btns, 
                                       text="Просмотреть результат аугментации",
                                       command=self.__show_aug_data)
    self.__augshow_btn.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)
    
    self.__aug_save_btn = ctk.CTkButton(master=self, 
                                        text="Сохранить результат аугментации",
                                        command=self.__upload_data)
    self.__aug_save_btn.pack(side="top", fill="x", padx=10, pady=0, ipadx=3,
                             ipady=3, expand=False)
    
  def __call_aug_win(self):
    Augmentation_win(self)

  def __show_data(self):
    data = Command_handler().get_images()
    if data != None:
      Gallery_win(self, data)

  def __show_aug_data(self):
    data = Command_handler().get_augmentation_images()
    if data != None:
      Gallery_win(self, data)

  def __download_data(self):
    dirpath = tk.filedialog.askdirectory()
    try:
      Command_handler().download(dirpath)
    except exception.Invalid_dirpath as exc:
      tk.messagebox.showerror(title="Ошибка", message=exc)

  def __upload_data(self):
    dirpath = tk.filedialog.askdirectory()
    try:
      Command_handler().upload(dirpath)
    except exception.Invalid_dirpath as exc:
      tk.messagebox.showerror(title="Ошибка", message=exc)
    except exception.Aug_data_empty as exc:
      tk.messagebox.showerror(title="Ошибка", message=exc)

  def __init_textbox(self):
    self.__textbox = ctk.CTkTextbox(master=self, width=400, height=300, 
                                    fg_color="white", text_color="black")
    self.__textbox.pack(side="top", fill="both", padx=10, pady=6, ipadx=3,
                        ipady=3, expand=True)