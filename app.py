import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Просмотр каналов изображения")

        self.btn_load = tk.Button(master, text="Загрузить изображение", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.channel_var = tk.StringVar(value="R")
        self.rb_red = tk.Radiobutton(master, text="Красный", variable=self.channel_var, value="R", state='disabled', command=self.update_channel)
        self.rb_green = tk.Radiobutton(master, text="Зелёный", variable=self.channel_var, value="G", state='disabled', command=self.update_channel)
        self.rb_blue = tk.Radiobutton(master, text="Синий", variable=self.channel_var, value="B", state='disabled', command=self.update_channel)
        self.rb_red.pack(anchor="w")
        self.rb_green.pack(anchor="w")
        self.rb_blue.pack(anchor="w")

        self.img_label = tk.Label(master)
        self.img_label.pack(pady=5)

        self.image = None
        self.tk_image = None

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Все файлы", "*.*")]
        )
        if path:
            self.image = Image.open(path).convert("RGB")  
            self.update_channel()
            for rb in (self.rb_red, self.rb_green, self.rb_blue):
                rb.config(state='normal')

    def get_channel_image(self):
        if self.image is None:
            return None
        # Разделяем каналы
        r, g, b = self.image.split()
        channel = self.channel_var.get()
        if channel == "R":
            return r
        elif channel == "G":
            return g
        elif channel == "B":
            return b
        else:
            return self.image

    def update_channel(self):
        channel_img = self.get_channel_image()
        if channel_img:
            self.show_image(channel_img)

    def show_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.tk_image)
        self.img_label.image = self.tk_image


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
