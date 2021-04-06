from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys

start_pos_x, start_pos_y = 100, 100
width, height = 720, 720


def push_btn():
    print("Кнопка работает")


def main():
    app = QApplication(sys.argv)
    root = QMainWindow()

    button = QtWidgets.QPushButton(root)
    button.move(100, 100)
    button.setText("Жми")
    button.setFixedWidth(50)
    button.setFixedHeight(50)
    button.clicked.connect(push_btn)
    button.show()

    root.setWindowTitle("Тестовое приложение")
    root.setGeometry(start_pos_x, start_pos_y, width, height)

    root.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
