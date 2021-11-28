from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

class InstagramCrawler:
    def __init__(self, keyword, requestTime, idx):
        self.keyword = keyword
        self.requestTime = requestTime
        self.userId = ['test_ywoosang', 'hyena_crawler', 'kimfe9', 'ninei_yat','Hong_test1','eses20010427','so_omin0703']
        self.userPassword = ['test1234', 'crawler123','yhcm2618','ninei1234','testtest123','nonochadan','chadannono']
        self.idx = idx


    def run(self):
        """
        스크래핑 시작
        """
        try:
            self.setDriver()
            response = self.getComments()
            return response
        except Exception as error:
            print(error)
            raise Exception(f'{self.keyword} Scrapping Error')

    def setDriver(self):
        """
        로그인 상태의 드라이버 생성
        """
        try:
            time.sleep(2)
            chromedriver = "/usr/src/chrome/chromedriver"
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('--no-sandbox')
            options.add_argument('window-size=1920x1080')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("disable-gpu")
            options.add_argument(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
            options.add_argument("lang=ko_KR")
            driver = webdriver.Chrome(chromedriver, options=options)
            driver.get('https://www.instagram.com/accounts/login')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rgFsT"))
            )
            time.sleep(2)
            id_section = driver.find_element_by_name('username')
            id_section.clear()
            i = random.randrange(0,3)
            id_section.send_keys(self.userId[self.idx])
            pw_section = driver.find_element_by_name('password')
            pw_section.clear()
            pw_section.send_keys(self.userPassword[self.idx])
            pw_section.submit()
            time.sleep(i)
            self.driver = driver
        except Exception as error:
            print(error)            
            pass

    def getUrl(self, word):
        """
        검색 키워드로 url 생성
        """
        if(word == '코로나'):
            word = '코로나확진'
        url = f'https://www.instagram.com/explore/tags/{word}'
        return url

    def calcTime(self, time):
        """
        시간 문자열을 받아 년,월,일,시,분 을 리스트로 만들어 반환
        """
        [year, month] = time.split('-')[:2]
        day = time.split('-')[-1].split('T')[0]
        [hour, minute] = time.split('-')[-1].split('T')[-1].split(':')[:2]
        return [year, month, day, hour, minute]

    def checkTimeValidation(self, requestTime, postTime):
        """
        게시물 작성 시간이 요청 시간 이후인지 여부 반환
        ex) 요청시간이 2021 11 10 00 00 이라면 게시물 작성 시간이 그 이후인지
        """
        for index in list(range(len(requestTime))):
            if requestTime[index] > postTime[index]:
                return False
            elif requestTime[index] < postTime[index]:
                return True
        return False

    def getComments(self):
        # 모든 키워드 탐색 결과
        response = []
        url = self.getUrl(self.keyword)
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Nnq7C"))
        )
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]').click()
        condition = True
        while condition:
            post = {
                "keyword": self.keyword,
                "link": "",
                "comments": [],
                "date": ""
            }
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "EtaWk"))
            )
            nextButton = self.driver.find_element_by_xpath(
                '/html/body/div[6]/div[1]/div/div/div[2]/button')
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            comments = soup.select('ul.Mr508 div.C4VMK span')
            post["link"] = self.driver.current_url
            postTime = self.calcTime(soup.find('time')['datetime'])
            post["date"] = '-'.join(postTime)
            condition = self.checkTimeValidation(
                self.requestTime, list(map(lambda x: int(x), postTime)))
            # 댓글 조회
            for comment in comments:
                post["comments"].append(comment.string)
                print(post)
            if(len(post["comments"])):
                response.append(post)
            sleepTime = random.uniform(1, 3)
            sleepTime = round(sleepTime, 2)
            time.sleep(sleepTime)
            nextButton.click()
        # 현재 키워드 탐색 결과 추가
        self.driver.close()
        return response