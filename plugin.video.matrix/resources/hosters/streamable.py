#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamable', 'streamable')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
            # (.+?) .+?
        sPattern = 'poster=.+?src="([^"]+)'
        
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = 'https:'+ aResult[1][0] 

        if (api_call):
            return True, api_call 

        return False, False