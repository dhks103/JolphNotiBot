from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re

_ARTICLE_LIST = []

def check_article():
    url = 'http://cs.hanyang.ac.kr/board/gradu_board.php'
    res = requests.get(url)
    bs = BeautifulSoup(res.text, "lxml")
    td = bs.tbody.find_all('td')
    tb = bs.tbody.find_all('a')
    
    tmp_article_title = []
    tmp_article_url = []

    # 제목 리스트에 추가
    for title in tb:
        if title.text == '':
            continue
        tmp_article_title.append(title.text)

    # URL 리스트에 추가
    for url in tb:
        if url == '':
            continue
        if url.attrs['href'].split('/')[1] == 'admin':
            continue
        tmp_article_url.append('http://cs.hanyang.ac.kr' + url.attrs['href'])

    # 날짜 리스트에 추가
    # for date in td:
    #     if re.match("2[0-9]\.[0-1][0-9]\.[0-3][0-9]", date.text):
    #         tmp_article_date.append(date.text)
            
    # 처음 실행이면 전체 데이터 그대로 저장
    if _ARTICLE_LIST == []:
        _ARTICLE_LIST.append(tmp_article_title)
        _ARTICLE_LIST.append(tmp_article_url)

    # 새글 작성 확인 후, 새글 있으면 return
    diff_article = set(_ARTICLE_LIST[0]) - set(tmp_article_title)
    if diff_article != set():
        new_article = dict()
        new_article['title'] = list(set(_ARTICLE_LIST[0]) - set(tmp_article_title))
        new_article['url'] = list()
        
        for title in new_article['title']:
            idx = _ARTICLE_LIST[0].index(title)
            new_article['url'].append(_ARTICLE_LIST[1][idx])
        
        _ARTICLE_LIST[0] = tmp_article_title
        _ARTICLE_LIST[1] = tmp_article_url
        
        return new_article
    else:
        return dict()
    
    # 테스트용
    # for article in _ARTICLE_LIST:
    #     if not article: # 딕셔너리가 비었을 경우, 종료
    #         break
    #     print(article['title'], '/', article['url'], '/', article['date'])
        
        
if __name__ == "__main__":
    check_article()
# check_article()