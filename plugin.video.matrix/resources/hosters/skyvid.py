from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'skyvid', 'skyvid')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', 'https://cima-club.bar/')
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       # (.+?) .+? ([^<]+)
        sPattern =  'sources: (.+?), ' 
        aResult = oParser.parse(sHtmlContent,sPattern) 
        if aResult[0] :
            api_call = aResult[1][0].replace('["','').replace('"]','')

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + self._url
        sPattern =  'src: "([^<]+)", type: "video/mp4", res: "(.+?)",' 
        aResult = oParser.parse(sHtmlContent,sPattern) 
        if aResult[0] :
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + self._url

        return False, False