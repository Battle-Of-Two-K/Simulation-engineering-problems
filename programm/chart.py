

class Chart:
	def __init__(self, canvas, start_coord_x, start_coord_y):
		self.__start_coord_x = start_coord_x
		self.__start_coord_y = start_coord_y
		self.canvas = canvas
		self.canvas_width = int(self.canvas["width"])
		self.canvas_height = int(self.canvas["height"])

	def convert_coords(self, time, cube_position_x, chart_factor):
		if cube_position_x > 0:
			return self.canvas.coords(self.canvas.find_all()[1])[0] + time * chart_factor,\
				self.canvas.coords(self.canvas.find_all()[0])[1] - cube_position_x * chart_factor
		elif cube_position_x < 0:
			return self.canvas.coords(self.canvas.find_all()[1])[0] + time * chart_factor, \
				self.canvas.coords(self.canvas.find_all()[0])[1] + abs(cube_position_x) * chart_factor

	@property
	def start_coord_x(self):
		return self.__start_coord_x

	@start_coord_x.setter
	def start_coord_x(self, new_value):
		if new_value == 0:
			self.__start_coord_x = self.canvas.coords(self.canvas.find_all()[1])[0]
		elif new_value > 0:
			self.__start_coord_x = self.canvas.coords(self.canvas.find_all()[1])[0] + new_value
		else:
			self.__start_coord_x = self.canvas.coords(self.canvas.find_all()[1])[0] - new_value

	@property
	def start_coord_y(self):
		return self.__start_coord_x

	@start_coord_y.setter
	def start_coord_y(self, new_value):
		if new_value == 0:
			self.__start_coord_y = self.canvas.coords(self.canvas.find_all()[0])[1]
		elif new_value > 0:
			self.__start_coord_y = self.canvas.coords(self.canvas.find_all()[0])[1] + new_value
		else:
			self.__start_coord_y = self.canvas.coords(self.canvas.find_all()[0])[1] - new_value
