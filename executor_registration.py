from db_search import executor_registration, authorize
from executor_window import ExecutorWindow
from PyQt6.QtWidgets import QWidget
from py_ui.exec_reg import Ui_Form
import user_session_info


class ExecutorRegistration(QWidget):
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
        check = executor_registration(self.ui.info)
        if check == 1:
            self.ui.error.setText("Данный логин уже занят, введите другой логин!")
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
        if len(self.ui.info[2].text()) < 4 or len(self.ui.info[0].text()) > 16:
            self.ui.error.setText("Никнейм должен быть длиной от 4 до 16")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(self.ui.info[3].toPlainText()) > 325:
            self.ui.error.setText("Описание должно быть не длиннее 325 символов")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if j == 1:
            return 0
        else:
            id = authorize("executor", self.ui.info[0].text(), self.ui.info[1].text())
            user_session_info.USER_ID = id
            user_session_info.USER_TYPE = "executor"
            if self.w is None:
                self.w = ExecutorWindow()
            self.w.show()
            self.close()


