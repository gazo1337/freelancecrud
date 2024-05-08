import datetime
import psycopg2

conn = psycopg2.connect("dbname=freelance_db user=postgres password=FoRgH228")
cur = conn.cursor()


def sel_max(col, table):
    script = f"select max({col}) from {table}"
    cur.execute(script)
    max = cur.fetchone()
    return max


def sel_task(col):
    script = f"select * from task where tasks_id = {col}"
    cur.execute(script)
    max_t = cur.fetchone()
    return max_t


def fetch_table(table):
    script = f"select * from {table}"
    cur.execute(script)
    some = cur.fetchall()
    return some


def get_card(id, type):
    script = f"select * from {type}s_vc where owner = {id}"
    cur.execute(script)
    some = cur.fetchone()
    return some


def send_message(text, em_id, ex_id):
    max_el = sel_max("message_id", "chat")
    date = datetime.date.today().strftime("%d/%m/%Y")
    script = f"insert into chat values ({max_el[0] + 1},\'{text}\', {em_id}, {ex_id}, \'{date}\')"
    cur.execute(script)
    conn.commit()


def create_task(name, descr, em_id, amount, compl):
    script = f"select balance from employers_vc where owner = {em_id}"
    cur.execute(script)
    bal = cur.fetchone()
    if bal[0] < amount:
        print("Не хватает денег на балансе для совершения данного действия!")
        return 0
    script = f"update employers_vc set balance = {bal[0] - amount} where owner = {em_id}"
    cur.execute(script)
    max_el = sel_max("tasks_id", "task")
    script = f"insert into task values ({max_el[0] + 1}, \'{name}\', \'{descr}\', {em_id}, {amount}, 0, {compl})"
    cur.execute(script)
    conn.commit()
    print("Задание добавлено успешно!")


def take_task(task_id, ex_id):
    script = f"select task_id from task_execution where task_id = {task_id}"
    cur.execute(script)
    ex = cur.fetchone()
    if ex is not None:
        print("Вы не можете взять данное задание, оно уже занято!")
        return 0
    date = datetime.date.today().strftime("%d/%m/%Y")
    script = f"insert into task_execution values ({task_id}, {ex_id}, \'{date}\')"
    cur.execute(script)
    script = f"update task set task_status = 1 where tasks_id = {task_id}"
    cur.execute(script)
    conn.commit()
    print("Вы успешно взялись за выполнение задания, удачи!")
    return 1


def transaction(task_id):
    script = f"select amount, executor, employer, task_status from task, task_execution where tasks_id = {task_id} and task_id = {task_id} and task_status <> 2"
    cur.execute(script)
    info = cur.fetchone()
    if info is None:
        print("Транзакция по данной задаче уже была выполнена ранее!")
        return 0
    script = f"update executors_vc set balance = balance + {info[0]} where owner = {info[1]}"
    cur.execute(script)
    script = f"update task set task_status = 2 where tasks_id = {task_id}"
    cur.execute(script)
    date = datetime.date.today().strftime("%d/%m/%Y")
    script = f"insert into transactions_history values ({task_id}, {info[1]}, {info[2]}, {info[0]}, \'{date}\')"
    cur.execute(script)
    print("Транзакция успешно выполнена!")
    conn.commit()


def delete_task(task_id):
    script = f"select task_status, employer, amount from task where tasks_id = {task_id}"
    cur.execute(script)
    status = cur.fetchone()
    if status == None:
        print("Данного задания не существует!")
        return 0
    elif status[0] != 0:
        print("Задание невозможно удалить - оно уже выполняется!")
        return 0
    script = f"update employers_vc set balance = balance + {status[2]} where owner = {status[1]}"
    cur.execute(script)
    script = f"delete from task where tasks_id = {task_id}"
    cur.execute(script)
    conn.commit()
    print("Задание успешно удалено!")


def authorize(type, login, password):
    script = f"select {type}s_id from {type} where login = \'{login}\' and password = \'{password}\'"
    cur.execute(script)
    id = cur.fetchone()
    if id == None:
        print("Неверный логин или пароль!")
        return None
    return id[0]


def executor_registration(info):
    max = sel_max("executors_id", "executor")
    script = f"select login from executor where login = \'{info[0].text()}\'"
    cur.execute(script)
    check = cur.fetchone()
    if check != None:
        return 1
    script = f"insert into executor values ({max[0] + 1}, {max[0] + 1}, 0, 0, \'{info[2].text()}\', \'{info[3].toPlainText()}\', \'{info[0].text()}\', \'{info[1].text()}\')"
    cur.execute(script)
    script = f"insert into executors_vc values({max[0] + 1}, 0, {max[0] + 1})"
    cur.execute(script)
    conn.commit()
    return 0


def employer_registration(info):
    max = sel_max("employers_id", "employer")
    script = f"select login from employer where login = \'{info[0].text()}\'"
    cur.execute(script)
    check = cur.fetchone()
    if check != None:
        return 1
    script = f"insert into employer values (\'{info[2].text()}\', \'{info[3].text()}\', \'{info[4].toPlainText()}\', \'{info[0].text()}\', \'{info[1].text()}\', {max[0] + 1}, {max[0] + 1})"
    cur.execute(script)
    script = f"insert into employers_vc values({max[0] + 1}, 0, {max[0] + 1})"
    cur.execute(script)
    conn.commit()
    return 0


def search_tasks(employer):
    script = f"select name, description, amount, task_status, tasks_id from task where employer = {employer} and task_status <> 2"
    cur.execute(script)
    result = cur.fetchall()
    return result


def search_task_exe(task):
    script = f"select task_execution.executor, nickname from task_execution, executor where task_id = {task} and task_execution.executor = executors_id"
    cur.execute(script)
    result = cur.fetchone()
    return result


def update_embalance(employer, amount):
    script = f"update employers_vc set balance = balance + {amount} where owner = {employer}"
    cur.execute(script)
    conn.commit()


def update_exbalance(executor, amount):
    script = f"update executors_vc set balance = balance - {amount} where owner = {executor}"
    cur.execute(script)
    conn.commit()


def taked_tasks(executor):
    script = f"select name, description, amount from task, task_execution where executor = {executor} and task_status = 1 and tasks_id = task_id"
    cur.execute(script)
    result = cur.fetchall()
    return result

