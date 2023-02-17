from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'myvid', 'myvid')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' not in self._url:
             self._url = self._url.replace("https://myviid.com/","https://myviid.com/embed-")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        

        sPattern = 'file:"([^<]+)",label'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + self._url
       
        sPattern = "(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>"
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)",label:".+?"}'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                api_call = aResult[1][0] 
        #VSlog(api_call)

        if api_call:
            return True, api_call

        return False, False