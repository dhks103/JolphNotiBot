import schedule
import time
import parsing_board
import smtplib
from email.mime.text import MIMEText

_EMAIL_ID = "dhksl103@gmail.com"
_EMAIL_PW = "qvzktcpiddydhnwm"
_DEST_EMAIL = ["dhks103@hanyang.ac.kr", "maysecond32@hanyang.ac.kr"]
# _DEST_EMAIL = ["dhks103@hanyang.ac.kr"]

def sending_mail(ctx, title):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    smtp.ehlo()
    smtp.starttls()

    # 로그인을 통한 지메일 접속
    smtp.login(_EMAIL_ID, _EMAIL_PW)
    
    msg = MIMEText(ctx, 'html')
    msg['Subject'] = ''.join(title)
    msg['From'] = '새글 알림봇'
    
    # 이메일 전송 설정
    for mail in _DEST_EMAIL:
        smtp.sendmail(_EMAIL_ID, mail, msg.as_string())
        
    smtp.quit()

def writing_mail():
    # 메일 내용 입력
    article_info = parsing_board.check_article()
    if article_info == dict():
        print(time.strftime('%Y년 %m월 %d일 현재 새글이 없습니다.', time.localtime()))
    elif len(article_info['title']) == 1:
        print(time.strftime('%Y년 %m월 %d일 현재 1개의 새글', time.localtime()))
        ctx = '<b>게시글 확인하기</b><br>' + ''.join(article_info['url'])
        sending_mail(ctx, article_info['title'])
    else:
        print(time.strftime('%Y년 %m월 %d일 현재 여러 개의 새글', time.localtime()))
        list_title = list()
        list_url = list()
        ctx = ''
        for article in article_info['title']:
            list_title.append('<b>' + article + '</b>')
        for article in article_info['url']:
            list_url.append(article)
            
        while i in range(len(list_title)):
            ctx = ctx + list_title[i] + '<br>' + list_url[i] + '<br><br>'
            
        sending_mail(ctx, list_title)
    
def main():
    schedule.every().days.at("12:00").do(writing_mail)
    # schedule.every(5).seconds.do(writing_mail)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()