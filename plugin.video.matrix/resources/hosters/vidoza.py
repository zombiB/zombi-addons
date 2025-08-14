#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidoza', 'Vidoza')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        
        sPattern =  'src: *"([^"]+)".+?label:"([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:

            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
