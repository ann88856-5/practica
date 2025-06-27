import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk


class ImageApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Просмотр каналов изображения")

        self.btn_load = tk.Button(master, text="Загрузить изображение", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_resize = tk.Button(master, text="Изменить размер", command=self.resize_image, state='disabled')
        self.btn_resize.pack(pady=5)

        # Новая кнопка для поворота
        self.btn_rotate = tk.Button(master, text="Повернуть изображение", command=self.rotate_image, state='disabled')
        self.btn_rotate.pack(pady=5)

        self.channel_var = tk.StringVar(value="R")
        self.rb_red = tk.Radiobutton(master, text="Красный", variable=self.channel_var, value="R",
                                     state='disabled', command=self.update_channel)
        self.rb_green = tk.Radiobutton(master, text="Зелёный", variable=self.channel_var, value="G",
                                       state='disabled', command=self.update_channel)
        self.rb_blue = tk.Radiobutton(master, text="Синий", variable=self.channel_var, value="B",
                                      state='disabled', command=self.update_channel)
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
            self.btn_resize.config(state='normal')
            self.btn_rotate.config(state='normal')

    def get_channel_image(self):
        if self.image is None:
            return None
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

    def resize_image(self):
        if self.image is None:
            return

        w, h = self.image.size
        dlg = ResizeDialog(self.root, w, h)
        if dlg.result is not None:
            new_w, new_h = dlg.new_width, dlg.new_height
            self.image = self.image.resize((new_w, new_h), Image.ANTIALIAS)
            self.update_channel()

    def rotate_image(self):
        if self.image is None:
            return

        # Запрашиваем угол
        angle_str = simpledialog.askstring("Поворот", "Введите угол вращения (в градусах):", parent=self.root)
        if angle_str is None:  # Нажата отмена
            return

        try:
            angle = float(angle_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение угла.")
            return

        self.image = self.image.rotate(-angle, expand=True)
        self.update_channel()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
