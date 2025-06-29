import datetime
import sys
import json
import psycopg
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ui_main import Ui_MainWindow
from logic import refresh_table

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.items = QStandardItemModel()
        self.items.setHorizontalHeaderLabels([
            "Тема",
            "Ссылка",
            "Дата повтора",
            "Приоритет",
            "Категория"
        ])
        self.ui.table_object.setModel(self.items)
        #Пропишем события из кнопки

        #Клик кнопки обновить таблицу
        self.ui.refresh_table.clicked.connect(self.handle_refresh_table)

        #Клик загрузки отправить
        self.ui.send_to_bd_button.clicked.connect(self.handle_send_to_bd)

    def handle_refresh_table(self):
        """
        Ловит сигнал кнопки refresh_table и подгружает данные из бд
        :return:
        """
        data = refresh_table()
        #Удаляем все строки для очистки модели
        self.items.removeRows(0, self.items.rowCount())
        for row in data:
            #Оборачиваем каждую строку элемента в обертку QStandartItem
            items = [QStandardItem(str(x)) for x in row]
            #Добавляем строку
            self.items.appendRow(items)

    def handle_send_to_bd(self):
        """
        1) Улавливает сигнал кнопки отправить
        2) Формирует автоматически строку в БД
        3) Автоматически расставляет временную метку
        :return:
        """
        #Собираем данные из полей ввода
        name: str = self.ui.name_object.text()
        href: str = self.ui.object_href.text()
        category: str = self.ui.category_object.text()
        prioritet: bool = self.ui.prioritet_check.isChecked()

        #Подгружаем бд
        # Параметры БД
        db_name = "mindsurfer"
        db_user = "mindsurfer"
        db_host = "localhost"
        db_port = "5433"
        # Подключаемся
        conn = psycopg.connect(
            dbname=db_name,
            user=db_user,
            host=db_host,
            port=db_port,
        )
        cursor = conn.cursor()
        #Добавляем введенные данные в БД
        cursor.execute('''
                       INSERT INTO object_memory
                       (object_name, object_href, object_hardcore, object_category)
                       VALUES (%s, %s, %s, %s)''', (name, href, prioritet, category))
        conn.commit()
        #Собираем значения буллевых колонок, кроме хардкор каждой строки
        cursor.execute('''
        SELECT object_name,
        object_1,
        object_3,
        object_7,
        object_14,
        object_31
        FROM object_memory
        ''')
        #Обозначи колонки и строки
        columns = ['object_name', 'object_1', 'object_3', 'object_7', 'object_14', 'object_31']
        rows = cursor.fetchall()
        #Формируем словари по каждой строки
        # Каждая строка превращается в словарь с ключами из columns
        data_json = [dict(zip(columns, row)) for row in rows]
        # Сохраняем в нормальном виде
        with open('bufer.json', 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=2)
        #Теперь пройдемся по буферу
        with open('bufer.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        #Возьмем сегодняшнюю дату
        now = datetime.datetime.today()
        #Пробегаемся по каждой строке и опираясь на object 1-31 выставляем даты повторений
        for row in data_json:
            if row['object_1'] == False:
                timestamp = now + datetime.timedelta(days=1)
            elif row['object_3'] == False and row['object_1'] == True:
                timestamp = now + datetime.timedelta(days=3)
            elif row["object_7"] == False and row["object_3"] == True:
                timestamp = now + datetime.timedelta(days=7)
            elif row["object_14"] == False and row["object_7"] == True:
                timestamp = now + datetime.timedelta(days=14)
            elif row["object_31"] == False and row["object_14"] == True:
                timestamp = now + datetime.timedelta(days=31)
            #Обновляем timestamp опираясь на каждое имя строки
            cursor.execute(f'''UPDATE object_memory SET object_timestamp = %s WHERE object_name = %s''',
            (timestamp, row['object_name']))
            conn.commit()
        conn.commit()
        conn.close()
        cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
