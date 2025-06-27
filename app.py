import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
from PIL.Image import Image as PILImage
from typing import Union
import cv2
from typing import Optional


class ResizeDialog(simpledialog.Dialog):
    def __init__(self, parent, curr_w, curr_h):
        self.curr_w = curr_w
        self.curr_h = curr_h
        self.new_width = None
        self.new_height = None
        self.width_entry = None
        self.height_entry = None
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


class LineDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.x1_entry = None
        self.y1_entry = None
        self.x2_entry = None
        self.y2_entry = None
        self.width_entry = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.width = None
        super().__init__(parent, title="Нарисовать линию")

    def body(self, master):
        tk.Label(master, text="X1:").grid(row=0, column=0)
        self.x1_entry = tk.Entry(master)
        self.x1_entry.grid(row=0, column=1)

        tk.Label(master, text="Y1:").grid(row=1, column=0)
        self.y1_entry = tk.Entry(master)
        self.y1_entry.grid(row=1, column=1)

        tk.Label(master, text="X2:").grid(row=2, column=0)
        self.x2_entry = tk.Entry(master)
        self.x2_entry.grid(row=2, column=1)

        tk.Label(master, text="Y2:").grid(row=3, column=0)
        self.y2_entry = tk.Entry(master)
        self.y2_entry.grid(row=3, column=1)

        tk.Label(master, text="Толщина:").grid(row=4, column=0)
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=4, column=1)

        return self.x1_entry

    def validate(self):
        try:
            self.x1 = int(self.x1_entry.get())
            self.y1 = int(self.y1_entry.get())
            self.x2 = int(self.x2_entry.get())
            self.y2 = int(self.y2_entry.get())
            self.width = int(self.width_entry.get())
            if self.width <= 0:
                raise ValueError("Толщина должна быть положительной")
            return True
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
            return False


class ImageApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Просмотр каналов изображения")

        control_frame = tk.Frame(master)
        control_frame.pack(pady=10)

        self.btn_load = tk.Button(control_frame, text="Загрузить изображение", command=self.load_image)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_camera = tk.Button(control_frame, text="Снять с камеры",
                                    command=self._capture_from_camera, state='normal')
        self.btn_camera.pack(side=tk.LEFT, padx=5)

        self.btn_resize = tk.Button(control_frame, text="Изменить размер", command=self.resize_image,
                                    state='disabled')
        self.btn_resize.pack(side=tk.LEFT, padx=5)

        self.btn_rotate = tk.Button(control_frame, text="Повернуть", command=self.rotate_image, state='disabled')
        self.btn_rotate.pack(side=tk.LEFT, padx=5)

        self.btn_draw = tk.Button(control_frame, text="Нарисовать линию", command=self.draw_line, state='disabled')
        self.btn_draw.pack(side=tk.LEFT, padx=5)

        channel_frame = tk.Frame(master)
        channel_frame.pack(pady=5)

        self.channel_var = tk.StringVar(value="")
        self.rb_red = tk.Radiobutton(channel_frame, text="Красный", variable=self.channel_var, value="R",
                                     state='disabled', command=self.update_channel)
        self.rb_green = tk.Radiobutton(channel_frame, text="Зелёный", variable=self.channel_var, value="G",
                                       state='disabled', command=self.update_channel)
        self.rb_blue = tk.Radiobutton(channel_frame, text="Синий", variable=self.channel_var, value="B",
                                      state='disabled', command=self.update_channel)
        self.rb_red.pack(side=tk.LEFT, padx=5)
        self.rb_green.pack(side=tk.LEFT, padx=5)
        self.rb_blue.pack(side=tk.LEFT, padx=5)

        self.img_label = tk.Label(master)
        self.img_label.pack(pady=5)

        self.image: Optional[PILImage] = None
        self.tk_image = None
        self.camera_capture: Optional[cv2.VideoCapture] = None

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Все файлы", "*.*")]
        )
        if not path:
            return

        try:
            loaded_img = Image.open(path).convert("RGB")
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{error}")
            return

        self.image = loaded_img
        self.show_image(self.image)

        for radio_button in (self.rb_red, self.rb_green, self.rb_blue):
            radio_button.config(state='normal')
        self.btn_resize.config(state='normal')
        self.btn_rotate.config(state='normal')
        self.btn_draw.config(state='normal')
        self.btn_camera.config(state='normal')

    def _capture_from_camera(self):
        """Захват изображения с веб-камеры"""
        try:
            if self.camera_capture is not None:
                self.camera_capture.release()

            self.camera_capture = cv2.VideoCapture(0)

            if not self.camera_capture.isOpened():
                raise RuntimeError("Не удалось подключиться к камере")

            preview_window = tk.Toplevel(self.root)
            preview_window.title("Предпросмотр камеры")
            preview_label = tk.Label(preview_window)
            preview_label.pack()

            def on_capture():
                self._take_photo(preview_window)

            btn_capture = tk.Button(preview_window, text="Сделать снимок",
                                    command=on_capture)
            btn_capture.pack(pady=10)

            def update_preview():
                ret, frame = self.camera_capture.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    preview_img = Image.fromarray(frame)
                    preview_imgtk = ImageTk.PhotoImage(image=preview_img)
                    preview_label.imgtk = preview_imgtk
                    preview_label.configure(image=preview_imgtk)  # type: ignore

                preview_label.after(10, update_preview)

            update_preview()

            preview_window.protocol("WM_DELETE_WINDOW", lambda: self._close_camera(preview_window))

        except Exception as error:
            messagebox.showerror("Ошибка камеры",
                                 f"Проблема с подключением камеры:\n{error}\n\n"
                                 "Возможные решения:\n"
                                 "1. Проверьте подключение камеры\n"
                                 "2. Убедитесь, что камера не используется другим приложением\n"
                                 "3. Проверьте права доступа для приложения")
            self._close_camera()

    def _take_photo(self, preview_window):
        """Сохранение снимка с камеры"""
        try:
            ret, frame = self.camera_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = Image.fromarray(frame)
                self.show_image(self.image)

                for radio_button in (self.rb_red, self.rb_green, self.rb_blue):
                    radio_button.config(state='normal')
                self.btn_resize.config(state='normal')
                self.btn_rotate.config(state='normal')
                self.btn_draw.config(state='normal')

            preview_window.destroy()
            self._close_camera()

        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить снимок:\n{error}")
            preview_window.destroy()
            self._close_camera()

    def _close_camera(self, window=None):
        """Безопасное закрытие камеры"""
        if self.camera_capture is not None:
            self.camera_capture.release()
            self.camera_capture = None
        if window:
            window.destroy()

    def get_channel_image(self) -> Optional[PILImage]:
        if self.image is None:
            return None

        if not self.channel_var.get():
            return self.image

        r, g, b = self.image.split()
        channel = self.channel_var.get()

        if channel == "R":
            g = g.point(lambda _: 0)
            b = b.point(lambda _: 0)
        elif channel == "G":
            r = r.point(lambda _: 0)
            b = b.point(lambda _: 0)
        elif channel == "B":
            r = r.point(lambda _: 0)
            g = g.point(lambda _: 0)

        return Image.merge("RGB", (r, g, b))

    def update_channel(self):
        if self.image is None:
            return
        channel_img = self.get_channel_image()
        if channel_img:
            self.show_image(channel_img)

    def show_image(self, img: Union[PILImage, str]) -> None:
        """Отображает изображение в интерфейсе."""
        if isinstance(img, str):
            img = Image.open(img).convert("RGB")

        self.tk_image = ImageTk.PhotoImage(image=img)
        self.img_label.config(image=self.tk_image)  # type: ignore
        self.img_label.image = self.tk_image

    def resize_image(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        w, h = self.image.size
        dlg = ResizeDialog(self.root, w, h)
        if dlg.new_width is not None and dlg.new_height is not None:
            try:
                self.image = self.image.resize((dlg.new_width,
                                                dlg.new_height), Image.Resampling.LANCZOS)
                self.update_channel()
            except Exception as e:
                messagebox.showerror("Ошибка",
                                     f"Ошибка при изменении размера:\n{e}")

    def rotate_image(self):
        if self.image is None:
            messagebox.showwarning("Внимание",
                                   "Сначала загрузите изображение.")
            return

        angle_str = simpledialog.askstring("Поворот",
                                           "Введите угол вращения (в градусах):", parent=self.root)
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

    def draw_line(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        dlg = LineDialog(self.root)
        if not hasattr(dlg, 'x1'):  
            return

        try:
            img_copy = self.image.copy()
            draw = ImageDraw.Draw(img_copy)

            # Рисуем зеленую линию
            draw.line([(dlg.x1, dlg.y1), (dlg.x2, dlg.y2)],
                      fill="green",
                      width=dlg.width)

            self.image = img_copy
            self.update_channel()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось нарисовать линию:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
