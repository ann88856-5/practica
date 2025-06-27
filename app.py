import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk


class ResizeDialog(simpledialog.Dialog):
    def __init__(self, parent, current_width, current_height):
        self.new_width = current_width
        self.new_height = current_height
        super().__init__(parent, title="Изменить размер изображения")

    def body(self, master):
        tk.Label(master, text="Ширина:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(master, text="Высота:").grid(row=1, column=0, padx=5, pady=5)

        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)
        self.width_entry.insert(0, str(self.new_width))

        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        self.height_entry.insert(0, str(self.new_height))

        return self.width_entry 

    def validate(self):
        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            if w <= 0 or h <= 0:
                raise ValueError
            self.new_width = w
            self.new_height = h
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительные целые числа для ширины и высоты.")
            return False

    def apply(self):
        pass


class ImageApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Просмотр каналов изображения")

        self.btn_load = tk.Button(master, text="Загрузить изображение", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_resize = tk.Button(master, text="Изменить размер", command=self.resize_image, state='disabled')
        self.btn_resize.pack(pady=5)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
