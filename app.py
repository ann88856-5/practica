import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk


class ResizeDialog(simpledialog.Dialog):
    def __init__(self, parent, curr_w, curr_h):
        self.curr_w = curr_w
        self.curr_h = curr_h
        self.new_width = None
        self.new_height = None
        super().__init__(parent, title="Изменить размер")

    def body(self, master):
        tk.Label(master, text=f"Текущая ширина: {self.curr_w}").grid(row=0, column=0, columnspan=2)
        tk.Label(master, text=f"Текущая высота: {self.curr_h}").grid(row=1, column=0, columnspan=2)

        tk.Label(master, text="Новая ширина:").grid(row=2, column=0)
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=2, column=1)
        self.width_entry.insert(0, str(self.curr_w))

        tk.Label(master, text="Новая высота:").grid(row=3, column=0)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=3, column=1)
        self.height_entry.insert(0, str(self.curr_h))

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
            messagebox.showerror("Ошибка", "Введите корректные положительные числа для размеров.")
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
        if not path:
            return

        try:
            img = Image.open(path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
            return

        self.image = img
        self.channel_var.set("R")
        self.update_channel()

        # Активируем элементы управления
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
        if self.image is None:
            return
        channel_img = self.get_channel_image()
        if channel_img:
            self.show_image(channel_img)

    def show_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.tk_image)
        self.img_label.image = self.tk_image

    def resize_image(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        w, h = self.image.size
        dlg = ResizeDialog(self.root, w, h)
        if dlg.result is not None:
            new_w, new_h = dlg.new_width, dlg.new_height
            try:
                self.image = self.image.resize((new_w, new_h), Image.ANTIALIAS)
                self.update_channel()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при изменении размера:\n{e}")

    def rotate_image(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        angle_str = simpledialog.askstring("Поворот", "Введите угол вращения (в градусах):", parent=self.root)
        if angle_str is None:
            return

        try:
            angle = float(angle_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение угла.")
            return

        try:
            self.image = self.image.rotate(-angle, expand=True)
            self.update_channel()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при повороте изображения:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

