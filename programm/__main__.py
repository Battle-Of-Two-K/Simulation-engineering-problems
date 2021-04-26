import os
import json
import logging
from math import pi
from animation import *
import tkinter.ttk as ttk
from tkinter import filedialog
from equation import DiffEqSecKind
from tkinter_app_pattern import TkinterApp

# Константы:
SPRING_SHAPE = 10, 20  # 10 - кол-во витков, 20 - диаметр
CUBE_LENGTH = 80  # длина ребра куба

ROOT_SIZE = "1182x724+300+100"
PLACE_WIN_ANIMATION = 0, 0
PLACE_SET_WINDOW = 720, 0
PLACE_CHART_WINDOW = 0, 240
ARROW_SHAPE = 10, 20, 5
ORDINATE_POSITION = 50
OUTSIDE_CANVAS = -50, -50, -50, -50
MAIN_PARAMS = (600, 25), 25
CORRECT_COORDS_DATA = 220

CHART_STOP_POINT = 700
CHART_FACTOR = 1
TIME_FACTOR = 50

FORM_RESISTANCE_COEFFICIENT = 1.05  # коэффициент сопротивления формы
COEFFICIENT_FRICTION = 0.4  # коэффициент трения скольжения
free_fall_coefficient = 9.8
PIXEL_FACTOR = 38

# строчка, позволяет не выводить лишние данные (они нужны только разработчику):
logging.basicConfig(level=logging.ERROR)


def find(name):
    """
    Поиск файла
    Args:
        name: имя файла

    Returns: True или False
    """
    return os.path.exists(name)


def button_app_style():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('TButton', background='#2B2E35',
                    foreground='#FF6A54', width=10,
                    borderwidth=1, focusthickness=2,
                    relief='sunken',
                    focuscolor='#2B2E30',
                    font=('Comic Sans MS', 16, 'italic'))

    style.map('TButton', foreground=[('pressed', 'red'), ('active', '#FCEAC6')],
              background=[('pressed', '!disabled', '#FCEAC6'), ('active', '#4B505C')])

    style.configure('TCombobox', background='#2B2E35',
                    foreground='#FCEAC6', width=10,
                    borderwidth=1, focusthickness=2,
                    relief='sunken',
                    fieldbackground='#2B2E35',
                    selectbackground='#2B2E35',
                    selectforeground='#FCEAC6',
                    font=('Comic Sans MS', 16, 'italic'))

    style.map('TCombobox', foreground=[('pressed', '#FCEAC6'), ('active', 'black')])


