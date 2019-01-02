import requests
from bs4 import BeautifulSoup
import json
import os
from multiprocessing import Pool

#python파일의 위치
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
Django에서도 parser.py를 활용하기 위한 코드
'''
#Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")

#이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

#Import Django Model at parser.py 
from parsed_data.models import BlogData

'''
파싱 함수 부분
'''
def parse_blog():
    req = requests.get('https://beomi.github.io/beomi.github.io_old/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'h3 > a'
    ) #아마 여러 객체가 끌려올 것

    #json 변환을 위한 empty dict 생성
    data = {}
    for title in my_titles:
        data[title.text] = title.get('href')
    return data

#import가 아닌 직접 실행시켰을 경우에만 작동하도록 정의해둠
if __name__=='__main__':
    blog_data_dict = parse_blog()

    #t : 앞의 값
    #l : 실제 링크를 가져다줌
    for t, l in blog_data_dict.items(): 
        BlogData(title=t, link=l).save()