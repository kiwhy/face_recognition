import pymysql
import datetime

log_db = pymysql.connect(
    user='root',
    password='test',
    host='127.0.0.1',
    database='eventlog',
    charset='utf8'
)

cursor = log_db.cursor(pymysql.cursors.DictCursor)
sql = "insert into eventlogtbl (log) values (%s)"
val = datetime.datetime.now().strftime("%y년%m월%d일%H시%M분%S초")
cursor.execute(sql,val)
log_db.commit()