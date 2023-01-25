#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sendit', 'sendit')
			
    def __getIdFromUrl(self):
        sPattern = "v=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0] :
            return aResult[1][0]

        return 

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        api_call = ''
        #type1/([^"]+)/
        oParser = cParser()
        sPattern = 'source src="([^"]+)" type="video/mp4">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            api_call = aResult[1][0]
            
        #type2?   
        if api_call:
            return True,api_call 

        return False, False