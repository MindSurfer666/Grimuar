import datetime
import os
import sys
import json
import traceback

import psycopg
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ui_main import Ui_MainWindow
from logic import refresh_table, sync_calendar_for_ics, sync_for_apple_calendar, mark_topic_repeated

import os
os.environ["QT_MAC_WANTS_LAYER"] = "0"  # Использовать CoreAnimation вместо Metal
os.environ["QT_QUICK_BACKEND"] = "software"  # Программный рендеринг для QML

class Backend(QObject):
    sendEvents = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = None  # назначим позже

    @Slot(str)
    def markAsRepeated(self, name):
        print("🔁 Повторение темы:", name)
        mark_topic_repeated(name)
        if self.main_window:
            self.main_window.show_popup(f"✅ Повторено: {name}")
            self.main_window.handle_refresh_table()
            sync_for_apple_calendar()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.backend = Backend()
        self.backend.main_window = self
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.backend)
        # Важно: это должен быть QWebEngineView
        self.ui.view.page().setWebChannel(self.channel)
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

        #Клик по кнопке удаления
        self.ui.delete_button.clicked.connect(self.handle_delete_rows)

        #Загрузка календаря
        self.ui.view.loadFinished.connect(self.load_events)

    def handle_refresh_table(self):
        """
        Ловит сигнал кнопки refresh_table и подгружает данные из бд
        :return:
        """
        data = refresh_table()
        self.refresh_delete_row()
        #Удаляем все строки для очистки модели
        self.items.removeRows(0, self.items.rowCount())
        for row in data:
            #Оборачиваем каждую строку элемента в обертку QStandartItem
            items = [QStandardItem(str(x)) for x in row]
            #Добавляем строку
            self.items.appendRow(items)
        sync_calendar_for_ics()
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
        self.load_events()
        sync_calendar_for_ics()
        sync_for_apple_calendar()
    def refresh_delete_row(self):
        """
        Обновляет список удаления строк
        :return:
        """
        #Очищаем строки в списке
        self.ui.delete_rows.clear()  # Очищаем список

        topics = []
        for row in range(self.items.rowCount()):
            item = self.items.item(row, 0)  # Первый столбец — тема
            if item is not None:
                topics.append(str(item.text()))

        self.ui.delete_rows.addItems(topics)
        sync_calendar_for_ics()
    def handle_delete_rows(self):
        """
        1) Воспринимает сигнал кнопки `удалить`
        2) Извлекает значение из списка удаления
        3) Удаляет его из БД
        :return:
        """
        #Получаем имя темы
        row: str = self.ui.delete_rows.currentText()
        # Подгружаем бд
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
        #Удаляем строку со значением выпадающего списка
        cursor.execute('''
        DELETE FROM object_memory WHERE object_name = %s
        ''', (row,))
        conn.commit()
        cursor.close()
        conn.close()
        #Обновляем список удаления
        self.refresh_delete_row()
        #Обновляем таблицу
        self.handle_refresh_table()
        sync_calendar_for_ics()
    def load_events(self):
        """
        Отправляет все обьекты в календарь
        :return:
        """
        print("📤 Отправляем события в календарь...")
        events = self.load_from_db_events()
        events_json = json.dumps(events, indent=2, ensure_ascii=False)
        print("📦 JSON для календаря:")
        print(events_json)
        self.backend.sendEvents.emit(events_json)
        sync_calendar_for_ics()
    def load_from_db_events(self):
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
        cursor.execute('''
        SELECT object_name, object_href, object_category, object_timestamp FROM object_memory''')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        events = []
        for name, href, cat, ts in rows:
            if isinstance(ts, datetime.date) and not isinstance(ts, datetime.datetime):
                ts = datetime.datetime.combine(ts, datetime.time())
            events.append({
                'title': name,
                'url': href,
                "extendedProps": {"category": cat},
                "start": ts.isoformat(),
            })
        return events

    def show_popup(self, message: str):
        """
        Вывод уведомлений
        :param message:
        :return:
        """
        popup = QLabel(message, self)
        popup.setStyleSheet("""
            QLabel {
                background-color: #444;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        popup.adjustSize()

        # Позиция — правый нижний угол окна
        geo = self.geometry()
        x = geo.width() - popup.width() - 40
        y = geo.height() - popup.height() - 40
        popup.move(x, y)
        popup.show()

        # Автоматически исчезает через 3 секунды
        QTimer.singleShot(3000, popup.deleteLater)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        exit_code = app.exec()
    except Exception as e:
        with open(os.path.expanduser("~/grimoire_error.log"), "w", encoding="utf-8") as f:
            f.write("Произошла ошибка при запуске:\n")
            traceback.print_exc(file=f)
