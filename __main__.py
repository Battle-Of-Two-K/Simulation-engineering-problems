from tkinter import Tk, Canvas
import json


def read_data_json_file():
    """
    Метод считывает данные из файла 'Input_data.json'
    """
    with open('Input_data.json', encoding="utf-8") as file:
        data = json.loads(file.read())
        print(data["Входные данные"]["Отклонение"])


class App:
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    input_data = {}
    parameters = ['Отклонение', 'Размер куба',
                  'Диаметр пружины', 'Шаг витков пружины']

    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        read_data_json_file()
        # self.decor()
        # input()


    def decor(self):
        print('Входные данные:')
        for i, j in zip(self.input_data, self.input_data.values()):
            print(f' - {i}: {j}')

    def write_text(self, data: str):
        self.canvas.create_text(100, 100, text=data, font=('Comic Sans MS', 30))

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    # app.run()
