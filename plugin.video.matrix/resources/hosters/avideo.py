#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
import requests

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'avideo', 'aVideo', 'gold')

    def setUrl(self, sUrl):
        self._url = str(sUrl).replace(".html","")


    def _getMediaLinkForGuest(self, autoPlay = False):
        sUrl = self._url

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        if '/e' in sUrl:
            sHost = sUrl.split('/e')[0]
            sCode = sUrl.split('/e-')[1]
        else:
            sHost = sUrl
            sCode = sUrl           

        Sgn = requests.Session()

        hdr = {'Origin': sHost,
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        	'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        	'Content-Type': 'application/x-www-form-urlencoded',
        	'Content-Length': '47',
        	'Referer': sUrl}
        prm={
                "op": "embed",
                "file_code": sCode,
                "auto": "1",
                "referer": ""}
        
        _r = Sgn.post('https://avideo.host/dl',headers=hdr,data=prm)
        sHtmlContent = _r.content.decode('utf8',errors='ignore')
        oParser = cParser() 

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            sHtmlContent2 = cPacker().unpack(aResult[1][0])

            sPattern = 'file:"([^"]+)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
        
            if aResult[0]:
                api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|AUTH=TLS&verifypeer=false' 

        return False, False