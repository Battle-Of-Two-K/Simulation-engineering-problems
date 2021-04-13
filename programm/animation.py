import tkinter as tk
from tkinter_app_pattern import TkinterApp
from math import sin


class Chart:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_width = int(self.canvas["width"])
        self.canvas_height = int(self.canvas["height"])

    def convert_coords(self, time, cube_position_x, chart_factor):
        if cube_position_x > 0:
            return self.canvas.coords(self.canvas.find_all()[1])[0] + time * chart_factor, \
                   self.canvas.coords(self.canvas.find_all()[0])[1] - cube_position_x * chart_factor
        elif cube_position_x < 0:
            return self.canvas.coords(self.canvas.find_all()[1])[0] + time * chart_factor, \
                   self.canvas.coords(self.canvas.find_all()[0])[1] + abs(cube_position_x) * chart_factor


class Spring:
    def __init__(self, amount_turns: int, diameter: int or float):
        """
        Пружина

        Args:
            amount_turns: кол-во витков пружины
            diameter: диаметр пружины
        """
        self.__amount_turns = amount_turns
        self.__diameter = diameter

    def create_coords(self, start_coord: tuple, end_coord: tuple):
        if start_coord[1] == end_coord[1] and start_coord[0] < end_coord[0]:

            distance_turns = abs(end_coord[0] - start_coord[0]) / self.__amount_turns

            plus = distance_turns
            distance_turns = 0
            for _ in range(self.__amount_turns + 1):
                yield (start_coord[0] + distance_turns, start_coord[1] + self.diameter // 2), \
                      (start_coord[0] + distance_turns, start_coord[1] - self.diameter // 2)
                distance_turns += plus
        else:
            print("Ордината начала и ордината конца должны совпадать")

    @property
    def amount_turns(self):
        return self.__amount_turns

    @property
    def diameter(self):
        return self.__diameter


class Cube:
    def __init__(self, size):
        """
        Кубик

        Args:
            size: размер ребра куба
        """
        self.__size = size

    @property
    def size(self):
        return self.__size


class Table:
    objects_data = {}

    def __init__(self, width, canvas, cube_center_mass_pos):
        """
        Стол

        Args:
            width: ширина стола
            canvas: полотно, на котором отобразится стол
        """
        self.__width = width
        self.canvas_width = int(canvas["width"])
        self.canvas_height = int(canvas["height"])

        self.__center_mass_position = self.canvas_width // 2 + cube_center_mass_pos

    def add_obj(self, additional_object: Spring or Cube):
        if isinstance(additional_object, Cube):
            self.objects_data["cube_size"] = additional_object.size
        elif isinstance(additional_object, Spring):
            self.objects_data["spring_amount_turns"] = additional_object.amount_turns
            self.objects_data["spring_diameter"] = additional_object.diameter

    def generate_table_coords(self):
        """
        Метод возвращает координаты, по которым можно отобразить на полотне стол

        Returns: координаты стола
        """
        return (self.objects_data["cube_size"] // 2, self.canvas_height // 2
                - self.objects_data["cube_size"] // 2), \
               (self.objects_data["cube_size"] // 2, self.canvas_height
                // 2 + self.objects_data["cube_size"] // 2 + 2), \
               (self.canvas_width - self.objects_data["cube_size"] // 2,
                self.canvas_height // 2 + self.objects_data["cube_size"] // 2 + 2), \
               (self.canvas_width - self.objects_data["cube_size"] // 2,
                self.canvas_height // 2 - self.objects_data["cube_size"] // 2)

    def create_coords_mesh_left_spring(self):
        return (self.objects_data["cube_size"] // 2, self.canvas_height // 2), \
               (self.__center_mass_position - self.objects_data["cube_size"] // 2, self.canvas_height // 2)

    def create_coords_mesh_right_spring(self):
        return (self.__center_mass_position + self.objects_data["cube_size"] // 2, self.canvas_height // 2), \
               (self.canvas_width - self.objects_data["cube_size"] // 2, self.canvas_height // 2)

    def combine_objects_on_table(self):
        pass

    @property
    def width(self):
        return self.__width

    @property
    def center_mass_position(self):
        return self.__center_mass_position

    @center_mass_position.setter
    def center_mass_position(self, new_value):
        if new_value == 0:
            self.__center_mass_position = self.canvas_width // 2
        elif new_value > 0:
            self.__center_mass_position = self.canvas_width // 2 + new_value
        else:
            self.__center_mass_position = self.canvas_width // 2 - abs(new_value)


class App(TkinterApp):
    canvas_opts = {
        "width": 720,
        "height": 200,
        "bg": "black"
    }

    app_time = 0  # время, прошедшее со старта

    def _ready(self):
        self.canvas = tk.Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        # создание объетов
        self.start_pos_cube = -400
        self.table = Table(520, self.canvas, self.start_pos_cube)

        self.cube_len = 90
        self.cube = Cube(self.cube_len)
        self.left_spring = Spring(20, 25)
        self.right_spring = Spring(20, 25)

        # Добавление объектов на стол:
        self.table.add_obj(self.cube)
        self.table.add_obj(self.left_spring)
        self.table.add_obj(self.right_spring)

    def _physics_process(self, delta):
        self.canvas.delete('spring')
        self.canvas.delete('table')
        self.canvas.delete('cube')
        self.table.center_mass_position = 200 * sin(self.app_time / 10 - self.start_pos_cube)
        self.app_time += delta

    def _draw(self):
        self.canvas.create_line(*self.table.generate_table_coords(), fill="#B2B428", width=2, tags=("table",))
        self.canvas.create_line(*self.left_spring.create_coords(self.table.create_coords_mesh_left_spring()[0],
                                                                self.table.create_coords_mesh_left_spring()[1]),
                                fill="#B2B428", tags=("spring",))

        self.canvas.create_line(*self.right_spring.create_coords(self.table.create_coords_mesh_right_spring()[0],
                                                                 self.table.create_coords_mesh_right_spring()[1]),
                                fill="#B2B428", tags=("spring",))

        self.canvas.create_rectangle(self.table.center_mass_position - self.cube_len // 2,
                                     self.canvas_opts['height'] // 2 - self.cube_len // 2,
                                     self.table.center_mass_position + self.cube_len // 2,
                                     self.canvas_opts['height'] // 2 + self.cube_len // 2,
                                     fill="#B2B428", tags=("cube",))


if __name__ == '__main__':
    app = App()
    app.run()
