import tkinter as tk
from tkinter_app_pattern import TkinterApp
from math import sin, e
import random


def create_spring_coords(start_coord: tuple, amount, distance, diameter, vector):
	list_coords_y = [(start_coord[1] - diameter, start_coord[1] + diameter)] * amount

	if vector > 0:
		plus = distance
		for point in list_coords_y:
			for coord in point:
				yield distance + start_coord[0], coord
				distance += plus

	if vector < 0:
		plus = distance
		for point in list_coords_y:
			for coord in point:
				yield -distance + start_coord[0], coord
				distance += plus

		return list_coords_y


class SpringPendulumAnimation:
	def __init__(self, canvas: tk.Canvas, cube_length):
		self.canvas = canvas
		self.cube_length = cube_length

		self.canvas_width = int(self.canvas['width'])
		self.canvas_height = int(self.canvas['height'])

	def draw_table(self, width, color='black'):
		"""
        Рисовать стол
        Args:
            color:
            width: толщина стола
        """

		# Горизонтальная прямая
		self.canvas.create_line(self.cube_length // 2,
		                        width + self.canvas_height // 2 + self.cube_length // 2,
		                        self.canvas_width - self.cube_length // 2,
		                        width + self.canvas_height // 2 + self.cube_length // 2,
		                        width=width, fill=color)

		# Вертикальные прямые
		self.canvas.create_line(self.cube_length // 2,
		                        self.canvas_height // 2 - self.cube_length // 2,
		                        self.cube_length // 2,
		                        width + self.canvas_height // 2 + self.cube_length // 2,
		                        width=width, fill=color)

		self.canvas.create_line(self.canvas_width - self.cube_length // 2,
		                        self.canvas_height // 2 - self.cube_length // 2,
		                        self.canvas_width - self.cube_length // 2,
		                        width + self.canvas_height // 2 + self.cube_length // 2,
		                        width=width, fill=color)

	def draw_cube(self, plus, color='black'):
		return self.canvas.create_rectangle(self.canvas_width // 2 - self.cube_length // 2 + plus,
		                                    self.canvas_height // 2 - self.cube_length // 2,
		                                    self.canvas_width // 2 + self.cube_length // 2 + plus,
		                                    self.canvas_height // 2 + self.cube_length // 2,
		                                    fill=color)

	def draw_left_spring(self, amount_turn, diameter, distance_turns, color='black'):
		"""
        Рисовать левую пружину.
        Args:
            color:
            amount_turn: кол-во витков пружины
            distance_turns: межвитковое расстояние
            diameter: диаметр пружины
        """
		start_coord = self.cube_length // 2, self.canvas_height // 2
		return self.canvas.create_line(start_coord,
		                               *create_spring_coords(start_coord, amount_turn, distance_turns, diameter, 1),
		                               width=2, fill=color)

	def draw_right_spring(self, amount_turn, diameter, distance_turns, color='black'):
		"""
        Рисовать правую пружину.
        Args:
            amount_turn: кол-во витков пружины
            distance_turns: межвитковое расстояние
            diameter: диаметр пружины
        """
		start_coord = self.canvas_width - self.cube_length // 2, self.canvas_height // 2
		return self.canvas.create_line(start_coord,
		                               *create_spring_coords(start_coord, amount_turn, distance_turns, diameter, -1),
		                               width=2, fill=color)


class App(TkinterApp):
	plus = 1
	delta_right = 20
	delta_left = 20

	@staticmethod
	def get_random_hex_color(red_limit=(0, 255), green_limit=(0, 255), blue_limit=(0, 255)):
		return '#%.2x%.2x%.2x' % (random.randint(*red_limit), random.randint(*green_limit), random.randint(*blue_limit))

	def _ready(self):
		self.window = tk.Canvas(self.root, width=1100, height=400, bg=self.get_random_hex_color())
		self.window.pack()

		self.table = SpringPendulumAnimation(self.window, 150)
		self.table.draw_table(3, self.get_random_hex_color())
		self.left_spring_id = self.table.draw_left_spring(10, 20, self.delta_left, self.get_random_hex_color())
		self.right_spring_id = self.table.draw_right_spring(10, 20, self.delta_right, self.get_random_hex_color())
		self.cube_id = self.table.draw_cube(self.delta_left, self.get_random_hex_color())

	def _physics_process(self, delta):
		self.window.delete(self.left_spring_id)
		self.window.delete(self.right_spring_id)
		self.window.delete(self.cube_id)
		self.left_spring_id = 0
		self.right_spring_id = 0
		self.cube_id = 0
		self.plus += .1

		# гармонические
		self.delta_right = 15 * sin(self.plus) + 20
		self.delta_left = 15 * sin(-self.plus) + 20

		# затухающие
		# self.delta_right = 15 * e ** (-self.plus / 20) * sin(self.plus) + 20
		# self.delta_left = 15 * e ** (-self.plus / 20) * sin(-self.plus) + 20

	def _draw(self):
		self.left_spring_id = self.table.draw_left_spring(10, 20, self.delta_left, self.get_random_hex_color())
		self.right_spring_id = self.table.draw_right_spring(10, 20, self.delta_right, self.get_random_hex_color())
		self.cube_id = self.table.draw_cube(self.delta_left * 20 - 400, self.get_random_hex_color())


if __name__ == '__main__':
	app = App()
	app.run()
