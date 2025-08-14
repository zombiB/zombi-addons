#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mp4upload', 'mp4upload')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        api_call = False
        oParser = cParser()
        urlmain = 'https://www.mp4upload.com'

        if 'embed' in self._url:
            oRequestHandler = cRequestHandler(self._url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', urlmain + '/')
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()

            sPattern = 'src:.+?"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                api_call = aResult[1][0] + '|Referer=' + self._url + '&verifypeer=false'

        else:
            self._url = str(self._url ).replace(".html","").replace("embed-","")
            oRequestHandler = cRequestHandler(self._url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', urlmain + '/')
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()

            s = requests.Session()
            _id = self._url.split('/')[-1].replace(".html","")
            headers = {'Host': 'www.mp4upload.com',
        	    'User-Agent': UA,
        	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        	    'Accept-Language': 'en-US,en;q=0.9',
        	    'Content-Type': 'application/x-www-form-urlencoded',
        	    'Origin': urlmain,
        	    'Connection': 'keep-alive',
        	    'Referer': self._url,
        	    'Upgrade-Insecure-Requests': '1'}
            data={
                "op": "download1",
                "id": _id,
                'usr_login':'',
                "referer": '',
                "method_free": "Free Download"} 
            
            r = s.post(self._url, data=data, headers=headers)
            sHtmlContent = r.content

            sPattern = 'IFRAME SRC="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sURL = aResult[1][0]

            oRequestHandler = cRequestHandler(sURL)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', urlmain + '/')
            sHtmlContent2 = oRequestHandler.request()

            sPattern = 'src:.+?"([^"]+)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0] + '|Referer=' + self._url + '&verifypeer=false'

        if api_call:
            return True, api_call
        
        return False, False
