import os, shutil, time, math, json, pandas, zipfile
from functools import partial

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql

from model.my_sql_table_model import MySqlTableModel
from dialog.dialog_add import DialogAdd
from dialog.dialog_create import DialogCreate
from dialog.dialog_settings import DialogSettings
from filter.filter_tri_state import FilterTriState
from filter.filter_line import FilterLine
from data_base import DataBase
from json_helper import JsonHelper


class MainWindow(QtWidgets.QMainWindow):

    data_base = DataBase()

    layout_main = None
    tab_widget = None

    db_layout_main = None
    db_widget_main = None
    db_window_main = None
    db_tool_bar_cor = None
    db_act_cor = None
    db_act_red = None
    db_act_add = None
    db_act_del = None
    db_act_cut = None
    db_act_copy = None
    db_act_paste = None
    db_menu_other = None
    db_tool_bar_basic = None
    db_act_basic = None
    db_act_filter = None
    db_act_crt_set = None
    db_act_stn = None
    db_act_exp = None

    db_widget_filter = None
    db_layout_filter = None

    db_tri_choice = None
    db_tri_source = None
    db_tri_country = None
    db_tri_carrier = None
    db_tri_type = None

    db_table_view = None
    db_scroll_bar = None
    db_sql_table_model = None

    str_filter = None
    action_grp = None
    value = 0
    old_start = 0
    old_end = 0

    # Инициализация компонентов во вкладке База данных РЛС
    def dbInitComponents(self):
        self.db_window_main = QtWidgets.QMainWindow()
        self.db_layout_main = QtWidgets.QHBoxLayout()
        self.db_widget_main = QtWidgets.QWidget()
        self.db_widget_filter = QtWidgets.QWidget()
        self.db_layout_filter = QtWidgets.QVBoxLayout()

        self.db_act_basic = QtWidgets.QAction('Основное')
        self.db_act_cor = QtWidgets.QAction('Правка')

        self.db_tool_bar_basic = QtWidgets.QToolBar()
        self.db_tool_bar_cor = QtWidgets.QToolBar()

        self.db_act_filter = QtWidgets.QAction('Отобразить фильтр', self)
        self.db_act_crt_set = QtWidgets.QAction('Создать набор', self)
        self.db_act_exp = QtWidgets.QAction('Экспорт', self)
        self.db_act_stn = QtWidgets.QAction('Настройки', self)

        self.db_act_red = QtWidgets.QAction('Включить редактирование', self)
        self.db_act_add = QtWidgets.QAction('Добавить строки', self)
        self.db_act_del = QtWidgets.QAction('Удалить строки', self)
        self.db_act_cut = QtWidgets.QAction('Вырезать', self)
        self.db_act_copy = QtWidgets.QAction('Копировать', self)
        self.db_act_paste = QtWidgets.QAction('Вставить', self)

        self.db_table_view = QtWidgets.QTableView()

    # Создание меню с панелью инструментов
    def dbCreateMenu(self):
        self.db_act_basic.setEnabled(False)
        self.db_act_basic.triggered.connect(self.dbBasicTriggered)
        # self.db_action_correction.setEnabled(False)
        self.db_act_cor.triggered.connect(self.dbCorTriggered)
        self.db_window_main.menuBar().addAction(self.db_act_basic)
        self.db_window_main.menuBar().addAction(self.db_act_cor)

        self.db_tool_bar_basic.setMovable(False)
        self.db_tool_bar_basic.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.db_tool_bar_basic.toggleViewAction().setVisible(False)
        self.db_tool_bar_cor.setMovable(False)
        self.db_tool_bar_cor.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.db_tool_bar_cor.toggleViewAction().setVisible(False)
        self.db_window_main.addToolBar(self.db_tool_bar_basic)
        self.db_window_main.addToolBar(self.db_tool_bar_cor)

        self.db_act_filter.setToolTip('Отобразить фильтр')
        self.db_act_filter.triggered.connect(self.dbFilterTriggered)
        self.dbCreateMenuInFilter()

        self.db_act_crt_set.setToolTip('Создать набор')
        self.db_act_crt_set.triggered.connect(self.dbCrtSetTriggered)
        self.db_act_exp.setToolTip('Экспорт')
        self.dbCreateMenuInExp()

        self.db_act_stn.setToolTip('Настройки')
        self.db_act_stn.triggered.connect(self.dbStnTriggered)

        self.db_tool_bar_basic.addAction(self.db_act_filter)
        self.db_tool_bar_basic.addAction(self.db_act_crt_set)
        self.db_tool_bar_basic.addAction(self.db_act_exp)
        self.db_tool_bar_basic.addAction(self.db_act_stn)

        self.db_tool_bar_basic.addSeparator()

        self.db_tool_bar_basic.addWidget(self.dbCreateVisStateOfTable())
        # -------------------------
        self.db_act_red.setShortcut('Ctrl+R')
        self.db_act_red.setToolTip('Включить редактирование (Ctrl+R)')
        self.db_act_red.triggered.connect(self.dbRedTriggered)

        self.db_act_add.setShortcut('Ctrl+N')
        self.db_act_add.setToolTip('Добавить строки (Ctrl+N)')
        self.db_act_add.setEnabled(False)
        self.db_act_add.triggered.connect(self.dbAddRowTriggered)
        self.db_act_del.setShortcut('Ctrl+Del')
        self.db_act_del.setToolTip('Удалить строки (Ctrl+Del)')
        self.db_act_del.setEnabled(False)
        self.db_act_del.triggered.connect(self.dbDelRowsTriggered)
        self.db_act_cut.setShortcut(QtGui.QKeySequence.Cut)
        self.db_act_cut.setToolTip('Вырезать (Ctrl+X)')
        self.db_act_cut.setEnabled(False)
        self.db_act_cut.triggered.connect(self.dbCutTriggered)
        self.db_act_copy.setShortcut(QtGui.QKeySequence.Copy)
        self.db_act_copy.setToolTip('Копировать (Ctrl+C)')
        self.db_act_copy.triggered.connect(self.dbCopyTriggered)
        self.db_act_paste.setShortcut(QtGui.QKeySequence.Paste)
        self.db_act_paste.setToolTip('Вставить (Ctrl+V)')
        self.db_act_paste.setEnabled(False)
        self.db_act_paste.triggered.connect(self.dbPasteTriggered)

        self.db_tool_bar_cor.addAction(self.db_act_red)
        self.db_tool_bar_cor.addSeparator()
        self.db_tool_bar_cor.addAction(self.db_act_add)
        self.db_tool_bar_cor.addAction(self.db_act_del)
        self.db_tool_bar_cor.addSeparator()
        self.db_tool_bar_cor.addAction(self.db_act_cut)
        self.db_tool_bar_cor.addAction(self.db_act_copy)
        self.db_tool_bar_cor.addAction(self.db_act_paste)
        self.db_tool_bar_cor.hide()

    # Создание компонента 'Вид таблицы' в панели инструментов
    def dbCreateVisStateOfTable(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Вид таблицы:"))
        layout.setContentsMargins(10, 0, 10, 0)
        combo_box = QtWidgets.QComboBox()
        combo_box.addItem('Полный')
        combo_box.addItem('Информационный')
        combo_box.addItem('Наборный')
        combo_box.setFixedSize(170, 29)
        combo_box.activated[str].connect(self.dbSelVisStateOfTable)
        layout.addWidget(combo_box)
        widget.setLayout(layout)
        return widget

    # Обработчик сигнала в выпадающем списке
    # при смене вида отображения таблицы
    def dbSelVisStateOfTable(self, text):
        if text == 'Полный':
            for i in range(7, 18):
                self.db_table_view.showColumn(i)
        elif text == 'Информационный':
            for i in range(7, 18):
                if i % 2 == 0 and (i != 16):
                    self.db_table_view.hideColumn(i)
                else:
                    self.db_table_view.showColumn(i)
        elif text == 'Наборный':
            for i in range(7, 18):
                if i % 2 == 1 or (i == 16):
                    self.db_table_view.hideColumn(i)
                else:
                    self.db_table_view.showColumn(i)

    # Создание выпадающего меню в пункте
    # 'Отобразить/Убрать фильтр'
    def dbCreateMenuInFilter(self):
        menu = QtWidgets.QMenu()
        actions = [QtWidgets.QAction('id', self), QtWidgets.QAction('Название', self),
                   QtWidgets.QAction('Выбор', self), QtWidgets.QAction('Источник', self),
                   QtWidgets.QAction('Страна', self), QtWidgets.QAction('Носитель', self),
                   QtWidgets.QAction('Тип', self), QtWidgets.QAction('Частоты, мГц', self)]

        for action in actions:
            action.setCheckable(True)
            action.setChecked(False)
        menu.addActions(actions)
        self.action_grp = QtWidgets.QActionGroup(menu)
        self.action_grp.setExclusive(False)
        for action in actions:
            self.action_grp.addAction(action)
            # print(action.text())
        self.action_grp.triggered.connect(partial(self.dbCheckFilterState, menu))
        self.db_act_filter.setMenu(menu)

    # Обработчик сигнала при выборе пункта
    # в выпадающем меню 'Отобразить/Убрать фильтр'
    def dbCheckFilterState(self, menu, act):
        name = act.text()
        for filter in self.db_widget_filter.children():
            if type(filter) is FilterTriState or type(filter) is FilterLine:
                if filter.title() == name:
                    if act.isChecked() == True:
                        filter.show()
                    else:
                        filter.hide()
        menu.show()

    # Создание выпадающего меню в пункте 'Экспорт'
    def dbCreateMenuInExp(self):
        menu = QtWidgets.QMenu()
        act_db = QtWidgets.QAction('Базы данных', self)
        act_sel = QtWidgets.QAction('Выбранных строк', self)
        act_files = QtWidgets.QAction('Файлов', self)

        act_db.triggered.connect(self.dbExpDBTriggered)
        act_sel.triggered.connect(self.dbExpSelTriggered)
        act_files.triggered.connect(self.dbExpFilesTriggered)

        menu.addAction(act_db)
        menu.addAction(act_sel)
        menu.addAction(act_files)
        self.db_act_exp.setMenu(menu)

    # Создание окна во вкладке База данных РЛС
    def dbCreateWindow(self):
        self.db_layout_main.setSpacing(0)
        self.db_layout_main.addWidget(self.db_widget_filter, stretch=1)
        self.db_layout_main.addWidget(self.db_table_view, stretch=5)
        self.db_layout_main.setContentsMargins(6, 6, 6, 6)
        self.db_widget_main.setLayout(self.db_layout_main)
        self.db_window_main.setCentralWidget(self.db_widget_main)

    # Создание фильтра во вкладке База данных РЛС
    def dbCreateFilter(self):
        label = QtWidgets.QLabel('Фильтр')
        label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed))
        self.db_layout_filter.setAlignment(QtCore.Qt.AlignTop)
        self.db_layout_filter.addWidget(label, alignment=QtCore.Qt.AlignHCenter)

        values = [['id', 'Поиск по id'],
                  ['Название', 'Поиск по названию']]

        for i in range(len(values)):
            search = FilterLine(values[i][0], values[i][1])
            search.lineEdit.textChanged.connect(partial(self.dbTextChangedInFilter, search.title()))
            self.db_layout_filter.addWidget(search)
            search.hide()

        values = [['Выбор', ['Выбранные', 'Невыбранные']],
                ['Источник', 'source'],
                ['Страна', 'country'],
                ['Носитель', 'carrier'],
                ['Тип', 'type'],
                ['Частоты, мГц', 'carry_freq']]
        for i in range(len(values)):
            if values[i][0] == 'Выбор':
                tri_state = FilterTriState(values[i][0], values[i][1])
            else:
                tri_state = FilterTriState(values[i][0], self.data_base.selectGroup(values[i][1]))
            self.dbConTriState(tri_state)
            self.db_layout_filter.addWidget(tri_state, stretch=10)
            tri_state.hide()

        self.db_layout_filter.setContentsMargins(0, 6, 6, 0)
        self.db_widget_filter.setContentsMargins(0, 0, 0, 0)
        self.db_widget_filter.setLayout(self.db_layout_filter)
        self.db_widget_filter.hide()

        self.dbCreateStrFilter()

    # Обработчик сигнала при использовании
    # поисковых строк в фильтре
    def dbTextChangedInFilter(self, t, text):
        self.dbCreateStrFilter()
        self.db_sql_table_model.setFilter(self.str_filter)
        # print(self.str_filter)
        self.dbResizeFields(self.db_scroll_bar.value())
        self.dbCreateWidgetsInTable(self.db_scroll_bar.value())

    # Назначение обработчиков сигналов в фильтре
    def dbConTriState(self, tri_state):
        tri_state.cb_all.stateChanged.connect(partial(self.dbTriStateChanged, tri_state.btn_grp))
        tri_state.btn_grp.buttonToggled.connect(partial(self.dbTriStateButtonToggled, tri_state.btn_grp, tri_state.cb_all))

    # Обновление конкретного наименования в
    # фильтре при изменениях в БД.
    # Обновляет конкретное наименование в
    # соответсвтии с названием столбца в БД
    def dbUpdateTriState(self, column):
        field = ''
        if column == 'Источник':
            field = 'source'
        elif column == 'Страна':
            field = 'country'
        elif column == 'Носитель':
            field = 'carrier'
        elif column == 'Тип':
            field = 'type'
        elif column == 'Частоты, мГц':
            field = 'carry_freq'
        for old_tri_state in self.db_widget_filter.children():
            if type(old_tri_state) is FilterTriState:
                if old_tri_state.title() == column:
                    index = self.db_layout_filter.indexOf(old_tri_state)
                    new_tri_state = FilterTriState(column, self.data_base.selectGroup(field), old_tri_state.btn_grp)
                    self.dbConTriState(new_tri_state)
                    # if old_tri_state.isHidden():
                    #     print(old_tri_state.title())
                    #     new_tri_state.hide()
                    self.db_layout_filter.removeWidget(old_tri_state)
                    self.db_layout_filter.insertWidget(index, new_tri_state, stretch=10)
                    for act in self.action_grp.actions():
                        if act.text() == column and not act.isChecked():
                            new_tri_state.hide()

        # self.dbCreateStrFilter()
        # self.dbCreateWidgetsInTable()

    #Обработчик сигнала для изменения состояния пункта
    #конкретного наименования в фильтре
    def dbTriStateChanged(self, btn_grp, state):
        for button in btn_grp.buttons():
            if state == QtCore.Qt.Checked:
                button.setChecked(True)
            elif state == QtCore.Qt.Unchecked:
                button.setChecked(False)

    #
    def dbTriStateButtonToggled(self, btn_grp, cb_all):
        button_states = []
        for button in btn_grp.buttons():
            button_states.append(button.isChecked())

        if all(button_states):
            cb_all.setCheckState(QtCore.Qt.Checked)
            cb_all.setTristate(False)
        elif any(button_states) == False:
            cb_all.setCheckState(QtCore.Qt.Unchecked)
            cb_all.setTristate(False)
        else:
            cb_all.setCheckState(QtCore.Qt.PartiallyChecked)

        self.dbCreateStrFilter()
        self.db_sql_table_model.setFilter(self.str_filter)

        self.dbCreateWidgetsInTable(self.db_scroll_bar.value())
        if (self.db_act_red.text() == 'Включить редактирование'):
            self.dbSetBtnsEnabled(False, self.db_scroll_bar.value(), self.db_scroll_bar.value() + 20)
        elif (self.db_act_red.text() == 'Отключить редактирование'):
            self.dbSetBtnsEnabled(True, self.db_scroll_bar.value(), self.db_scroll_bar.value() + 20)
        self.dbResizeFields(self.db_scroll_bar.value())

    # Создание промежуточной строки для фильтрации
    # конкретного наименования в фильтре
    def dbGetFilDataFromTri(self, tri_filter, db_filed_name):
        list = []
        filter = None
        for button in tri_filter.btn_grp.buttons():
            if tri_filter.btn_grp.parent().title() == 'Выбор':
                if button.isChecked():
                    if button.text() == 'Выбранные':
                        list.append(f'{db_filed_name} = 2')
                    if button.text() == 'Невыбранные':
                        list.append(f'{db_filed_name} = 0')
            else:
                if button.isChecked():
                    list.append(f'{db_filed_name} = "{button.text()}"')

        if len(list) > 1:
            filter = ' or '.join(list)
        elif len(list) == 1:
            filter = list[0]
        elif len(list) == 0:
            filter = f'{db_filed_name} = -1'
        return '(' + filter + ')'

    # Создание строки SQL для итоговой фильтрации
    # данных в таблице
    def dbCreateStrFilter(self):
        list = []
        self.str_filter = None
        for filter in self.db_widget_filter.children():
            if type(filter) is FilterTriState or type(filter) is FilterLine:
                if type(filter) is FilterLine:
                    if filter.title() == 'id':
                        if filter.lineEdit.text() != '':
                            list.append('(id = ' + str(filter.lineEdit.text()) + ')')
                    elif filter.title() == 'Название':
                        if filter.lineEdit.text() != '':
                            list.append("(name LIKE '%" + str(filter.lineEdit.text()) + "%')")
                else:
                    if filter.title() == 'Выбор':
                        list.append(self.dbGetFilDataFromTri(filter, 'choice'))
                    elif filter.title() == 'Источник':
                        list.append(self.dbGetFilDataFromTri(filter, 'source'))
                    elif filter.title() == 'Страна':
                        list.append(self.dbGetFilDataFromTri(filter, 'country'))
                    elif filter.title() == 'Носитель':
                        list.append(self.dbGetFilDataFromTri(filter, 'carrier'))
                    elif filter.title() == 'Тип':
                        list.append(self.dbGetFilDataFromTri(filter, 'type'))
                    elif filter.title() == 'Частоты, мГц':
                        list.append(self.dbGetFilDataFromTri(filter, 'carry_freq'))
                        # break

        if len(list) > 1:
            self.str_filter = ' and '.join(list)
        elif len(list) == 1:
            self.str_filter = list[0]

    # Подключение к БД и настройка модели
    # для последующего отображения данных в таблице
    def dbCreateModel(self):
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName('rls.sqlite')
        con.open()
        self.db_sql_table_model = MySqlTableModel()
        self.db_sql_table_model.setTable('rls')
        self.db_sql_table_model.select()

        self.db_sql_table_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Выбор')
        self.db_sql_table_model.setHeaderData(1, QtCore.Qt.Horizontal, 'id')
        self.db_sql_table_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Название')
        self.db_sql_table_model.setHeaderData(3, QtCore.Qt.Horizontal, 'Источник')
        self.db_sql_table_model.setHeaderData(4, QtCore.Qt.Horizontal, 'Страна')
        self.db_sql_table_model.setHeaderData(5, QtCore.Qt.Horizontal, 'Носитель')
        self.db_sql_table_model.setHeaderData(6, QtCore.Qt.Horizontal, 'Тип')
        self.db_sql_table_model.setHeaderData(7, QtCore.Qt.Horizontal, 'Частоты, мГц')
        self.db_sql_table_model.setHeaderData(8, QtCore.Qt.Horizontal, 'Частоты, мГц\n(для набора)')
        self.db_sql_table_model.setHeaderData(9, QtCore.Qt.Horizontal, 'Период следования импульсов, мкс')
        self.db_sql_table_model.setHeaderData(10, QtCore.Qt.Horizontal, 'Период следования импульсов, мкс\n(для набора)')
        self.db_sql_table_model.setHeaderData(11, QtCore.Qt.Horizontal, 'Длительность импульсов, мкс')
        self.db_sql_table_model.setHeaderData(12, QtCore.Qt.Horizontal, 'Длительность импульсов, мкс\n(для набора)')
        self.db_sql_table_model.setHeaderData(13, QtCore.Qt.Horizontal, 'Период следования серии импульсов, с')
        self.db_sql_table_model.setHeaderData(14, QtCore.Qt.Horizontal, 'Период следования серии импульсов, с\n(для набора)')
        self.db_sql_table_model.setHeaderData(15, QtCore.Qt.Horizontal, 'Описание объекта')
        self.db_sql_table_model.setHeaderData(16, QtCore.Qt.Horizontal, 'Описание источника')
        self.db_sql_table_model.setHeaderData(17, QtCore.Qt.Horizontal, 'Сигналы')

        while self.db_sql_table_model.canFetchMore():
            self.db_sql_table_model.fetchMore()


    # Создание таблицы и связка с ней созданной модели,
    # связанной непосредственно с указанной БД
    def dbCreateTable(self):
        self.db_table_view.setModel(self.db_sql_table_model)

        font = QtGui.QFont()
        font.setBold(True)
        self.db_table_view.horizontalHeader().setFont(font)
        self.db_table_view.setSortingEnabled(True)
        self.db_table_view.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.db_table_view.setWordWrap(True)
        self.db_table_view.setTextElideMode(QtCore.Qt.ElideRight)

        self.db_table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.db_table_view.model().dataChanged.connect(self.dbTableDataChanged)

        for i in self.db_table_view.children():
            for j in i.children():
                if type(j) is QtWidgets.QScrollBar:
                    if j.orientation() == QtCore.Qt.Vertical:
                        self.db_scroll_bar = j
        self.db_scroll_bar.valueChanged.connect(self.dbScrollValueChanged)
        # self.db_scroll_bar.sliderMoved.connect(self.test)
        # self.db_scroll_bar.sliderPressed.connect(self.test1)
        # self.db_scroll_bar.sliderReleased.connect(self.test2)
        # self.db_scroll_bar.actionTriggered.connect(self.test3)

        self.db_table_view.horizontalHeader().sectionClicked.connect(lambda: self.dbCreateWidgetsInTable(self.db_scroll_bar.value()))

        for obj in self.db_table_view.children():
            if type(obj) is QtWidgets.QAbstractButton:
                obj.clicked.connect(self.dbSelAllRowsClicked)
                obj.setToolTip('Выбрать все')
                break
        self.dbResizeFields(self.db_scroll_bar.value())
        self.dbCreateWidgetsInTable(self.db_scroll_bar.value())

    # Обработчик сигнала, отвечающий за
    # создание виджетов в видимой
    # области таблицы при прокручивании
    # ScrollBar`а
    def dbScrollValueChanged(self, value):
        start = value
        end = value + 20
        if start > 1:
            start = start - 1
        if end > self.db_table_view.model().rowCount():
            end = self.db_table_view.model().rowCount()

        if self.old_start != 0 and self.old_end != 0:
            for row in range(self.old_start, self.old_end):
                index = self.db_table_view.model().index(row, 0)
                w = self.db_table_view.indexWidget(index)
                del w
                self.db_table_view.setIndexWidget(index, None)
                # w.deleteLater()
                index = self.db_table_view.model().index(row, 15)
                w = self.db_table_view.indexWidget(index)
                del w
                self.db_table_view.setIndexWidget(index, None)

                index = self.db_table_view.model().index(row, 16)
                w = self.db_table_view.indexWidget(index)
                del w
                self.db_table_view.setIndexWidget(index, None)

                index = self.db_table_view.model().index(row, 17)
                w = self.db_table_view.indexWidget(index)
                del w
                self.db_table_view.setIndexWidget(index, None)

        self.old_start = start
        self.old_end = end

        self.dbCreateWidgetsInTable(value)
        self.dbResizeFields(value)


    # Обработчик сигнал, срабатывающий при изменении
    # данных в таблице
    def dbTableDataChanged(self, left, right):
        columns = ['Источник', 'Страна', 'Носитель', 'Тип', 'Частоты, мГц']
        for column in columns:
            self.dbUpdateTriState(column)
        self.dbCreateStrFilter()
        self.db_sql_table_model.submitAll()
        self.db_sql_table_model.select()
        while self.db_sql_table_model.canFetchMore():
            self.db_sql_table_model.fetchMore()

        # self.db_scroll_bar.setValue(self.db_scroll_bar.value())
        self.dbScrollValueChanged(self.db_scroll_bar.value())
        self.dbCreateWidgetsInTable(self.db_scroll_bar.value())
        self.dbResizeFields(self.db_scroll_bar.value())

    # Изменение размера полей в таблице
    # для удобного для чтения отображения данных в ней
    def dbResizeFields(self, value):
        start = value
        end = value + 20
        if start > 1:
            start = start - 1
        if end > self.db_table_view.model().rowCount():
            end = self.db_table_view.model().rowCount()

        self.db_table_view.resizeColumnsToContents()
        self.db_table_view.setColumnWidth(7, 350)
        self.db_table_view.setColumnWidth(8, 350)
        self.db_table_view.setColumnWidth(9, 350)
        self.db_table_view.setColumnWidth(10, 350)
        self.db_table_view.setColumnWidth(11, 350)
        self.db_table_view.setColumnWidth(12, 350)
        self.db_table_view.setColumnWidth(13, 350)
        self.db_table_view.setColumnWidth(14, 350)
        for row in range(start, end):
            self.db_table_view.setRowHeight(row, 52)

    # Создание галочек в столбце 'Выбор'
    def dbCreateCheckBoxes(self, start, end):
        for row in range(start, end):
            checkBox = QtWidgets.QCheckBox()
            layout = QtWidgets.QHBoxLayout()
            widget = QtWidgets.QWidget()
            layout.addWidget(checkBox, alignment=QtCore.Qt.AlignCenter)
            widget.setLayout(layout)
            widget.setAutoFillBackground(True)
            index = self.db_table_view.model().index(row, 0)
            self.db_table_view.setIndexWidget(index, widget)

            data = self.db_table_view.model().data(index)
            for obj in self.db_table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox:
                    obj.setChecked(2 if data == 2 else 0)

            checkBox.stateChanged.connect(partial(self.dbCheckStateChanged, index))

    # Создание виджета с лейблом и
    # кнопкой для отображения ссылки
    # и управление ей в назначенных столбцах
    def dbCreateLinks(self, col, start, end):
        for row in range(start, end):
            label = QtWidgets.QLabel()
            button = QtWidgets.QPushButton()
            menu = QtWidgets.QMenu()
            layout = QtWidgets.QHBoxLayout()
            widget = QtWidgets.QWidget()
            act_add_link = QtWidgets.QAction('Добавить ссылку', self)
            act_del_link = QtWidgets.QAction('Удалить ссылку', self)
            layout.addWidget(label, stretch=1, alignment=QtCore.Qt.AlignCenter)
            layout.addWidget(button, stretch=0)
            widget.setLayout(layout)
            index = self.db_table_view.model().index(row, col)
            data = self.db_table_view.model().data(index)
            # data = str(data)
            label.setText(f'<a href={data}>{os.path.basename(data)}</a>')
            label.setToolTip(data)
            label.setOpenExternalLinks(True)
            button.setToolTip('Управление ссылкой')
            menu.addAction(act_add_link)
            menu.addSeparator()
            menu.addAction(act_del_link)
            button.setMenu(menu)
            button.setFixedSize(24, 30)
            if self.db_act_red.text() == 'Включить редактирование':
                button.setEnabled(False)
            widget.setAutoFillBackground(True)
            act_add_link.triggered.connect(partial(self.dbAddLinkTriggered, index, col))
            act_del_link.triggered.connect(partial(self.dbDelLinkTriggered, index))
            self.db_table_view.setIndexWidget(index, widget)

    # Назначение состояния кнопки
    # в виджете управления ссылкой в зависимости
    # от состояния редактирования таблицы
    def dbSetBtnsEnabled(self, state, start, end):
        if start > 1:
            start = start - 1
        if end > self.db_table_view.model().rowCount():
            end = self.db_table_view.model().rowCount()

        for row in range(start, end):
            for col in range(15, 18):
                index = self.db_table_view.model().index(row, col)
                if self.db_table_view.indexWidget(index).children() is not None:
                    for obj in self.db_table_view.indexWidget(index).children():
                        if type(obj) is QtWidgets.QPushButton:
                            obj.setEnabled(state)

    # Создание галочки и виджета
    # управления ссылкой в назначенных столбцах
    def dbCreateWidgetsInTable(self, value):
        start = value
        end = value + 20
        if start > 1:
            start = start - 1
        if end > self.db_table_view.model().rowCount():
            end = self.db_table_view.model().rowCount()

        self.dbCreateCheckBoxes(start, end)
        self.dbCreateLinks(15, start, end)
        self.dbCreateLinks(16, start, end)
        self.dbCreateLinks(17, start, end)

    # Обработчик сигнала, добавлящий ссылку
    # в ячейку строки и загружающий выбранный файл в ПО
    def dbAddLinkTriggered(self, index, col):
        old_data = self.db_table_view.model().data(index)
        if col == 15 or col == 16:
            file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         caption='Выбор файла',
                                                         directory=os.path.sep)
            if file[0] != '':
                for obj in self.db_table_view.indexWidget(index).children():
                    if type(obj) is QtWidgets.QLabel:
                        try:
                            if col == 15:
                                shutil.copyfile(file[0], 'files/objects' + os.path.sep + os.path.basename(file[0]))
                            elif col == 16:
                                shutil.copyfile(file[0], 'files/sources' + os.path.sep + os.path.basename(file[0]))
                        except (OSError, FileNotFoundError) as e:
                            # print(e)
                            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                            'Ошибка',
                                                            'Не удалось добавить файл в ПО. ',
                                                            QtWidgets.QMessageBox.Ok)
                            msg_box.exec()
                        else:
                            new_data = ''
                            if col == 15:
                                new_data = 'files/objects' + os.path.sep + os.path.basename(file[0])
                            elif col == 16:
                                new_data = 'files/sources' + os.path.sep + os.path.basename(file[0])
                            # if old_data != '':
                            #     try:
                            #         os.remove(old_data)
                            #     except (OSError, FileNotFoundError):
                            #         pass
                            obj.setText(f'<a href={new_data}>{os.path.basename(new_data)}</a>')
                            self.db_table_view.model().setData(index, new_data)

        elif col == 17:
            dir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             caption='Выбор каталога',
                                                             directory=os.path.sep)
            if dir != '':
                new_data = 'files/signals' + os.path.sep + os.path.basename(dir)
                for obj in self.db_table_view.indexWidget(index).children():
                    if type(obj) is QtWidgets.QLabel:
                        try:
                            shutil.copytree(dir, new_data)
                        except FileExistsError:
                            shutil.rmtree(new_data, ignore_errors=True)
                            shutil.copytree(dir, new_data)

                            obj.setText(f'<a href={new_data}>{os.path.basename(new_data)}</a>')
                            self.db_table_view.model().setData(index, new_data)
                        except FileNotFoundError:
                            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                            'Ошибка',
                                                            'Не удалось добавить каталог в ПО.',
                                                            QtWidgets.QMessageBox.Ok)
                            msg_box.exec()
                        else:
                            # if old_data != '':
                            #     shutil.rmtree(old_data, ignore_errors=True)
                            obj.setText(f'<a href={new_data}>{os.path.basename(new_data)}</a>')
                            self.db_table_view.model().setData(index, new_data)

    # Обработчик сигнала, удаляющий ссылку
    # из ячейки строки
    def dbDelLinkTriggered(self, index):
        for obj in self.db_table_view.indexWidget(index).children():
            if type(obj) is QtWidgets.QLabel:
                data = self.db_table_view.model().data(index)
                # if os.path.isfile(data):
                #     try:
                #         os.remove(data)
                #     except OSError:
                #         pass
                # elif os.path.isdir(data):
                #     shutil.rmtree(data, ignore_errors=True)
                obj.setText(None)
                self.db_table_view.model().setData(index, None)

    # Обработчик сигнала, срабатывающий
    # при изменении состояния галочки
    # в столбце 'Выбор'
    def dbCheckStateChanged(self, index, a0):
        self.value = self.db_scroll_bar.value()
        self.db_table_view.model().setData(index, a0)
        self.db_scroll_bar.setValue(self.value)

    # Обработчик сигнала, срабатывающий
    # при нажатии на кнопку в таблице
    # 'Выбрать все'
    def dbSelAllRowsClicked(self):
        if self.str_filter is not None:
            s = self.str_filter.replace('(choice = 2 or choice = 0) and ', '')
            s = s.replace('(choice = 2) and ', '')
            s = s.replace('(choice = 0) and ', '')
            list = self.data_base.selectIdWhere(0, s)
            if len(list) > 0:
                self.data_base.updateChoiceWhere(2, s)
            elif len(list) == 0:
                self.data_base.updateChoiceWhere(0, s)
            # print(self.str_filter)
            self.db_sql_table_model.select()
            while self.db_sql_table_model.canFetchMore():
                self.db_sql_table_model.fetchMore()
            # self.db_sql_table_model.setFilter(s)
            self.dbResizeFields(self.db_scroll_bar.value())
            self.dbCreateWidgetsInTable(self.db_scroll_bar.value())


    # Обработчик сигнала, срабатывающий
    # при нажатии на пункт меню 'Правка'
    def dbCorTriggered(self):
        self.db_act_cor.setEnabled(False)
        self.db_act_basic.setEnabled(True)
        self.db_tool_bar_cor.show()
        self.db_tool_bar_basic.setVisible(False)

    # Обработчик сигнала, срабатывающий
    # при нажатии на пункт меню 'Основное'
    def dbBasicTriggered(self):
        self.db_act_basic.setEnabled(False)
        self.db_act_cor.setEnabled(True)
        self.db_tool_bar_basic.show()
        self.db_tool_bar_cor.setVisible(False)

    # Обработчик сигнала, срабатывающий
    # при нажатии на пункт панели инструментов
    # 'Включить/Отключить редактирование'
    def dbRedTriggered(self):
        if(self.db_act_red.text() == 'Включить редактирование'):
            self.dbChangeRedState('Отключить редактирование')
        elif(self.db_act_red.text() == 'Отключить редактирование'):
            self.dbChangeRedState('Включить редактирование')

    # Включает/выключает редактирование таблицы
    def dbChangeRedState(self, text):
        if text == 'Отключить редактирование':
            state = True
            self.db_table_view.setEditTriggers(QtWidgets.QTableView.AnyKeyPressed |
                                               QtWidgets.QTableView.SelectedClicked |
                                               QtWidgets.QTableView.DoubleClicked)
        elif text == 'Включить редактирование':
            state = False
            self.db_table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

        self.db_act_red.setText(text)
        self.db_act_red.setToolTip(f'{text} (Ctrl+R)')
        self.db_act_add.setEnabled(state)
        self.db_act_del.setEnabled(state)
        self.db_act_cut.setEnabled(state)
        self.db_act_paste.setEnabled(state)
        self.dbSetBtnsEnabled(state, self.db_scroll_bar.value(), self.db_scroll_bar.value() + 20)

    # Обработчик сигнала, срабатывающий
    # при добавлении новой строки
    def dbAddRowTriggered(self):
        # record = self.db_sql_table_model.record()
        # record.setValue('choice', 0)
        # record.setValue('id', int(self.data_base.selectMaxId() + 1))
        # record.setValue('name', "")
        # record.setValue('source', "")
        # record.setValue('country', "")
        # record.setValue('carrier', "")
        # record.setValue('type', "")
        # record.setValue('carry_freq', "")
        # record.setValue('period_mks', "")
        # record.setValue('width_mks', "")
        # record.setValue('rotate_period_sec', "")
        # record.setValue('description_of_the_object', "")
        # record.setValue('description_of_the_source', "")
        # record.setValue('signals', "")
        # self.db_sql_table_model.insertRecord(-1, record)
        self.data_base.insertRow()
        columns = ['Источник', 'Страна', 'Носитель', 'Тип', 'Частоты, мГц']
        for column in columns:
            self.dbUpdateTriState(column)
        self.dbCreateStrFilter()

        self.db_sql_table_model.submitAll()
        self.db_sql_table_model.select()
        while self.db_sql_table_model.canFetchMore():
            self.db_sql_table_model.fetchMore()
        self.dbScrollValueChanged(self.db_scroll_bar.value())

        # self.db_sql_table_model.select()
        # while self.db_sql_table_model.canFetchMore():
        #     self.db_sql_table_model.fetchMore()
        #
        # self.dbCreateWidgetsInTable(self.db_scroll_bar.value())
        # self.dbResizeFields(self.db_scroll_bar.value())

    # Обработчик сигнала, срабатывающий
    # при удалении строк
    def dbDelRowsTriggered(self):
        data = self.data_base.selectChoices(2)
        if len(data) == 0:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                            'Информация',
                                            'Выберите строки.',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question,
                                            'Удалить строки',
                                            'Вы уверены, что хотите удалить выбранные строки?'
                                            ' Удаление невозможно будет отменить.',
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msg_box.exec()
            if msg_box.result() == QtWidgets.QMessageBox.Yes:
                self.data_base.deleteChoices(2)
                columns = ['Источник', 'Страна', 'Носитель', 'Тип', 'Частоты, мГц']
                for column in columns:
                    self.dbUpdateTriState(column)
                self.dbCreateStrFilter()
                # q = self.db_scroll_bar.value()
                # print(q)
                self.db_sql_table_model.submitAll()
                self.db_sql_table_model.select()
                while self.db_sql_table_model.canFetchMore():
                    self.db_sql_table_model.fetchMore()
                self.dbScrollValueChanged(self.db_scroll_bar.value())
                # print(q)
                # self.db_scroll_bar.setValue(q)
                # self.dbCreateWidgetsInTable(self.db_scroll_bar.value())

    # Обработчик сигнала, срабатывающий
    # при вырезании данных из ячеек
    def dbCutTriggered(self):
        indexes = self.db_table_view.selectionModel().selectedIndexes()
        if indexes:
            for index in range(len(indexes)):
                self.db_table_view.model().setData(indexes[index], '')

    # Обработчик сигнала, срабатывающий
    # при копировании данных из ячеек
    def dbCopyTriggered(self):
        indexes = self.db_table_view.selectionModel().selectedIndexes()
        if indexes:
            text = [str(self.db_table_view.model().data(index)) for index in indexes]
            separator = '\t'
            text = separator.join(text)
            QtWidgets.QApplication.clipboard().setText(text)

    # Обработчик сигнала, срабатывающий
    # при вставке данных в ячейки
    def dbPasteTriggered(self):
        text = QtWidgets.QApplication.clipboard().text()
        indexes = self.db_table_view.selectionModel().selectedIndexes()
        if text and indexes:
            text = text.split('\t')
            for index in range(len(indexes)):
                if(len(text) - 1 >= index):
                    self.db_table_view.model().setData(indexes[index], text[index], QtCore.Qt.EditRole)
                    # self.dbTableView.model().submit()
                else:
                    break

    # Обработчик сигнала, срабатывающий
    # при нажатии на 'Фильтр' в панели инструментов
    def dbFilterTriggered(self):
        if(self.db_widget_filter.isHidden()):
            self.db_act_filter.setText('Убрать фильтр')
            self.db_act_filter.setToolTip('Убрать фильтр')
            self.db_widget_filter.show()
        elif(self.db_widget_filter.isHidden() == False):
            self.db_act_filter.setText('Отобразить фильтр')
            self.db_act_filter.setToolTip('Отобразить фильтр')
            self.db_widget_filter.hide()

    # Обработчик сигнала, срабатывающий
    # при нажатии на 'Создать набор' в панели инструментов
    def dbCrtSetTriggered(self):
        data = self.data_base.selectChoices(2)
        if len(data) == 0:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                           'Информация',
                                           'Выберите строки.',
                                           QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            id_list = []
            for obj in data:
                if (obj.name == '' or obj.country == '' or obj.type == '' or obj.carry_freq_set == ''
                        or obj.period_mks_set == '' or obj.width_mks_set == '' or obj.rotate_period_sec_set == ''):
                    id_list.append(obj.id)

            if len(id_list) != 0:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                'Информация',
                                                'Для создания набора поля: "Название", "Страна", "Тип", "Частоты, мГц (для набора)", '
                                                '"Период следования импульсов, мкс (для набора)", "Длительность импульсов, мкс (для набора)", '
                                                '"Период следования серии импульсов (для набора)" являются обязательлными для заполнения.\n\n'
                                                f'Строки с данными id имеют незаполненные поля: {str(id_list).strip("[]")}.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
            else:
                data_country = self.data_base.selectGroupValues('country', 2)
                data_type = self.data_base.selectGroupValues('type', 2)
                data_date = time.strftime('%d.%m.%Y')
                dialog = DialogCreate(data, data_country, data_type, data_date)
                dialog.exec()

    # Обработчик сигнала, срабатывающий
    # при нажатии на 'Выбранных строк' в пункте 'Экспорт'
    def dbExpSelTriggered(self):
        list = self.data_base.selectChoices(2)
        if len(list) != 0:
            file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         caption='Выберите каталог',
                                                         directory=os.path.sep,
                                                         filter='Excel 2007-365 (.xlsx) (*.xlsx);;'
                                                                'Excel 97-2003 (.xls) (*.xls)')

            if file[1] != '':
                self.dbToExcel(file, list)
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                            'Информация',
                                            'Выберите строки.',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()

    # Обработчик сигнала, срабатывающий
    # при нажатии на 'Файлов' в пункте 'Экспорт'
    def dbExpFilesTriggered(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                     caption='Выберите каталог',
                                                     directory=os.path.sep,
                                                     filter='Архив ZIP (.zip) (*.zip)')
        path = 'files'
        if file[0] != '':
            with zipfile.ZipFile(file[0], 'w') as zipf:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=path)
                        zipf.write(file_path, arcname)

    # Обработчик сигнала, срабатывающий
    # при нажатии на 'Базы данных' в пункте 'Экспорт'
    def dbExpDBTriggered(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                  caption='Выберите каталог',
                                                  directory=os.path.sep,
                                                  filter='Исходный файл (.sqlite) (*.sqlite);;'
                                                         'Excel 2007-365 (.xlsx) (*.xlsx);;'
                                                         'Excel 97-2003 (.xls) (*.xls)')
        if file[1] != '':
            if file[1] == 'Исходный файл (.sqlite) (*.sqlite)':
                shutil.copy(f'rls.sqlite', f'{file[0]}')
            else:
                list = self.data_base.select_all()
                self.dbToExcel(file, list)

    # Перевод данных из БД в таблицу Excel
    def dbToExcel(self, file, list):
        data = []
        for i in range(len(list)):
            data.append([list[i].id, list[i].name, list[i].source,
                         list[i].country, list[i].carrier, list[i].type,
                         list[i].carry_freq, list[i].period_mks, list[i].width_mks, list[i].rotate_period_sec])

        column = ['id', 'Название', 'Источник', 'Страна', 'Носитель',
               'Тип', 'Частоты, мГц', 'Период следования импульсов, мкс',
               'Длительность импульсов, мкс', 'Период следования импульсов, с']
        data_frame = pandas.DataFrame(data=data, columns=column)
        data_frame = data_frame.set_index('id')
        data_frame.to_excel(file[0], freeze_panes=[1, 1])

    # Обработчик сигнала, срабатывающий
    # нажатии на 'Настройки'
    def dbStnTriggered(self):
        dialog = DialogSettings()
        dialog.exec()

    # --------------------------------------------

    set_window_main = None
    set_widget_main = None
    set_layout_main = None
    set_tool_bar = None
    set_act_add_obj = None
    set_act_del_obj = None
    set_act_dwn_set = None
    set_act_del_set = None

    set_layout_left = None
    set_line_search = None
    set_list_view = None

    set_layout_right = None
    set_table_view = None

    # Инициализация компонентов во
    # вкладке 'Наборы РЛС'
    def setInitComponents(self):
        self.set_tool_bar = QtWidgets.QToolBar()
        self.set_act_add_obj = QtWidgets.QAction('Добавить объекты')
        self.set_act_del_obj = QtWidgets.QAction('Удалить объекты')
        self.set_act_dwn_set = QtWidgets.QAction('Загрузить набор в СПО')
        self.set_act_del_set = QtWidgets.QAction('Удалить набор')

        self.set_line_search = QtWidgets.QLineEdit()
        self.set_list_view = QtWidgets.QListView()
        self.set_layout_left = QtWidgets.QVBoxLayout()

        self.set_table_view = QtWidgets.QTableView()
        self.set_layout_right = QtWidgets.QHBoxLayout()

        self.set_layout_main = QtWidgets.QHBoxLayout()
        self.set_widget_main = QtWidgets.QWidget()

        self.set_window_main = QtWidgets.QMainWindow()

    # Создание меню во вкладке 'Наборы РЛС'
    def setCreateMenu(self):
        self.set_act_add_obj.setToolTip('Добавить объекты')
        self.set_act_del_obj.setToolTip('Удалить объекты')
        self.set_act_dwn_set.setToolTip('Загузить набор в СПО')
        self.set_act_del_set.setToolTip('Удалить набор')
        self.set_act_add_obj.triggered.connect(self.setAddOBjClicked)
        self.set_act_del_obj.triggered.connect(self.setDelOBjClicked)
        self.set_act_dwn_set.triggered.connect(self.setDwnSetClicked)
        self.set_act_del_set.triggered.connect(self.setDelSetClicked)
        self.set_tool_bar.setMovable(False)
        self.set_tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.set_tool_bar.toggleViewAction().setVisible(False)
        self.set_tool_bar.addAction(self.set_act_add_obj)
        self.set_tool_bar.addAction(self.set_act_del_obj)
        self.set_tool_bar.addSeparator()
        self.set_tool_bar.addAction(self.set_act_dwn_set)
        self.set_tool_bar.addAction(self.set_act_del_set)
        self.set_window_main.addToolBar(self.set_tool_bar)

    # Создание окна во вкладке 'Наборы РЛС'
    def setCreateWindow(self):
        self.set_line_search.setClearButtonEnabled(True)
        self.set_line_search.setPlaceholderText('Поиск набора')
        self.set_line_search.textChanged.connect(self.setCreateModel)
        self.set_layout_left.addWidget(QtWidgets.QLabel('Каталог наборов'), stretch=0,
                                       alignment=QtCore.Qt.AlignHCenter)
        self.set_layout_left.addWidget(self.set_line_search, stretch=0)
        self.set_layout_left.addWidget(self.set_list_view, stretch=1)
        self.set_layout_left.setContentsMargins(0, 0, 0, 0)

        self.set_layout_right.addWidget(self.set_table_view)

        self.set_layout_main.addLayout(self.set_layout_left, stretch=1)
        self.set_layout_main.addLayout(self.set_layout_right, stretch=5)
        self.set_layout_main.setContentsMargins(6, 6, 6, 6)
        self.set_widget_main.setLayout(self.set_layout_main)
        self.set_window_main.setCentralWidget(self.set_widget_main)

        self.set_list_view.setSpacing(1)
        self.set_list_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.set_list_view.setWordWrap(True)
        self.set_list_view.clicked.connect(self.setSelItemClicked)

        for obj in self.set_table_view.children():
            if type(obj) is QtWidgets.QAbstractButton:
                obj.clicked.connect(self.setSelAllClicked)
                obj.setToolTip('Выбрать все')
                break

    # Создание модели для отображения
    # каталога созданных наборов
    def setCreateModel(self):
        line = self.set_line_search.text()
        try:
            json_helper = JsonHelper()
            files = os.listdir(json_helper.settings['path_rtr_model'] + json_helper.paths['path_rls_parameters'])
            model = QtGui.QStandardItemModel()
            for obj in files:
                if (obj != 'debug_config.json' and obj != 'config.json' and obj != 'rcvr_parameters.json'
                        and obj != 'rls_parameters.json'):
                    if line != '':
                        if obj.lower().find(line.lower()) != -1:
                            model.appendRow(QtGui.QStandardItem(obj))
                    else:
                        model.appendRow(QtGui.QStandardItem(obj))
            model.sort(0, QtCore.Qt.AscendingOrder)
            head_item = QtGui.QStandardItem('rls_parameters.json')
            font = QtGui.QFont()
            font.setBold(True)
            head_item.setFont(font)
            head_item.setToolTip('Файл загрузки набора')
            model.insertRow(0, head_item)
            self.set_list_view.setModel(model)
        except FileNotFoundError:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                            'Ошибка',
                                            'Не удалось найти каталог с наборами. '
                                            'Возможно неправильно указан путь в настройках.',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()

    # Создание галочек в таблице для чтения наборов
    def setCreateCheckBoxes(self):
        for row in range(self.set_table_view.model().rowCount()):
            checkBox = QtWidgets.QCheckBox()
            layout = QtWidgets.QHBoxLayout()
            widget = QtWidgets.QWidget()
            layout.addWidget(checkBox, alignment=QtCore.Qt.AlignCenter)
            widget.setLayout(layout)
            widget.setAutoFillBackground(True)
            index = self.set_table_view.model().index(row, 0)
            self.set_table_view.setIndexWidget(index, widget)

    # Обработчик сигнала, срабатывающий
    # при нажатии на кнопку в таблице
    # 'Выбрать все'
    def setSelAllClicked(self):
        flag = False

        for row in range(self.set_table_view.model().rowCount()):
            index = self.set_table_view.model().index(row, 0)
            for obj in self.set_table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox:
                    if obj.checkState() == 0:
                        flag = True

        for row in range(self.set_table_view.model().rowCount()):
            index = self.set_table_view.model().index(row, 0)
            for obj in self.set_table_view.indexWidget(index).children():
                if type(obj) is QtWidgets.QCheckBox:
                    obj.setChecked(2 if flag else 0)

        self.dbResizeFields(self.db_scroll_bar.value())

    # Обработчик сигнала, срабатывающий
    # при выборе набора в каталоге наборов
    def setSelItemClicked(self, index):
        try:
            name = self.set_list_view.model().data(index)
            json_helper = JsonHelper()
            list = json_helper.getDataFromSelItem(name)
            model = QtGui.QStandardItemModel()
            for obj in list:
                obj['carry_freq'] = [i / math.pow(10, 6) for i in obj['carry_freq']]
                model.appendRow([QtGui.QStandardItem(),
                                 QtGui.QStandardItem(obj['name'] if 'name' in obj else ''),
                                 QtGui.QStandardItem(obj['country'] if 'country' in obj else ''),
                                 QtGui.QStandardItem(obj['type'] if 'country' in obj else ''),
                                 QtGui.QStandardItem(str(obj['carry_freq']).strip('[]') if 'carry_freq' in obj else ''),
                                 QtGui.QStandardItem(str(obj['period_mks']).strip('[]') if 'period_mks' in obj else ''),
                                 QtGui.QStandardItem(str(obj['width_mks']).strip('[]') if 'width_mks' in obj else ''),
                                 QtGui.QStandardItem(str(obj['rotate_period_sec']).strip('[]') if 'rotate_period_sec' in obj else '')
                                 ])
            model.setHorizontalHeaderLabels(['Выбор', 'Название\n(name)', 'Страна\n(country)', 'Тип\n(type)', 'Частоты, мГц\n(carry_freq)',
                                             'Периоды следования импульсов, мкс\n(period_mks)', 'Длительность импульсов, мкс\n(width_mks)',
                                             'Период следования серии импульсов, с\n(rotate_period_sec)'])

            for row in range(model.rowCount()):
                for col in range(model.columnCount()):
                    model.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)

            font = QtGui.QFont()
            font.setBold(True)
            self.set_table_view.horizontalHeader().setFont(font)
            self.set_table_view.setSortingEnabled(True)
            self.set_table_view.sortByColumn(1, QtCore.Qt.AscendingOrder)
            self.set_table_view.setWordWrap(True)
            self.set_table_view.setTextElideMode(QtCore.Qt.ElideRight)
            self.set_table_view.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)

            self.set_table_view.setModel(model)
            self.setCreateCheckBoxes()

            self.set_table_view.resizeColumnsToContents()
            self.set_table_view.setColumnWidth(4, 320)
            self.set_table_view.setColumnWidth(5, 320)
            self.set_table_view.setColumnWidth(6, 320)
            for row in range(self.set_table_view.model().rowCount()):
                self.set_table_view.setRowHeight(row, 52)

        except (KeyError, TypeError, json.decoder.JSONDecodeError, UnicodeDecodeError):
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                'Ошибка',
                                                'Выбранный файл имеет неккоректную структуру.',
                                                QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        except FileNotFoundError:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                            'Ошибка',
                                            'Выбранный файл не найден, возможно он удален.',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()
            self.setCreateModel()

    # Обработчик сигнала, срабатывающий
    # при добавлении объекта в выбранный набор
    def setAddOBjClicked(self):
        data = self.set_list_view.currentIndex().data()
        if data is None:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                            'Информация',
                                            'Выберите набор.',
                                            QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            name = self.set_list_view.currentIndex().data()
            dialog = DialogAdd(name, self.db_table_view.model())
            dialog.exec()
            if dialog.result() == -1:
                self.setCreateModel()
                self.set_table_view.setModel(QtGui.QStandardItemModel())
            else:
                self.setSelItemClicked(self.set_list_view.currentIndex())

    # Обработчик сигнала, срабатывающий
    # при удалении объекта из выбранного набора
    def setDelOBjClicked(self):
        data = self.set_list_view.currentIndex().data()
        if data is None:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                           'Информация',
                                           'Выберите набор.',
                                           QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            json_helper = JsonHelper()
            list = []
            try:
                for row in range(self.set_table_view.model().rowCount()):
                    index = self.set_table_view.model().index(row, 0)
                    for obj in self.set_table_view.indexWidget(index).children():
                        if type(obj) is QtWidgets.QCheckBox and obj.checkState() == 0:
                                list.append(json_helper.getObj(data, self.set_table_view.model().data(self.set_table_view.model().index(row, 1))))
            except FileNotFoundError:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                'Ошибка',
                                                'Ошибка при удалении объектов. '
                                                'Возможно выбранный файл удален.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
                self.setCreateModel()
                self.set_table_view.setModel(QtGui.QStandardItemModel())
            else:
                if len(list) == self.set_table_view.model().rowCount():
                    msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                    'Информация',
                                                    'Выберите объекты.',
                                                    QtWidgets.QMessageBox.Ok)
                    msg_box.exec()
                else:
                    msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question,
                                                    'Удалить объекты',
                                                    'Вы уверены, что хотите удалить выбранные объекты? '
                                                    'Удаление невозможно будет отменить.',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    msg_box.exec()
                    if msg_box.result() == QtWidgets.QMessageBox.Yes:
                        json_helper.updateSet(data, list)
                        self.setSelItemClicked(self.set_list_view.currentIndex())

    # Обработчик сигнала, срабатывающий
    # при загрузке набора в СПО инструктора
    def setDwnSetClicked(self):
        set_name = self.set_list_view.currentIndex().data()
        if set_name is None:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                           'Информация',
                                           'Выберите набор.',
                                           QtWidgets.QMessageBox.Ok)
            msg_box.exec()
        else:
            try:
                json_helper = JsonHelper()
                json_helper.dwnSet(set_name)
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                'Информация',
                                                'Набор успешно загружен.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
            except OSError:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                'Ошибка',
                                                'Ошибка при загрузке набора. '
                                                'Вы пытаетесь загрузить содержимое файла '
                                                'в этот же файл, либо файл удален.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
                self.setCreateModel()

    # Обработчик сигнала, срабатывающий
    # при удалении набора из каталога наборов
    def setDelSetClicked(self):
        data = self.set_list_view.currentIndex().data()
        if data is not None:
            if data == 'rls_parameters.json':
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                                'Информация',
                                                'Файл загрузки нельзя удалять.',
                                                QtWidgets.QMessageBox.Ok)
                msg_box.exec()
            else:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question,
                                                'Удалить набор',
                                                'Вы уверены, что хотите удалить выбранный набор? '
                                                'Удаление невозможно будет отменить.',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                msg_box.exec()
                if msg_box.result() == QtWidgets.QMessageBox.Yes:
                    try:
                        json_helper = JsonHelper()
                        path = (json_helper.settings['path_rtr_model'] + json_helper.paths['path_rls_parameters'] +
                                os.path.sep + data)
                        os.remove(path)
                        self.set_table_view.setModel(QtGui.QStandardItemModel())
                    except FileNotFoundError:
                        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                                        'Ошибка',
                                                        'Выбранный файл не найден, возможно он удален.',
                                                        QtWidgets.QMessageBox.Ok)
                        msg_box.exec()
                    finally:
                        self.setCreateModel()
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                           'Информация',
                                           'Выберите набор.',
                                           QtWidgets.QMessageBox.Ok)
            msg_box.exec()

    # --------------------------------------------

    # Инициализация компонентов в двух вкладках
    def initComponents(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()
        self.dbInitComponents()
        self.setInitComponents()

    # Создание панели с двумя вкладками
    def createTabWidget(self):
        self.tab_widget.addTab(self.db_window_main, 'База данных РЛС')
        self.tab_widget.addTab(self.set_window_main, 'Наборы РЛС')
        self.tab_widget.setCurrentIndex(0)

        self.tab_widget.widget(0).addAction(self.db_act_red)
        self.tab_widget.widget(0).addAction(self.db_act_add)
        self.tab_widget.widget(0).addAction(self.db_act_del)
        self.tab_widget.widget(0).addAction(self.db_act_cut)
        self.tab_widget.widget(0).addAction(self.db_act_copy)
        self.tab_widget.widget(0).addAction(self.db_act_paste)

        self.tab_widget.widget(1).addAction(self.set_act_add_obj)
        self.tab_widget.widget(1).addAction(self.set_act_del_obj)
        self.tab_widget.widget(1).addAction(self.set_act_dwn_set)
        self.tab_widget.widget(1).addAction(self.set_act_del_set)

        self.tab_widget.currentChanged.connect(self.tabWidgetChanged)

        self.main_layout.addWidget(self.tab_widget)


    # Обработчик сигнала, срабатывающий
    # при выборе вкладки в панели вкладок
    def tabWidgetChanged(self, index):
        if index == 1:
            self.setCreateModel()
            self.set_table_view.setModel(QtGui.QStandardItemModel())

    def __init__(self):
        super().__init__()

        self.initComponents()
        self.createTabWidget()

        self.dbCreateMenu()
        self.dbCreateWindow()
        self.dbCreateFilter()
        self.dbCreateModel()
        self.dbCreateTable()

        self.setCreateMenu()
        self.setCreateWindow()
        self.setWindowTitle('База данных РЛС')
        self.resize(1500, 900)
        self.setCentralWidget(self.tab_widget)