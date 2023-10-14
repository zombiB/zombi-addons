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
        iHoster.__init__(self, 'volvovideo', 'volvovideo')

    def setUrl(self, url):
        self._url = str(url)
        if not '/e/' in self._url:
             self._url = self._url.replace("/f/","/e/")
				 
    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        api_call = ''
        #type1/([^"]+)/
        oParser = cParser()
      # (.+?) ([^<]+) .+?
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            
        #type2?   
        if api_call:
            return True,api_call 

        return False, False