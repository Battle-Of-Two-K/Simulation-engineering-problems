from tkinter import Tk, Canvas
import json


class App:
    canvas_opts = {
        'width': 720,
        'height': 720,
        'bg': 'black'
    }

    data = {}

    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, **self.canvas_opts)
        self.canvas.pack()

        self.read_data_json_file()
        self.decor()

        # print(self.input_data.items())
        # input()

    def read_data_json_file(self):
        """
        Метод считывает данные из файла 'Input_data.json'
        """
        with open('Input_data.json', encoding="utf-8") as file:
            self.data = json.loads(file.read())

    def decor(self):
        for key, value in self.data.items():
            print()
            print(f"{key}:")

            if isinstance(value, dict):
                for inside_key, inside_value in value.items():
                    print(f"    {inside_key}: {inside_value}")
            elif isinstance(value, list):
                for step in value:
                    print(f"    {step}")
            else:
                print(f"    {key}: {value}\n")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    # app.run()
