# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'darkibox', 'DarkiBox')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self, api_call=None, autoPlay = False):
        VSlog(self._url)
        oParser = cParser()
        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        api_call = ''
        sPattern = 'sources: *\[{src: "([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]  + '|User-Agent=' + UA + '&Referer=' + self._url

        file_code = self._url.split('/')[-1].split('.')[0]

        postdata = 'op=embed&auto=1&file_code=%s' % file_code

        oRequest = cRequestHandler("https://darkibox.com/dl")
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.enableCache(False)
        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()
        oParser = cParser()
        sPattern = 'sources: *\[{src: "([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]  + '|User-Agent=' + UA + '&Referer=' + self._url

        return api_call != None, api_call
