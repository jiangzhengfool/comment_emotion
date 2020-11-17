# 获取店名
# 获取评论
# 存储评论
# 分析评论
# 预测感情
import re
import random

import requests
import time
import util
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
cookie = "ua=fool1211; ctu=f89a43267420426f0e7dab9e686f7e105b9134f7a48eb311223f5e8164aa7cbd; " \
             "_lxsdk_cuid=175b02d2c8e9a-0d32aefe311c65-584b2f11-100200-175b02d2c8fc8; " \
             "_lxsdk=175b02d2c8e9a-0d32aefe311c65-584b2f11-100200-175b02d2c8fc8; " \
             "_hc.v=8e0f266e-1ac5-1ce9-03b8-266554eb4474.1604978553; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1604978483," \
             "1605494210; ll=7fd06e815b796be3df069dec7836c3df; thirdtoken=13e53740-9c0e-47f2-8c50-1244a6ec7b45; " \
             "dper=ed3b143a9ece09b056f1f7ccbf4efa547c171b8d8eb74e861e7d5a85168cdf76401bad6af62c8f05677bccfa308500a7252b04f176f83fe227aaf177a7c42e14a89c7bf78262b263a7defa6b5399ef0ece03fb4a4f179b7ce10e2a4df0b6d178; ctu=b1c8d9b3fccde903ddc3565987456f2054f6842e44fc9c719994a78a715fb83c2c0f2128868912768ee636cc39358c26; dplet=19815fefe38157e9be25c850c07084d8; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1605580266; _lxsdk_s=175d4088dd0-8c9-73f-937%7C%7C197 "

headers = {
        'User-Agent': ua.random,  # 修改请求头
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/shop/521698/review_all/p6'
    }


def get_shop():
    url = 'http://www.dianping.com/chengdu/ch10/g110o3p1'
    infoList = []  # 用于存储提取后的信息，列表的每一项都是一个字典
    res = requests.get(url, headers=headers, timeout=5)
    if not res.status_code == 200:
        return False
    soup = BeautifulSoup(res.text, "html.parser")
    for item in soup('div', 'tit'):
        links = item.find_all('a', attrs={'href': True})
        url = links[0]['href']
        shopID = url.split('/')[-1]

        shopname= item.find('h4').text.replace('[()]','')
        infoList.append((shopID,shopname))
    print(infoList)

    return infoList


def getHTMLText(url, code="utf-8"):
    try:
        time.sleep(random.random() * 6 + 2)
        r = requests.get(url, timeout=5, headers=headers)
        #                       proxies=get_random_ip()

        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("产生异常")
        return "产生异常"


# 因为评论中带有emoji表情，是4个字符长度的，mysql数据库不支持4个字符长度，因此要进行过滤
def remove_emoji(text):
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'', text)


# 从html中提起所需字段信息
def parsePage(html, shopID,shopname):
    infoList = []  # 用于存储提取后的信息，列表的每一项都是一个字典
    soup = BeautifulSoup(html, "html.parser")

    for item in soup('div', 'main-review'):
        cus_id = item.find('a', 'name').text.strip()
        comment_time = item.find('span', 'time').text.strip()
        try:
            comment_star = item.find('span', re.compile('sml-rank-stars')).get('class')[1]
        except:
            comment_star = 'NAN'
        cus_comment = item.find('div', "review-words").text.strip()
        scores = str(item.find('span', 'score'))
        try:
            kouwei = re.findall(r'口味：([\u4e00-\u9fa5]*)', scores)[0]
            huanjing = re.findall(r'环境：([\u4e00-\u9fa5]*)', scores)[0]
            fuwu = re.findall(r'服务：([\u4e00-\u9fa5]*)', scores)[0]
        except:
            kouwei = huanjing = fuwu = '无'

        infoList.append({'cus_id': cus_id,
                         'comment_time': comment_time,
                         'comment_star': comment_star,
                         'cus_comment': remove_emoji(cus_comment),
                         'kouwei': kouwei,
                         'huanjing': huanjing,
                         'fuwu': fuwu,
                         'shopID': shopID,
                         'shopname':shopname})

    return infoList


def get_detail(shopID='l4k6FPkNSo8IQyF7',shopname='海底捞火锅'):
    shop_url = "http://www.dianping.com/shop/" + shopID + "/review_all/"
    for i in range(1, 2):
            url = shop_url + 'p' + str(i)
            print(url)
            html = getHTMLText(url)
            infoList = parsePage(html,shopID,shopname)
            for info in infoList:
                util.save_data(info)
            print('成功爬取第{}页数据,有评论{}条'.format(i,len(infoList)))


if __name__ == '__main__':
    get_detail()