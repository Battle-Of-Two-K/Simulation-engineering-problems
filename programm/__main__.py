import os
import json
import logging
from animation import *
from math import sin, e, cos
import tkinter.ttk as ttk
from tkinter import filedialog
from equation import DiffEqSecKind
from tkinter_app_pattern import TkinterApp

# Константы:
PENDULUM_AMPLITUDE = 210  # амплитуда маятника
START_POSITION_CUBE = 150  # начальное положение куба
SPRING_SHAPE = 10, 20  # 10 - кол-во витков, 20 - диаметр
CUBE_LENGTH = 80  # длина ребра куба

ROOT_SIZE = "1182x724+300+100"
PLACE_WIN_ANIMATION = 0, 0
PLACE_SET_WINDOW = 720, 0
PLACE_CHART_WINDOW = 0, 240
ARROW_SHAPE = 10, 20, 5
ORDINATE_POSITION = 50
OUTSIDE_CANVAS = -50, -50, -50, -50
DASH = 4, 2
CHART_STOP_POINT = 700

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

    style.map('TButton', foreground=[('pressed', 'red'), ('active', '#FF6A54')],
              background=[('pressed', '!disabled', '#FCEAC6'), ('active', '#4B505C')])


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

    task_data = {}  # данные задачи

    app_time = 0  # время приложения
    coords_chart = []
    coords_chart_two = []
    coords_chart_three = []

    chart_factor = 2
    time_factor = 100

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
        self.table = Table(self.animation, START_POSITION_CUBE)  # стол
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
        self.add_line_up_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', dash=DASH)
        self.add_line_down_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', dash=DASH)

        self._phys_flag = False  # не запускать процесс (работу приложения)

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

        # Условие начала отрисовки графика:
        if len(self.coords_chart) > 2:
            # Отрисовка графика:
            self.window_chart.coords(self.main_chart_id, *self._flatten(self.coords_chart))
            self.window_chart.coords(self.add_line_up_id, *self._flatten(self.coords_chart_two))
            self.window_chart.coords(self.add_line_down_id, *self._flatten(self.coords_chart_three))

    def create_equation_motion(self, time_factor):
        self.equation = DiffEqSecKind(5, 10, 0)
        eq_roots = self.equation.solve_characteristic_equation()

        if isinstance(eq_roots[0], complex) or isinstance(eq_roots[1], complex):
            return (e ** (eq_roots[0].real * self.app_time / time_factor)) * \
                   (100 * cos(eq_roots[0].imag * self.app_time / time_factor) +
                    50 * sin(eq_roots[0].imag * self.app_time / time_factor)) \
                   + self.equation.particular_solution_equation()

        elif isinstance(eq_roots[0], float or int) or isinstance(eq_roots[1], float or int):
            return (100 * e ** (eq_roots[0] * self.app_time / time_factor) +
                    50 * e ** (eq_roots[1] * self.app_time / time_factor)) \
                   + self.equation.particular_solution_equation()

        else:
            return (e ** (eq_roots[0] * self.app_time / time_factor) * (100 + 50 * self.app_time / time_factor)) \
                   + self.equation.particular_solution_equation()

    def _physics_process(self, delta):
        self.function = self.create_equation_motion(self.time_factor)

        self.animation.delete('left_spring')
        self.animation.delete('right_spring')
        self.animation.delete('table')
        self.animation.delete('cube')

        # положение куба:
        self.table.center_mass_position = self.function

        # добавление в список следующей пары координат:
        self.coords_chart.append(self.chart.convert_coords(self.app_time, self.function, self.chart_factor))
        self.app_time += delta

        if self.coords_chart[-1][0] < CHART_STOP_POINT:
            self._phys_flag = True
        else:
            self._phys_flag = False

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

        start_btn = ttk.Button(self.window_chart, text=f'Start', command=self.button_start_process)
        start_btn.place(x=380, y=424)

        stop_btn = ttk.Button(self.window_chart, text=f'Stop', command=self.button_stop_process)
        stop_btn.place(x=550, y=424)

    def button_stop_process(self):
        self._phys_flag = False

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
        self.window_chart.delete(self.add_line_up_id)
        self.window_chart.delete(self.add_line_down_id)

        # Отрисовка осей:
        self.draw_chart_axes()

        # Обновление времени приложения:
        self.app_time = 0

        # Очистка списка координат:
        self.coords_chart = []
        self.coords_chart_two = []
        self.coords_chart_three = []

        # Приведение положения кубика к начальному состоянию:
        self.table.center_mass_position = START_POSITION_CUBE

        self.main_chart_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FFB54F', width=2)
        self.add_line_up_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', dash=DASH)
        self.add_line_down_id = self.window_chart.create_line(OUTSIDE_CANVAS, fill='#FF6A54', dash=DASH)

    def button_start_process(self):
        """
        Начать процесс (начать работу приложения)
        """
        self._phys_flag = True

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
