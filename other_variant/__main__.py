import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from math import sin, cos, e
from tkinter_app_pattern import TkinterApp


def find(name):
	return os.path.exists(name)


class App(TkinterApp):
	frame_color = '#FCEAC6'
	chart_opts = {
		'width': 720,
		'height': 480,
		'bg': '#2B2E35',
		'highlightbackground': frame_color,
		'highlightcolor': frame_color
	}

	animation_opts = {
		'width': 720,
		'height': 240,
		'bg': '#2B2E35',
		'highlightbackground': frame_color,
		'highlightcolor': frame_color
	}

	settings_window_opts = {
		'width': 462,
		'height': 724,
		'bg': '#2B2E35',
		'highlightbackground': frame_color,
		'highlightcolor': frame_color,
		'highlightthickness': 2

	}

	text_param = {
		'font': ('Comic Sans MS', 15, "italic"),
		'bg': '#2B2E35',
		'fg': '#FCEAC6'
	}

	task_data = {}  # данные задачи
	materials_data = {}  # таблица материалов
	buttons = []

	springs_ids = []
	plus = 0
	delta = 0

	def draw_table(self):
		pass

	def _ready(self):
		self.read_data_json_file()
		self.root.geometry("1182x724+300+100")
		self.root.resizable(width=False, height=False)
		# self.root.overrideredirect(1)

		self.settings_window = tk.Frame(self.root, **self.settings_window_opts)
		self.settings_window.place(x=720, y=0)

		self.animation = tk.Canvas(self.root, **self.animation_opts)
		self.animation.place(x=0, y=0)

		self.chart = tk.Canvas(self.root, **self.chart_opts)
		self.chart.place(x=0, y=240)

		self.draw_chart()
		self.information_canvas()

	# self.draw_model()

	def create_coords(self, delta_abscissa):
		diameter = 20
		center = self.animation_opts['height'] // 2
		set_ordinate_coords = [center, center - diameter // 2,
							   center + diameter // 2, center - diameter // 2,
							   center + diameter // 2, center - diameter // 2, center + diameter // 2, center]

		plus = delta_abscissa
		for i in set_ordinate_coords:
			yield delta_abscissa, i
			delta_abscissa += plus

	def draw_model(self, length):
		self.springs_ids.append(self.animation.create_line(*self.create_coords(length),
														   fill='white', width=2))

	def _draw(self):
		self.draw_model(self.delta)

	def _physics_process(self, delta):
		self.animation.delete(self.springs_ids)
		self.springs_ids = []

		self.plus += .1

		self.delta = 20 * cos(self.plus) + 60

	def information_canvas(self):
		"""
		Вывод информации о задаче + вывод кнопок на полотно
		"""
		height, delta = 50, 35
		abscissa = 5

		tk.Label(self.settings_window, text='Задача №2. Вариант 59', font=('Comic Sans MS', 18, "bold"),
				 bg='#2B2E35', fg='#5188BA').place(x=80, y=10)

		# Первый блок данных
		tk.Label(self.settings_window, text="1.Входные данные:", font=('Comic Sans MS', 16, "bold"),
				 bg='#2B2E35', fg='#FFB54F').place(x=abscissa, y=height)

		for key, value in self.task_data["Входные данные"].items():
			tk.Label(self.settings_window, text=f'  {key}: {value} мм', **self.text_param).place(
				x=abscissa, y=height + delta)
			height += delta

		# Второй блок данных
		tk.Label(self.settings_window, text="2.Дополнительные условия:", font=('Comic Sans MS', 16, "bold"),
				 bg='#2B2E35', fg='#FFB54F').place(
			x=abscissa, y=height + delta)

		for key, value in self.task_data["Дополнительные условия"].items():
			tk.Label(self.settings_window, text=f'  {key}: {value}', **self.text_param).place(
				x=abscissa, y=height + 2 * delta)
			height += delta

		# Третий блок данных
		tk.Label(self.settings_window, text="3.Особые условия:", font=('Comic Sans MS', 16, "bold"),
				 bg='#2B2E35', fg='#FFB54F').place(
			x=abscissa, y=height + 2 * delta)

		for key in self.task_data["Особые условия"]:
			tk.Label(self.settings_window, text=f'  -{key}', **self.text_param).place(
				x=abscissa, y=height + 3 * delta)
			height += delta

		# Кнопки
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

		exit_btn = ttk.Button(self.settings_window, text=f'Выход', command=self.button_close_program)
		exit_btn.place(x=2 * delta, y=height + 3.5 * delta)

		update_btn = ttk.Button(self.settings_window, text=f'Сбросить', command=self.discard)
		update_btn.place(x=7 * delta, y=height + 3.5 * delta)

		start_btn = ttk.Button(self.chart, text=f'Start', command=self.discard)
		start_btn.place(x=550, y=424)

	def button_close_program(self):
		self.root.destroy()

	def draw_chart(self):
		self.chart.create_line(0, self.chart_opts['height'] // 2,
							   self.chart_opts['width'], self.chart_opts['height'] // 2,
							   fill='white', arrow=tk.LAST, arrowshape=(10, 20, 5))

		self.chart.create_line(50, self.chart_opts['height'], 50, 0,
							   fill='white', arrow=tk.LAST, arrowshape=(10, 20, 5))

	def discard(self):
		"""
		Сброс расчёта. Начальное состояние программы.
		"""
		self.chart.delete("all")
		self.draw_chart()

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


if __name__ == '__main__':
	app = App()
	app.run()
