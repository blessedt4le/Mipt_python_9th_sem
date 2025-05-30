import tkinter as tk
import customtkinter as ctk

class BloodCellsSearchWin(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        
        self.title("Поиск клеток крови")
        self.minsize(width=300, height=300)  # Увеличил высоту окна
        
        # Создаем переменную для RadioButton
        self.image_source_var = tk.StringVar(value="loaded")  # Значение по умолчанию
        
        # Фрейм для RadioButton
        radio_frame = ctk.CTkFrame(self)
        radio_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(radio_frame, text="Источник изображений:").pack(anchor="w")
        
        # Добавляем RadioButton
        ctk.CTkRadioButton(
            radio_frame,
            text="Загруженные картинки",
            variable=self.image_source_var,
            value="loaded"
        ).pack(pady=5, padx=20, anchor="w")
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Сгенерированные картинки",
            variable=self.image_source_var,
            value="generated"
        ).pack(pady=5, padx=20, anchor="w")
        
        # Фрейм для чекбоксов
        checkbox_frame = ctk.CTkFrame(self)
        checkbox_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(checkbox_frame, text="Методы поиска:").pack(anchor="w")
        
        # Чекбоксы для методов поиска
        self.method1_var = tk.BooleanVar()
        self.method2_var = tk.BooleanVar()
        self.method3_var = tk.BooleanVar()
        
        ctk.CTkCheckBox(
            checkbox_frame, 
            text="Метод 1", 
            variable=self.method1_var
        ).pack(pady=5, padx=20, anchor="w")
        
        ctk.CTkCheckBox(
            checkbox_frame, 
            text="Метод 2", 
            variable=self.method2_var
        ).pack(pady=5, padx=20, anchor="w")
        
        ctk.CTkCheckBox(
            checkbox_frame, 
            text="Метод 3", 
            variable=self.method3_var
        ).pack(pady=5, padx=20, anchor="w")
        
        ctk.CTkCheckBox(
            checkbox_frame, 
            text="Найти всеми методами", 
            command=self.__select_all_methods
        ).pack(pady=5, padx=20, anchor="w")
        
        # Кнопка запуска поиска
        ctk.CTkButton(
            self,
            text="Распознать",
            command=self.__search_cells
        ).pack(pady=20)
    
    def __select_all_methods(self):
        state = self.method1_var.get()
        self.method1_var.set(not state)
        self.method2_var.set(not state)
        self.method3_var.set(not state)
    
    def __search_cells(self):
        selected_methods = []
        if self.method1_var.get(): selected_methods.append("Метод 1")
        if self.method2_var.get(): selected_methods.append("Метод 2")
        if self.method3_var.get(): selected_methods.append("Метод 3")
        
        if not selected_methods:
            tk.messagebox.showwarning("Предупреждение", "Выберите хотя бы один метод!")
            return
        
        # Получаем выбранный источник изображений
        image_source = self.image_source_var.get()
        print(f"Источник: {'Загруженные' if image_source == 'loaded' else 'Сгенерированные'} изображения")
        print(f"Выбранные методы: {', '.join(selected_methods)}")
        
        # Здесь будет логика поиска клеток крови
        # Можно использовать image_source для определения типа изображений
        
        tk.messagebox.showinfo("Информация", "Поиск клеток завершен!")
        self.destroy()