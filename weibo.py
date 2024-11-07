# _*_coding UTF-8_*_
# @Author : Melnis
# @Time : 2024/11/1 21:17
# @File : weibo
# @Project : PycharmProjects

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd

opt = Options()
opt.add_argument("--headless")
opt.add_argument("disbale-gpu")

# web = Chrome(options=opt)
web = Chrome()
web.implicitly_wait(10)
web.get('https://m.weibo.cn/search?containerid=231583')
searchkeys = ['杨利伟的太空一日', '王亚平成中国首位出舱女航天员', '天宫课堂第二课', '欢迎翟志刚王亚平叶光富回地球', '中国空间站航天员首次出舱', '神舟十七号发射圆满成功']

web.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/div[1]/div[1]/div/div/div[2]/form/input').send_keys("杨利伟的太空一日", Keys.ENTER)

web.switch_to.window(web.window_handles[-1])
i = 4

# 爬取贴文相关数据
web.find_element(by=By.XPATH, value=f'//*[@id="app"]/div[1]/div[1]/div[{i}]//div[@class="weibo-og"]/div[@class="weibo-text"]').click()
web.switch_to.window(web.window_handles[-1])
postAuthor = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//a/h3[@class="m-text-cut"]').text
print(postAuthor)
postTime = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//h4[@class="m-text-cut"]/span[@class="time"]').text
print(postTime)
postContent = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="weibo-og"]/div[@class="weibo-text"]').text
print(postContent)
postTransmit = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="m-diy-btn m-box-col m-box-center m-box-center-a"][1]').text
if postTransmit == '转发': postTransmit = 0
print(postTransmit)
postComment = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="m-diy-btn m-box-col m-box-center m-box-center-a"][2]').text
if postComment == '评论': postComment = 0
print(postComment)
postLike = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="m-diy-btn m-box-col m-box-center m-box-center-a"][3]').text
if postLike == '赞': postLike = 0
print(postLike)

# 爬取评论相关数据

if int(postComment) > 0:
    comment = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="m-text-box"]/h3').text
    print(comment)