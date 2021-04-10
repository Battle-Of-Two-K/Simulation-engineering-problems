from other_variant.tkinter_app_pattern import TkinterApp
import tkinter as tk
from math import sin
from time import time
from tkinter import ttk


class Drawable:
	def draw(self):
		raise NotImplementedError


class Spring:
	__left = 0
	__right = 0

	def __init__(self, left, right, amount, diameter):
		self.__left = left
		self.__right = right
		self.amount = amount
		self.diameter = diameter
		self.zero_state_len = self.len

	def __str__(self):
		return f"{self.__class__.__name__}. start: {self.left}, end: {self.right}"

	def x_coords(self):
		count = self.len / self.turn_distance
		for i in range(int(count)):
			yield self.left + self.turn_distance * i

	def coords(self):
		for no, x in enumerate(self.x_coords()):
			if no % 2 == 0:
				yield x, self.diameter / 2
			else:
				yield x, -self.diameter / 2

	def with_y(self, y_value):
		for coords in self.coords():
			yield coords[0], coords[1] + y_value

	@property
	def left(self):
		return self.__left

	@property
	def right(self):
		return self.__right

	@left.setter
	def left(self, new_value):
		if new_value < self.right:
			self.__left = new_value
		elif new_value > self.right:
			self.__right, self.__left = new_value, self.__right
		else:
			raise RuntimeError("zero len spring")

	@right.setter
	def right(self, new_value):
		if new_value > self.left:
			self.__right = new_value
		elif new_value < self.left:
			self.__right, self.__left = self.__left, new_value
		else:
			RuntimeError("zero len spring")

	@property
	def turn_distance(self):
		return self.len / self.amount

	@property
	def energy(self):
		return (self.zero_state_len - self.len) * 2

	@property
	def len(self):
		return self.right - self.left

	@len.setter
	def len(self, new_value):
		self.zero_state_len = new_value


SPRING_SHAPE = 0, 500, 50, 20


class App(TkinterApp):
	def _ready(self):
		self.canvas = tk.Canvas(width=500, height=500, bg='white')
		self.canvas.grid(row=0, column=0)

		self.spring = Spring(*SPRING_SHAPE)

		self.left = tk.DoubleVar()
		self.right = tk.DoubleVar()
		self.scale = ttk.Scale(var=self.left, from_=0, to=9, length=500)
		self.scale2 = ttk.Scale(var=self.right, from_=0, to=9, length=500)
		self.scale.grid(row=1, column=0, pady=2)
		self.scale2.grid(row=2, column=0, pady=2)

	def _physics_process(self, delta):
		self.spring.left = self.left.get() * 50
		self.spring.right = self.right.get() * 50

	def _draw(self):
		self.canvas.delete('spring')
		self.canvas.create_line(list(self.spring.with_y((sin(time() * 2) + 1 / 2) * 100 + 100)), tags=("spring",))


if __name__ == '__main__':
	app = App()
	app.run()

