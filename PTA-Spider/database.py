# 此模块实现从数据库导出数据

import pymysql

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='pta_data')
cursor = db.cursor()
cursor.execute('SELECT * FROM problems')
results = cursor.fetchall()
for row in results:
    label = row[0]
    title = row[1]
    content = row[2]