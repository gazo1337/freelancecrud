from db_search import sel_max, sel_task, take_task, taked_tasks
from PyQt6.QtWidgets import QWidget
from py_ui.exec_window import Ui_Form
import user_session_info
from executor_tasks import ExecutorTasks
from exit_money import ExitMoney


class ExecutorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.confirm.hide()
        self.ui.confirm_2.hide()
        self.ui.confirm_3.hide()
        self.ui.pastB.hide()

        self.w = None
        self.t_number = sel_max("tasks_id", "task")[0]
        self.tasks_ids = []
        for j in range(0, 3):
            self.ui.lays[j].hide()
        i = 0
        while i != 3:
            task = sel_task(self.t_number)
            taked = taked_tasks(user_session_info.USER_ID)
            if task != None:
                if task[5] == 0:
                    self.tasks_ids.append(self.t_number)
                    self.ui.task_names[i].setText(task[1])
                    self.ui.task_descs[i].setText(task[2])
                    self.ui.price[i].setText(str(task[4]) + " руб.")
                    self.ui.lays[i].show()
                    if len(taked) >= 3:
                        self.ui.task_buttons[i].hide()
                    else:
                        self.ui.task_buttons[i].show()
                    i += 1
            self.t_number -= 1
            if self.t_number < 0:
                i = 3
                self.ui.nextB.hide()

        self.ui.task_buttons[0].clicked.connect(self.tb1)
        self.ui.task_buttons[1].clicked.connect(self.tb2)
        self.ui.task_buttons[2].clicked.connect(self.tb3)
        self.ui.pastB.clicked.connect(self.past)
        self.ui.nextB.clicked.connect(self.next)
        self.ui.pushButton_2.clicked.connect(self.toMyTasks)
        self.ui.pushButton.clicked.connect(self.exitBal)

    def tb1(self):
        self.take(0)

    def tb2(self):
        self.take(1)

    def tb3(self):
        self.take(2)

    def take(self, num):
        result = take_task(self.tasks_ids[num], user_session_info.USER_ID)
        if result == 1:
            self.ui.task_buttons[0].hide()
            self.ui.confirm.show()
            taked = taked_tasks(user_session_info.USER_ID)
            if len(taked) >= 3:
                for i in range(0, len(self.ui.task_buttons)):
                    self.ui.task_buttons[i].hide()

    def next(self):
        self.ui.pastB.show()
        self.tasks_ids = []
        for j in range(0, 3):
            self.ui.lays[j].hide()
        i = 0
        while i != 3:
            task = sel_task(self.t_number)
            if task != None:
                if task[5] == 0:
                    self.tasks_ids.append(self.t_number)
                    self.ui.task_names[i].setText(task[1])
                    self.ui.task_descs[i].setText(task[2])
                    self.ui.lays[i].show()
                    i += 1
            self.t_number -= 1
            if self.t_number < 0:
                i = 3
                self.ui.nextB.hide()

    def past(self):
        max = sel_max("tasks_id", "task")[0]
        self.ui.nextB.show()
        self.tasks_ids = []
        for j in range(0, 3):
            self.ui.lays[j].hide()
        i = 0
        while i != 3:
            task = sel_task(self.t_number)
            if task != None:
                if task[5] == 0:
                    self.tasks_ids.append(self.t_number)
                    self.ui.task_names[i].setText(task[1])
                    self.ui.task_descs[i].setText(task[2])
                    self.ui.price[i].setText(str(task[4]) + ".руб")
                    self.ui.lays[i].show()
                    i += 1
            self.t_number += 1
            if self.t_number == max:
                i = 3
                self.ui.pastB.hide()

    def toMyTasks(self):
        self.w = ExecutorTasks(self)
        self.w.show()
        self.hide()

    def exitBal(self):
        self.w = ExitMoney(self)
        self.w.show()
        self.hide()

    def update(self):
        self.ui.confirm.hide()
        self.ui.confirm_2.hide()
        self.ui.confirm_3.hide()
        self.ui.pastB.hide()
        self.t_number = sel_max("tasks_id", "task")[0]
        self.tasks_ids = []
        for j in range(0, 3):
            self.ui.lays[j].hide()
        i = 0
        while i != 3:
            task = sel_task(self.t_number)
            taked = taked_tasks(user_session_info.USER_ID)
            if task != None:
                if task[5] == 0:
                    self.tasks_ids.append(self.t_number)
                    self.ui.task_names[i].setText(task[1])
                    self.ui.task_descs[i].setText(task[2])
                    self.ui.price[i].setText(str(task[4]) + ".руб")
                    self.ui.lays[i].show()
                    if len(taked) >= 3:
                        self.ui.task_buttons[i].hide()
                    else:
                        self.ui.task_buttons[i].show()
                    i += 1
            self.t_number -= 1
            if self.t_number < 0:
                i = 3
                self.ui.nextB.hide()