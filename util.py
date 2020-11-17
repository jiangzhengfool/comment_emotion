# -*- coding: utf-8 -*-


import pymysql

#连接MYSQL数据库
db = pymysql.connect("192.168.1.101","root","123456","dianping" )
cursor = db.cursor()

#在数据库建表
def creat_table():
    print('创建表')
    cursor.execute("DROP TABLE IF EXISTS comment_info")
    sql = '''CREATE TABLE comment_info(
            cus_id varchar(100),
            comment_time varchar(55),
            comment_star varchar(55),
            cus_comment text(5000),
            kouwei varchar(55),
            huanjing varchar(55),
            fuwu varchar(55),
            shopID varchar(55),
            shop_name varchar(100)
            );'''
    cursor.execute(sql)
    return

#存储爬取到的数据
def save_data(data_dict):
    sql = '''INSERT INTO comment_info(cus_id,comment_time,comment_star,cus_comment,kouwei,huanjing,fuwu,shopID,shop_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    value_tup = (data_dict['cus_id']
                 ,data_dict['comment_time']
                 ,data_dict['comment_star']
                 ,data_dict['cus_comment']
                 ,data_dict['kouwei']
                 ,data_dict['huanjing']
                 ,data_dict['fuwu']
                 ,data_dict['shopID']
                 ,data_dict['shopname']
                 )
    print(value_tup)

    cursor.execute(sql,value_tup)
    db.commit()


#关闭数据库
def close_sql():
    db.close()

if __name__ == '__main__':
    # creat_table()
    import  re
    a= re.sub(u'[()]','','(hhh)')
    print(a)