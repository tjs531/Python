import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='webtoon_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("DB접속성공!")

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `w_no`,`w_title` FROM `t_webtoon` WHERE `w_no`=%c"
        cursor.execute(sql, (1))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()

