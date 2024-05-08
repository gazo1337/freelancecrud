import decimal
from db_search import update_embalance, get_card
from PyQt6.QtWidgets import QWidget
from py_ui.update_bal import Ui_Form
import user_session_info


class UpdateBalance(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.balance = get_card(user_session_info.USER_ID, user_session_info.USER_TYPE)
        self.ui.balance.setText("Ваш баланс: " + str(self.balance[1]) + " руб.")
        self.ui.error.hide()
        self.ui.trans.clicked.connect(self.update)

    def update(self):
        try:
            amount = decimal.Decimal(self.ui.amount.text())
        except:
            self.ui.error.setText("Недопустимые символы в поле Сумма")
            self.ui.error.setStyleSheet('color:red')
            self.ui.error.show()
            return 0
        update_embalance(user_session_info.USER_ID, amount)
        self.parent.show()
        self.parent.update()
        self.hide()
