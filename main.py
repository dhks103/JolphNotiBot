from selenium import webdriver
from bs4 import BeautifulSoup
from notion.client import *
from notion.block import *
import requests
import re


def check_article():
    url = 'http://cs.hanyang.ac.kr/board/gradu_board.php'
    res = requests.get(url)
    bs = BeautifulSoup(res.text, "lxml")
    td = bs.tbody.find_all('td')
    tb = bs.tbody.find_all('a')

    article_list = list(dict() for i in range(0, 30))
    cnt = 0

    for title in tb:
        if title.text == '':
            continue
        article_list[cnt].update(title=title.text)
        cnt = cnt + 1
    cnt = 0
    for url in tb:
        if url == '':
            continue
        if url.attrs['href'].split('/')[1] == 'admin':
            continue
        article_list[cnt].update(url='http://cs.hanyang.ac.kr' + url.attrs['href'])
        cnt = cnt + 1
    cnt = 0
    for date in td:
        if re.match("2[0-9]\.[0-1][0-9]\.[0-3][0-9]", date.text):
            article_list[cnt].update(date=date.text)
            cnt = cnt + 1

    for article in article_list:
        print(article['title'], '/', article['url'], '/', article['date'])

check_article()

# def get_collection_schema():
