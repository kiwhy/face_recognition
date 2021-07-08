from flask import Flask, render_template
import pymysql

app = Flask(__name__)
log_db = pymysql.connect(
    user='root',
    password='test',
    host='127.0.0.1',
    database='eventlog',
    charset='utf8'
)
cursor = log_db.cursor(pymysql.cursors.DictCursor)

sql = 'select * from eventlogtbl'
cursor.execute(sql)

data_list = cursor.fetchall()

print(data_list[0])
print(data_list[1])