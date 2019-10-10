

# 逻辑顺序：第一页，解析代码和页数，送给翻页的页数，解析第二页 解析代码和页数
#
# 1.登录第一页
# 2.解析代码的
# 3.解析页数的
# 4.翻页操作的
# 或者55也而已，直接把要翻页的页码通过测算得到一个列表，后面直接遍历这个礼拜即可！
# 陷阱挺深，逐渐增加了好几次，到了一定程度停止下来，后面在逐渐下降！手动可以处理


# js小陷阱用点击下一页给破掉了！
# body > div.con > div > div.page > a.next
# 1.翻页正常，第一页解析正常
# 2.翻页过快。没有时间解析
# 3.用selenium请求，翻页，解析
# 翻页小陷阱，定位不准xpath ,css定位都会失效 ,一个思路就统计页码标签的个数，统计出和之后赋值给# //*[@id="tbl_wrap"]/div/a[7] b


# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
import pyautogui

import time
from selenium import webdriver
from lxml import etree
import datetime


import sys
sys.path.append("../") # python 怎么引入上上级目录的文件 ​​​​

from d_list import s_list

#请求

def get_first_page(url):

    driver.get(url)
    html = driver.page_source
    return html


def removeStall(i_list):
    f_list = []

    for item in i_list:
        f_i = "".join(item.split())
        f_list.append(f_i)
    return f_list

def changeTO_int(i_list):
    f_list = []

    for item in i_list:
        f_i = int(item)
        f_list.append(f_i)
    return f_list



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    dates = selector.xpath('//*[@id="flightTypeList"]/div[1]/div[4]/div/div/div[1]/input/@value')
    week = selector.xpath('//*[@id="flightTypeList"]/div[1]/div[4]/span[1]/text()')
    f_date = [dates[0]+week[0]]

    price = selector.xpath('//*[@id="base_bd"]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div/div[7]/div/span/text()')
    f_price = removeStall(price)
    fi_price =changeTO_int(f_price)
    try:

        max_price = max(fi_price)
        min_price = min(fi_price)
        f_date.append(str(max_price))
        f_date.append(str(min_price))
        f_tuple = tuple(f_date)
        big_list.append(f_tuple)

        return  big_list
    except:
        pass







#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='YC',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into xian_yinchuan (f_date,max_price,min_price) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except pymysql.err.IntegrityError :
        pass











if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    for sdate in s_list:
        pyautogui.keyDown("down")  # 按下往下

        url = 'https://flights.ctrip.com/itinerary/oneway/sia-inc?date=' + sdate
                
        html = get_first_page(url)
        time.sleep(6)
        content = parse_html(html)
        insertDB(content)
        print(content)




# 字段设置了唯一性 unique
#f_date,max_price,min_price
# create table xian_yinchuan(
# id int not null primary key auto_increment,
# f_date varchar(20),
# max_price int,
# min_price int
# ) engine=InnoDB  charset=utf8;

# drop table xian_yinchuan;



