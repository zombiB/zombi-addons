#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
import re, json
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'gofile', 'GoFile')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        if '|' in self._url:
            self._url = self._url.split('|')[0]

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url,
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*",
                   "Connection": "keep-alive",
                   }
        host = self._url.rsplit("/")[2]
        
        media_id = self._url.rsplit("/",1)[1]
        
        base_api = 'https://api.gofile.io'
        s = requests.session()
        sHtmlContent = s.post('{}/accounts'.format(base_api), headers=headers)
        token = json.loads(sHtmlContent.content).get('data', {}).get('token')
        
        sHtmlContent = s.get('https://{}/dist/js/global.js'.format(host), headers=headers).text
        
        wtoken = re.search(r'wt\s*=\s*"([^"]+)', sHtmlContent)
        
        headers.update({"Authorization": "Bearer" + " " + token})
        content_url = '{}/contents/{}?wt={}&cache=true'.format(base_api, media_id, wtoken.group(1))
        sHtmlContent = s.get(content_url, headers=headers).content
        
        data = json.loads(sHtmlContent).get('data').get('children')
        
        
        sources = [(data[x].get('size'), data[x].get('link')) for x in data]

        if len(sources) == 1:
            api_call = sources[0][1]

        elif len(sources) > 1:
            url=[]
            qua=[]
            for aEntry in sources:
                url.append(str(aEntry[1]))
                qua.append(str(aEntry[0]))
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Cookie=' + 'accountToken={}'.format(str(token))

        return False, False