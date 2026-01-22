from PyQt5 import QtCore, QtSql


# Переопределенная модель, связанная с БД
class MySqlTableModel(QtSql.QSqlTableModel):
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        return QtSql.QSqlTableModel.data(self, index, role)
