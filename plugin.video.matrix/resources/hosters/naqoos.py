from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'naqoos', 'Naqoos')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request(jsonDecode=True)

        files = sHtmlContent["files"]
        for file_obj in files:
            url = []
            qua = []
            url.append(file_obj["file"])
            qua.append(file_obj["label"])

        api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False