from app import db, login
import json
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pymysql.cursors
import pymysql


class Expense():
    def __init__(self, expdate, expdesc, expamount, expcat, vendor):
        self.expdesc = expdesc
        self.expdate = expdate
        self.expamount = expamount
        self.expcat = expcat
        self.vendor = vendor

    @classmethod
    def get_expenses(cls):
        the_expenses = []
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT e.expense_id,e.expdate, e.expdesc, e.expamount, ec.expcat, e.vendor FROM expenses e join expcats ec on (e.expcat = ec.id)" # WHERE  username='{}'".format(username)
                cursor.execute(sql)

                result = cursor.fetchall()
                print('29 ', result)
        #        print('55 models.py', result)
        #        print("56 ", result['username'])
                the_expenses = result
        finally:
            print('34 models.py')
            connection.close()
        return the_expenses


    def create(self):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
# #                "INSERT INTO TABLE_A (COL_A,COL_B) VALUES (%s, %s)" % (val1, val2)
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

                sql = "INSERT INTO expenses(expdate,expdesc, expamount, expcat, vendor) values(%s,%s,%s,%s,%s)"
                cursor.execute(sql,(self.expdate, self.expdesc, self.expamount, self.expcat, self.vendor))
                connection.commit()
        finally:
            connection.close()



#---------------------class TODO ----------------------------------------------

class Todo():
    '''class representing a tasks to be finished on this project'''

    def __init__(self,todo, project_id):
        self.id = id
        self.todo = todo
        self.project_id = int(project_id)

    def create(self):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO todo( todo, project_id) values(%s,%s)"
                cursor.execute(sql,( self.todo, self.project_id))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def get_todos(cls):
        todos = []
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                #sql = "SELECT id, todo FROM todo ORDER BY id" # WHERE  username='{}'".format(username)
                sql = "select p.project as project, project_id as pid, t.todo as todo from projects p join todo t on (p.id = t.project_id) order by p.id "

                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()
        return result


#---------------------class EXPCAT ----------------------------------------------

class Expcat():
    '''class representing a category of expenses'''

    def __init__(self, id, expcat):
        self.id = id
        self.expcat = expcat

    def create(self):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO expcats(id, expcat) values(%s,%s)"
                cursor.execute(sql,(self.id, self.expcat))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def get_expcats(cls):
        expcats = []
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, expcat FROM expcats ORDER BY expcat" # WHERE  username='{}'".format(username)
                cursor.execute(sql)

                result = cursor.fetchall()
                print('87', result)
        #        print('55 models.py', result)
        #        print("56 ", result['username'])
                expcats = result
        finally:
            print('92 models.py')
            connection.close()
        return expcats


#---------------------class BANKITEM ----------------------------------------------

class BankItem():
    '''class representing a check payment or credit card charge'''

    def __init__(self, bi_date, bank_id, bi_amount, vendor):
        self.bi_date = bi_date
        self.bank_id = bank_id
        self.bi_amount = bi_amount
        self.vendor = vendor

    def create(self):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO bankitems(bi_date,bank_id, bi_amount, vendor) values(%s,%s,%s,%s)"
                cursor.execute(sql,(self.bi_date, self.bank_id, self.bi_amount,  self.vendor))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def get_bankitems(cls):
        bankitems = []
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT bankitem_id, bi_date, bi_amount, bank_id, vendor FROM bankitems" # WHERE  username='{}'".format(username)
                cursor.execute(sql)

                result = cursor.fetchall()
                print('87', result)
        #        print('55 models.py', result)
        #        print("56 ", result['username'])
                bankitems = result
        finally:
            print('92 models.py')
            connection.close()
        return bankitems


#---------------------class USER ----------------------------------------------

class User(UserMixin):
# class User(UserMixin, username, email, pwhash):
#    __tablename__='users'
#    id = db.Column(db.Integer, primary_key=True)
    def __init__():
        self.username = username #db.Column(db.String(64), index=True, unique=True)
        self.email = email#db.Column(db.String(120), index=True, unique=True)
        self.password_hash =  pwhash#db.Column(db.String(128))

#--------------------------------------------------------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

#--------------------------------------------------------------------------
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#--------------------------------------------------------------------------

    def get_self(self, id):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users where id={}".format(id)
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            connection.close()
        if result:
            return jsonify(result)
        else:
            return "No joy"

#------------------------------------------------------
#User.find_username(form.username.data)
    @classmethod
    def get_expenses(cls, username):
    # def check_user_exists(cls, username):
        YesNo = False
        the_expenses = []
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # sql = "SELECT EXISTS (SELECT 1 FROM users WHERE  username='{}')".format(username)
                sql = "SELECT expense_id,expdate, expdesc, expamount, expcat, vendor FROM expenses" # WHERE  username='{}'".format(username)
                cursor.execute(sql)

                result = cursor.fetchall()
                print('54 ', result)
        #        print('55 models.py', result)
        #        print("56 ", result['username'])
                the_expenses = result

                # if result['username'] == username:
                #         YesNo = True
                # z = jsonify(result)
                # print("58 ",z)

                # try23 = jsonify(result)
                # try23.status_code = 200 # or 400 or whatever
                # print(try23)
                # return try23

                #
                # if result:
                #     return True#   result["username"]
                # else:
                #     return False
                # return z
                # return result['username']
        finally:
            print('63 models.py')
            connection.close()
        return the_expenses
        # if result:
        #     return True
        # else:
        #     return False
# ????????? 'return result' ?

#------------------- check_email_exists----------------------------------
    @classmethod
    def check_email_exists(cls, email):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT EXISTS (SELECT 1 FROM users WHERE  email ='{}')".format(email)
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            connection.close()
        if result:
            return True
        else:
            return False

#------------------- check_password_exists----------------------------------
    @classmethod
    def check_password_exists(cls, password):
        connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT EXISTS (SELECT 1 FROM users WHERE  password ='{}')".format(password)
                cursor.execute(sql)
                result = cursor.fetchone()
        finally:
            connection.close()
        if result:
            return True
        else:
            return False


#-----------------------------------------------------
    def __repr__(self):
        return '<User {}>'.format(self.username)



@login.user_loader
def load_user(id):
    return User.get_self(int(id))
