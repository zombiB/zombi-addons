# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'rumble', 'Rumble')

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()       
        sPattern = '},"(.+?)":{"url":"(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            url=[]
            qua=[]
            
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call 

        else:
            sPattern = 'RESOLUTION=(\d+x\d{0,3}).+?(https.+?m3u8)'
            aResult = oParser.parse(sHtmlContent, sPattern)
        
            api_call = False

            if aResult[0]:            
                url=[]
                qua=[]
            
                for i in aResult[1]:
                    url.append(str(i[1]))
                    qua.append(str(i[0]))
                api_call = dialog().VSselectqual(qua, url)
 
                if api_call:
                    return True, api_call 

        return False, False
