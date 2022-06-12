import pymysql
# 1、连接数据库

con = pymysql.connect(host='api.lemonban.com',
                port=3306,
                user='future',
                password='123456',
                charset='utf8')

#  # 2、创建游标对象
with con as cur:
    sql = 'select * from futureloan.member where mobile_phone="17783427543"'
    res = cur.execute(sql)
print(res)

# 查询结果
# fetchall:获取查询集中所有的内容
# res2 = cur.fetchall()
# print(res2)

# fetchone:获取查询集中的第一条数据
res2 = cur.fetchone()
print(res2)

# con.close()
# 提交事务
# con.commit()

# sql = 'select * from futureloan.member LIMIT 5'
# 2、创建游标对象与执行sql语句
# cur = con.cursor()
# res1 = cur.execute(sql)

# print(res1)


