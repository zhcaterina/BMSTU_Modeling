from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox
)

import system
from laws import UniformDistributionLaw, ConstantDistributionLaw


class View(QMainWindow):
    def __init__(self):
        self.qapp = QApplication([])
        super().__init__()
        self.setFixedSize(1080, 700)
        self.move(100, 10)
        self.setWindowTitle(
            'Лабораторная работа №5 по моделированию.'
            'Жарова ИУ7-73Б'
        )

        self.normal_label = QLabel('Параметры\nклиентов', self)
        self.normal_label.setFixedSize(300, 50)
        self.normal_label.move(50, 50)

        self.client = 10
        self.client_label = QLabel('average =', self)
        self.client_label.setFixedSize(100, 50)
        self.client_label.move(50, 100)
        self.client_line_edit = QLineEdit(str(self.client), self)
        self.client_line_edit.setFixedSize(100, 50)
        self.client_line_edit.move(120, 100)

        self.client_delta = 2
        self.client_delta_label = QLabel(' +-', self)
        self.client_delta_label.setFixedSize(100, 50)
        self.client_delta_label.move(220, 100)
        self.client_delta_line_edit = QLineEdit(str(self.client_delta), self)
        self.client_delta_line_edit.setFixedSize(100, 50)
        self.client_delta_line_edit.move(250, 100)

        self.op_label = QLabel('Параметры\nоператоров', self)
        self.op_label.setFixedSize(300, 100)
        self.op_label.move(380, 20)

        self.op1_m = 20
        self.op1_m_label = QLabel('average1 =', self)
        self.op1_m_label.setFixedSize(100, 50)
        self.op1_m_label.move(380, 100)
        self.op1_m_line_edit = QLineEdit(str(self.op1_m), self)
        self.op1_m_line_edit.setFixedSize(100, 50)
        self.op1_m_line_edit.move(460, 100)

        self.op1_delta = 5
        self.op1_delta_label = QLabel(' +-', self)
        self.op1_delta_label.setFixedSize(100, 50)
        self.op1_delta_label.move(560, 100)
        self.op1_delta_line_edit = QLineEdit(str(self.op1_delta), self)
        self.op1_delta_line_edit.setFixedSize(100, 50)
        self.op1_delta_line_edit.move(590, 100)

        self.op2_m = 40
        self.op2_m_label = QLabel('average2 =', self)
        self.op2_m_label.setFixedSize(100, 50)
        self.op2_m_label.move(380, 160)
        self.op2_m_line_edit = QLineEdit(str(self.op2_m), self)
        self.op2_m_line_edit.setFixedSize(100, 50)
        self.op2_m_line_edit.move(460, 160)

        self.op2_delta = 10
        self.op2_delta_label = QLabel(' +-', self)
        self.op2_delta_label.setFixedSize(100, 50)
        self.op2_delta_label.move(560, 160)
        self.op2_delta_line_edit = QLineEdit(str(self.op2_delta), self)
        self.op2_delta_line_edit.setFixedSize(100, 50)
        self.op2_delta_line_edit.move(590, 160)

        self.op3_m = 40
        self.op3_m_label = QLabel('average3 =', self)
        self.op3_m_label.setFixedSize(100, 50)
        self.op3_m_label.move(380, 220)
        self.op3_m_line_edit = QLineEdit(str(self.op3_m), self)
        self.op3_m_line_edit.setFixedSize(100, 50)
        self.op3_m_line_edit.move(460, 220)

        self.op3_delta = 20
        self.op3_delta_label = QLabel(' +-', self)
        self.op3_delta_label.setFixedSize(100, 50)
        self.op3_delta_label.move(560, 220)
        self.op3_delta_line_edit = QLineEdit(str(self.op3_delta), self)
        self.op3_delta_line_edit.setFixedSize(100, 50)
        self.op3_delta_line_edit.move(590, 220)

        self.comp_label = QLabel('Параметры\nкомпьютеров', self)
        self.comp_label.setFixedSize(300, 100)
        self.comp_label.move(720, 20)

        self.comp1 = 15
        self.comp1_label = QLabel('const1 =', self)
        self.comp1_label.setFixedSize(100, 50)
        self.comp1_label.move(720, 100)
        self.comp1_m_line_edit = QLineEdit(str(self.comp1), self)
        self.comp1_m_line_edit.setFixedSize(100, 50)
        self.comp1_m_line_edit.move(785, 100)

        self.comp2 = 30
        self.comp2_label = QLabel('const2 =', self)
        self.comp2_label.setFixedSize(100, 50)
        self.comp2_label.move(720, 160)
        self.comp2_m_line_edit = QLineEdit(str(self.comp2), self)
        self.comp2_m_line_edit.setFixedSize(100, 50)
        self.comp2_m_line_edit.move(785, 160)

        self.method_label = QLabel('Метод рассчета', self)
        self.method_label.setFixedSize(200, 100)
        self.method_label.move(920, 14)

        self.method_box = QComboBox(self)
        self.method_box.addItems(['delta t', 'events'])
        self.method_box.setFixedSize(140, 60)
        self.method_box.move(920, 90)
        self.method_box.currentTextChanged.connect(self.select_method)

        self.dt = 0.01
        self.dt_label = QLabel('dt =', self)
        self.dt_label.setFixedSize(200, 100)
        self.dt_label.move(920, 135)
        self.dt_line_edit = QLineEdit(str(self.dt), self)
        self.dt_line_edit.setFixedSize(100, 50)
        self.dt_line_edit.move(960, 160)

        self.select_method()

        self.n = 300
        self.n_label = QLabel('Обработать \nзаявок (n) = ', self)
        self.n_label.setFixedSize(100, 50)
        self.n_label.move(50, 200)
        self.n_line_edit = QLineEdit(str(self.n), self)
        self.n_line_edit.setFixedSize(100, 50)
        self.n_line_edit.move(140, 200)

        self.system = system.System(
            client_law=UniformDistributionLaw(a=8, b=12),
            op1_law=UniformDistributionLaw(a=15, b=25),
            op2_law=UniformDistributionLaw(a=30, b=50),
            op3_law=UniformDistributionLaw(a=20, b=60),
            comp1_law=ConstantDistributionLaw(c=15),
            comp2_law=ConstantDistributionLaw(c=30),
            n=self.n, dt=1, method='delta t'
        )

        result = self.system.calculate()

        self.button = QPushButton('Провести рассчет', self)
        self.button.setFixedSize(500, 100)
        self.button.clicked.connect(self.calculate)
        self.button.move(100, 500)

        self.result_label = QLabel('Результаты рассчета', self)
        self.result_label.setFixedSize(200, 100)
        self.result_label.move(760, 280)

        self.generated_count_label = QLabel('Количество\nобработанных заявок =', self)
        self.generated_count_label.setFixedSize(300, 50)
        self.generated_count_label.move(720, 420)
        #self.generated_count_label.hide()
        self.generated_count_line_edit = QLineEdit(str(result['generated_count']), self)
        self.generated_count_line_edit.setFixedSize(100, 50)
        self.generated_count_line_edit.move(880, 420)
        #self.generated_count_line_edit.hide()

        self.processed_count_label = QLabel('Количество\nобработанных заявок =', self)
        self.processed_count_label.setFixedSize(300, 50)
        self.processed_count_label.move(720, 420)
        self.processed_count_label.hide()
        self.processed_count_line_edit = QLineEdit(str(result['processed_count']), self)
        self.processed_count_line_edit.setFixedSize(100, 50)
        self.processed_count_line_edit.move(880, 420)
        self.processed_count_line_edit.hide()

        self.rejected_count_label = QLabel('Количество\nпропущенных заявок =', self)
        self.rejected_count_label.setFixedSize(300, 50)
        self.rejected_count_label.move(720, 480)
        self.rejected_count_line_edit = QLineEdit(str(result['rejected_count']), self)
        self.rejected_count_line_edit.setFixedSize(100, 50)
        self.rejected_count_line_edit.move(880, 480)

        self.rejected_probability_label = QLabel('Вероятность\nотказа =', self)
        self.rejected_probability_label.setFixedSize(300, 50)
        self.rejected_probability_label.move(720, 540)
        self.rejected_probability_line_edit = QLineEdit(str(round(result['rejected_count'] / (result['generated_count'] + result['rejected_count']), 4)), self)
        self.rejected_probability_line_edit.setFixedSize(100, 50)
        self.rejected_probability_line_edit.move(880, 540)

    def start_application(self):
        self.update()
        self.show()
        self.qapp.exec_()

    def select_method(self):
        self.method = self.method_box.currentText()
        if self.method == 'events':
            self.dt_label.hide()
            self.dt_line_edit.hide()
        else:
            self.dt_label.show()
            self.dt_line_edit.show()

    def calculate(self):
        try:
            self.client = float(self.client_line_edit.text())
            self.client_delta = float(self.client_delta_line_edit.text())
            self.op1_m = float(self.op1_m_line_edit.text())
            self.op1_delta = float(self.op1_delta_line_edit.text())
            self.op2_m = float(self.op2_m_line_edit.text())
            self.op2_delta = float(self.op2_delta_line_edit.text())
            self.op3_m = float(self.op3_m_line_edit.text())
            self.op3_delta = float(self.op3_delta_line_edit.text())
            self.comp1 = float(self.comp1_m_line_edit.text())
            self.comp2 = float(self.comp2_m_line_edit.text())
            self.dt = float(self.dt_line_edit.text())
            self.n = int(self.n_line_edit.text())
        except ValueError as exc:
            print(exc)
            return
        self.system = system.System(
            client_law=UniformDistributionLaw(a=self.client-self.client_delta, b=self.client+self.client_delta),
            op1_law=UniformDistributionLaw(a=self.op1_m-self.op1_delta, b=self.op1_m+self.op1_delta),
            op2_law=UniformDistributionLaw(a=self.op2_m-self.op2_delta, b=self.op2_m+self.op2_delta),
            op3_law=UniformDistributionLaw(a=self.op3_m-self.op3_delta, b=self.op3_m+self.op3_delta),
            comp1_law=ConstantDistributionLaw(c=self.comp1),
            comp2_law=ConstantDistributionLaw(c=self.comp2),
            n=self.n, dt=self.dt, method=self.method
        )
        result = self.system.calculate()
        self.generated_count_line_edit.setText(str(result['generated_count']))
        self.processed_count_line_edit.setText(str(result['processed_count']))
        self.rejected_count_line_edit.setText(str(result['rejected_count']))
        self.rejected_probability_line_edit.setText(str(round(result['rejected_count'] / (result['generated_count'] + result['rejected_count']), 4)))
