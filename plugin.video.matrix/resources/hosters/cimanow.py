#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimanow', 'cimanow')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        import requests
        s = requests.Session()
        r = s.get(self._url).content

        oParser = cParser()
        sPattern =  '<source src="([^"]+)" type=\'(.+?)\'>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            url = []
            qua = []
            for x in aResult[1]:
                url.append(x[0])
                qua.append(x[1])
                	
                api_call = dialog().VSselectqual(qua,url)
                    
        if api_call:
            return True, api_call + '|User-Agent=' + UA 
            
        return False, False