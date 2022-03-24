#-*- coding: utf-8 -*-
#https://www.cloudy.ec/embed.php?id=etc...
#http://www.cloudy.ec/v/etc...
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog,VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'Cloudy', 'Cloudy')

    def isDownloadable(self):
        return True

    def __getIdFromUrl(self):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0] is True:
            return aResult[1][0]
        return ''
        
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        oParser = cParser()
        sPattern =  'id=([a-zA-Z0-9]+)'
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0] is True:
            self._url = 'https://www.cloudy.ec/embed.php?id=' + aResult[1][0] + '&playerPage=1'
            #Patch en attendant kodi V17
            self._url = self._url.replace('https','http')
        else:
            VSlog(self._url)

    def _getMediaLinkForGuest(self):
    
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        VSlog(self._url)
        
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
