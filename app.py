import tkinter as tk


class ImageApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Просмотр каналов изображения")

        btn_load = tk.Button(master, text="Загрузить изображение", state='disabled')
        btn_load.pack(pady=10)

        self.channel_var = tk.StringVar(value="R")
        for text, val in [("Красный", "R"), ("Зелёный", "G"), ("Синий", "B")]:
            rb = tk.Radiobutton(master, text=text, variable=self.channel_var, value=val, state='disabled')
            rb.pack(anchor="w")

        self.img_label = tk.Label(master)
        self.img_label.pack(pady=5)

        btn_line = tk.Button(master, text="Нарисовать линию", state='disabled')
        btn_line.pack(pady=5)

        btn_rotate = tk.Button(master, text="Вращение", state='disabled')
        btn_rotate.pack(pady=5)

        btn_resize = tk.Button(master, text="Изменить размер", state='disabled')
        btn_resize.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
