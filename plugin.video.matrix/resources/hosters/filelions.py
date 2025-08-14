# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker
from six.moves import urllib_parse

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filelions', 'FileLions')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url
        if '|Referer=' in self._url:
            self._url, referer = self._url.split('|Referer=')
            referer = urllib_parse.urljoin(referer, '/')
        else:
            referer = self._url

        self._url = self._url.replace('/d/','/v/').replace('/f/','/v/').replace('/file/','/v/').replace('/download/','/v/')
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', referer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = r'"(hls2|hls3|hls4)"\s*:\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult and aResult[0]:
            link_map = {item[0]: item[1] for item in aResult[1]}

            base_url = f'https://{urlHostName(self._url)}'
            for key in ["hls4", "hls2", "hls3"]:
                if key in link_map:
                    link = link_map[key]
                    if not link.startswith("http"):
                        link = base_url + link
                    api_call = link

        if api_call:
            return True, api_call

        return False, False
