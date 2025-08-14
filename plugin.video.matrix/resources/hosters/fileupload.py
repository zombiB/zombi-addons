from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import unicodedata

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fileupload', 'File-Upload')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        if 'embed' not in self._url:
            Vid = self._url.split("/")[3]
            self._url = self._url.replace(Vid,('embed-'+Vid+'-1920x1080.html'))

        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry("host", "file-upload.org")
        sHtmlContent = oRequest.request()

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent2 = cPacker().unpack(data)

            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0]:
                api_call = aResult[1][0]

        if api_call:
            return True, api_call + "|verifypeer=false"

        return False, False