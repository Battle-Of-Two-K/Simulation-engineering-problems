import tkinter as tk
from tkinter_app_pattern import TkinterApp


# B2B428
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

    def __init__(self, width):
        """
        Стол
        Args:
            width: ширина стола
        """
        self.__width = width

    def add_obj(self, additional_object: Spring or Cube):
        if additional_object is Cube:
            # self.objects_data["cube_size"] = additional_object.size  # этот вариант не работает
            self.objects_data.update({"cube_size": additional_object.size})  # этот тоже
        elif additional_object is Spring:
            self.objects_data["spring_amount_turns"] = additional_object.amount_turns
            self.objects_data["spring_diameter"] = additional_object.diameter

    @property
    def width(self):
        return self.__width


class App(TkinterApp):
    canvas_opts = {
        "width": 720,
        "height": 300,
        "bg": "black"
    }

    def _ready(self):
        self.canvas = tk.Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        # создание объетов
        self.table = Table(520)
        self.cube = Cube(70)
        self.left_spring = Spring(10, 20)
        self.right_spring = Spring(10, 20)

        # Добавление объектов на стол:
        self.table.add_obj(self.cube)
        self.table.add_obj(self.left_spring)
        self.table.add_obj(self.right_spring)

        self.table.add_obj(self.canvas)

        print(self.table.objects_data)  # словарь остаётся пустым после добавления объектов на стол

    def _physics_process(self, delta):
        pass

    def _draw(self):
        pass


if __name__ == '__main__':
    app = App()
    app.run()
