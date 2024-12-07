import json
import sys
import os
import requests
import xml.etree.ElementTree

lc = os.environ.get('lc')
tk = os.environ.get('tk')
url = 'https://fsop.caac.gov.cn/g13/jsyzzapp/services/examFace/testScoremesstk?licenum=' + lc + '&messid=' + tk

response = requests.get(url, headers={'tk': tk, 'lc': lc})

if response.text == '<ns:testScoremesstkResponse xmlns:ns="http://pepec.icss.com"><ns:return></ns:return></ns:testScoremesstkResponse>':
    print(sys.getdefaultencoding())
    sys.exit("云执照账号配置不正确")

root = xml.etree.ElementTree.fromstring(response.text)
textReturned = json.loads(root[0].text)['result']
if textReturned == '未查询到成绩信息':
    wxpusherResponse = requests.post('https://wxpusher.zjiecode.com/api/send/message',
                                     headers={'Content-Type': 'application/json'},
                                     json={
                                         'appToken': os.environ.get('WXPusherAppToken'),
                                         'content': '<h1 style=\"color:blue;\">{}</p>'.format(textReturned),
                                         'summary': 'ICAO：未查询到' + os.environ.get('EXAMDATE') + '成绩信息',
                                         'contentType': 2,
                                         'uids': eval(os.environ.get('WXPusherUIDS'))
                                     })
    if not wxpusherResponse.json()['code'] == 1000:
        print(wxpusherResponse.text)
        sys.exit("WxPusher报错")
    print(textReturned)
    exit()
elif textReturned['data']:
    for result in textReturned['data']:
        if result['EXAM_DATE'] == os.environ.get('EXAMDATE'):
            wxpusherResponse = requests.post('https://wxpusher.zjiecode.com/api/send/message',
                                             headers={'Content-Type': 'application/json'},
                                             json={
                                                 'appToken': os.environ.get('WXPusherAppToken'),
                                                 'content': '<h1 style=\"color:red;\">{}</p>'.format(result),
                                                 'summary': os.environ.get('EXAMDATE') + '考试成绩：' + result['SCORE'],
                                                 'contentType': 2,
                                                 'uids': eval(os.environ.get('WXPusherUIDS'))
                                             })
            if not wxpusherResponse.json()['code'] == 1000:
                print(wxpusherResponse.text)
                sys.exit("WxPusher报错")
            print(textReturned)
            exit()
        else:
            wxpusherResponse = requests.post('https://wxpusher.zjiecode.com/api/send/message',
                                             headers={'Content-Type': 'application/json'},
                                            json={
                                                 'appToken': os.environ.get('WXPusherAppToken'),
                                                 'content': '<h1 style=\"color:blue;\">{}</p>'.format(textReturned),
                                                 'summary': 'ICAO：未查询到' + os.environ.get('EXAMDATE') + '成绩信息',
                                                 'contentType': 2,
                                                 'uids': eval(os.environ.get('WXPusherUIDS'))
                                            })
            if not wxpusherResponse.json()['code'] == 1000:
                print(wxpusherResponse.text)
                sys.exit("WxPusher报错")
            print(textReturned)
            exit()
print(textReturned)
sys.exit('程序异常结束')
