import urllib.request
import sqlite3       # 데이터 베이스 기능을 함 아마도 sqlite3는 기본 내장라이브러리라서 바로 쓸 수 있을거?

from bs4 import BeautifulSoup
req = urllib.request.Request("http://ce.pknu.ac.kr/05_community/01_community.php"); # 컴퓨터 공학과 공지사항 주소
data = urllib.request.urlopen(req).read()
bs = BeautifulSoup(data, 'html.parser')
l = bs.select('.txt-l > a')
king = 0

for s in l:
        ss = str(s)
        number = ss[98:102:]
        if (king < int(number)):
                king = int(number)
result = 'http://ce.pknu.ac.kr/05_community/01_community.php?bid=&page=0&sv=title&sw=&tgt=view&idx=' + str(king)

# sqlite3 사용 

conn=sqlite3.connect("comnotice.db")  # 이 이름의 db파일에 접근 => 이름은 지마음대로지만 명령어마다 똑같이 적어줘야됨
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS comnotice (NUM INTEGER)") # comnotice란 파일 존재하면 안만들고 존재하지 않으면 만드고 => 이름은 지마음대로지만 명령어마다 똑같이 적어줘야됨
x = False
cur.execute("SELECT * FROM comnotice ORDER BY NUM DESC") # comnotice 란 파일 내림차순으로 조회 ORDER BY NUM DESC는 아마 쓰인 순서로 조회? => 이름은 지마음대로지만 명령어마다 똑같이 적어줘야됨
k = '('+str(king)+',)'
g = str(cur.fetchone()) # 저장 목록 제일 앞에꺼 가져옴
print('g'+g) # 저장 목록 제일 앞에꺼 가져옴
print('k'+k) # 파싱 했을 때 가장 최신 데이터
if(g == k):  # 그 둘을 비교한다
        x = True
        print('wait...') # 같으면 종료
if(x == False):          # 다르면 출력과 슬랙에 쏴주기
        print(king)
        cur.execute("INSERT INTO comnotice (NUM) VALUES (?)",(king,)) # 데이터 베이스에 새 데이터 기록 => 이름은 지마음대로지만 명령어마다 똑같이 적어줘야됨
        cur.execute("SELECT * FROM comnotice") #  => 이름은 지마음대로지만 명령어마다 똑같이 적어줘야됨
        print(cur.fetchone()) # 저장 목록 제일 앞에꺼 가져옴
        print(cur.fetchall()) # 저장 목록 모두 가져옴
        req2 = urllib.request.Request(result);
        data2 = urllib.request.urlopen(req2).read()
        bs2 = BeautifulSoup(data2, 'html.parser')
        l2 = bs2.find_all('p')
        result2 = ""
        for s2 in l2 :
                result2 += s2.get_text() + "\n"
        print(result2)
                
        from slacker import Slacker
        token = 'xoxp-209950700770-210772248070-215942233537-0da85a56158fc71fd64883fb90344363'
        slack = Slacker(token)
        slack.chat.post_message('#2017_summer_project_2', result2) 
   
conn.commit()
conn.close()

# 컴퓨터 공학과 공지사항 파싱
