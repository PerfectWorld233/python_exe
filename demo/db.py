#coding=utf-8
#导入pymysql的包
import  pymysql
import  pymysql.cursors

#获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
#port 必须是数字不能为字符串
connection=pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           db='opac',
                           port=3306,
                           charset='utf8')
try:
    #获取一个游标
   with connection.cursor() as cursor:
       #sql='create table student(id int ,name varchar(20),class varchar(30),age varchar(10))'
       sql="SELECT * FROM cpu WHERE id < 10"
       cout=cursor.execute(sql)
       for row in cursor.fetchall():
            print(row)
            exit()
       connection.commit()

finally:
    connection.close()