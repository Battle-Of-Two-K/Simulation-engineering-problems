from tkinter import *
# from tkinter import ttk
import json


class App:
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    settings_window_opts = {
        'width': 620,
        'height': 720
    }

    button_opts = {
        'font': ("Courier", 16, "italic")
    }

    data = {}

    def __init__(self):
        self.read_data_json_file()
        self.root = Tk()
        self.root.title('Лабораторная работа')

        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack(side='left')

        self.settings_window = Canvas(self.root, **self.settings_window_opts)
        self.settings_window.pack(side='right')

        self.color_frames = Frame(self.root)

        # Кнопки
        self.btn = Button(self.settings_window, text='Посчитать', **self.button_opts)
        self.btn.place(x=self.settings_window_opts['width'] // 2,
                       y=720 - 720 / 10)

        # Галочки
        self.check = Checkbutton(self.settings_window, text='Текст', font=("Courier", 14, "italic"))
        self.check.place(x=10, y=400)

        # Текст
        self.settings_window.create_text(self.settings_window_opts['width'] // 2, 30,
                                         text='Задача №2. Вариант 59', font=("Times New Roman", 14, "bold"))

        # self.settings_window.create_text(160, 60, text='Входные данные:', font=("Courier", 16, "italic"))

        i = 100
        for key, value in self.data.items():
            print(f"{key}:")
            self.settings_window.create_text(self.settings_window_opts['width'] // 2, i,
                                             text=f'{key}:', font=("Courier", 14, "italic"))
            i += 30

            if isinstance(value, dict):
                for inside_key, inside_value in value.items():
                    self.settings_window.create_text(self.settings_window_opts['width'] // 2, i,
                                                     text=f"    {inside_key}: {inside_value}",
                                                     font=("Courier", 16, "italic"))
                    i += 20

            elif isinstance(value, list):
                for step in value:
                    self.check = Checkbutton(self.settings_window, text=f"{step}", font=("Courier", 14, "italic"))
                    self.check.place(x=10, y=i)
                    i += 30
            else:
                self.settings_window.create_text(self.settings_window_opts['width'] // 2,
                                                 i, text=f"    {key}: {value}\n",
                                                 font=("Courier", 16, "italic"))
                i += 20

        self.decor()

    def read_data_json_file(self):
        """
        Метод считывает данные из файла 'Input_data.json'
        """
        with open('Input_data.json', encoding="utf-8") as file:
            self.data = json.loads(file.read())

    def decor(self):
        task_text = "Горизонтальный реальный пружинный маятник, " \
                    "закреплённый двумя пружинами. Тело - куб."

        print("Задача №2. Вариант 59.".center(len(task_text)))
        print("Подготовил студент группы М1О-302С-18 Коновалов Ф.Д.\n".center(len(task_text)))
        print("Условие задачи:")
        print(task_text)

        for key, value in self.data.items():
            print()
            print(f"{key}:")

            if isinstance(value, dict):
                for inside_key, inside_value in value.items():
                    print(f"    {inside_key}: {inside_value}")
            elif isinstance(value, list):
                for step in value:
                    print(f"   - {step}")
            else:
                print(f"    {key}: {value}\n")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
