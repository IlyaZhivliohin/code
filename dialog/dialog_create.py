import os

from PyQt5 import QtWidgets, QtCore, QtGui

from json_helper import JsonHelper

# Окно предварительного просмотра при
# создания набора из выбранных
# объектов в таблице во вкладке 'База данных РЛС'
class DialogCreate(QtWidgets.QDialog):
    layout_main = None

    table_view = None

    widget_fields = None
    layout_fields = None
    layout_left = None
    line_name = None
    line_country = None
    line_type = None
    layout_right = None
    line_date = None
    line_other = None

    button_box = None

    def initComponents(self):
        self.table_view = QtWidgets.QTableView()

        self.line_name = QtWidgets.QLineEdit()
        self.line_country = QtWidgets.QLineEdit()
        self.line_type = QtWidgets.QLineEdit()
        self.line_date = QtWidgets.QLineEdit()
        self.line_other = QtWidgets.QLineEdit()
        self.layout_left = QtWidgets.QFormLayout()
        self.layout_right = QtWidgets.QFormLayout()
        self.layout_fields = QtWidgets.QHBoxLayout()
        self.widget_fields = QtWidgets.QWidget()

        self.button_box = QtWidgets.QDialogButtonBox()

        self.layout_main = QtWidgets.QVBoxLayout()

    def createDialog(self):
        self.line_country.setText(', '.join(self.data_country))
        self.line_type.setText(', '.join(self.data_type))
        self.line_date.setText(self.data_date)
        
        self.line_name.setClearButtonEnabled(True)
        self.line_country.setClearButtonEnabled(True)
        self.line_type.setClearButtonEnabled(True)
        self.line_date.setClearButtonEnabled(True)
        self.line_date.setInputMask('99.B9.9999')
        self.line_other.setClearButtonEnabled(True)
        self.layout_left.addRow('*Название:', self.line_name)
        self.layout_left.addRow('Страна:', self.line_country)
        self.layout_left.addRow('Тип:', self.line_type)
        self.layout_left.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.layout_right.addRow('Дата:', self.line_date)
        self.layout_right.addRow('Доп.\nинформация:', self.line_other)
        self.layout_right.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.layout_fields.addLayout(self.layout_left, stretch=1)
        self.layout_fields.addLayout(self.layout_right, stretch=1)
        self.widget_fields.setLayout(self.layout_fields)
        self.widget_fields.setContentsMargins(4, 0, 4, 0)
        self.layout_main.addWidget(self.table_view, stretch=1)
        self.layout_main.addWidget(self.widget_fields, stretch=0)
        self.layout_main.addWidget(self.button_box, stretch=0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        self.button_box.addButton('Создать', QtWidgets.QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Отмена', QtWidgets.QDialogButtonBox.RejectRole)
        self.button_box.accepted.connect(self.createClicked)
        self.button_box.rejected.connect(self.reject)
        self.button_box.setContentsMargins(10, 0, 10, 10)

        self.setLayout(self.layout_main)

    def createLinks(self, col):
        for row in range(self.table_view.model().rowCount()):
            label = QtWidgets.QLabel()
            index = self.table_view.model().index(row, col)
            data = str(self.table_view.model().data(index))
            label.setText(f'<a href={data}>{os.path.basename(data)}</a>')
            label.setToolTip(data)
            label.setOpenExternalLinks(True)
            label.setAutoFillBackground(True)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.table_view.setIndexWidget(index, label)

    def createTable(self):
        model = QtGui.QStandardItemModel()
        for i in range(len(self.data)):
            model.appendRow([QtGui.QStandardItem(str(self.data[i].id)),
                QtGui.QStandardItem(self.data[i].name),
                QtGui.QStandardItem(self.data[i].source),
                QtGui.QStandardItem(self.data[i].country),
                QtGui.QStandardItem(self.data[i].carrier),
                QtGui.QStandardItem(self.data[i].type),
                QtGui.QStandardItem(self.data[i].carry_freq),
                QtGui.QStandardItem(self.data[i].carry_freq_set),
                QtGui.QStandardItem(self.data[i].period_mks),
                QtGui.QStandardItem(self.data[i].period_mks_set),
                QtGui.QStandardItem(self.data[i].width_mks),
                QtGui.QStandardItem(self.data[i].width_mks_set),
                QtGui.QStandardItem(self.data[i].rotate_period_sec),
                QtGui.QStandardItem(self.data[i].rotate_period_sec_set),
                QtGui.QStandardItem(self.data[i].description_of_the_object),
                QtGui.QStandardItem(self.data[i].description_of_the_source),
                QtGui.QStandardItem(self.data[i].signals)])

        model.setHorizontalHeaderLabels(['id', 'Название', 'Источник',
                                       'Страна', 'Носитель', 'Тип', 'Частоты, мГц', 'Частоты, мГц (для набора)',
                                       'Периоды следования импульсов, мкс', 'Периоды следования импульсов, мкс (для набора)',
                                       'Длительность импульсов, мкс', 'Длительность импульсов, мкс (для набора)',
                                       'Период следования серии импульсов, с', 'Период следования серии импульсов, с (для набора)',
                                       'Описание объекта', 'Описание источника', 'Сигналы'])

        for row in range(model.rowCount()):
            for col in range(model.columnCount()):
                model.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)

        self.table_view.setModel(model)
        font = QtGui.QFont()
        font.setBold(True)
        self.table_view.horizontalHeader().setFont(font)
        self.table_view.setSortingEnabled(True)
        self.table_view.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.table_view.setWordWrap(True)
        self.table_view.setTextElideMode(QtCore.Qt.ElideRight)
        self.table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

        self.createLinks(15)
        self.createLinks(16)
        self.createLinks(17)

        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(6, 320)
        self.table_view.setColumnWidth(7, 320)
        self.table_view.setColumnWidth(8, 320)
        for row in range(self.table_view.model().rowCount()):
            self.table_view.setRowHeight(row, 52)

    def createClicked(self):
        if(self.line_name.text() == ''):
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                           'Информация',
                                           'Поле "Название" является обязательным для заполнения.',
                                           QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            json_helper = JsonHelper()
            if json_helper.settings['path_rtr_model'] != '':
                try:
                    json_helper.createSet(self.data, self.line_name.text(), self.line_country.text(),
                                          self.line_type.text(), self.line_date.text(), self.line_other.text())
                except FileNotFoundError:
                    msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                    'Ошибка',
                                                    'Ошибка при создании набора. '
                                                    'Возможно выбранный вами каталог в настройках '
                                                    'не является каталогом с СПО.',
                                                    QtWidgets.QMessageBox.Ok)
                    msg_box.exec()
                except ValueError:
                    msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                    'Ошибка',
                                                    'Ошибка при создании набора. '
                                                    'Возможно в ячейках хранятся некорректные данные.',
                                                    QtWidgets.QMessageBox.Ok)
                    msg_box.exec()
            else:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                'Информация',
                                                'Для создания набора необходимо указать в настройках '
                                                'пути сохранения и подгрузки набора.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
            self.accept()

    def __init__(self, data, data_country, data_type, data_date):
        super().__init__()
        self.data = data
        self.data_country = data_country
        self.data_type = data_type
        self.data_date = data_date

        self.initComponents()
        self.createDialog()
        self.createTable()
        self.resize(650, 450)
        self.setWindowTitle('Окно предварительного просмотра и создания набора')


