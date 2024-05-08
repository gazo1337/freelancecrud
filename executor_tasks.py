from PyQt6.QtWidgets import QWidget
from py_ui.exec_tasks import Ui_Form
from db_search import taked_tasks
import user_session_info


class ExecutorTasks(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent

        self.tasks = taked_tasks(user_session_info.USER_ID)
        for i in range(len(self.tasks), len(self.ui.frames)):
            self.ui.frames[i].hide()
        for i in range(0, len(self.tasks)):
            self.ui.task_names[i].setText(self.tasks[i][0])
            self.ui.task_descs[i].setText(self.tasks[i][1])
            self.ui.prices[i].setText(str(self.tasks[i][2]) + " руб.")

        self.ui.myProfile.clicked.connect(self.backwards)

    def backwards(self):
        self.parent.show()
        self.parent.update()
        self.hide()
