from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Android'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'govid', 'CimaClub', 'gold')
			
    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if '/down/'  in sUrl:
            self._url = self._url.replace("/down/","/play/")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

       # (.+?) .+? ([^<]+)
        sPattern =  '<small>([^<]+)</small> <a target="_blank" download=.+?href="([^<]+)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0] is True:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + self._url

        return False, False