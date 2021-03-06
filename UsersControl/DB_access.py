from sqlalchemy import and_
from models.Database import Session
from models.applications import Application
from models.user import User
from models.computer import Computer

from datetime import datetime

# дает полную информацию о компьютере по имени пользователя
def GetComputerInfo(session: Session, name: str) -> Computer:

    users = GetUsers(session)
    if name not in users:
        print('there is no such user')
        raise RuntimeError

    user_computer_history = session.query(Computer).join(User).filter(User.name == name)
    return user_computer_history[-1]

#TODO: изменить функции добавления юзера и компьютера, так как изменилась структура модели

# добавляет нового юзера и компьютер, соответствующий ему
def AddUser(session: Session, name: str, machine_id: str, comp: int, ip: str):
    new_user = User(name, comp, ip)
    new_comuter = Computer(machine_id, comp)
    
    exists_users = session.query(User)
    if new_user in exists_users:
        print("This user already exists")
        raise RuntimeError
    
    exists_computer = session.query(Computer)
    if new_comuter in exists_computer:
        print("This computer already exists")
        raise RuntimeError
    

    session.add(new_user)
    session.add(new_comuter)
    session.commit()
    session.close()

# возвращает текущий список пользователей
def GetUsers(session: Session) -> list:
    users = session.query(User)
    users_names = [user.name for user in users]
    return users_names

'''
дообавляем запись о компьютере под номером comp
информация передается в словаре, который имеет следующую стуктуру

название окна первого приоритета (str)
название окна второго приоритета (str)
название окна третьего приоритета (str)
процент, занимаемый окном первого приоритета (float)
процент, занимаемый окном второго приоритета (float)
процент, занимаемый окном третьего приоритета (float)
количество процессов (int)
disk memory used (float)
CPU frequency min (float)
CPU frequency max (float)
CPU frequency current (float)
Boot time (str)
Total memory used (float)
Текущая дата и время (указывается через datetime.datetime.now())

Пример:
info = {
    'first_window' : 'YouTube', 
    'second_window' : 'VK', 
    'third_window' : 'bash', 
    'first_window_percent' : 70, 
    'second_window_percent' : 20, 
    'third_window_percent' : 10, 
    'curent_window_active' : 'VK',
    'proc_number' : 200, 
    'disk_mem_usage' : 1.1, 
    'CPU_f_min' : 20, 
    'CPU_f_max' : 20, 
    'CPU_f_cur' : 20, 
    'Boot_time' : 'boot time', 
    'Total_mem_used' : 1.2
    }
'''
def AddComputerInfo(session: Session, machine_id: str, comp: int, info: dict):
    computer_number_list = [computer.number for computer in session.query(Computer)]
    if comp not in computer_number_list:
        print("You try to add computer without user. This is not you really want")
        raise RuntimeError

    computer = Computer(machine_id, comp)
    computer.first_window = info['first_window']
    computer.second_window = info['second_window']
    computer.third_window = info['third_window']

    computer.first_window_percent = info['first_window_percent']
    computer.second_window_percent = info['second_window_percent']
    computer.third_window_percent = info['third_window_percent']
    computer.curent_window_active = info['curent_window_active']

    computer.proc_number = info['proc_number']

    computer.disk_mem_usage = info['disk_mem_usage']

    computer.CPU_f_min = info['CPU_f_min']
    computer.CPU_f_max = info['CPU_f_max']
    computer.CPU_f_cur = info['CPU_f_cur']
    computer.Boot_time = info['Boot_time']
    computer.Total_mem_used = info['Total_mem_used']
    computer.date = datetime.now()

    session.add(computer)
    session.commit()
    session.close()

'''
Добавляет новое приложение в таблицу приложений, если его там не было
В аргументы функции передается словарь с информацией о приложении
Словарь имеет следующую структуру:

app_info = {
    'app_name': имя приложения,
    'computer': компьютер на котором было открыто приложение,
    'createtime': время создания,
    'status': статус работы,
    'rss': rss,
    'vms': vms,
    'shared': shared,
    'data': data
}

Пример:

app_info = {
    'app_name': 'YouTube',
    'computer': 4,
    'create_time': '01-01-01',
    'status': 'active',
    'rss': 0,
    'vms': 0,
    'shared': 0,
    'data': 0
}
'''
def AddApplication(session: Session, app_info: dict):

    computers = [comp.number for comp in session.query(Computer)]
    if app_info['computer'] not in computers:
        print('You try to add application for computer [№ %d], that is not exist' %app_info['computer'])
        raise RuntimeError

    # поучаем список все существующих приложений
    apps = session.query(Application)
    # создаем прообраз нового приложения
    new_app = Application(app_info['app_name'], app_info['computer'])

    new_app.create_time = app_info['create_time']
    new_app.status = app_info['status']
    new_app.rss = app_info['rss']
    new_app.vms = app_info['vms']
    new_app.shared = app_info['shared']
    new_app.data = app_info['data']
    new_app.date = datetime.now()


    session.add(new_app)
    session.commit()
    session.close()

'''
выводит время авторизации каждого пользователя
'''
def GetAuthorisationTime(session: Session) -> dict:
    users = GetUsers(session)

    time = {}

    for user in users:
        first_post = session.query(Computer).join(User).filter(User.name == user).first()
        authorisation_time = first_post.date.strftime("%d-%m-%Y %H:%M:%S")
        time[user] = authorisation_time
    return time

'''
выводит время последней активности каждого пользователя
'''
def GetExitTime(session: Session) -> dict:
    users = GetUsers(session)
    time = {}

    for user in users:
        computer_date = [computer.date 
                         for computer in 
                         session.query(Computer).join(User).filter(User.name == user)]
        exit_time = computer_date[-1].strftime("%d-%m-%Y %H:%M:%S")
        time[user] = exit_time
    return time

'''
функцию возвращает список приложений по имени юзера
'''
def GetAppsList(session: Session, user_name: str) -> list:
    comp = [user.computer for user in session.query(User).filter(User.name == user_name)]

    if not comp:
        print('there is not such user')
        raise RuntimeError

    app_list = []
    for it in session.query(Application).filter(Application.computer == comp[0]):
        app_list.append(it.app_name)
    
    return app_list

''' 
по заданному имени пользователя возвращает 2 списка:
первый список (с нулевого индекса) окна первого, второго и третьего приоритета
второй список -- их процентное соотношение по времени
'''
def GetMostUsableWindows(session: Session, user_name: str):
    comp = session.query(Computer).join(User).filter(User.name == user_name)
    cur_comp = comp[-1]

    most_usable_windows = []
    most_usable_windows_percent = []

    most_usable_windows.append(cur_comp.first_window)
    most_usable_windows.append(cur_comp.second_window)
    most_usable_windows.append(cur_comp.third_window)
    most_usable_windows_percent.append(cur_comp.first_window_percent)
    most_usable_windows_percent.append(cur_comp.second_window_percent)
    most_usable_windows_percent.append(cur_comp.third_window_percent)

    return most_usable_windows, most_usable_windows_percent

'''
возвращает список всех machine_id
'''
def GetMachineID(session: Session) -> list:
    machine_id = [comp.MachineID for comp in session.query(Computer)]
    return machine_id