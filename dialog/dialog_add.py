import os

from PyQt5 import QtWidgets, QtGui, QtCore

from rls import RLS
from json_helper import JsonHelper


# Окно добавления объектов в выбранный
# набор во вкладке 'Наборы РЛС'
class DialogAdd(QtWidgets.QDialog):
    layout_main = None
    table_view = None
    button_box = None

    def initComponents(self):
        self.table_view = QtWidgets.QTableView()
        self.button_box = QtWidgets.QDialogButtonBox()
        self.layout_main = QtWidgets.QVBoxLayout()

    def createDialog(self):
        self.button_box.addButton('Добавить', QtWidgets.QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Отмена', QtWidgets.QDialogButtonBox.RejectRole)
        self.button_box.accepted.connect(self.addClicked)
        self.button_box.rejected.connect(self.reject)
        self.button_box.setContentsMargins(10, 3, 10, 10)
        self.layout_main.addWidget(self.table_view)
        self.layout_main.addWidget(self.button_box)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        for obj in self.table_view.children():
            if type(obj) is QtWidgets.QAbstractButton:
                obj.clicked.connect(self.selectAllClicked)
                obj.setToolTip('Выбрать все')
                break

    def selectAllClicked(self):
        flag = False
        for row in range(self.table_view.model().rowCount()):
            index = self.table_view.model().index(row, 0)
            for obj in self.table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox:
                    if obj.checkState() == 0:
                        flag = True

        for row in range(self.table_view.model().rowCount()):
            index = self.table_view.model().index(row, 0)
            for obj in self.table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox:
                    obj.setChecked(2 if flag else 0)

    def createCheckBoxes(self):
        for row in range(self.table_view.model().rowCount()):
            checkBox = QtWidgets.QCheckBox()
            layout = QtWidgets.QHBoxLayout()
            widget = QtWidgets.QWidget()
            layout.addWidget(checkBox, alignment=QtCore.Qt.AlignCenter)
            widget.setLayout(layout)
            widget.setAutoFillBackground(True)
            index = self.table_view.model().index(row, 0)
            self.table_view.setIndexWidget(index, widget)

    def createLinks(self, col):
        for row in range(self.table_view.model().rowCount()):
            label = QtWidgets.QLabel()
            index = self.table_view.model().index(row, col)
            data = self.table_view.model().data(index)
            label.setText(f'<a href={data}>{os.path.basename(data)}</a>')
            label.setToolTip(data)
            label.setOpenExternalLinks(True)
            label.setAutoFillBackground(True)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.table_view.setIndexWidget(index, label)

    def createTable(self):
        self.sim_model = QtGui.QStandardItemModel()
        for row in range(self.model.rowCount()):
            items = []
            for col in range(self.model.columnCount()):
                if col == 0:
                    items.append(QtGui.QStandardItem())
                else:
                    index = self.model.index(row, col)
                    items.append(QtGui.QStandardItem(str(self.model.data(index))))
            self.sim_model.appendRow(items)

        self.sim_model.setHorizontalHeaderLabels(['Выбор', 'id', 'Название', 'Источник',
                                       'Страна', 'Носитель', 'Тип', 'Частоты, мГц', 'Частоты, мГц (для набора)',
                                       'Периоды следования импульсов, мкс', 'Периоды следования импульсов, мкс (для набора)',
                                       'Длительность импульсов, мкс', 'Длительность импульсов, мкс (для набора)',
                                       'Период следования серии импульсов, с', 'Период следования серии импульсов, с (для набора)',
                                       'Описание объекта', 'Описание источника', 'Сигналы'])

        for row in range(self.sim_model.rowCount()):
            for col in range(self.sim_model.columnCount()):
                self.sim_model.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)

        self.table_view.setModel(self.sim_model)
        font = QtGui.QFont()
        font.setBold(True)
        self.table_view.horizontalHeader().setFont(font)
        self.table_view.setSortingEnabled(True)
        self.table_view.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.table_view.setWordWrap(True)
        self.table_view.setTextElideMode(QtCore.Qt.ElideRight)
        self.table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

        self.createCheckBoxes()
        self.createLinks(15)
        self.createLinks(16)
        self.createLinks(17)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(7, 320)
        self.table_view.setColumnWidth(8, 320)
        self.table_view.setColumnWidth(9, 320)
        for row in range(self.table_view.model().rowCount()):
            self.table_view.setRowHeight(row, 52)

    def addClicked(self):
        list = []
        for row in range(self.table_view.model().rowCount()):
            index = self.table_view.model().index(row, 0)
            for obj in self.table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox and obj.checkState() == 2:
                    list.append(RLS(self.table_view.model().data(self.table_view.model().index(row, 0)),
                                    self.table_view.model().data(self.table_view.model().index(row, 1)),
                                    self.table_view.model().data(self.table_view.model().index(row, 2)),
                                    self.table_view.model().data(self.table_view.model().index(row, 3)),
                                    self.table_view.model().data(self.table_view.model().index(row, 4)),
                                    self.table_view.model().data(self.table_view.model().index(row, 5)),
                                    self.table_view.model().data(self.table_view.model().index(row, 6)),
                                    self.table_view.model().data(self.table_view.model().index(row, 7)),
                                    self.table_view.model().data(self.table_view.model().index(row, 8)),
                                    self.table_view.model().data(self.table_view.model().index(row, 9)),
                                    self.table_view.model().data(self.table_view.model().index(row, 10)),
                                    self.table_view.model().data(self.table_view.model().index(row, 11)),
                                    self.table_view.model().data(self.table_view.model().index(row, 12)),
                                    self.table_view.model().data(self.table_view.model().index(row, 13)),
                                    self.table_view.model().data(self.table_view.model().index(row, 14)),
                                    self.table_view.model().data(self.table_view.model().index(row, 15)),
                                    self.table_view.model().data(self.table_view.model().index(row, 16)),
                                    self.table_view.model().data(self.table_view.model().index(row, 17))))
        json_helper = JsonHelper()
        try:
            json_helper.addInSet(list, self.name)
        except FileNotFoundError:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                            'Ошибка',
                                            'Ошибка при добавлении объектов в файл, '
                                            'возможно он был удален',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()
            self.done(-1)
        else:
            self.accept()

    def __init__(self, name, model):
        super().__init__()
        self.name = name
        self.model = model
        self.sim_model = None
        self.initComponents()
        self.createDialog()
        self.createTable()
        self.resize(750, 450)
        self.setWindowTitle('Окно добавления объектов в набор')
