import decimal
from db_search import get_card, create_task
from PyQt6.QtWidgets import QWidget
import employer_window
from py_ui.create_t import Ui_Form
import user_session_info


class CreateTask(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.error.hide()
        self.balance = get_card(user_session_info.USER_ID, "employer")
        self.ui.balance.setText("Ваш баланс: " + str(self.balance[1]) + " руб.")

        self.ui.submit.clicked.connect(self.onButtonClick)
        self.ui.cancel_b.clicked.connect(self.cancel)

    def onButtonClick(self):
        j = 0
        info = []
        info.append(self.ui.amount)
        info.append(self.ui.name)
        info.append(self.ui.description)
        for i in range(0, len(info)-1):
            if len(info[i].text()) == 0:
                self.ui.error.setText("Одно из полей не заполнено!")
                self.ui.error.setStyleSheet('color:red')
                self.ui.error.show()
                j = 1
        if len(info[2].toPlainText()) == 0:
            self.ui.error.setText("Одно из полей не заполнено!")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        try:
            amount = decimal.Decimal(self.ui.amount.text())
        except:
            self.ui.error.setText("Недопустимые символы в поле Стоимость")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            return 0
        if decimal.Decimal(info[0].text()) > self.balance[1]:
            self.ui.error.setText("На балансе недостаточно средств!")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(info[1].text()) < 8 or len(info[1].text()) > 30:
            self.ui.error.setText("Длина названия должна быть от 8 до 30")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if len(info[2].toPlainText()) > 300:
            self.ui.error.setText("Длина описания должна быть до 300")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            j = 1
        if j == 1:
            return 0
        else:
            create_task(info[1].text(), info[2].toPlainText(), user_session_info.USER_ID, decimal.Decimal(info[0].text()), user_session_info.comps.index(self.ui.complexity.currentText()))
            self.parent = employer_window.EmployerWindow()
            self.parent.show()
            self.parent.update()
            self.hide()

    def cancel(self):
        self.parent.show()
        self.parent.update()
        self.hide()

