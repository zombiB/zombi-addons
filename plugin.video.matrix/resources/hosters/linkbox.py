#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
import json
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'linkbox', 'linkbox')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        url = 'https://www.linkbox.to/api/open/get_url?itemId=' + self._url.rsplit('/', 1)[1]
        VSlog(url)
        import requests
        s = requests.Session()  
        postdata = self._url.rsplit('/', 1)[1]     
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36',
							'itemId': postdata,
							'origin': 'www.linkbox.to',
							'Referer': 'https://www.linkbox.to/'}
        r = s.get(url, headers=headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()
        

        sPattern = ',"url":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + self._url

        return False, False