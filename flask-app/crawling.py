import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.notebook import tqdm
import time
import re
import requests
import random
import pickle
import openpyxl
#Queue의 기본적인 기능 구현
class Queue():
    def __init__(self, maxsize):
        self.queue = []
        self.maxsize = maxsize
        
    # Queue에 Data 넣음
    def enqueue(self, data):
        self.queue.append(data)

    # Queue에 가장 먼저 들어온 Data 내보냄
    def dequeue(self):
        dequeue_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            dequeue_object = self.queue[0]
            self.queue = self.queue[1:]
        return dequeue_object
    
    # Queue에 가장 먼저들어온 Data return
    def peek(self):
        peek_object = None
        if self.isEmpty():
            print("Queue is Empty")
        else:
            peek_object = self.queue[0]
        return peek_object
    
    # Queue가 비어있는지 확인
    def isEmpty(self):
        is_empty = False
        if len(self.queue) == 0:
            is_empty = True
        return is_empty
    
    # Queue의 Size가 Max Size를 초과하는지 확인
    def isMaxSizeOver(self):
        queue_size = len(self.queue)
        if (queue_size > self.maxsize):
            return False
        else :
            return True


def scraping(url):
    if __name__=="__main__":
        #set option of selenium
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('headless') # 크롬 띄우는 창 없애기
        options.add_argument('user')
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

        #target of crawling
        data_list = []
        driver.get(url)
        
        #페이지 Open 후 기다리는 시간
        time.sleep(5.0)

        #초기 댓글 보이게 창 내려보기 
        driver.execute_script("window.scrollTo(0,300)")

        time.sleep(5.0)

        #down the scroll
        #body = driver.find_element_by_tag_name('body')
        body = driver.find_element("name", "body")
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        


        # max size 50의 Queue 생성
        # 0.1sec * 50 = 5sec 동안 Scroll 업데이트가 없으면 스크롤 내리기 종료
        szQ = Queue(100)
        enqueue_count = 0
        
        while True:
            # Scroll 내리기
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            
            # Scroll Height를 가져오는 주기
            time.sleep(0.1)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            # Queue가 꽉 차는 경우 스크롤 내리기 종료
            if(enqueue_count > szQ.maxsize):
                break
            
            # 첫 Loop 수행 (Queue가 비어있는 경우) 예외 처리
            if(szQ.isEmpty()) :
                szQ.enqueue(new_page_height)
                enqueue_count += 1
                
            # Queue에 가장 먼저 들어온 데이터와 새로 업데이트 된 Scroll Height를 비교함
            # 같으면 그대로 Enqueue, 다르면 Queue의 모든 Data를 Dequeue 후 새로운 Scroll Height를 Enqueue 함.    
            else :
                if(szQ.peek() == new_page_height) :
                    szQ.enqueue(new_page_height)
                    enqueue_count += 1
                else :
                    szQ.enqueue(new_page_height)
                    for z in range(enqueue_count) :
                        szQ.dequeue()
                    enqueue_count = 1
            
            # 기존의 Scroll 내리는 방식      
            #if new_page_height == last_page_height:
            #    break
            #last_page_height = new_page_height
            #time.sleep(2.0)
        
        # print ("[PASS] Get all comments of URL")

        html0 = driver.page_source
        # driver.close()
        html = BeautifulSoup(html0, 'html.parser')

        comments_list = html.findAll('ytd-comment-thread-renderer', {'class':'style-scope ytd-item-section-renderer'})
        # print (comments_list)
        ## 재생목록이름
        
    # list_name = comments_list[j].find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text
    list_name = driver.find_element_by_css_selector('#header-description > h3:nth-child(1) > yt-formatted-string > a').text

    ## 전체 조회수
    # views = comments_list[j].find('span', {'class': 'view-count style-scope ytd-video-view-count-renderer'}).text
    views = driver.find_element_by_css_selector('#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer').text

    ## 제목 
    # name = comments_list[j].find('yt-formatted-string', {'class': 'style-scope ytd-video-primary-info-renderer'}).text
    name = driver.find_element_by_css_selector('#container > h1 > yt-formatted-string').text

    for j in range(len(comments_list)):
        ## 댓글 내용
        comment = comments_list[j].find('yt-formatted-string', {'id': 'content-text'}).text
        comment = comment.replace('\n', '') # 줄 바뀜 없애기
        comment = comment.replace('\t', '') # 탭 줄이기
        # print(comment)

        ##유튜브 댓글 id

        youtube_id = comments_list[j].find('a', {'id': 'author-text'}).span.text
        youtube_id = youtube_id.replace('\n', '') # 줄 바뀜 없애기
        youtube_id = youtube_id.replace('\t', '') # 탭 줄이기
        youtube_id = youtube_id.strip()

        ## 댓글 좋아요 개수 (0인 경우 예외 처리)
        try:
            like_num = comments_list[j].find('span',
                                        {'id': 'vote-count-middle',
                                        'class': 'style-scope ytd-comment-action-buttons-renderer',
                                        'aria-label': re.compile('좋아요')}).text
            like_num = like_num.replace('\n', '') # 줄 바뀜 없애기
            like_num = like_num.replace('\t', '') # 탭 줄이기
            like_num = like_num.strip()
        except:
            like_num = 0

        data = {'list_name': list_name, 'name': name, 'views': views, 'youtube_id': youtube_id, 'comment': comment, 'like_num': like_num}
        # data = {'comment': comment, 'like_num': like_num}
        data_list.append(data)
        # print(data)

    result_df = pd.DataFrame(data_list,
                            columns=['list_name','name','views', 'youtube_id', 'comment', 'like_num'])
    # result_df = pd.DataFrame(data_list,
                            #  columns=['comment', 'like_num'])
    # result_df.to_excel(dir, index = False)
    driver.close()
    return result_df


a = scraping('https://www.youtube.com/watch?v=xvqsFTUsOmc')
print(a.info())