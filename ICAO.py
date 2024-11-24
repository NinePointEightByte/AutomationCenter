import json
import requests
import xml.etree.ElementTree

lc = '360923200111013114'
tk = '93891115-eb36-417c-a0ca-d40644d52f5f'
url = 'https://fsop.caac.gov.cn/g13/jsyzzapp/services/examFace/testScoremesstk?licenum=' + lc + '&messid=' + tk

response = requests.get(url, headers={'tk': tk, 'lc': lc})

if response:

    root = xml.etree.ElementTree.fromstring(response.text)
    textReturned = json.loads(root[0].text)['result']
    print(textReturned)

else:
    print()
