from PyQt5 import QtSql

from rls import RLS


class DataBase:
    con = None

    def __init__(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')

    def connect(self):
        self.con.setDatabaseName('rls.sqlite')
        self.con.open()

    def createTable(self):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec('create table if not exists rls('
                   'choice integer,'
                   'id integer primary key autoincrement,'
                   'name text,'
                   'source text,'
                   'country text,'
                   'carrier text,'
                   'type text,'
                   'carry_freq text,' 
                   'carry_freq_set text,' 
                   'period_mks text,'
                   'period_mks_set text,'
                   'width_mks text,'
                   'width_mks_set text,'
                   'rotate_period_sec text,'
                   'rotate_period_sec_set text,'
                   'description_of_the_object text,'
                   'description_of_the_source text,'
                   'signals text'
                   ')')
        self.con.close()

    def selectMaxId(self):
        self.connect()
        res = 0
        query = QtSql.QSqlQuery()
        query.exec('select max(id) from rls')
        if query.isActive():
            query.first()
            while query.isValid():
                res = query.value(0)
                query.next()
                if res == '':
                    res = 0
        self.con.close()
        return res

    def selectValues(self, name):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select {name} from rls')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value(name))
                query.next()
        self.con.close()
        return lst

    def updateChoiceWhere(self, value, filter):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'update rls set choice = {value} where {filter}')
        self.con.close()

    def insertRow(self):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'insert into rls values '
                   f'(0, {int(self.selectMaxId() + 1)}, "", "", "", "", "", "", "", '
                   f'"", "", "", "", "", "", "", "", "")')
        self.con.close()

    def deleteChoices(self, value):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'delete from rls where choice = {value}')
        self.con.close()

    def selectIdWhere(self, value, filter):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select id from rls where choice = {value} and {filter}')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value(0))
                query.next()
        self.con.close()
        return lst

    def selectGroupValues(self, name, value):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select {name} from rls where choice = {value} group by {name}')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value(name))
                query.next()
        self.con.close()
        return lst

    def selectGroup(self, name):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select {name} from rls group by {name}')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(query.value(name))
                query.next()
        self.con.close()
        return lst

    def selectChoices(self, value):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select * from rls where choice = {value}')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(RLS(
                    query.value(0), query.value(1),
                    query.value(2), query.value(3),
                    query.value(4), query.value(5),
                    query.value(6), query.value(7),
                    query.value(8), query.value(9),
                    query.value(10), query.value(11),
                    query.value(12), query.value(13),
                    query.value(14), query.value(15),
                    query.value(16), query.value(17)
                )
                )
                query.next()
        self.con.close()
        return lst

    def select_all(self):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select * from rls')
        lst = []
        if query.isActive():
            query.first()
            while query.isValid():
                lst.append(RLS(
                    query.value(0), query.value(1),
                    query.value(2), query.value(3),
                    query.value(4), query.value(5),
                    query.value(6), query.value(7),
                    query.value(8), query.value(9),
                    query.value(10), query.value(11),
                    query.value(12), query.value(13),
                    query.value(14), query.value(15),
                    query.value(16), query.value(17)
                )
                )
                query.next()
        self.con.close()
        return lst

    def sel(self):
        self.connect()
        query = QtSql.QSqlQuery()
        query.exec(f'select count(id) from rls')
        lst = ''
        if query.isActive():
            query.first()
            while query.isValid():
                lst = query.value(0)
                query.next()
        self.con.close()
        return lst


if __name__ == '__main__':
    db = DataBase()
    print(db.sel())