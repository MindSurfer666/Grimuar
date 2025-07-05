# -*- coding: utf-8 -*-
import os.path
import sys

################################################################################
## Form generated from reading UI file 'nabrosok.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QStandardItemModel)
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
                               QLayout, QLineEdit, QMainWindow, QMenuBar,
                               QPushButton, QScrollArea, QSizePolicy, QStatusBar,
                               QTableView, QWidget, QComboBox, QVBoxLayout)
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from pip._internal.metadata import Backend


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setStyleSheet("""
            QWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        font-family: 'San Francisco', 'Inter', 'Arial', sans-serif;
        font-size: 13px;
    }

    QTableView {
        background-color: #2d2d2d;
        alternate-background-color: #252526;
        gridline-color: #3c3c3c;
        border: 1px solid #444;
        selection-background-color: #094771;
        selection-color: white;
    }

    QHeaderView::section {
        background-color: #3c3c3c;
        color: #d4d4d4;
        padding: 5px;
        border: none;
    }

    QLineEdit, QComboBox {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        padding: 5px;
        border-radius: 4px;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #007acc;
    }

    QPushButton {
        background-color: #0e639c;
        color: white;
        padding: 6px 12px;
        border: none;
        border-radius: 4px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #1177bb;
    }

    QCheckBox {
        padding: 2px;
    }

    QCheckBox::indicator {
        width: 14px;
        height: 14px;
    }

    QCheckBox::indicator:checked {
        background-color: #007acc;
        border: 1px solid #007acc;
    }

    QStatusBar {
        background: #2d2d2d;
        color: #cccccc;
    }

    QMenuBar {
        background-color: #2d2d2d;
        color: #cccccc;
    }

    QMenuBar::item:selected {
        background: #007acc;
    }
        """)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Главный вертикальный layout
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 📊 Таблица
        self.table_object = QTableView()
        self.items = QStandardItemModel()
        self.items.setHorizontalHeaderLabels(["Тема", "Ссылка", "Дата повтора", "Приоритет", "Категория"])
        self.table_object.setModel(self.items)
        self.table_object.horizontalHeader().setStretchLastSection(True)
        self.table_object.setAlternatingRowColors(True)
        self.table_object.setSelectionBehavior(QTableView.SelectRows)
        self.main_layout.addWidget(self.table_object)

        # 📆 Календарь
        self.view = QWebEngineView()

        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

        # Путь к HTML-файлу
        html_path = resource_path("calendar.html")
        base_url = QUrl.fromLocalFile(os.path.dirname(html_path) + "/")

        # Читаем HTML
        with open(html_path, encoding='utf-8') as f:
            html = f.read()

        # Отображаем HTML с baseUrl (для корректной загрузки JS и ресурсов)
        self.view.setHtml(html, base_url)
        self.main_layout.addWidget(self.view, stretch=1)

        # 🔄 Кнопка обновления
        self.refresh_table = QPushButton("Обновить данные")
        self.main_layout.addWidget(self.refresh_table)

        # 📥 Layout ввода и управления
        self.line_layout = QHBoxLayout()
        self.line_layout.setSpacing(8)

        self.name_object = QLineEdit()
        self.name_object.setPlaceholderText("Имя темы")
        self.line_layout.addWidget(self.name_object)

        self.object_href = QLineEdit()
        self.object_href.setPlaceholderText("Ссылка темы")
        self.line_layout.addWidget(self.object_href)

        self.category_object = QLineEdit()
        self.category_object.setPlaceholderText("Категория темы")
        self.line_layout.addWidget(self.category_object)

        self.prioritet_check = QCheckBox("Приоритет")
        self.line_layout.addWidget(self.prioritet_check)

        self.send_to_bd_button = QPushButton("Отправить")
        self.line_layout.addWidget(self.send_to_bd_button)

        self.delete_rows = QComboBox()
        self.delete_rows.setMinimumWidth(150)
        self.line_layout.addWidget(self.delete_rows)

        self.delete_button = QPushButton("Удалить")
        self.line_layout.addWidget(self.delete_button)

        self.main_layout.addLayout(self.line_layout)

        # 🔽 Меню и статусбар
        self.menubar = QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Гримуар.app", None))
        self.refresh_table.setText("Обновить данные")
        self.send_to_bd_button.setText("Отправить")
        self.delete_button.setText("Удалить")
        self.prioritet_check.setText("Приоритет")

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)
