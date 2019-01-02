import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#1.HTTP GET Request

#requests.get("URL주소")로 HTTP 요청을 보낼 수 있음
req = requests.get('https://beomi.github.io/beomi.github.io_old/') 

#HTML 리소스를 가져오기
html = req.text #HTML
header = req.headers #Headers
status = req.status_code #Check 통신상태

#BeautifulSoup : Change HTML source into Python object
soup = BeautifulSoup(html, 'html.parser')

#select : CSS Selector를 기반으로 객체들을 List형태로 return 해주나
my_titles = soup.select('h3 > a')

'''
for title in my_titles:    
    print(title.text) #Tag안에 있는 텍스트
    print(title.get('href')) #title.get(속성이름)으로 다양한 속성 내용을 가져올 수 있음
'''

#json 형식으로 만들어주는 기능
data = {}
for title in my_titles:
    data[title.text] = title.get('href')


#2.Session으로 로그인 한 상태에서 크롤링 하기 (HTML Form 태그 사용했을 경우)
LOGIN_INFO = {
    'userId' : 'inputIdhere', #HTML에서의 id태그 = userId
    'userPassword' : 'inputPWhere' #HTML에서의 pw태그 = userPassword
}

with requests.Session() as s:
    first_page = s.get('https://www.clien.net/service')
    html = first_page.text
    soup = BeautifulSoup(html, 'html.parser')

    csrf = soup.find('input', {'name':'_csrf'}) #input태그들 중에서 name이 _csrf인 것을 찾음
    print(csrf['value']) #찾은 태그의 value를 print

    #LOGIN_INFO 합치기
    LOGIN_INFO = {**LOGIN_INFO, **{'_csrf':csrf['value']}} #unpacking해서 두 dict를 합쳐주고

    #HTTP Post Request : 로그인을 위해 POST url과 함께 전송될 데이터를 보내주기
    login_req = s.post('https://www.clien.net/service/login', data=LOGIN_INFO)
    #print(login_req.status_code) - 테스팅 코드

    if login_req.status_code != 200:
        raise Exception('Login Failed')

    '''
    Login Session Starts from here
    '''

#3. Selenium
driver = webdriver.Chrome('C:/Users/kpark/AppData/Local/Programs/Python/chromedriver.exe')

driver.implicitly_wait(3) #암묵적으로 웹 리소스 로딩까지 3초를 기다린다

driver.get('https://google.com')


#4 Explicitly Wait : Resolve the problem of Loading Time

#안나오면 나올때 까지 10초 기다리고, 나오면 바로 진행
try:
    title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.intro_main > h3')))
    print(title.text)

finally:
    driver.quit()