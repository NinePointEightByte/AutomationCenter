import json
import sys
import os
import requests
import xml.etree.ElementTree

reload(sys) 
sys.setdefaultencoding('utf8')   

lc = os.environ.get('lc')
tk = os.environ.get('tk')
url = 'https://fsop.caac.gov.cn/g13/jsyzzapp/services/examFace/testScoremesstk?licenum=' + lc + '&messid=' + tk

response = requests.get(url, headers={'tk': tk, 'lc': lc})

if response.text == '<ns:testScoremesstkResponse xmlns:ns="http://pepec.icss.com"><ns:return></ns:return></ns:testScoremesstkResponse>':
    print(sys.getdefaultencoding())
    sys.exit("云执照账号配置不正确")

root = xml.etree.ElementTree.fromstring(response.text)
textReturned = json.loads(root[0].text)['result']
print(textReturned)
