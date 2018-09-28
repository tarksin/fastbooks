import pymysql.cursors
import pymysql

def check_username_exists(username):

    connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
                                db='fastbooks', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
                # sql = "SELECT EXISTS (SELECT 1 FROM users WHERE  username='{}')".format(username)
            sql = "SELECT username FROM users WHERE  username='{}'".format(username)
            cursor.execute(sql)
            result = cursor.fetchone()
                #
                # if result:
                #     return True#   result["username"]
                # else:
                #     return False
            return {'a':2, 'b':55}
    finally:
        connection.close()
