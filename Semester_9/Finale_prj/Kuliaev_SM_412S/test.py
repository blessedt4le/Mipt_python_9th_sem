import os
import customtkinter as ctk
from PIL import Image

root = ctk.CTk()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = Image.open("color.jpg")
w, h = src.size

img = ctk.CTkImage(dark_image=src, size=(w, h))
lbl = ctk.CTkLabel(master=root, image=img, text='')
lbl.pack()

root.mainloop()