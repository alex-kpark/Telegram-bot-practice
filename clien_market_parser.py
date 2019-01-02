import requests
from bs4 import BeautifulSoup
import os
import telegram

#Telegram 부분
bot = telegram.Bot(token='725562183:AAGBVtfYegGW0zBDn5Nq84mbVaOKUmBmnO0')
chat_id = '473511007'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#시스템이 돌아가는 동안 계속해서 돌아가도록 작동
while True:
    req = requests.get('http://clien.net/cs2/bbs/board.php?bo_table=sold')
    req.encoding = 'utf-8' # Clien에서 encoding 정보를 보내주지 않아 encoding옵션을 추가

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('td.post_subject')
    latest = posts[1].text #0번은 규칙이므로

    #읽기 상태로 열고 업데이트가 되었는지 확인
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        if before != latest:
            #텔레그램 메시지를 보내는 로직을 추가하면 됨
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
        else:
            bot.sendMessage(chat_id=chat_id, text='새 글이 아직 없어요!ㅠㅠ')

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()


    time.sleep(60) #60초 쉬기