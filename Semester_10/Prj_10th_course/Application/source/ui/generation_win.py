import tkinter as tk
import customtkinter as ctk

class Generation_win(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        self.title("Настройка генерации")
        self.minsize(width=400, height=300)
        
        # Поля для ввода параметров
        ctk.CTkLabel(self, text="Размер изображения (ширина высота):").pack(pady=5)
        self.size_entry = ctk.CTkEntry(self)
        self.size_entry.pack(pady=5)
        self.size_entry.insert(0, "400 600")
        
        ctk.CTkLabel(self, text="Количество изображений:").pack(pady=5)
        self.num_images_entry = ctk.CTkEntry(self)
        self.num_images_entry.pack(pady=5)
        self.num_images_entry.insert(0, "10")
        
        ctk.CTkLabel(self, text="Количество клеток:").pack(pady=5)
        self.num_cells_entry = ctk.CTkEntry(self)
        self.num_cells_entry.pack(pady=5)
        self.num_cells_entry.insert(0, "50")
        
        # Кнопка генерации
        generate_btn = ctk.CTkButton(
            self, 
            text="Сгенерировать",
            command=self.generate_images
        )
        generate_btn.pack(pady=20)
    
    def generate_images(self):
        try:
            # Получаем размер как кортеж
            width, height = map(int, self.size_entry.get().split())
            img_size = (width, height)
            
            nof_imgs = int(self.num_images_entry.get())
            nof_cells = int(self.num_cells_entry.get())
            
            from internal.command_handler import Command_handler
            Command_handler().generate(img_size, nof_imgs, nof_cells)
            
            self.destroy()
            
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")