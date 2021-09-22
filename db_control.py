# - * - coding:utf-8 - * -
import pymysql


class MysqlController(object):

    controller_count = 0

    def __init__(self, db_address, db_user, db_pwd, db_name):
        self.db_address = db_address
        self.db_user = db_user
        self.db_pwd = db_pwd
        self.db_name = db_name
        self.connection = pymysql.connect(self.db_address, self.db_user, self.db_pwd, self.db_name)
        MysqlController.controller_count += 1

    def __repr__(self):
        return f"<MysqlController Object {self.controller_count} Connections Alive>"

    def __call__(self, *args, **kwargs):
        return self

    def bye(self):
        if MysqlController.controller_count > 0:
            MysqlController.controller_count -= 1
        return self.connection.close()

    def run(self, sql, write_mode=False):
        database = self.connection
        cursor = database.cursor()
        try:
            cursor.execute(sql)
            database.commit()
            row_effected = cursor.rowcount
            if write_mode is False:
                results = cursor.fetchall()
                cursor.close()
                return dict(result=results, row_effected=row_effected)
            else:
                cursor.close()
                return dict(result=None, row_effected=row_effected)

        except Exception as e:
            database.rollback()
            return e


if __name__ in "__main__":
    con = MysqlController(db_address='localhost', db_user='root', db_pwd='jc17462315', db_name='message')
    msg = con.run("select * from wxmsg")
    print(con, msg)
    pass
