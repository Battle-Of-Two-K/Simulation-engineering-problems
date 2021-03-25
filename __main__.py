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
        'width': 320,
        'height': 720
    }

    button_opts = {
        'font': ("Courier", 16, "italic")
    }

    data = {}

    def __init__(self):
        self.read_data_json_file()
        self.root = Tk()
        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack(side='left')

        self.settings_window = Frame(self.root, **self.settings_window_opts)
        self.settings_window.pack(side='right')

        self.btn = Button(self.settings_window, text='Посчитать', **self.button_opts)
        self.btn.place(x=self.settings_window_opts['width'] // 2,
                       y=720 - 720 / 10)

        # self.settings_window.

        # textExample = Text(self.settings_window, height=10)
        # textExample.pack()

        print(self.btn['width'])

        self.check = Checkbutton(self.settings_window, text='Текст', font=("Courier", 16, "italic"))
        self.check.place(x=10, y=400)

        # self.decor()

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
