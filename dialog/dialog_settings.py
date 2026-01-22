import os

from PyQt5 import QtWidgets, QtCore

from json_helper import JsonHelper


# Окно настроей во вкладке 'База данных РЛС'
class DialogSettings(QtWidgets.QDialog):
    layout_main = None

    layout_fields = None
    line_dir = None

    layout_buttons = None
    button_dir = None

    button_box = None

    def initComponents(self):
        self.line_dir = QtWidgets.QLineEdit()
        self.button_dir = QtWidgets.QPushButton('Выбрать')
        self.layout_fields = QtWidgets.QFormLayout()

        self.button_box = QtWidgets.QDialogButtonBox()

        self.layout_main = QtWidgets.QVBoxLayout()

    def createDialog(self):
        json_helper = JsonHelper()
        self.line_dir.setText(json_helper.settings['path_rtr_model'])
        self.line_dir.setClearButtonEnabled(True)
        self.button_dir.clicked.connect(self.selectDirClicked)
        layout_dir = QtWidgets.QHBoxLayout()
        layout_dir.addWidget(self.line_dir, stretch=1)
        layout_dir.addWidget(self.button_dir, stretch=0)
        self.layout_fields.addRow('Каталог\nс СПО:', layout_dir)
        self.layout_fields.setLabelAlignment(QtCore.Qt.AlignLeft)
        self.button_box.addButton('Сохранить', QtWidgets.QDialogButtonBox.AcceptRole)
        self.button_box.addButton('Отмена', QtWidgets.QDialogButtonBox.RejectRole)
        self.button_box.accepted.connect(self.saveClicked)
        self.button_box.rejected.connect(self.reject)
        self.layout_main.addLayout(self.layout_fields)
        self.layout_main.addWidget(self.button_box)

        self.setLayout(self.layout_main)

    def selectDirClicked(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                         caption='Выбор каталога',
                                                         directory=os.path.sep)
        if dir != '':
            self.line_dir.setText(dir)

    def selectFileClicked(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     caption='Выбор файла',
                                                     directory=os.path.sep)
        if file[0] != '':
            self.line_file.setText(file[0])

    def saveClicked(self):
        json_helper = JsonHelper()
        json_helper.saveSettings(self.line_dir.text())
        self.accept()

    def __init__(self):
        super().__init__()
        self.initComponents()
        self.createDialog()
        self.resize(450, 0)
        self.setWindowTitle('Окно настроек')