class App(TkinterApp):
    FRAME_COLOR = '#FCEAC6'
    chart_opts = {
        'width': 720,
        'height': 480,
        'bg': '#2B2E35',
        'highlightbackground': FRAME_COLOR,
        'highlightcolor': FRAME_COLOR
    }

    animation_opts = {
        'width': 720,
        'height': 240,
        'bg': '#2B2E35',
        'highlightbackground': FRAME_COLOR,
        'highlightcolor': FRAME_COLOR
    }

    settings_window_opts = {
        'width': 462,
        'height': 724,
        'bg': '#2B2E35',
        'highlightbackground': FRAME_COLOR,
        'highlightcolor': FRAME_COLOR,
        'highlightthickness': 2

    }

    text_param = {
        'font': ('Comic Sans MS', 15, "italic"),
        'bg': '#2B2E35',
        'fg': '#FCEAC6'
    }

    font_main_params = ('Comic Sans MS', 12, "italic")

    task_data = {}  # данные задачи

    app_time = 0  # время приложения
    coords_chart = []
    coords_chart_two = []
    coords_chart_three = []

    info_text = []

    start_flag = False

    def _ready(self):

        # Считываем информацию с файла:
        self.read_data_json_file()

        self.root.geometry(ROOT_SIZE)
        self.root.title("Лабораторная работа по МИЗу. Подготовил: Коновалов Ф.Д., группа М1О-302С")
        self.root.resizable(width=False, height=False)  # неизменный размер окна

        # Рамка с информацией о задаче:
        self.settings_window = tk.Frame(self.root, **self.settings_window_opts)
        self.settings_window.place(x=PLACE_SET_WINDOW[0], y=PLACE_SET_WINDOW[1])

        # Полотно с анимацией маятника:
        self.animation = tk.Canvas(self.root, **self.animation_opts)
        self.animation.place(x=PLACE_WIN_ANIMATION[0], y=PLACE_WIN_ANIMATION[1])

        # Создание объектов
        self.table = Table(self.animation, self.task_data["Входные данные"]["Отклонение"])  # стол
        self.cube = Cube(CUBE_LENGTH)  # кубик
        self.left_spring = Spring(*SPRING_SHAPE)  # левая пружина
        self.right_spring = Spring(*SPRING_SHAPE)  # правая пружина

        # Добавление объектов на стол:
        self.table.add_obj(self.cube)  # добавление куба на стол
        self.table.add_obj(self.left_spring)  # добавление левой пружины на стол
        self.table.add_obj(self.right_spring)  # добавление правой пружины на стол

        # Полотно с графиком:
        self.window_chart = tk.Canvas(self.root, **self.chart_opts)
        self.window_chart.place(x=PLACE_CHART_WINDOW[0], y=PLACE_CHART_WINDOW[1])

        self.draw_chart_axes()  # отрисовка осей координат

        self.chart = Chart(self.window_chart)  # создание графика

        self.information_canvas()  # вывод считанной информации с файла на рамку

        self.main_chart_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FFB54F', width=2)
        self.main_chart_id_two = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', width=1, dash=(4, 2))
        self.main_chart_id_three = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', width=1, dash=(4, 2))

        self._phys_flag = False  # не запускать процесс (работу приложения)

        self.output_data(self.window_chart, *MAIN_PARAMS)

    def _draw(self):
        # Отрисовка стола:
        self.animation.create_line(*self.table.generate_table_coords(), fill='#FCEAC6', width=2, tags=("table",))

        # Отрисовка левой пружины:
        self.animation.create_line(*self.left_spring.create_coords(self.table.create_coords_mesh_left_spring()[0],
                                                                   self.table.create_coords_mesh_left_spring()[1]),
                                   fill='#FFB54F', tags=("left_spring",))

        # Отрисовка правой пружины:
        self.animation.create_line(*self.right_spring.create_coords(self.table.create_coords_mesh_right_spring()[0],
                                                                    self.table.create_coords_mesh_right_spring()[1]),
                                   fill='#FFB54F', tags=("right_spring",))

        # Отрисовка кубика:
        self.animation.create_rectangle(self.table.center_mass_position - CUBE_LENGTH // 2,
                                        self.animation_opts['height'] // 2 - CUBE_LENGTH // 2,
                                        self.table.center_mass_position + CUBE_LENGTH // 2,
                                        self.animation_opts['height'] // 2 + CUBE_LENGTH // 2,
                                        fill="#FF6A54", tags=("cube",))

        if not self.start_flag:
            self._draw_flag = False
        else:
            self._draw_flag = True

        # Условие начала отрисовки графика:
        if len(self.coords_chart) > 2:
            # Отрисовка графика:
            if len(self.coords_chart_two) != 0 and len(self.coords_chart_three) != 0:
                self.window_chart.coords(self.main_chart_id, *self._flatten(self.coords_chart))
                self.window_chart.coords(self.main_chart_id_two, *self._flatten(self.coords_chart_two))
                self.window_chart.coords(self.main_chart_id_three, *self._flatten(self.coords_chart_three))
            else:
                self.window_chart.coords(self.main_chart_id, *self._flatten(self.coords_chart))

            # Условие остановки графика:
            if self.coords_chart[-1][0] < CHART_STOP_POINT:
                self._phys_flag = True
            else:
                self._phys_flag = False
                self._draw_flag = False

    def _physics_process(self, delta):

        # Уравнение движения (составленное по 2-му з-ну Ньютона):
        self.equation = DiffEqSecKind(
            FORM_RESISTANCE_COEFFICIENT / self.cube_mass,
            2 * self.spring_coeff_elasticity / self.cube_mass,
            -COEFFICIENT_FRICTION * free_fall_coefficient,
            (self.task_data["Входные данные"]["Отклонение"], 0))

        # print(self.equation._calculate_discriminant())

        function = self.equation.create_equation(self.app_time, TIME_FACTOR)

        # Условие прорисовки вспомогательных (красных) линий при затухающих колебаниях:
        if isinstance(function, tuple):
            function = self.equation.create_equation(self.app_time, TIME_FACTOR)[0]
            function_two = self.equation.create_equation(self.app_time, TIME_FACTOR)[1]
            function_three = -self.equation.create_equation(self.app_time, TIME_FACTOR)[1]

        else:
            function = self.equation.create_equation(self.app_time, TIME_FACTOR)
            function_two = 0
            function_three = 0

        self.animation.delete('left_spring')
        self.animation.delete('right_spring')
        self.animation.delete('table')
        self.animation.delete('cube')

        # положение куба:
        self.table.center_mass_position = function

        # добавление в список следующей пары координат:
        self.coords_chart.append(self.chart.convert_coords(self.app_time, function, CHART_FACTOR))
        self.coords_chart_two.append(self.chart.convert_coords(self.app_time, function_two, CHART_FACTOR))
        self.coords_chart_three.append(
            self.chart.convert_coords(self.app_time, function_three, CHART_FACTOR))
        self.app_time += delta

    def information_canvas(self):
        """
        Вывод информации о задаче + вывод кнопок на полотно.
        Изначально метод получился слишком большим. Для простоты восприятия
        кода данный метод рыл разбит на несколько методов.
        Расположение данных и кнопок зависит от величин height, delta, abscissa,
        которые изменяются по мере заполнения данных.
        """
        # Величины, от к-х зависит расположение данных на окне:
        height, delta = 50, 35
        abscissa = 5

        # Заголовок:
        tk.Label(self.settings_window, text='Задача №2. Вариант 59', font=('Comic Sans MS', 18, "bold"),
                 bg='#2B2E35', fg='#5188BA').place(x=80, y=10)

        # Первый блок данных:
        height, delta, abscissa = self.print_input_data(height, delta, abscissa)

        # Второй блок данных:
        height, delta, abscissa = self.print_add_conditions(height, delta, abscissa)

        # Третий блок данных:
        height, delta, abscissa = self.print_special_conditions(height, delta, abscissa)

        # Кнопки:
        self.output_buttons(height, delta)

    def print_input_data(self, height, delta, abscissa):
        """
        Вывод входных данных
        Args:
            height: величина, влияющая на расположение данных на окне
            delta: величина, влияющая на расположение данных на окне
            abscissa: величина, влияющая на расположение данных на окне
        """
        tk.Label(self.settings_window, text="1.Входные данные:", font=('Comic Sans MS', 16, "bold"),
                 bg='#2B2E35', fg='#FFB54F').place(x=abscissa, y=height)

        for key, value in self.task_data["Входные данные"].items():
            tk.Label(self.settings_window, text=f'  {key}: {value}', **self.text_param).place(
                x=abscissa, y=height + delta)
            height += delta

        return height, delta, abscissa

    def print_add_conditions(self, height, delta, abscissa):
        """
        Вывод дополнительных условий
        Args:
            height: величина, влияющая на расположение данных на окне
            delta: величина, влияющая на расположение данных на окне
            abscissa: величина, влияющая на расположение данных на окне
        """
        tk.Label(self.settings_window, text="2.Дополнительные условия:", font=('Comic Sans MS', 16, "bold"),
                 bg='#2B2E35', fg='#FFB54F').place(
            x=abscissa, y=height + delta)

        for key, value in self.task_data["Дополнительные условия"].items():
            if key == "Материал тела":
                tk.Label(self.settings_window, text=f'  {key}: ', **self.text_param).place(
                    x=abscissa, y=height + 2 * delta)

                self.text_var_first = tk.StringVar(self.settings_window)
                material_box = ttk.Combobox(self.settings_window,
                                            width=10,
                                            textvariable=self.text_var_first,
                                            values=[i for i, j in self.task_data["Плотность"].items()],
                                            font=('Comic Sans MS', 16, "italic"))

                material_box.place(x=abscissa + 280, y=height + 2 * delta)
                material_box.current(0)
                material_box.bind("<<ComboboxSelected>>", self.box_call_first)

            elif key == "Материал пружины":
                tk.Label(self.settings_window, text=f'  {key}: ', **self.text_param).place(
                    x=abscissa, y=height + 2 * delta)

                self.text_var_second = tk.StringVar(self.settings_window)
                material_box = ttk.Combobox(self.settings_window,
                                            width=10,
                                            textvariable=self.text_var_second,
                                            values=[i for i, j in self.task_data["Модуль сдвига"].items()],
                                            font=('Comic Sans MS', 16, "italic"))

                material_box.place(x=abscissa + 280, y=height + 2 * delta)
                material_box.current(0)
                material_box.bind("<<ComboboxSelected>>", self.box_call_second)

            else:
                tk.Label(self.settings_window, text=f'  {key}: {value}', **self.text_param).place(
                    x=abscissa, y=height + 2 * delta)

            height += delta

        return height, delta, abscissa

    def print_special_conditions(self, height, delta, abscissa):
        """
        Вывод особых условий
        Args:
            height: величина, влияющая на расположение данных на окне
            delta: величина, влияющая на расположение данных на окне
            abscissa: величина, влияющая на расположение данных на окне
        """
        tk.Label(self.settings_window, text="3.Особые условия:", font=('Comic Sans MS', 16, "bold"),
                 bg='#2B2E35', fg='#FFB54F').place(
            x=abscissa, y=height + 2 * delta)

        for key in self.task_data["Особые условия"]:
            tk.Label(self.settings_window, text=f'  -{key}', **self.text_param).place(
                x=abscissa, y=height + 3 * delta)
            height += delta

        return height, delta, abscissa

    def output_buttons(self, height, delta):
        """
        Создание кнопок
        Args:
            height: величина, влияющая на расположение кнопки на окне
            delta: величина, влияющая на расположение кнопки на окне
        """
        button_app_style()  # установка стиля кнопок

        exit_btn = ttk.Button(self.settings_window, text=f'Выход', command=self.button_close_program)
        exit_btn.place(x=2 * delta, y=height + 3.5 * delta)

        update_btn = ttk.Button(self.settings_window, text=f'Сбросить', command=self.button_update_process)
        update_btn.place(x=7 * delta, y=height + 3.5 * delta)

        start_btn = ttk.Button(self.window_chart, text=f'Начать', command=self.button_start_process)
        start_btn.place(x=380, y=424)

        stop_btn = ttk.Button(self.window_chart, text=f'Пауза', command=self.button_stop_process)
        stop_btn.place(x=550, y=424)

    def box_call_first(self, event):
        self.task_data["Дополнительные условия"]["Материал тела"] = self.text_var_first.get()
        self.update_main_model_params()
        return event

    def box_call_second(self, event):
        self.task_data["Дополнительные условия"]["Материал пружины"] = self.text_var_second.get()
        self.update_main_model_params()
        return event

    def button_stop_process(self):
        self._phys_flag = False
        self._proc_flag = False
        self._draw_flag = False

    def button_update_process(self):
        """
        Сброс текущего состояния приложения
        """
        # Удаление объектов текущего состояния с анимации:
        self.animation.delete('left_spring')
        self.animation.delete('right_spring')
        # self.animation.delete('table')
        self.animation.delete('cube')

        # Удаление графика текущего состояния (и осей координат):
        self.window_chart.delete(self.main_chart_id)
        self.window_chart.delete(self.main_chart_id_two)
        self.window_chart.delete(self.main_chart_id_three)

        # Отрисовка осей:
        self.draw_chart_axes()

        # Обновление времени приложения:
        self.app_time = 0

        # Очистка списка координат:
        self.coords_chart = []
        self.coords_chart_two = []
        self.coords_chart_three = []

        # Приведение положения кубика к начальному состоянию:
        self.table.center_mass_position = self.task_data["Входные данные"]["Отклонение"]

        # Обновление основных параметров маятника:
        self.update_main_model_params()

        self._phys_flag = False
        self._draw_flag = True

        self.main_chart_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FFB54F', width=2)
        self.main_chart_id_two = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', width=1, dash=(2, 4))
        self.main_chart_id_three = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', width=1, dash=(2, 4))

        self.start_flag = False

    def button_start_process(self):
        """
        Начать процесс (начать работу приложения)
        """
        self._phys_flag = True
        self._draw_flag = True
        self.start_flag = True

    def button_close_program(self):
        """
        Закрыть приложение
        """
        self.root.destroy()

    def draw_chart_axes(self):
        """
        Отрисовка осей координат
        """
        self.window_chart.create_line(0, self.chart_opts['height'] // 2,
                                      self.chart_opts['width'], self.chart_opts['height'] // 2,
                                      fill='white', arrow=tk.LAST, arrowshape=ARROW_SHAPE)

        self.window_chart.create_line(ORDINATE_POSITION, self.chart_opts['height'], ORDINATE_POSITION, 0,
                                      fill='white', arrow=tk.LAST, arrowshape=ARROW_SHAPE)

    def discard(self):
        """
        Сброс расчёта. Начальное состояние программы.
        """
        self.window_chart.delete("all")
        self.draw_chart_axes()

    def read_data_json_file(self):
        """
        Читать данные файла.
        Данный метод ищет файл <Input_data.json> в той же директории где
        лежит файл программы и если не находит, то право на выбор нужного
        файла предоставляется пользователю.
        """
        if find('Input_data.json'):
            with open('../programm/Input_data.json', encoding="utf-8") as file:
                self.task_data = json.loads(file.read())
        else:
            with open(filedialog.askopenfilename(title="Откройте файл с данными (формат: .json)"), encoding="utf-8") \
                    as file:
                self.task_data = json.loads(file.read())

    def information_console(self):
        """
        Оформление данных задачи в консоли.
        """
        task_text = "Горизонтальный реальный пружинный маятник, закреплённый двумя пружинами. Тело - куб."

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

    def update_main_model_params(self):
        for i in self.info_text:
            self.window_chart.delete(i)
        self.info_text = []

        self.output_data(self.window_chart, *MAIN_PARAMS)

    def output_data(self, canvas: tk.Canvas, coords: tuple, delta):
        self.info_text.append(canvas.create_text(coords,
                                                 text=u"\u03B2 =" + f" {self.damping_factor}",
                                                 font=self.font_main_params,
                                                 fill=self.text_param["fg"]))

        self.info_text.append(canvas.create_text(coords[0], coords[1] + delta,
                                                 text="\u03C9_0 =" + f" {self.natural_frequency_ideal_pendulum}",
                                                 font=self.font_main_params,
                                                 fill=self.text_param["fg"]))

        self.info_text.append(canvas.create_text(coords[0], coords[1] + 2 * delta,
                                                 text="\u03C9 =" + f" {self.damped_oscillation_frequency}",
                                                 font=self.font_main_params,
                                                 fill=self.text_param["fg"]))

        self.info_text.append(canvas.create_text(coords[0] - CORRECT_COORDS_DATA, coords[1],
                                                 text="\u03A4 =" + f" {self.period}",
                                                 font=self.font_main_params,
                                                 fill=self.text_param["fg"]))

        self.info_text.append(canvas.create_text(coords[0] - CORRECT_COORDS_DATA, coords[1] + delta,
                                                 text="\u03BB =" + f" {self.damping_decrement}",
                                                 font=self.font_main_params,
                                                 fill=self.text_param["fg"]))

    @property
    def damping_factor(self):
        """
        Расчёт коэффициента затухания
        Returns: коэффициент затухания
        """
        return FORM_RESISTANCE_COEFFICIENT / (2 * self.cube_mass)

    @property
    def natural_frequency_ideal_pendulum(self):
        """
        Расчёт частоты собственных колебаний идеального маятника
        Returns: частота собственных колебаний идеального маятника
        """
        return (self.spring_coeff_elasticity / self.cube_mass) ** .5

    @property
    def damped_oscillation_frequency(self):
        """
        Расчёт частоты затухающих колебаний
        Returns: частота затухающих колебаний
        """
        return (self.natural_frequency_ideal_pendulum ** 2 - self.damping_factor ** 2) ** .5

    @property
    def period(self):
        """
        Расчёт периода затухающих колебаний
        Returns: период затухающих колебаний
        """
        return 2 * pi / self.damped_oscillation_frequency

    @property
    def damping_decrement(self):
        """
        Расчёт логарифмического декремента затухания
        Returns: период затухающих колебаний
        """
        return self.period * self.damping_factor

    @property
    def cube_mass(self):
        """
        Расчёт массы кубика
        Returns: масса кубика
        """

        for key, value in self.task_data["Плотность"].items():
            if self.task_data["Дополнительные условия"]["Материал тела"] == key:
                return value * (self.task_data["Входные данные"]["Размер куба"] ** 3) / 1000

    @property
    def shear_modulus(self):
        """
        Подбор модуля сдвига (зависит от материала пружины)
        Returns: модуль сдвига
        """
        for key, value in self.task_data["Модуль сдвига"].items():
            if self.task_data["Дополнительные условия"]["Материал пружины"] == key:
                return value * (10 ** 10)

    @property
    def spring_coeff_elasticity(self):
        """
        Расчёт коэффициента упругости пружины
        Returns: коэффициент упругости пружины
        """
        amount_turns_spring = (PIXEL_FACTOR * self.task_data["Дополнительные условия"]["Длина пружин"] /
                               PIXEL_FACTOR * self.task_data["Входные данные"]["Шаг витков пружины"]) + 1

        return (self.shear_modulus * PIXEL_FACTOR * (self.task_data["Входные данные"]["Диаметр проволоки"] ** 4)) / \
               (8 * (PIXEL_FACTOR * self.task_data["Входные данные"]["Диаметр пружины"] ** 3) * amount_turns_spring)

    @property
    def coefficient_friction(self):
        """
        Расчёт коэффициента трения скольжения
        Returns: коэффициент трения скольжения
        """
        return float(input("Введите коэффициент трения скольжения: "))

    @staticmethod
    def _flatten(seq):
        """Internal function."""
        res = ()
        for item in seq:
            if isinstance(item, (tuple, list)):
                res = res + App._flatten(item)
            elif item is not None:
                res = res + (item,)
        return res


if __name__ == '__main__':
    app = App()
    app.run()
