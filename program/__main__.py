from tkinter import filedialog
from tkinter.ttk import *
from tkinter import *
from sympy import *
import json
import os


def find(name):
    return os.path.exists(name)


class App:
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    settings_window_opts = {
        'width': 470,
        'height': 720,
    }

    border_effects = {
        "flat": FLAT,
        "sunken": SUNKEN,
        "raised": RAISED,
        "groove": GROOVE,
        "ridge": RIDGE,
    }

    task_data = {}  # данные задачи
    materials_data = {}  # таблица материалов
    buttons = []

    def __init__(self):
        self.equation_for_normal_conditions()
        self.root = Tk()
        self.root.title('Моделирование инженерных задач. Лабораторная работа')
        self.root.resizable(width=False, height=False)  # запрет на изменение размеров виджета

        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack(side='left')

        self.chart()

        self.settings_window = Frame(self.root, **self.settings_window_opts)
        self.settings_window.pack(side='right')

        self.read_data_json_file()

        self.deviation = self.task_data["Входные данные"]["Отклонение"]
        self.cube_size = self.task_data["Входные данные"]["Размер куба"]
        self.spring_diameter = self.task_data["Входные данные"]["Диаметр пружины"]
        self.spring_coil_pitch = self.task_data["Входные данные"]["Шаг витков пружины"]
        self.wire_diameter = self.task_data["Входные данные"]["Диаметр пружины"]
        self.spring_length = self.task_data["Дополнительные условия"]["Длина пружин"]
        self.shear_modulus = 10  # модуль сдвига

        self.information_canvas()
        self.information_console()
        # print(self.calc_coefficient_spring_stiffness())

    def calc_coefficient_spring_stiffness(self):
        """
        Расчёт коэффициента упругости (жёсткости) пружины.

        Returns: коэффициент упругости (жёсткости) пружины
        """
        number_turns_spring = self.spring_length // self.spring_coil_pitch + 1  # кол-во витков
        return (self.shear_modulus * self.wire_diameter ** 4) / (8 * number_turns_spring * self.spring_diameter ** 3)

    def information_canvas(self):
        """
        Вывод информации о задаче + вывод кнопок на полотно
        """
        height, delta = 50, 31

        Label(self.settings_window, text='Задача №2. Вариант 59',
              font=("Courier", 18, "bold")).place(x=0, y=0)

        # Первый блок данных
        Label(self.settings_window, text="1.Входные данные:",
              font=("Courier", 14, "bold")).place(x=0, y=height)

        for key, value in self.task_data["Входные данные"].items():
            Label(self.settings_window, text=f'  {key}: {value} мм',
                  font=("Courier", 14, "italic")).place(x=0, y=height + delta)
            height += delta

        # Второй блок данных
        Label(self.settings_window, text="2.Дополнительные условия:",
              font=("Courier", 14, "bold")).place(x=0, y=height + delta)

        for key, value in self.task_data["Дополнительные условия"].items():
            Label(self.settings_window, text=f'  {key}: {value}',
                  font=("Courier", 14, "italic")).place(x=0, y=height + 2 * delta)
            height += delta

        # Третий блок данных
        Label(self.settings_window, text="3.Выберете один из вариантов расчёта:",
              font=("Courier", 14, "bold")).place(x=0, y=height + 2 * delta)

        i = 0
        for value in self.task_data["Особые условия"]:
            checkbutton = Button(self.settings_window, text=f'{value}'.center(40),
                                 font=("Courier", 14, "italic"), relief=GROOVE)
            self.buttons.append(checkbutton)
            checkbutton.place(x=5, y=height + 3 * delta)
            i += 1
            height += 50

        # Кнопки
        self.buttons[0]['command'] = self.button_reaction
        exit_btn = Button(self.settings_window, text=f'Выход',
                          font=("Courier", 12, "italic"), command=self.button_close_program)
        exit_btn.place(x=4 * delta, y=height + 3 * delta)

        exit_btn = Button(self.settings_window, text=f'Сбросить',
                          font=("Courier", 12, "italic"), command=self.discard)
        exit_btn.place(x=7 * delta, y=height + 3 * delta)

    def button_close_program(self):
        self.root.destroy()

    def equation_for_normal_conditions(self):
        t = Symbol('t')
        x = Function('x')
        func = Eq(x(t).diff(t, t), -2*x(t)-3), x(t)
        pprint(func)

    def discard(self):
        """
        Сброс расчёта. Начальное состояние программы.
        """
        self.canvas.delete("all")
        self.chart()

    def button_reaction(self):
        # TODO: проверка работоспособности кнопки
        print('Hello')

    def chart(self):
        self.canvas.create_line(0, self.canvas_opts['height'] // 2,
                                self.canvas_opts['width'], self.canvas_opts['height'] // 2,
                                fill='white', arrow=LAST, arrowshape=(10, 20, 5))

        self.canvas.create_line(self.canvas_opts['width'] // 2, self.canvas_opts['height'],
                                self.canvas_opts['width'] // 2, 0,
                                fill='white', arrow=LAST, arrowshape=(10, 20, 5))

    def read_data_json_file(self):
        """
        Читать данные файла.
        Данный метод ищет файл <Input_data.json> в той же директории где
        лежит файл программы и если не находит, то право на выбор нужного
        файла предоставляется пользователю.
        """
        if find('Input_data.json'):
            with open('Input_data.json', encoding="utf-8") as file:
                self.task_data = json.loads(file.read())
        else:
            with open(filedialog.askopenfilename(title="Откройте файл с данными (формат: .json)"),
                      encoding="utf-8") as file:
                self.task_data = json.loads(file.read())

    def information_console(self):
        """
        Оформление данных задачи в консоли.
        """
        task_text = "Горизонтальный реальный пружинный маятник, " \
                    "закреплённый двумя пружинами. Тело - куб."

        print("Задача №2. Вариант 59.".center(len(task_text)))
        print("Подготовил студент группы М1О-302С-18 Коновалов Ф.Д.\n".center(len(task_text)))
        print("Условие задачи:")
        print(task_text)

        for key, value in self.task_data.items():
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
