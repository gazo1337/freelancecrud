from db_search import search_tasks, search_task_exe, transaction, delete_task
from PyQt6.QtWidgets import QWidget
from py_ui.empl_window import Ui_Form
import user_session_info
from create_task import CreateTask
from update_balance import UpdateBalance


class EmployerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.w = None

        self.executor = None
        self.tasks = search_tasks(user_session_info.USER_ID)
        if len(self.tasks) == 3:
            self.ui.newTask.hide()
        for i in range(len(self.tasks), len(self.ui.frames)):
            self.ui.frames[i].hide()
        for i in range(0, len(self.tasks)):
            self.ui.task_names[i].setText(self.tasks[i][0])
            self.ui.task_descs[i].setText(self.tasks[i][1])
            self.ui.prices[i].setText(str(self.tasks[i][2]) + " руб.")
            if self.tasks[i][3] == 0:
                self.ui.exes[i].setText("Без исполнителя")
                self.ui.finish[i].hide()
                self.ui.finishLab[i].hide()
                self.ui.delLab[i].hide()
            else:
                self.executor = search_task_exe(self.tasks[i][4])
                self.ui.exes[i].setText("Исполнитель: " + self.executor[1])
                self.ui.deletes[i].hide()
                self.ui.delLab[i].hide()
                self.ui.finishLab[i].hide()
        self.ui.finish[0].clicked.connect(self.trB1)
        self.ui.finish[1].clicked.connect(self.trB2)
        self.ui.finish[2].clicked.connect(self.trB3)
        self.ui.deletes[0].clicked.connect(self.delB1)
        self.ui.deletes[1].clicked.connect(self.delB2)
        self.ui.deletes[2].clicked.connect(self.delB3)
        self.ui.newTask.clicked.connect(self.createButton)
        self.ui.myProfile.clicked.connect(self.balance)

    def trB1(self):
        self.transactionButton(0)

    def trB2(self):
        self.transactionButton(1)

    def trB3(self):
        self.transactionButton(2)

    def transactionButton(self, num):
        transaction(self.tasks[num][4])
        self.ui.finish[num].hide()
        self.ui.finishLab[num].show()
        self.ui.finishLab[num].setStyleSheet('color:green')
        self.ui.newTask.show()

    def delB1(self):
        self.delete(0)

    def delB2(self):
        self.delete(1)

    def delB3(self):
        self.delete(2)

    def delete(self, num):
        delete_task(self.tasks[num][4])
        self.ui.deletes[num].hide()
        self.ui.delLab[num].show()
        self.ui.delLab[num].setStyleSheet('color:red')
        self.ui.newTask.show()

    def createButton(self):
        self.w = CreateTask(self)
        self.w.show()
        self.hide()

    def update(self):
        self.executor = None
        self.tasks = search_tasks(user_session_info.USER_ID)
        if len(self.tasks) == 3:
            self.ui.newTask.hide()
        for i in range(len(self.tasks), len(self.ui.frames)):
            self.ui.frames[i].hide()
        for i in range(0, len(self.tasks)):
            self.ui.task_names[i].setText(self.tasks[i][0])
            self.ui.task_descs[i].setText(self.tasks[i][1])
            self.ui.prices[i].setText(str(self.tasks[i][2]) + " руб.")
            if self.tasks[i][3] == 0:
                self.ui.exes[i].setText("Без исполнителя")
                self.ui.finish[i].hide()
                self.ui.finishLab[i].hide()
                self.ui.delLab[i].hide()
            else:
                self.executor = search_task_exe(self.tasks[i][4])
                self.ui.exes[i].setText("Исполнитель: " + self.executor[1])
                self.ui.deletes[i].hide()
                self.ui.delLab[i].hide()
                self.ui.finishLab[i].hide()

    def balance(self):
        self.w = UpdateBalance(self)
        self.w.show()
        self.hide()



