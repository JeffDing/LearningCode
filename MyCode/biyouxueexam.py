#import time

import requests
#import selenium
#from PIL import Image
#from selenium import webdriver
#from io import StringIO
n = 0
scn = '14中学'
for page in range(44, 896):
    print('这是第{}页'.format(page))

    res = requests.get(
        url='http://study2.biyouxue.com/ByxStudy/DailyAffairsQuery/getStuListAjax',
        headers={
            'Cookie': 'JSESSIONID=04AF818CA4D8AC3E432B0060C8148567-n1; acw_tc=2f624a6c15900530037524420e5f05c7d94952772eb7c9599a6780f5741631; SERVERID=10bd6bc8c7172322b77e5212d976e9c7|1590053906|1590051126',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            # 'Referer': 'http://study2.biyouxue.com/ByxStudy/DailyAffairsQuery/stuListView?testManagerId=5e96c5e1e4b0a2c5b8d8a675',

        },
        params={
            'qNo': 1,
            'schoolNo': 'all',
            'startScore': '',
            'endScore': '',
            'stuSchoolNo': '',
            'stuName': '',
            'testManagerId': '5e96c5e1e4b0a2c5b8d8a675',
            'isPaperPage': 'true',
            '_search': 'false',
            'nd': '',
            'rows': 10,
            'page': page,
            'sidx': '',
            'sord': 'asc',
        }
    )

    students = res.json()

    for stu in students['rows']:

        stuno = stu['stuNo']
        after_scn = stu['schoolName']
        if scn == after_scn:
            pass
        else:
            n+=1
            scn=stu['schoolName']
        name = stu['schoolName']+stu['gardeName']+stu['className']+stu['name']
        tid = stu['tId'][n]
        print(name)
        for p in range(1,3):

            paper = requests.get(
                url='http://study2.biyouxue.com/ByxStudy/common/getEntirePaperImg',
                headers={
                    'Cookie': 'JSESSIONID=04AF818CA4D8AC3E432B0060C8148567-n1; acw_tc=2f624a6c15900530037524420e5f05c7d94952772eb7c9599a6780f5741631; SERVERID=10bd6bc8c7172322b77e5212d976e9c7|1590053906|1590051126',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                    # 'Referer': 'http://study2.biyouxue.com/ByxStudy/DailyAffairsQuery/stuListView?testManagerId=5e96c5e1e4b0a2c5b8d8a675',

                },
                params={
                    'page': p,
                    'testId': tid,
                    'stuNo': stuno

                }
            )

            with open((str(name+str(p))+'.png'), 'wb') as file:
                file.write(paper.content)
            time.sleep(3)
