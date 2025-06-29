# -*- coding: utf-8 -*-

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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(698, 595)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 350, 661, 51))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 390, 671, 80))
        self.line_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.line_layout.setObjectName(u"line_layout")
        self.line_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.line_layout.setContentsMargins(0, 0, 0, 0)
        self.name_object = QLineEdit(self.horizontalLayoutWidget)
        self.name_object.setObjectName(u"name_object")
        self.name_object.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_layout.addWidget(self.name_object)

        self.object_href = QLineEdit(self.horizontalLayoutWidget)
        self.object_href.setObjectName(u"object_href")
        self.object_href.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_layout.addWidget(self.object_href)

        self.category_object = QLineEdit(self.horizontalLayoutWidget)
        self.category_object.setObjectName(u"category_object")
        self.category_object.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_layout.addWidget(self.category_object)

        self.send_to_bd_button = QPushButton(self.horizontalLayoutWidget)
        self.send_to_bd_button.setObjectName(u"send_to_bd_button")

        self.line_layout.addWidget(self.send_to_bd_button)

        self.prioritet_check = QCheckBox(self.horizontalLayoutWidget)
        self.prioritet_check.setObjectName(u"prioritet_check")

        self.line_layout.addWidget(self.prioritet_check)

        self.table_area = QScrollArea(self.centralwidget)
        self.table_area.setObjectName(u"table_area")
        self.table_area.setGeometry(QRect(50, 20, 601, 351))
        self.table_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 599, 349))
        self.table_object = QTableView(self.scrollAreaWidgetContents)
        self.table_object.setObjectName(u"table_object")
        self.table_object.setGeometry(QRect(0, 30, 601, 401))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_object.sizePolicy().hasHeightForWidth())
        self.table_object.setSizePolicy(sizePolicy)
        self.table_object.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.table_object.horizontalHeader().setMinimumSectionSize(120)
        self.table_object.horizontalHeader().setHighlightSections(True)
        self.items = QStandardItemModel()
        self.items.setHorizontalHeaderLabels([
            "Тема",
            "Ссылка",
            "Дата повтора",
            "Приоритет",
            "Категория"
        ])
        self.table_object.setModel(self.items)
        self.refresh_table = QPushButton(self.scrollAreaWidgetContents)
        self.refresh_table.setObjectName(u"refresh_table")
        self.refresh_table.setGeometry(QRect(240, 0, 131, 32))
        self.table_area.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 698, 37))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.name_object.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f \u0442\u0435\u043c\u044b", None))
        self.object_href.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0441\u044b\u043b\u043a\u0430 \u0442\u0435\u043c\u044b", None))
        self.category_object.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0442\u0435\u043c\u044b", None))
        self.send_to_bd_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.prioritet_check.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442", None))
        self.refresh_table.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435", None))
    # retranslateUi

