# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

import urllib.request as urllib2
import json
import ssl
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevideo_me', 'TheVideo')

    def __getIdFromUrl(self, sUrl):
        sPattern = '\/(?:embed-)?(\w+)(?:-\d+x\d+)?(?:\.html)?$'
        aResult = cParser().parse( sUrl, sPattern )
        if aResult[0]:
            return aResult[1][0]
        return ''

    def setUrl(self, url):
        sId = self.__getIdFromUrl(url)
        if 'video.' in url:
            self._url = 'http://thevideo.me/embed-' + sId + '.html'
        else:
            self._url = "https://vev.io/embed/" + sId


    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False
        aResult = False

        request_headers = {"User-Agent": UA}

        req = urllib2.Request(self._url,headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, context=gcontext)

        self._url = response.geturl()
        response.close()

        Json_url = 'https://vev.io/api/serve/video/' + self.__getIdFromUrl(self._url)

        req = urllib2.Request(Json_url, headers=request_headers)
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urllib2.urlopen(req, data={}, context=gcontext)
        sHtmlContent = response.read()
        aResult = json.loads(sHtmlContent)
        response.close()

        if (aResult):
            url = []
            qua = []

            for i in aResult['qualities']:
                url.append(aResult['qualities'][i])
                qua.append(str(i))

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
