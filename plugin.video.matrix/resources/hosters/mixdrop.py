#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.util import urlHostName
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mixdrop', 'Mixdrop')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)
        self._url = self._url.replace("/f/","/e/")

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        sReferer = f'https://{urlHostName(self._url)}/'
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Cookie', 'hds2=1')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'wurl="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                api_call = aResult[1][0]

            if api_call.startswith('//'):
                api_call = 'https:' + aResult[1][0]

            if api_call:
                return True, f'{api_call}|Referer={sReferer}&User-Agent={UA}&Sec-Fetch-Dest=video&Sec-Fetch-Mode=cors&Sec-Fetch-Site=cross-site'

        return False, False
