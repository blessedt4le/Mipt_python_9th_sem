import tkinter as tk
import customtkinter as ctk

from internal.command_handler import Command_handler
from internal.tools.singleton import singleton
from internal.tools import exception

from ui.augmentation_win import Augmentation_win
from ui.gallery_win import Gallery_win
from ui.generation_win import Generation_win
from ui.image_type_win import ImageTypeWin
from ui.blood_cells_search_win import BloodCellsSearchWin


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
        # Верхний фрейм с маленькими кнопками (оставляем как было)
        btn_frm = ctk.CTkFrame(master=self)
        btn_frm.pack(side="top", fill="both", padx=3, pady=3, expand=False)
        self.__init_download(btn_frm)
        self.__init_aug(btn_frm)

        # Нижний фрейм для больших кнопок в столбик
        bottom_frm = ctk.CTkFrame(master=self)
        bottom_frm.pack(side="top", fill="x", padx=10, pady=5, expand=False)

        # Три большие кнопки в столбик (как были)
        self.__seek_cell_blood = ctk.CTkButton(
            master=bottom_frm,
            text="Искать клетки крови",
            command=self.__open_blood_cells_search
        )
        self.__seek_cell_blood.pack(side="top", fill="x", padx=10, pady=5, expand=False)

        self.__open_BD = ctk.CTkButton(
            master=bottom_frm,
            text="Открыть базу данных",
            #command=self.__upload_data
        )
        self.__open_BD.pack(side="top", fill="x", padx=10, pady=5, expand=False)

        self.__copy = ctk.CTkButton(
            master=bottom_frm,
            text="Копировать базу данных",
            command=self.__upload_data
        )
        self.__copy.pack(side="top", fill="x", padx=10, pady=5, expand=False)

    # Остальной код остается без изменений
    def __init_download(self, src_frm):
        left_btns = ctk.CTkFrame(master=src_frm)
        left_btns.pack(side="left", fill="both", padx=3, pady=3, expand=True)

        self.__download_btn = ctk.CTkButton(
            master=left_btns,
            text="Загрузить изображения",
            command=self.__download_data
        )
        self.__download_btn.pack(side="top", fill="x", padx=3, pady=3, expand=True)

        self.__gen_btn = ctk.CTkButton(
            master=left_btns,
            text="Сгенерировать изображения",
            command=self.open_generation_window
        )
        self.__gen_btn.pack(side="top", fill="x", padx=3, pady=3, expand=True)

    def __init_aug(self, src_frm):
        right_btns = ctk.CTkFrame(master=src_frm)
        right_btns.pack(side="right", fill="both", padx=3, pady=3, expand=True)

        self.__aug_btn = ctk.CTkButton(
            master=right_btns,
            text="Аугментировать изображения",
            command=self.__call_aug_win
        )
        self.__aug_btn.pack(side="top", fill="x", padx=3, pady=3, expand=True)

        self.__show_images_btn = ctk.CTkButton(
            master=right_btns,
            text="Показать изображения",
            command=self.__open_image_type_window
        )
        self.__show_images_btn.pack(side="top", fill="x", padx=3, pady=3, expand=True)

    # Остальные методы без изменений
    def open_generation_window(self):
        Generation_win(self)

    def __init_textbox(self):
        self.__textbox = ctk.CTkTextbox(
            master=self,
            width=400,
            height=300,
            fg_color="white",
            text_color="black"
        )
        self.__textbox.pack(side="top", fill="both", padx=10, pady=6, expand=True)

    def __call_aug_win(self):
        Augmentation_win(self)

    def __open_image_type_window(self):
        ImageTypeWin(self)

    def __open_blood_cells_search(self):
        BloodCellsSearchWin(self) 

    def __show_data(self):
        data = Command_handler().get_images()
        if data is not None:
            Gallery_win(self, data)
        else:
            tk.messagebox.showerror(title="Ошибка", message="Данные отсутствуют!")

    def __show_aug_data(self):
        data = Command_handler().get_augmentation_images()
        if data is not None:
            Gallery_win(self, data)
        else:
            tk.messagebox.showerror(title="Ошибка", message="Данные отсутствуют!")

    def __download_data(self):
        dirpath = tk.filedialog.askdirectory()
        try:
            Command_handler().download(dirpath)
        except exception.Invalid_dirpath as exc:
            tk.messagebox.showerror(title="Ошибка", message=str(exc))

    def __upload_data(self):
        dirpath = tk.filedialog.askdirectory()
        try:
            Command_handler().upload(dirpath)
        except exception.Invalid_dirpath as exc:
            tk.messagebox.showerror(title="Ошибка", message=str(exc))
        except exception.Aug_data_empty as exc:
            tk.messagebox.showerror(title="Ошибка", message=str(exc))

