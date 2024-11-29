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
wxpusherResponse = requests.post('https://wxpusher.zjiecode.com/api/send/message',
                                 headers={'Content-Type': 'application/json'},
                                 json={
                                     'appToken': os.environ.get('WXPusherAppToken'),
                                     'content': '<h1 style=\"color:blue;\">{}</p>'.format(textReturned),
                                     'summary': 'ICAO：' + textReturned,
                                     'contentType': 2,
                                     'uids': eval(os.environ.get('WXPusherUIDS'))
                                 })
if not wxpusherResponse.json()['code'] == 1000:
    print(wxpusherResponse.text)
    sys.exit("WxPusher报错")

print(textReturned)
