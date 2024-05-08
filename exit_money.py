import decimal
from db_search import update_exbalance, get_card
from PyQt6.QtWidgets import QWidget
from py_ui.exit_mon import Ui_Form
import user_session_info


class ExitMoney(QWidget):
    def __init__(self,  parent):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
        self.balance = get_card(user_session_info.USER_ID, user_session_info.USER_TYPE)
        self.ui.balance.setText("Ваш баланс: " + str(self.balance[1]) + " руб.")
        self.ui.error.hide()
        self.ui.pushButton.clicked.connect(self.update)

    def update(self):
        try:
            amount = decimal.Decimal(self.ui.amount.text())
        except:
            self.ui.error.setText("Недопустимые символы в поле Сумма")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            return 0
        if decimal.Decimal(self.balance[1]) < amount:
            self.ui.error.setText("На балансе недостаточно средств")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            return 0
        update_exbalance(user_session_info.USER_ID, amount)
        self.parent.show()
        self.parent.update()
        self.hide()
