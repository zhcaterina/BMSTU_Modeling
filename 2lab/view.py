import random

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QGridLayout, QWidget, QCheckBox
)
from PyQt5.QtCore import Qt

import matrix


class Item(QTableWidgetItem):
    def __init__(self, *args, editable=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not editable:
            self.setFlags(self.flags() & (~ Qt.ItemIsEditable))


class View(QWidget):
    def __init__(self):
        self.qapp = QApplication([])
        super().__init__()
        self.setWindowTitle(
            'Лабораторная работа №2 по моделированию. '
            'Жарова ИУ7-73Б'
        )
        self.setGeometry(600, 300, 800, 500)

        self.n = 6
        self.matrix = [
            [
                random.random() if i != j else 0.0 for j in range(self.n)
            ]
            for i in range(self.n)
        ]
        self.start_probabilities = [
            1 for i in range(self.n)
        ]


        self.matrix_lbl = QLabel('Матрица интенсивности', self)
        self.matrix_lbl.setGeometry(230, 0, 360, 50)

        self.matrix_table = QTableWidget(self)
        self.result_table = QTableWidget(self)
        self.fill_tables()

        self.calc()

        # == #

        self.n_edit = QLineEdit(str(self.n), self)
        self.n_edit.setGeometry(700, 50, 50, 50)
        self.n_btn = QPushButton('Изменить\nразмерность', self)
        self.n_btn.setGeometry(650, 100, 150, 50)
        self.n_btn.clicked.connect(self.resize_matrix)

        self.calc_btn = QPushButton('Рассчитать', self)
        self.calc_btn.setGeometry(650, 330, 150, 50)
        self.calc_btn.clicked.connect(self.calc)

    def start_application(self):
        self.update()
        self.show()
        self.qapp.exec_()

    def fill_tables(self):
        start_probabilities = [
            p / sum(self.start_probabilities)
            for p in self.start_probabilities
        ]
        self.limit_probabilities = matrix.calc_limit_probabilities(self.matrix)
        self.stabilization_times = matrix.calc_stabilization_times(self.matrix, start_probabilities, self.limit_probabilities)

        self.matrix_table.setGeometry(10, 50, 594, 323)
        self.matrix_table.setColumnCount(self.n)
        self.matrix_table.setHorizontalHeaderLabels(
            [str(i + 1) for i in range(self.n)]
        )
        for i in range(self.n):
            self.matrix_table.setColumnWidth(i, 50)
        self.matrix_table.setRowCount(0)
        for i in range(self.n):
            self.matrix_table.insertRow(i)
            for j in range(self.n):
                self.matrix_table.setItem(i, j, Item(str(self.matrix[i][j])[:6], editable=(i != j)))

        self.result_table.setGeometry(10, 400, 785, 97)
        self.result_table.setColumnCount(self.n + 1)
        self.result_table.setHorizontalHeaderLabels(
            [''] + [str(i + 1) for i in range(self.n)]
        )
        self.result_table.setColumnWidth(0, 200)
        for i in range(self.n):
            self.result_table.setColumnWidth(i + 1, 50)
        self.result_table.setRowCount(0)
        self.result_table.insertRow(0)
        self.result_table.insertRow(1)
        self.result_table.setItem(0, 0, Item('Предельная вероятность'))
        self.result_table.setItem(1, 0, Item('Время стабилизации'))
        for i in range(self.n):
            self.result_table.setItem(0, i + 1, Item(str(self.limit_probabilities[i])[:6]))
            self.result_table.setItem(1, i + 1, Item(str(self.stabilization_times[i])[:6]))

    def resize_matrix(self):
        try:
            self.n = int(self.n_edit.text())
            if self.n <= 0:
                raise RuntimeError
            new_matrix = [
                [
                    random.random() if i != j else 0.0 for j in range(self.n)
                ]
                for i in range(self.n)
            ]
            for i in range(min(self.n, len(self.matrix))):
                for j in range(min(self.n, len(self.matrix))):
                    new_matrix[i][j] = self.matrix[i][j]
            self.matrix = new_matrix
            self.start_probabilities = (
                self.start_probabilities[:self.n] +
                [0 for i in range(self.n - len(self.start_probabilities))]
            )
            self.fill_tables()
        except Exception as exc:
            print(exc)

    def calc(self):
        try:
            self.matrix = [
                [
                    float(self.matrix_table.item(i, j).text())
                    for j in range(self.n)
                ]
                for i in range(self.n)
            ]
            self.fill_tables()
        except Exception as exc:
            print(exc)
