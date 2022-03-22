from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Android'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'govidme', 'govid')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36')
        sHtmlContent = oRequest.request()
        
        api_call = ''
        #type1/([^"]+)/
        oParser = cParser()

       # (.+?) .+? ([^<]+)
        sPattern =  'file:"([^<]+)",label:"([^<]+)"}' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0] is True:
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]).replace("[","%5B").replace("]","%5D").replace("+","%20"))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + self._url

        return False, False