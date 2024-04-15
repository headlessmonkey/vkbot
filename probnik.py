
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
import threading
import time
import datetime
from config import TOKEN
from config import GROUP_ID
from keyboards import																																											 keyboard_start,keyboard_admin_menu,keyboard_start_admin,keyboard_info,keyboard_timers,keyboard_stirka,keyboard_spam,keyboard_suhka,keyboard_podpiski,keyboard_da_net,keyboard_choice_washmashine, keyboard_DIXI, keyboard_DIXI_status

# Инициализация подключения к базе данных
conn = sqlite3.connect('main.db')
cur = conn.cursor()
flag=""
message_time="ещё не задано"
status_DIXI="Закрыто"

def display_users_table():
    cur.execute("SELECT * FROM users")
    print("Таблица users:")
    print(cur.fetchall())

    cur.execute("SELECT * FROM wash_mashine")
    print("Таблица wash_mashine:")
    print(cur.fetchall())
    

def get_washing_machine_status(machine_id):
    cur.execute("SELECT kto_zanyal FROM wash_mashine WHERE nimer_stiralki = ?", (machine_id,))
    result = cur.fetchone()
    # Проверка, что result не равен None перед доступом к его элементам
    return "занята" if result is not None and result[0] is not None else "свободна"

def check_and_add_user(user_id):
    query = "SELECT COUNT(*) FROM users WHERE user_id = ?"
    cur.execute(query, (user_id,))
    result = cur.fetchone()

    if result[0] == 0:
        cur.execute('''
            INSERT INTO users (user_id, vk_or_tg)
            VALUES (?, ?)
        ''', (user_id, 'vk'))
        conn.commit()

# Создание таблицы users, если её нет
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        user_role TEXT DEFAULT 'default_user',
        floor INTEGER DEFAULT 0,
        stirka_zanyul INTEGER DEFAULT 0,
        podpiska1 INTEGER DEFAULT 1,
        podpiska2 INTEGER DEFAULT 1,
        vk_or_tg TEXT
    )
''')

# Создание таблицы wash_mashine, если её нет
cur.execute('''
    CREATE TABLE IF NOT EXISTS wash_mashine (
        kto_zanyal INTEGER,
        kto_soobshaet INTEGER,
        nimer_stiralki INTEGER
    )
