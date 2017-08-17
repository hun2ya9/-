import urllib.request
import time
import sqlite3

from bs4 import BeautifulSoup
                    #
                    #------- 공지사항 목록 파싱 - 중복 채크: 데이터베이스에 저장/비교 - 새 공지사항 파싱 - 기다림 ---------
                    #
while True:
        req = urllib.request.Request("http://www.pknu.ac.kr/usrBoardActn.do?p_bm_idx=5&p_boardcode=PK10000005"); # 공지사항 주소
        data = urllib.request.urlopen(req).read()
        bs = BeautifulSoup(data, 'html.parser')
        l = bs.find_all('a') # 모든 a 태그
        king = 0
        for s in l:
                p = s.get('href') # 모든 a태그의 href
                pp = str(p)
                ppp = pp.endswith('pageno=1') #(문자열)로 끝나는것들
                if(ppp == True):
                        number = p[36:42:] #슬라이스 = [start:stop:step] 36번째 ~ 42번째 추출 -> 항상 고정이길래
                        if (king < int(number)) : # 킹보다 number가 크다면
                                king = int(number) # 킹의 자리를 뺏는다.
                                result = 'http://www.pknu.ac.kr/usrBoardActn.do?p_cmd=view&p_b_idx='+ str(king)+'&p_bm_idx=5&p_boardcode=PK10000005&p_pageno=1'
        #print(result)
        conn=sqlite3.connect("notice.db")
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS notice (NUM INTEGER)")  # 없으면 만들기
        
        x = False               # 중복 채크용 변수
        cur.execute("SELECT * FROM notice ORDER BY NUM DESC") # 내림차순 정렬
        k = '('+str(king)+',)'
        g = str(cur.fetchone()) # 제일 앞에꺼 가져옴
        print('g'+g)
        print('k'+k)
        if(g == k):             # 이미 보낸 공지사항을 다시 올릴 필요는 없으니까 중복 채크
                    x = True
                    print('중복')
        if(x == False):         # 새 공지사항이 올라왔을 경우
                    print(king)
                    cur.execute("INSERT INTO notice (NUM) VALUES (?)",(king,))   # 없으면 쓰기
                    cur.execute("SELECT * FROM notice")                       # 읽기
                    print(cur.fetchone())       # 제일 앞에꺼
                    print(cur.fetchall())       # 전체 목록
                    #
                    #------- 여기서 부터는 새 공지사항을 다시 파싱하는 과정 ---------
                    #
                    req2 = urllib.request.Request(result);
                    data2 = urllib.request.urlopen(req2).read()
                    bs2 = BeautifulSoup(data2, 'html.parser')
                    l2 = bs2.find_all('div')
                    l3 = bs2.find('td')
                    s3 = '제목 : ' + l3.get_text() # 공지사항에 제목을 추가하였음
                    print(s3)
                    for s2 in l2:
                            if(s2.get('class') == ['bbs-body']):
                                    result2 = s2.get_text()
                                    print(result2)
                                    R = s3 + "\n"+ result+ "\n"+ result2
                                    from slacker import Slacker
                                    token = 'xoxp-216393310067-216465253826-217564504615-c488544fbf212b2e169b8014a084c5d1'
                                    slack = Slacker(token)
                                    slack.chat.post_message('#general', R) 
        conn.commit()
        conn.close()
        time.sleep(300)

