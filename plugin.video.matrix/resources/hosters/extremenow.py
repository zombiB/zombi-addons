# coding: utf-8
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'extremenow', 'ExtremeNow')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):

        if '|Referer=' in self._url:
            Refer = self._url.split('|Referer=')[1]
            Referer = getHost(Refer)
            self._url = self._url.split('|Referer=')[0]
        else:
            Referer = self._url
        
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', Referer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            
            url=[]
            qua=[]
            
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url +'&verifypeer=false'

        return False, False

def getHost(self):
    parts = self.rsplit("/", 1)
    host = parts[0] 
    return f'{host}/'