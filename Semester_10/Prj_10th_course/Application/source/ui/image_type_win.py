import tkinter as tk
import customtkinter as ctk

class ImageTypeWin(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        self.title("Выбор типа изображений")
        self.minsize(width=300, height=200)
        
        # Создаем основной фрейм для кнопок
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Настройки для всех кнопок
        button_options = {
            'master': button_frame,
            'width': 200,  # Фиксированная ширина для всех кнопок
            'height': 40,  # Фиксированная высота для всех кнопок
            'corner_radius': 6,
            'font': ('Arial', 14)
        }
        
        # Кнопки для выбора типа изображений
        ctk.CTkButton(
            **button_options,
            text="Загруженные изображения",
            command=lambda: self.show_images("loaded")
        ).pack(pady=10, fill="x")
        
        ctk.CTkButton(
            **button_options,
            text="Сгенерированные изображения",
            command=lambda: self.show_images("generated")
        ).pack(pady=10, fill="x")
        
        ctk.CTkButton(
            **button_options,
            text="Аугментированные изображения",
            command=lambda: self.show_images("augmented")
        ).pack(pady=10, fill="x")
    
    def show_images(self, img_type):
        from internal.command_handler import Command_handler
        from ui.gallery_win import Gallery_win
        import tkinter.messagebox as msg
        
        data = None
        handler = Command_handler()
        
        if img_type == "loaded":
            data = handler.get_images()
        elif img_type == "generated":
            data = handler.get_generated_images()
        elif img_type == "augmented":
            data = handler.get_augmentation_images()
        
        if data:
            Gallery_win(self, data)
        else:
            msg.showerror("Ошибка", f"{img_type.capitalize()} изображения отсутствуют!")