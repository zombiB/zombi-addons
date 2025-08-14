#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'anavids', 'Anavids')

    def isDownloadable(self):
        return True

    def setUrl(self, url):
        self._url = str(url)
        if not 'embed-' in self._url:
             self._url = self._url.replace(".com/",".com/embed-")

    def _getMediaLinkForGuest(self, autoPlay = False):
        
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        VSlog(self._url)
        
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
        
