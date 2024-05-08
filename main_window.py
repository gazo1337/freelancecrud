from db_search import authorize
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QLineEdit, QWidget
from PyQt6.QtGui import QFont
from employer_registration import EmployerRegistration
from executor_window import ExecutorWindow
import employer_window
from executor_registration import ExecutorRegistration
import user_session_info
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.setWindowTitle("FreelanceDay!")

        self.thisType = "executor"
        self.login_label = QLabel("Логин")
        self.password_label = QLabel("Пароль")
        self.access_label = QLabel()
        self.button = QPushButton("Войти")
        self.typeButton = QPushButton("Вход заказчиком")
        self.regButton = QPushButton("Регистрация")
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()

        self.login_label.setFont(QFont("Times", 10))
        self.password_label.setFont(QFont("Times", 10))
        self.access_label.setFont(QFont("Times", 10))

        self.button.clicked.connect(self.buttonClick)
        self.typeButton.clicked.connect(self.swapType)
        self.regButton.clicked.connect(self.registration)

        l = QVBoxLayout()
        l.setContentsMargins(400, 250, 400, 250)
        l.addWidget(self.login_label)
        l.addWidget(self.login_input)
        l.addWidget(self.password_label)
        l.addWidget(self.password_input)
        l.addWidget(self.button)
        l.addWidget(self.regButton)
        l.addWidget(self.typeButton)
        l.addWidget(self.access_label)

        self.setMinimumSize(QSize(1080, 720))

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def buttonClick(self):
        self.access_label.setStyleSheet('color:black')
        if len(self.login_input.text()) == 0 or len(self.password_input.text()) == 0:
            self.access_label.setStyleSheet('color:red')
            self.access_label.setText("Одно из полей не заполнено!")
            return 0
        id = authorize(self.thisType, self.login_input.text(), self.password_input.text())
        if id == None:
            self.access_label.setStyleSheet('color:red')
            self.access_label.setText("Неверный логин или пароль!")
            return 0
        self.access_label.setText(f"Добро пожаловать! Ваш id - {id}")
        user_session_info.USER_ID = id
        user_session_info.USER_TYPE = self.thisType
        if self.w == None:
            if self.thisType == "executor":
                self.w = ExecutorWindow()
            else:
                self.w = employer_window.EmployerWindow()
        self.w.show()
        self.close()

    def swapType(self):
        if self.thisType == "executor":
            self.thisType = "employer"
            self.typeButton.setText("Вход исполнителем")
        else:
            self.thisType = "executor"
            self.typeButton.setText("Вход заказчиком")

    def registration(self):
        if self.thisType == "executor":
            if self.w == None:
                self.w = ExecutorRegistration()
        else:
            if self.w == None:
                self.w = EmployerRegistration()
        self.w.show()
        self.close()




