import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter_app_pattern import TkinterApp


def find(name):
	return os.path.exists(name)


class App(TkinterApp):
	frame_color = 'white'
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
		'bg': '#2B2E35'
	}

	task_data = {}  # данные задачи
	materials_data = {}  # таблица материалов
	buttons = []

	def litter(self):
		# self.root.geometry("1120x720")
		# self.root.configure(background='red')
		self.root.resizable(width=False, height=False)

		self.settings_window = tk.Frame(self.root, **self.settings_window_opts)
		# self.settings_window.config(bg='red')
		self.settings_window.pack(side='right')

		self.animation = tk.Canvas(self.root, **self.animation_opts)
		self.animation.pack()

		self.chart = tk.Canvas(self.root, **self.chart_opts)
		self.chart.pack()

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

	def information_canvas(self):
		"""
		Вывод информации о задаче + вывод кнопок на полотно
		"""
		height, delta = 50, 31

		tk.Label(self.settings_window, text='Задача №2. Вариант 59', font=('Comic Sans MS', 18, "bold"),
				 bg='').place(x=0, y=0)

		# Первый блок данных
		tk.Label(self.settings_window, text="1.Входные данные:", font=("Courier", 14, "bold")).place(x=0, y=height)

		for key, value in self.task_data["Входные данные"].items():
			tk.Label(self.settings_window, text=f'  {key}: {value} мм', font=("Courier", 14, "italic")).place(
				x=0, y=height + delta)
			height += delta

		# Второй блок данных
		tk.Label(self.settings_window, text="2.Дополнительные условия:", font=("Courier", 14, "bold")).place(
			x=0, y=height + delta)

		for key, value in self.task_data["Дополнительные условия"].items():
			tk.Label(self.settings_window, text=f'  {key}: {value}', **self.text_param).place(
				x=0, y=height + 2 * delta)
			height += delta

		# Третий блок данных
		tk.Label(self.settings_window, text="3.Особыые условия:", font=("Courier", 14, "bold")).place(
			x=0, y=height + 2 * delta)

		for key in self.task_data["Особые условия"]:
			tk.Label(self.settings_window, text=f'  -{key}', font=("Courier", 14, "italic")).place(
				x=0, y=height + 3 * delta)
			height += delta

		# Кнопки
		exit_btn = tk.Button(self.settings_window, text=f'Выход', font=(
			"Courier", 12, "italic"), command=self.button_close_program)
		exit_btn.place(x=4 * delta, y=height + 3 * delta)

		exit_btn = tk.Button(self.settings_window, text=f'Сбросить', font=(
			"Courier", 12, "italic"), command=self.discard)
		exit_btn.place(x=7 * delta, y=height + 3 * delta)

	def button_close_program(self):
		self.root.destroy()

	def draw_chart(self):
		self.chart.create_line(0, self.chart_opts['height'] // 2,
							   self.chart_opts['width'], self.chart_opts['height'] // 2,
							   fill='white', arrow=tk.LAST, arrowshape=(10, 20, 5))

		self.chart.create_line(self.chart_opts['width'] // 2, self.chart_opts['height'], self.chart_opts['width'] // 2,
							   0,
							   fill='white', arrow=tk.LAST, arrowshape=(10, 20, 5))

	def discard(self):
		"""
		Сброс расчёта. Начальное состояние программы.
		"""
		self.chart.delete("all")

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
