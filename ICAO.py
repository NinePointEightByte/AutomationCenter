import json
import requests
import xml.etree.ElementTree

lc = os.environ.get('lc')
tk = os.environ.get('tk')
url = 'https://fsop.caac.gov.cn/g13/jsyzzapp/services/examFace/testScoremesstk?licenum=' + lc + '&messid=' + tk

    response = requests.get(url, headers={'tk': tk, 'lc': lc})

if response:

    print(response.text)
    root = xml.etree.ElementTree.fromstring(response.text)
    textReturned = json.loads(root[0].text)['result']
    print(textReturned)

else:
    print()
