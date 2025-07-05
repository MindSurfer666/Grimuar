import psycopg
from ics import Calendar, Event, DisplayAlarm
import datetime
import subprocess
import os

def refresh_table():
    """
    Обновляет данные таблицы обьектов памяти из бд
    :return:
    """
    #Параметры БД
    db_name = "mindsurfer"
    db_user = "mindsurfer"
    db_host = "localhost"
    db_port = "5433"
    #Подключаемся
    conn = psycopg.connect(
        dbname=db_name,
        user=db_user,
        host=db_host,
        port=db_port,
    )
    cursor = conn.cursor()
    #Запрашиваем все строки
    cursor.execute("SELECT object_name, object_href, object_timestamp, object_hardcore, object_category FROM object_memory")
    #Генерируем список списков
    listochek = [i for i in cursor.fetchall()]
    cursor.close()
    conn.close()
    return listochek

def sync_calendar_for_ics():
    """
    Функция синхронизации с любым календарем — генерирует .ics файл из базы данных
    """
    # Подключение к БД
    conn = psycopg.connect(
        dbname="mindsurfer",
        user="mindsurfer",
        host="localhost",
        port="5433",
    )
    cursor = conn.cursor()

    cursor.execute('''
        SELECT object_name, object_href, object_category, object_timestamp
        FROM object_memory
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    calendar = Calendar()

    for name, href, cat, ts in rows:
        event = Event()
        event.name = name
        event.description = f"Категория: {cat}\nСсылка: {href}"

        # Преобразуем дату в datetime для начала и окончания
        dt_start = datetime.datetime.combine(ts, datetime.time(hour=12, minute=0))
        dt_end = dt_start + datetime.timedelta(hours=2)

        event.begin = dt_start
        event.end = dt_end

        # UID через datetime
        event.uid = f"{name}-{int(dt_start.timestamp())}@grimuar.local"

        alarm = DisplayAlarm(
            trigger=datetime.timedelta(minutes=-30),
            display_text=f"Напоминание: {name}"
        )
        event.alarms.append(alarm)

        calendar.events.add(event)

    with open("calendar.ics", "w", encoding='utf-8') as f:
        f.writelines(calendar.serialize_iter())

def sync_for_apple_calendar():
    """
    Запускает баш скрипт для синхронизации с Apple календарь
    :return:
    """
    script_path = os.path.abspath('import_ics_to_calendar.sh')
    result = subprocess.run(["/bin/bash", script_path], check=True, text=True)

def mark_topic_repeated(name):
    """
    Реагирует на нажатие события в календаре
    Меняет ближайшую метку повторения на True в БД
    Сдвигает дату в зависимости от нее
    :param name: Имя темы
    :return:
    """
    conn = psycopg.connect(dbname="mindsurfer", user="mindsurfer", host="localhost", port="5433")
    cursor = conn.cursor()

    # Загружаем текущее состояние
    cursor.execute('''
        SELECT object_1, object_3, object_7, object_14, object_31, object_timestamp
        FROM object_memory
        WHERE object_name = %s
    ''', (name,))
    result = cursor.fetchone()
    if not result:
        print(f"❌ Тема не найдена: {name}")
        return

    keys = ['object_1', 'object_3', 'object_7', 'object_14', 'object_31']
    days = [1, 3, 7, 14, 31]
    now = datetime.datetime.today()
    timestamp = result[-1]
    for i, flag in enumerate(result[:-1]):
        if not flag:
            column_to_update = keys[i]
            next_time = now + datetime.timedelta(days=days[i])
            print(f"✅ Устанавливаем {column_to_update}=True, новая дата {next_time}")
            cursor.execute(f'''
                UPDATE object_memory
                SET {column_to_update} = TRUE, object_timestamp = %s
                WHERE object_name = %s
            ''', (next_time, name))
            break

    conn.commit()
    cursor.close()
    conn.close()
