import tkinter as tk
import customtkinter as ctk

from internal.command_handler import Command_handler
from internal.tools import exception

class Augmentation_win(ctk.CTkToplevel):
  def __init__(self, root):
    super().__init__(root)

    self.__init_win()
    self.__init_noi()
    self.__init_noise()
    self.__init_dnoise()
    self.__init_angle()
    self.__init_mirror()
    self.__init_resize()
    self.__init_aug()

  def __init_win(self):
    self.title("Augmintation setup")
    self.minsize(width=700, height=200)
    ctk.set_appearance_mode("system")

  def __init_noi(self):
    noi_lbl = ctk.CTkLabel(master=self,
                           text="Коэффициент аугментации",
                           corner_radius=8)
    noi_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                 ipady=3, expand=True)
    
    self.__oni_ent = ctk.CTkEntry(master=self, placeholder_text="1",
                                  text_color="white", justify="center")
    self.__oni_ent.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                        ipady=3, expand=True)
    
  def __init_noise(self):
    noise_lbl = ctk.CTkLabel(master=self,
                             text="Параметры добавления шума",
                             corner_radius=8)
    noise_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                        ipady=3, expand=True)
    

    self.__check_noise = tk.BooleanVar()
    noise_chb = ctk.CTkCheckBox(master=self, text="Добавить шум на фото", 
                                variable=self.__check_noise, onvalue=True, 
                                offvalue=False)
    noise_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                   ipady=3, expand=True)
    

    mean_lbl = ctk.CTkLabel(master=self, 
                            text="Cеднее значение гауссовского распределения", 
                            corner_radius=8)
    mean_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3, ipady=3, 
                  expand=True)
    
    mean_frm = ctk.CTkFrame(master=self)
    mean_frm.pack(side="top", fill="both", padx=0, pady=0, expand=True)

    self.__meanmin_ent = ctk.CTkEntry(master=mean_frm, 
                                      placeholder_text="Минимальное значение", 
                                      text_color="white", justify="center")
    self.__meanmin_ent.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)
    
    self.__meanmax_ent = ctk.CTkEntry(master=mean_frm, 
                                      placeholder_text="Максимальное значение", 
                                      text_color="white", justify="center")
    self.__meanmax_ent.pack(side="right", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)


    std_lbl = ctk.CTkLabel(master=self, 
                           text="Стандартное отклонение гауссовского "
                           "распределения",
                           corner_radius=8)
    std_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3, ipady=3, 
                 expand=True)
    
    std_frm = ctk.CTkFrame(master=self)
    std_frm.pack(side="top", fill="both", padx=0, pady=0, expand=True)

    self.__stdmin_ent = ctk.CTkEntry(master=std_frm, 
                                     placeholder_text="Минимальное значение", 
                                     text_color="white", justify="center")
    self.__stdmin_ent.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                        ipady=3, expand=True)
    
    self.__stdmax_ent = ctk.CTkEntry(master=std_frm, 
                                     placeholder_text="Максимальное значение", 
                                     text_color="white", justify="center")
    self.__stdmax_ent.pack(side="right", fill="x", padx=3, pady=3, ipadx=3,
                           ipady=3, expand=True)
    
  def __init_dnoise(self):
    dnoise_lbl = ctk.CTkLabel(master=self,
                              text="Параметры добавления шума",
                              corner_radius=8)
    dnoise_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                    ipady=3, expand=True)
    

    self.__check_dnoise = tk.BooleanVar()
    dnoise_chb = ctk.CTkCheckBox(master=self, text="Удалить шум", 
                                 variable=self.__check_dnoise,
                                 onvalue=True, offvalue=False)
    dnoise_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                    ipady=3, expand=True)
    

    ratio_lbl = ctk.CTkLabel(master=self, 
                             text="Коэффициент для расчета размера ядра фильтра", 
                             corner_radius=8)
    ratio_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3, ipady=3, 
                   expand=True)
    
    self.__ratio_ent = ctk.CTkEntry(master=self, 
                                    placeholder_text="значение в диапазоне от "
                                    "0 до 1", 
                                    text_color="white", justify="center")
    self.__ratio_ent.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                          ipady=3, expand=True)
    
  def __init_angle(self):
    angl_lbl = ctk.CTkLabel(master=self,
                            text="Параметры поворота изображения",
                            corner_radius=8)
    angl_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                    ipady=3, expand=True)
    

    self.__check_angl = tk.BooleanVar()
    angl_chb = ctk.CTkCheckBox(master=self, text="Повернуть изображение", 
                               variable=self.__check_angl, 
                               onvalue=True, offvalue=False)
    angl_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                  ipady=3, expand=True)
    

    arng_lbl = ctk.CTkLabel(master=self, 
                           text="Диапозон поворота изображения в градусах",
                           corner_radius=8)
    arng_lbl.pack(side="top", fill="x", padx=3, pady=3, ipadx=3, ipady=3, 
                 expand=True)
    
    arng_frm = ctk.CTkFrame(master=self)
    arng_frm.pack(side="top", fill="both", padx=0, pady=0, expand=True)

    self.__arngmin_ent = ctk.CTkEntry(master=arng_frm, 
                                      placeholder_text="Минимальное значение", 
                                      text_color="white", justify="center")
    self.__arngmin_ent.pack(side="left", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)
    
    self.__arngmax_ent = ctk.CTkEntry(master=arng_frm, 
                                      placeholder_text="Максимальное значение", 
                                      text_color="white", justify="center")
    self.__arngmax_ent.pack(side="right", fill="x", padx=3, pady=3, ipadx=3,
                            ipady=3, expand=True)
    
  def __init_mirror(self):
    mirror_lbl = ctk.CTkLabel(master=self,
                              text="Параметры добавления эффекта зеркала",
                              corner_radius=8)
    mirror_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                    ipady=3, expand=True)
    

    self.__check_mirror = tk.BooleanVar()
    mirror_chb = ctk.CTkCheckBox(master=self, text="Отзеркалить изображение", 
                                 variable=self.__check_mirror,
                                 onvalue=True, offvalue=False)
    mirror_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                    ipady=3, expand=True)
    
  def __init_resize(self):
    resize_lbl = ctk.CTkLabel(master=self,
                              text="Параметры изменения масштаба",
                              corner_radius=8)
    resize_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                    ipady=3, expand=True)
    

    self.__check_resize = tk.BooleanVar()
    resize_chb = ctk.CTkCheckBox(master=self, text="Изменить масштаба", 
                                 variable=self.__check_resize,
                                 onvalue=True, offvalue=False)
    resize_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                    ipady=3, expand=True)
    
  def __init_aug(self):
    self.__check_mode = tk.BooleanVar()
    mode_chb = ctk.CTkCheckBox(master=self, text="Применять фильтры ко всем "
                               "получаемым в процессе аугментации "
                               "изображениям", 
                               variable=self.__check_mode,
                               onvalue=True, offvalue=False)
    mode_chb.pack(side="top", fill="x", padx=3, pady=3, ipadx=3,
                  ipady=3, expand=True)
    
    aug_btn = ctk.CTkButton(master=self, 
                            text="Начать аугментацию",
                            command=self.__augmentate)
    aug_btn.pack(side="top", fill="x", padx=5, pady=5, ipadx=5,
                 ipady=5, expand=True)
    
    augst_lbl = ctk.CTkLabel(master=self,
                             text="Дождитесь окна с сообщением о "
                             "завершении процесса!",
                             corner_radius=8)
    augst_lbl.pack(side="top", fill="x", padx=3, pady=6, ipadx=3,
                   ipady=3, expand=True)
    
  def __augmentate(self):
    try:
      Command_handler().augmentate(oni=self.__oni_ent.get(),
                                   noise=self.__check_noise.get(), 
                                   mean=[self.__meanmin_ent.get(), 
                                         self.__meanmax_ent.get()], 
                                   std=[self.__stdmin_ent.get(),
                                        self.__stdmax_ent.get()],
                                   angle=self.__check_angl.get(),
                                   angl_rng=[self.__arngmin_ent.get(),
                                             self.__arngmax_ent.get()],
                                   delete_noise=self.__check_dnoise.get(),
                                   ratio=self.__ratio_ent.get(),
                                   mirror=self.__check_mirror.get(),
                                   resize=self.__check_resize.get(),
                                   mode=self.__check_mode.get())
    except exception.Invalid_args_type as exc:
      tk.messagebox.showerror(title="Ошибка", message=exc)
    except exception.Invalid_arg_range as exc:
      tk.messagebox.showerror(title="Ошибка", message=exc)