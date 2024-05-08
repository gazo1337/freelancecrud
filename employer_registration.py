from db_search import employer_registration, authorize
from employer_window import EmployerWindow
from PyQt6.QtWidgets import QWidget
from py_ui.empl_reg import Ui_Form
import user_session_info


class EmployerRegistration(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.error.hide()
        self.w = None
        self.ui.regButton.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        j = 0
        for i in range(0, len(self.ui.info)-1):
            if len(self.ui.info[i].text()) == 0:
                self.ui.error.setText("Одно из полей не заполнено!")
                self.ui.error.setStyleSheet('color:red')
                self.ui.error.show()
                j = 1
        check = employer_registration(self.ui.info)
        if check == 1:
            self.ui.error.setText("Данный логин уже занят, введите другой логин!")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        for i in range(0, len(user_session_info.wrong)):
            if user_session_info.wrong[i] in self.ui.info[0].text():
                self.ui.error.setText("В логине имеются недопустимые символы")
                self.ui.error.setStyleSheet('color:red')
                self.ui.error.show()
                j = 1
            if user_session_info.wrong[i] in self.ui.info[1].text():
                self.ui.error.setText("В логине имеются недопустимые символы")
                self.ui.error.setStyleSheet('color:red')
                self.ui.error.show()
                j = 1

        if len(self.ui.info[0].text()) < 6 or len(self.ui.info[0].text()) > 16:
            self.ui.error.setText("Логин должен быть длиной от 8 до 16")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(self.ui.info[1].text()) < 8 or len(self.ui.info[1].text()) > 20:
            self.ui.error.setText("Пароль должен быть длиной от 8 до 20")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(self.ui.info[2].text()) < 3 or len(self.ui.info[0].text()) > 10:
            self.ui.error.setText("Имя должно быть длиной от 3 до 10")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(self.ui.info[3].text()) < 8 or len(self.ui.info[3].text()) > 20:
            self.ui.error.setText("Название компании должно быть длиной от 8 до 20")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(self.ui.info[4].toPlainText()) > 325:
            self.ui.error.setText("Описание должно быть не длиннее 325 символов")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if j == 1:
            return 0
        else:
            user_session_info.USER_TYPE = "employer"
            id = authorize(user_session_info.USER_TYPE, self.ui.info[0].text(), self.ui.info[1].text())
            user_session_info.USER_ID = id
            if self.w is None:
                self.w = EmployerWindow()
            self.w.show()
            self.close()


