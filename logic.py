import psycopg

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

ponos = refresh_table()
print(ponos)