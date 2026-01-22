from PyQt5 import QtWidgets, QtCore

# Компонент поисковая строка в фильтре
class FilterLine(QtWidgets.QGroupBox):

    def __init__(self, title, place_holder_text):
        super().__init__()
        self.setTitle(title)
        self.layout = None
        self.lineEdit = None

        self.initComponents()
        self.createFilter(place_holder_text)

    def initComponents(self):
        self.lineEdit = QtWidgets.QLineEdit()
        self.layout = QtWidgets.QVBoxLayout()

    def createFilter(self, place_holder_text):
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText(place_holder_text)
        # self.lineEdit.textChanged.connect(self.setCreateModel)
        self.setAlignment(QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.lineEdit)
        self.setLayout(self.layout)
        # self.setFixedSize(0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed))
