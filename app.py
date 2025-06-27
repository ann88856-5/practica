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
        for text, val in [("Красный", "R"), ("Зелёный", "G"), ("Синий", "B")]:
            rb = tk.Radiobutton(master, text=text, variable=self.channel_var, value=val, state='disabled')
            rb.pack(anchor="w")

        self.img_label = tk.Label(master)
        self.img_label.pack(pady=5)

        self.btn_line = tk.Button(master, text="Нарисовать линию", state='disabled')
        self.btn_line.pack(pady=5)

        self.btn_rotate = tk.Button(master, text="Вращение", state='disabled')
        self.btn_rotate.pack(pady=5)

        self.btn_resize = tk.Button(master, text="Изменить размер", state='disabled')
        self.btn_resize.pack(pady=5)

        self.image = None
        self.tk_image = None

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Все файлы", "*.*")]
        )
        if path:
            self.image = Image.open(path)
            self.show_image(self.image)
            for rb in self.root.winfo_children():
                if isinstance(rb, tk.Radiobutton):
                    rb.config(state='normal')

    def show_image(self, img):
        self.tk_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.tk_image)
        self.img_label.image = self.tk_image  


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
