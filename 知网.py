# _*_coding UTF-8_*_
# @Author : Melnis
# @Time : 2024/10/24 20:46
# @File : 知网
# @Project : PycharmProjects


from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd

def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)

if __name__ == '__main__':
    # 配置无头浏览器参数
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("disbale-gpu")
    # 将参数加入实例
    web = Chrome(options=opt)
    web.implicitly_wait(10)
    web.get('https://search.cnki.com.cn/Search/Result')
    web.find_element(by=By.XPATH, value='//*[@id="textSearchKey"]').send_keys("机器学习", Keys.ENTER)
    web.switch_to.window((web.window_handles[-1]))
    time.sleep(1)
    titles = []
    descriptions = []
    authors = []
    publishtimes = []
    levels = []
    tags = []
    download_l = []
    quoted_l = []
    for _ in range(10):
        print(f"scraping data from page {_}")
        random_sleep()
        for i in range(1,21):
            try:
                title = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[1]/a[1]').text
                # //*[@id="article_result"]/div/div[1]/p[1]/a[1]
                print(title)
            except:
                title = ' '
            try:
                description = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[2]').text
                print(description)
            except:
                description = ' '
            try:
                author = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[3]/span[1]/.').text
                # //*[@id="article_result"]/div/div[2]/p[3]/span[1]/a[2]
                print(author)
            except:
                author = ' '
            try:
                source = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[3]/a[1]/span | //*[@id="anticle-result"]/div/div[{i}]/p[3]/span[2]').text
                # //*[@id="article_result"]/div/div[18]/p[3]/span[2]
                # //*[@id="article_result"]/div/div[1]/p[3]/a[1]/span
                print(source)
            except:
                source = ' '
            try:
                publishtime = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[3]/a[2]/span | //*[@id="article_result"]/div/div[{i}]/p[3]/span[3]').text
                # //*[@id="article_result"]/div/div[5]/p[3]/span[3]
                # //*[@id="article_result"]/div/div[1]/p[3]/a[2]/span
                print(publishtime)
            except:
                publishtime = ' '
            try:
                level = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/p[3]/span[2]').text
                print(level)
            except:
                level = ' '
            try:
                tag = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/div[1]/p[1]/.').text
                print(tag)
            except:
                tag = ' '
            try:
                download = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/div[1]/p[2]/span[1]').text
                print(download)
            except:
                download = ' '
            try:
                quoted = web.find_element(by=By.XPATH, value=f'//*[@id="article_result"]/div/div[{i}]/div[1]/p[2]/span[2]').text
                print(quoted)
            except:
                quoted = ' '
            titles.append(title)
            descriptions.append(description)
            authors.append(author)
            publishtimes.append(publishtime)
            levels.append(level)
            tags.append(tag)
            download_l.append(download)
            quoted_l.append(quoted)
            print(f"{len(titles)} articles have been scrapied")
        web.find_element(by=By.XPATH, value='//*[@id="PageContent"]/div/div[1]/div[13]/a[11]').click()
        web.switch_to.window((web.window_handles[-1]))
    print(titles)
    data = {
        "文献标题": titles,
        "简介": descriptions,
        "作者": authors,
        "发布时间": publishtimes,
        "文献类型": levels,
        "标签": tags,
        "下载数": download_l,
        "引用数": quoted_l
    }
    df = pd.DataFrame(data)
    df.to_csv('zhiwang.csv', index=False, encoding='utf-8')