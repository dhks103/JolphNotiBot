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
    msg['From'] = '새글 알림봇'
    
    if title == '0':
        msg['Subject'] = '오늘은 새 글이 없습니다.'
        smtp.sendmail(_EMAIL_ID, 'dhks103@hanyang.ac.kr', msg.as_string())
    else:
        # 이메일 전송 설정
        msg['Subject'] = ''.join(title)
        for mail in _DEST_EMAIL:
            smtp.sendmail(_EMAIL_ID, mail, msg.as_string())
        
    smtp.quit()

def writing_mail():
    # 메일 내용 입력
    article_info = parsing_board.check_article()
    if article_info == dict():  # 새 글이 없을 경우
        print(time.strftime('%Y년 %m월 %d일 현재 새글이 없습니다.', time.localtime()))
        sending_mail('http://cs.hanyang.ac.kr/board/gradu_board.php', '0')
    elif len(article_info['title']) == 1:   # 새글이 1개일 경우
        print(time.strftime('%Y년 %m월 %d일 현재 1개의 새글', time.localtime()))
        ctx = '<b>게시글 확인하기</b><br>' + ''.join(article_info['url'])
        sending_mail(ctx, article_info['title'])
    else:       # 새글이 2개 이상일 경우
        print(time.strftime('%Y년 %m월 %d일 현재 여러 개의 새글', time.localtime()))
        list_title = list()
        list_url = list()
        ctx = ''
        for article in article_info['title']:
            list_title.append('<b>' + article + '</b>')
        for article in article_info['url']:
            list_url.append(article)
        
        for i in range(len(list_title)):
            ctx = ctx + list_title[i] + '<br>' + list_url[i] + '<br><br>'
            
            
        sending_mail(ctx, list_title)
    
def main():
    print("작동 시작")
    # schedule.every().days.at("00:00").do(writing_mail)
    schedule.every().days.at("15:00").do(writing_mail)
    # schedule.every(10).seconds.do(writing_mail)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()