''')

cur.execute('INSERT INTO wash_mashine VALUES (null, null, 1)')
cur.execute('INSERT INTO wash_mashine VALUES (null, null, 2)')
cur.execute('INSERT INTO wash_mashine VALUES (null, null, 3)')
cur.execute('INSERT INTO wash_mashine VALUES (null, null, 4)')
# Авторизация бота
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Инициализация клавиатур
num_washing_machines = 4

conn.commit()

def is_admin(user_id):
    admins = [444863423, 3232]  # Замените на фактические ID админов
    return user_id in admins

def check_zanyatoy_stirku(nimer_stiralki):#Если возвращаемое значение равно 0, это означает, что стиральная машина занята. Если значение больше 0, стиральная машина свободна.
    cur.execute("SELECT COUNT(*) FROM wash_mashine WHERE kto_zanyal is NULL AND nimer_stiralki = ?", (nimer_stiralki,))
    result=cur.fetchone()
    return result[0]


def clear_database():
    cur.execute("DELETE FROM wash_mashine")
    cur.execute("INSERT INTO wash_mashine (kto_zanyal, kto_soobshaet, nimer_stiralki) VALUES (NULL, NULL, 1)")
    cur.execute("INSERT INTO wash_mashine (kto_zanyal, kto_soobshaet, nimer_stiralki) VALUES (NULL, NULL, 2)")
    cur.execute("INSERT INTO wash_mashine (kto_zanyal, kto_soobshaet, nimer_stiralki) VALUES (NULL, NULL, 3)")
    cur.execute("INSERT INTO wash_mashine (kto_zanyal, kto_soobshaet, nimer_stiralki) VALUES (NULL, NULL, 4)")
    vk.messages.send(user_id=user_id, message='очищена',random_id=0)
    conn.commit()


def selfproverka(nimer_stiralki):
    cur.execute("SELECT kto_zanyal FROM wash_mashine WHERE nimer_stiralki = ?",(nimer_stiralki,)) 
    result=cur.fetchone()
    if result is not None:
        user_id = result[0]
        return user_id

    return None
def func_soobshit(message):
    if check_zanyatoy_stirku(message) ==0:
                cur.execute(f"UPDATE wash_mashine SET kto_soobshaet = ? WHERE nimer_stiralki = {message}", (user_id,))
                cur.execute(f"SELECT kto_zanyal FROM wash_mashine WHERE nimer_stiralki = ?", (message))
                result = cur.fetchone()
                result=result[0]
                flag=''
                conn.commit()
                vk.messages.send(user_id=result,message='Стиральная машина окончила работу',random_id=0)
                vk.messages.send(user_id=user_id,message=' сообщение успешно отправлено',keyboard=keyboard_timers.get_keyboard(),random_id=0)
    else:
                vk.messages.send(user_id=user_id, message='К сожалению, этот человек не использует бота', random_id=0)
def func_osvobodit(message):
    if check_zanyatoy_stirku(message) ==0:
                    if selfproverka(message)==user_id:
                        flag=''
                        status1='свободна'
                        cur.execute(f"UPDATE wash_mashine SET kto_zanyal = NULL WHERE nimer_stiralki = {message}")
                        conn.commit()
                        vk.messages.send(user_id=user_id,message=' стиральная машина успешно освобождена',keyboard=keyboard_timers.get_keyboard(),random_id=0)
                    else:
                        vk.messages.send(user_id=user_id,message=' стиральную машину заняли не вы',keyboard=keyboard_timers.get_keyboard(),random_id=0)
    else:
                    vk.messages.send(user_id=user_id,message='Эта стиральная машина не занята',keyboard=keyboard_timers.get_keyboard(),random_id=0)

def func_zanyatiya(message):
                if check_zanyatoy_stirku(message) !=0:
                    result = check_zanyatoy_stirku(message)
                    status1='занята'
                    flag =''
                    vk.messages.send(user_id=user_id,message=' стиральная машина успешно занята',keyboard=keyboard_timers.get_keyboard(),random_id=0)
                    cur.execute(f"UPDATE wash_mashine SET kto_zanyal = ? WHERE nimer_stiralki = {message}", (user_id,))
                    conn.commit()
                else:
                    vk.messages.send(user_id=user_id,message='Эта стиральная машина занята',keyboard=keyboard_timers.get_keyboard(),random_id=0)
def timer(napominalka_time):###############
    seconds = 60
    minutes60 = 60*seconds
    print(napominalka_time)
    hour=int(napominalka_time)*minutes60

    start_time = time.time()
    end_time = start_time + hour

    while time.time() < end_time:
        pass
    vk.messages.send(user_id=user_id, message='Проверьте, не высохли ли ваши вещи',random_id=0,keyboard=keyboard_suhka.get_keyboard())

# Обработка сообщений
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Получение данных о сообщении
        user_id = event.user_id
        message = event.text
        check_and_add_user(user_id)
        admin_privilege = is_admin(user_id)

        if message == "ДРОП":
            if admin_privilege:
                clear_database()
                
            else:
                vk.messages.send(user_id=user_id, message='права получи',random_id=0)
  
        if message == "Рассылка":
            if admin_privilege:
                vk.messages.send(user_id=user_id, message='Введите текст для рассылки:', random_id=0)
                for event_admin in longpoll.listen():
                    if event_admin.type == VkEventType.MESSAGE_NEW and event_admin.to_me and event_admin.user_id == user_id:
                        text_for_broadcast = event_admin.text
                        break  # Выход из цикла, когда получен текст
                if text_for_broadcast.lower() == "назад":
                    vk.messages.send(user_id=user_id, message='Рассылка отменена.', random_id=0)
                else:
                    # Отправляем рассылку только в случае, если текст не равен "Назад"
                    all_users = cur.execute("SELECT user_id FROM users").fetchall()
                    for user in all_users:
                        vk.messages.send(user_id=user[0], message=text_for_broadcast, random_id=0)
            else:
                vk.messages.send(user_id=user_id, message='У вас недостаточно прав для выполнения рассылки.', random_id=0)
                ##########
        if message == "Сообщить":
            flag='сообщить'
            vk.messages.send(user_id=user_id,message='Выбирай',keyboard=keyboard_choice_washmashine.get_keyboard(),random_id=0)
        if message  == '1' and flag =='сообщить':
             func_soobshit(message)
        if message  == '2' and flag =='сообщить':
            func_soobshit(message)
        if message  == '3' and flag =='сообщить':
            func_soobshit(message)
        if message  == '4' and flag =='сообщить':
            func_soobshit(message)
 
        if message == "Освободить":
            flag='освободить'
            vk.messages.send(user_id=user_id,message='Выбирай',keyboard=keyboard_choice_washmashine.get_keyboard(),random_id=0)
        if message  == '1' and flag =='освободить':
            func_osvobodit(message)    
        if message  == '2' and flag =='освободить':
             func_osvobodit(message)
        if message  == '3' and flag =='освободить':
             func_osvobodit(message)
 
        if message  == '4' and flag =='освободить':
                func_osvobodit(message)
###########                
        if message in ['Занять',"занять"]:
            flag='занять'
            vk.messages.send(user_id=user_id,message='Выбирай',keyboard=keyboard_choice_washmashine.get_keyboard(),random_id=0)
        if message  == '1' and flag =='занять':
           func_zanyatiya(message)
        if message  == '2' and flag =='занять':
             func_zanyatiya(message)
        if message  == '3' and flag =='занять':
             func_zanyatiya(message)
        if message  == '4' and flag =='занять':
            func_zanyatiya(message)
        elif message == 'Стирка':
            display_users_table()
            status_message = f'Занятость стиральных машин\n'
            for machine_id in range(1, num_washing_machines + 1):
                status_message += f'Стиралка{machine_id} {get_washing_machine_status(machine_id)}\n'

            # Отправляем сообщение с состоянием стиральных машин
            if status_message:
                vk.messages.send(user_id=user_id, message=status_message, keyboard=keyboard_stirka.get_keyboard(), random_id=0)
            else:
                vk.messages.send(user_id=user_id, message='Не удалось получить состояние стиральных машин', random_id=0)
        elif message in ['обновить таймер']:
            vk.messages.send(user_id=user_id, message=f"напоминание сработает через  час",keyboard=keyboard_timers.get_keyboard(), random_id=0)
            napominalka_time=1
            thread = threading.Thread(target=timer(napominalka_time))
            thread.start()
        elif flag=='Сушка':
            if  message in ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48"]:
                napominalka_time=message
                vk.messages.send(user_id=user_id, message=f"напоминание сработает через {napominalka_time} часов",keyboard=keyboard_timers.get_keyboard(), random_id=0)
                thread = threading.Thread(target=timer(napominalka_time))
                thread.start()
                flag=''
            else:
                vk.messages.send(user_id=user_id, message=f"Выберите временной диапазон от 10 до 48 часов",keyboard=keyboard_timers.get_keyboard(), random_id=0)

        elif message =="Сушка":
             flag='Сушка'
             vk.messages.send(user_id=user_id, message=f"Введите количество часов,через которое сработает напоминание", random_id=0)
        elif message == '⚙️':
            query = "SELECT podpiska1, podpiska2 FROM users WHERE user_id = ?"
            cur.execute(query, (user_id,))
            result = cur.fetchone()
            cur.execute("SELECT floor FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            floor = row[0]
            if result:
                podpiska1, podpiska2 = result
                # Формирование сообщения с информацией о подписках
                settings_message = f"Ваши настройки:\n"
                settings_message += f"Постельное бельё: {'подписаны' if podpiska1 == 1 else 'не подписаны'}\n"
                settings_message += f"Оповещение этажа: {'подписаны' if podpiska2 == 1 else 'не подписаны'}\n"
                settings_message += f"Ваш этаж: {floor}\n"
                vk.messages.send( message=settings_message,user_id=user_id,  random_id=0, keyboard=keyboard_podpiski.get_keyboard())
            else:
                vk.messages.send(user_id=user_id, message="Информация о ваших настройках не найдена", keyboard=keyboard_start.get_keyboard(), random_id=0)                    
        if message  in ['Привет',"Начать"]:
            if admin_privilege:
                vk.messages.send(user_id=user_id, message='Привет!\nЯ бот третьего общежития МТУСИ\nЯ создан для упрощения твоей жизни\n⚙️-здесь находятся данные вашей учётной записи(подписки на рассылки, номер вашего этажа)\nℹ️ - здесь находится справочная информация\nтаймеры-здесь вы можжете получить информацию о стиральных машинах и поставить напоминание', keyboard=keyboard_start_admin.get_keyboard(), random_id=0)
            else:
                vk.messages.send(user_id=user_id, message='Привет!\nЯ бот третьего общежития МТУСИ\nЯ создан для упрощения твоей жизни\n⚙️-здесь находятся данные вашей учётной записи(подписки на рассылки, номер вашего этажа)\nℹ️ - здесь находится справочная информация\nтаймеры-здесь вы можжете получить информацию о стиральных машинах и поставить напоминание', keyboard=keyboard_start.get_keyboard(), random_id=0)
        elif message == "Назад":
            if admin_privilege:
                vk.messages.send(user_id=user_id, message='Стартовое меню!', keyboard=keyboard_start_admin.get_keyboard(), random_id=0)
            else:
                 vk.messages.send(user_id=user_id, message='Стартовое меню!', keyboard=keyboard_start.get_keyboard(), random_id=0)
        elif message == 'Чат':
            vk.messages.send(user_id=user_id, message='Проверь, чтобы тебя можно было приглашать в чаты и твой профиль не был закрытым', keyboard=keyboard_start.get_keyboard(), random_id=0)
        elif message == 'Таймеры':
            vk.messages.send(user_id=user_id, message='Выбери раздел', keyboard=keyboard_timers.get_keyboard(), random_id=0)
        elif message == 'ℹ️':
            vk.messages.send(user_id=user_id, message="Информационный раздел\n чтобы вызвать стартовое сообщение, напишите Начать",keyboard=keyboard_info.get_keyboard(), random_id=0)
        if message == 'ЖКО':
            vk.messages.send(user_id=user_id, message="Ул. Авиамоторная 8А, Ауд. 101,\nТел: 8 (495) 957-77-29 t.a.novikova@mtuci.ru\nПн-Пт 9:00-18:00\nОбед 13:00-14:00", keyboard=keyboard_start.get_keyboard(), random_id=0)
        if message == 'Деканаты':
            vk.messages.send(user_id=user_id, message="деканат КиИБ +7 (495) 957-78-20\nдеканат РиТ 8 (495) 957-79-27\nдеканат ИТ 8 (495) 925-10-67\nдеканат СиСС 8 (495) 957-79-22", keyboard=keyboard_start.get_keyboard(), random_id=0)
        if message == 'Администрация':
            vk.messages.send(user_id=user_id, message='Елена Владимировна Руднева-Заведующая\nКоменданты\nОльга Александровна - комендант с рыжими волосами\nВячеслав Анатольевич \nАнастасия Александровна - многие тут называют её Урсула\nОльга Ивановна - Старший комендант\nИрина Юрьевна Сидоркина-ЗамПроректора\nАлександр Владимироыич Долганин - пожарник', keyboard=keyboard_start.get_keyboard(), random_id=0)
        if message == "Правила":
            vk.messages.send(user_id=user_id,message='0. ПОСЛЕ 23.00 НЕЛЬЗЯ ШУМЕТЬ\nБудьте чистоплотны и уважайте место, где вы живёте с кем-то вместе\nКурить в туалетах строго запрещено\n', random_id=0,keyboard=keyboard_start.get_keyboard())
        if message == "Нет, я всё забрал/забралa":
            vk.messages.send(user_id=user_id,message='Спасибо💜', random_id=0)
        if message == "Админ":
            vk.messages.send(user_id=user_id,message='список команд будет здесь', random_id=0, keyboard=keyboard_admin_menu.get_keyboard())
        if message == "Услуги":
            vk.messages.send(user_id=user_id,message='Печать (7 руб/стр) - @vonelop \nУстановка/активация Windows (цена договорная) - @shhiz0id \nУстановка активированного office (цена договорная) - @shhiz0id \nПомощь с компьютером (цена договорная) - @shhiz0id \nРемонт замков, техники (бесплатно) - @pavel_ozone \nЗаточка ножей (бесплатно) - @pavel_ozone \nКонсультация по дипломам ТиЗВоским (бесплатно) - @pavel_ozone \nЛабы и курсачи для групп БРТ/БРА/БРВ (бесплатно) - @pavel_ozone \nВосстановления света в комнатах (бесплатно) - @pavel_ozone \nЛабы/курсачи и прочее по универу, по множеству направлений, это https://vk.com/karsonis или конкретнее https://vk.com/mtuci_labs \nhttps://vk.com/shhiz0id - бесплатная проходка в Lookin Rooms без депозита',keyboard=keyboard_start.get_keyboard(), random_id=0)        
        
        
        if message == "Дикси":
            vk.messages.send(user_id=user_id,message=f" {message_time} сказали, что {status_DIXI}",random_id=0,keyboard=keyboard_DIXI.get_keyboard())
        if message == "Изменить состояние":
            
            vk.messages.send(user_id=user_id,message=f"Меняйте статус, если точно уверены ", keyboard = keyboard_DIXI_status.get_keyboard(), random_id=0)
        if message == "Закрыто":
            message_time = message_time_DIXI()
            status_DIXI="Закрыто"
            vk.messages.send(user_id=user_id,message="Статус изменён", keyboard = keyboard_start.get_keyboard(), random_id=0) 
        if message == "Открыто":
            message_time = message_time_DIXI()
            status_DIXI="Открыто"
            vk.messages.send(user_id=user_id,message="Статус изменён", keyboard = keyboard_start.get_keyboard(), random_id=0) 

        def message_time_DIXI():
            message_time = datetime.datetime.now().time()
            hour = message_time.hour 
            minute = message_time.minute 
            date =  datetime.datetime.now().date()
            return f"{date} в  {hour}:{minute}"
             
        
        
        if message == "Заполнить":
            flag='setting'
            vk.messages.send(user_id=user_id,message='Введите цифру соответствующую номеру вашего этажа',random_id=0)
        if message in ['2','3','4','5'] and flag=='setting':
            flag2=1
            floor=message
            cur.execute("UPDATE users SET floor = ? WHERE user_id = ?", (floor, user_id,))
            vk.messages.send(user_id=user_id,message='Оставляем подписку на информацию о смене постельного белья?',keyboard=keyboard_da_net.get_keyboard(),random_id=0)
        if message== "Да" :
            if flag2==2:
                cur.execute("UPDATE users SET podpiska2 = 1 WHERE user_id = ?", (user_id,))
                vk.messages.send(user_id=user_id,message='настройка завершена',keyboard=keyboard_start.get_keyboard(),random_id=0)
                flag =''
            if flag2==1:
                cur.execute("UPDATE users SET podpiska1 = 1 WHERE user_id = ?", (user_id,))
                vk.messages.send(user_id=user_id,message='Оставляем подписку на информацию о вашем этаже?',keyboard=keyboard_da_net.get_keyboard(),random_id=0)
                flag2=2
            
        if message== "Нет" :
            
            if flag2==2:
            
                cur.execute("UPDATE users SET podpiska2 = 0 WHERE user_id = ?", (user_id,))
                flag =''
                vk.messages.send(user_id=user_id,message='настройка завершена',keyboard=keyboard_start.get_keyboard(),random_id=0)
            if  flag2==1:
                flag2=2 
                cur.execute("UPDATE users SET podpiska1 = 0 WHERE user_id = ?", (user_id,))
                vk.messages.send(user_id=user_id,message='Оставляем подписку на информацию о вашем этаже?',keyboard=keyboard_da_net.get_keyboard(),random_id=0)
            

             





        
