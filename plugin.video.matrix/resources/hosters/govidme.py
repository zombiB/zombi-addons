from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, siteManager
from resources.lib import random_ua
from six.moves import urllib_parse

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'govidme', 'Govid')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oParser = cParser()
        if '|Referer=' in self._url:
            self._url, sReferer = self._url.split('|Referer=')
            sReferer = urllib_parse.urljoin(sReferer, '/')
        else:
            sReferer = siteManager().getUrlMain('wecima')

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent', UA)
        oRequest.addHeaderEntry('Referer', sReferer)
        sHtmlContent = oRequest.request()
        
        sPattern =  'file:"([^<]+)",label:"([^<]+)"}' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            url=[]
            qua=[]
            for i in aResult[1]:
                url.append(str(i[0]).replace("[","%5B").replace("]","%5D").replace("+","%20"))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + sReferer
        else:
            return True, self._url

        return False, False