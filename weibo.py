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
def random_sleep(mu=2, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)

opt = Options()
opt.add_argument("--headless")
opt.add_argument("disbale-gpu")

# web = Chrome(options=opt)
web = Chrome()
web.implicitly_wait(5)
searchkeys = ['杨利伟的太空一日', '王亚平成中国首位出舱女航天员', '天宫课堂第二课', '欢迎翟志刚王亚平叶光富回地球', '中国空间站航天员首次出舱', '神舟十七号发射圆满成功']

for key in searchkeys:
    web.get('https://m.weibo.cn/search?containerid=231583')
    web.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/div[1]/div[1]/div/div/div[2]/form/input').send_keys(
        key, Keys.ENTER)
    i = 3
    # 爬取贴文相关数据
    while(1):
        try:
            web.find_element(by=By.XPATH, value=f'//*[@id="app"]/div[1]/div[1]/div[{i}]//div[@class="weibo-og"]/div[@class="weibo-text"]').click()
            random_sleep()
            # /html/body/div/div[1]/div[1]/div[3]/div/div/div/article/div[2]/div[1]/text()[2]
            web.switch_to.window(web.window_handles[-1])
            print(web.current_url)
            postAuthor = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//a/h3[@class="m-text-cut"]').text
            print(postAuthor)
            postTime = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//h4[@class="m-text-cut"]/span[@class="time"]').text
            print(postTime)
            postContent = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="weibo-og"]/div[@class="weibo-text"]').text
            print(postContent)
            postTransmit = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="lite-page-tab"]/div[@class="tab-item"][1]/i[2]').text
            # /html/body/div/div[1]/div/div[2]/div/article/div/div/div[1]/text()[2]
            if postTransmit == '转发': postTransmit = 0
            print(postTransmit)
            postComment = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="lite-page-tab"]/div[@class="tab-item cur"]/i[2]').text
            if postComment == '评论': postComment = 0
            print(postComment)
            postLike = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="lite-page-tab"]/div[@class="tab-item"][2]/i[2]').text
            if postLike == '赞': postLike = 0
            print(postLike)

            # 爬取评论相关数据
            if int(postComment) > 0:
                for j in range(1, int(postComment)+1):
                    # 这个try-excpt献给夹总，小馋猫十个评论夹走五个
                    try:
                        commentAuthor = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="comment-content"]/div[{j}]//div[@class="m-box-center-a"]/h4[@class="m-text-cut"]').text
                        print(commentAuthor)
                        commentContent = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="comment-content"]/div[{j}]//div[@class="m-text-box"]/h3').text
                        print(commentContent)
                        # 评论区ip显示不稳定，考虑追踪用户id去微博主网站找Ip
                        commentTimeIP = web.find_element(by=By.XPATH,value=f'//*[@id="app"]//div[@class="comment-content"]/div[{j}]//div[@class="m-box-center-a time"]').text
                        print(commentTimeIP)
                        # 评论区跟水军似的，互动真难找啊。我还以为是微博在网页版跟我藏着掖着了，去原版域名里找了找发现这话题真没人多聊
                        # 找不到啊找不到，最后自己去发了几条
                        # 有必要写展开的代码吗，，还是写吧，万一用上了呢
                        try:
                            web.find_element(by=By.XPATH, value=f'//*[@id="app"]//div[@class="comment-content"]//div[@class="cmt-sub-txt"]').click()
                            random_sleep()
                            k = 1
                            # 不晓得有多少二级评论，先爬着，报错了就是爬完了
                            while(1):
                                try:
                                    secAuthor = web.find_element(by=By.XPATH,
                                                value=f'div[@id="app"]//div[@class="card m-avatar-box lite-page-list list-bg"][{k}]//div[@class="m-text-cut"]/h4').text
                                    print(secAuthor)
                                    secContent = web.find_element(by=By.XPATH,
                                                value=f'div[@id="app"]//div[@class="card m-avatar-box lite-page-list list-bg"][{k}]//div[@class="m-text-cut"]/h3').text
                                    print(secContent)
                                    secTime = web.find_element(by=By.XPATH,
                                                value=f'div[@id="app"]//div[@class="card m-avatar-box lite-page-list list-bg"][{k}]///div[@class="m-box-center-a time"]').text
                                    print(secTime)
                                    k += 1
                                except:
                                    web.find_element(by=By.XPATH,
                                                     value=f'//*[@id="app"]//div[@class="nav-left"]/i[@class="m-font m-font-arrow-left"]').click()
                                    break
                        except:
                            print("这里没有二级评论")

                    except:
                        print(f"夹了{int(postComment)+1-j}个")
                        break
            i += 1
            print("准备退出本贴")
            web.find_element(by=By.XPATH,
                             value=f'//*[@id="app"]//div[@class="nav-left"]/i[@class="m-font m-font-arrow-left"]').click()
            random_sleep()
        except:
            print("这个话题爬完了")
            # web.find_element(by=By.XPATH,
            #                  value=f'//*[@id="app"]//div[@class="nt-left"]/i[@class="m-font m-font-arrow-left"]').click()
            random_sleep()
            break

