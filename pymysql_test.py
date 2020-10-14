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
        sql = "SELECT `w_no`,`w_title` FROM `t_webtoon` WHERE `w_no` in (%c,%c,%c)"
        #sql = "SELECT * FROM `t_user`"
        data = (1,2,3)
        cursor.execute(sql,data)
        result = cursor.fetchall()
        for r in result:
            print(r)
finally:
    connection.close()

