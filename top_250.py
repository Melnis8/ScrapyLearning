# _*_coding UTF-8_*_
# @Author : Melnis
# @Time : 2024/10/12 20:19
# @File : top_250
# @Project : pythonProject

import requests
import openpyxl
import pymysql
from bs4 import BeautifulSoup
from lxml import etree
import time
import random
import re
import pandas as pd
import csv

conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        charset='utf8mb4'
    )

cursor = conn.cursor()

# 随机休眠
# 调高mu的值可以降低中道崩殂的概率...

def random_sleep(mu=2, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


# 从网页爬数据
def get_data(url):
    session = requests.session()
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }
    proxies = {
        "http": "39.105.27.30:3128"
    }
    response = requests.get(url, headers=headers)
    random_sleep()
    return response

def get_sec_page(resp1):
    # 获取二级页面链接
    pattern = re.compile(r'<a[^>]+href=["\'](https.{3}movie.douban.com.subject.*?)["\'].class')
    url = re.findall(pattern, resp1.text)
    titles = []
    directors = []
    actors = []
    types = []
    dates = []
    runtimes = []
    rates = []
    rateNums = []
    for l in url:
        resp2 = get_data(l)
        time.sleep(1)
        tree = etree.HTML(resp2.text)
        title = tree.xpath('//*[@id="content"]/h1/span[1]/text()')
        titles.append(title)
        director = tree.xpath('//*[@id="info"]/span[2]/span[2]//a/text()')
        directors.append(director)
        actor = tree.xpath('//*[@id="info"]/span[3]/span[2]//a/text()')
        actors.append(actor)
        type = tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
        types.append(type)
        # area = tree.xpath('//*[@id="info"]/text()[2]') bs4
        # areas.append(area)
        date = tree.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        dates.append(date)
        runtime = tree.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()')  # 有机会试试bs4
        runtimes.append(runtime)
        rate = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        rates.append(rate)
        rateNum = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
        rateNums.append(rateNum)

    # 写入表格
    data = {
        '电影名称': titles,
        '导演': directors,
        '主演': actors,
        '类型': types,
        '发布日期':dates,
        '时长': runtimes,
        '评分': rates,
        '评价人数': rateNums,
    }
    print(data)
    df = pd.DataFrame(data)
    df.to_csv('top_250.csv', index=False, encoding='utf-8')

    with open('top_250.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO information ({', '.join(headers)}) VALUES ({placeholders})"

        for row in csv_reader:
            cursor.execute(insert_query, row)

    conn.commit()

    # cursor.close()
    # conn.close()

def database_create():
    cursor.execute('CREATE DATABASE IF NOT EXISTS Douban CHARSET=utf8;')
    cursor.execute('USE Douban')
    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS information (  
            movie_id INT(8) AUTO_INCREMENT PRIMARY KEY,  
            电影名称 VARCHAR(1024) NOT NULL,  
            导演 TEXT,  
            主演 TEXT,
            类型 VARCHAR(255),
            发布日期 VARCHAR(255),
            时长 VARCHAR(255),
            评分 VARCHAR(255),
            评价人数 VARCHAR(255)
        );  
        """)

    conn.commit()


if __name__ == '__main__':
    database_create()
    for page in range(10):
        url1 = r'https://movie.douban.com/top250?start={}&filter='.format(page*25)
        resp1 = get_data(url1)
        get_sec_page(resp1)


