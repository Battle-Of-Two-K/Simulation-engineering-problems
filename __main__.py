from tkinter import Tk, Canvas


class App:
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    input_data = {'Отклонение': -1,
                  'Размер куба': -1,
                  'Диаметр пружины': -1,
                  'Шаг витков пружины':-1}

    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        self.read_data_from_file()
        print(self.input_data)

    def read_data_from_file(self):
        """
        Метод считывает данные из файла 'Input_data.txt'
        """
        with open('Input_data.txt', encoding="utf-8") as file:
            strings = file.readlines()

        # for i in strings:
        #     if i.index('Отклонение') == 0:
        #         self.input_data['Отклонение'] = int(i.split()[-1])
        #
        #     elif i.index('Размер куба') == 0:
        #         self.input_data['Размер куба'] = int(i.split()[-1])
        #
        #     elif i.index('Диаметр пружины') == 0:
        #         self.input_data['Диаметр пружины'] = int(i.split()[-1])
        #
        #     elif i.index('Шаг витков пружины') == 0:
        #         self.input_data['Шаг витков пружины'] = int(i.split()[-1])

        self.input_data['Отклонение'] = int(strings[0].split()[-1])
        self.input_data['Размер куба'] = int(strings[1].split()[-1])
        self.input_data['Диаметр пружины'] = int(strings[2].split()[-1])
        self.input_data['Шаг витков пружины'] = int(strings[3].split()[-1])

    def write_text(self, data: str):
        self.canvas.create_text(100, 100, text=data, font=('Comic Sans MS', 30))

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    # app.run()
