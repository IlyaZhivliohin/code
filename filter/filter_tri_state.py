from PyQt5 import QtWidgets, QtCore, QtGui

# Компонент для фильтрации в таблице
# по выбранным объектам
class FilterTriState(QtWidgets.QGroupBox):
    
    def __init__(self, title, data, old_btn_grp=None):
        super().__init__()
        self.setTitle(title)
        self.data = data
        self.btn_grp = None
        self.cb_all = None
        self.btn_grp_layout = None
        self.scr_area = None
        self.group_box_layout = None

        self.initComponents()
        self.createFilter(old_btn_grp)

    def initComponents(self):
        self.btn_grp = QtWidgets.QButtonGroup(self)
        self.btn_grp_layout = QtWidgets.QVBoxLayout()
        self.group_box = QtWidgets.QGroupBox()
        self.scr_area = QtWidgets.QScrollArea()
        self.group_box_layout = QtWidgets.QVBoxLayout()
        self.cb_all = QtWidgets.QCheckBox('Все')

    def createFilter(self, old_btn_grp):
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_grp.setExclusive(False)
        if len(self.data) >= 2:
            self.cb_all.setCheckState(QtCore.Qt.Checked)
            self.btn_grp_layout.addWidget(self.cb_all)

        for item in self.data:
            # if str(i).isspace() is not True and str(i) != '':
            check_box = QtWidgets.QCheckBox(str(item))
            check_box.setCheckState(self.searchCheckState(item, old_btn_grp))
            self.btn_grp.addButton(check_box)
            self.btn_grp_layout.addWidget(check_box)

        self.group_box.setLayout(self.btn_grp_layout)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor("white"))
        self.group_box.setPalette(pal)
        self.group_box.setFlat(True)
        self.scr_area.setPalette(pal)
        self.scr_area.setWidget(self.group_box)
        self.group_box_layout.addWidget(self.scr_area)
        self.setLayout(self.group_box_layout)

    def searchCheckState(self, name, old_btn_grp):
        if old_btn_grp is not None:
            for i in old_btn_grp.buttons():
                if type(i) is QtWidgets.QCheckBox:
                    if i.text() == name:
                        return i.checkState()
        return QtCore.Qt.Checked
