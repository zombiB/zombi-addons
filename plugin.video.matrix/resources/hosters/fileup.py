#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://cloudvid.co/embed-xxxx.html
#https://clipwatching.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fileup', 'fileup')

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not self._url.endswith('.html'):
            self._url = self._url + '.html'

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        sUrl = self._url

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        if 'File was deleted' in sHtmlContent:
            VSlog("File was deleted")

        oParser = cParser()
        sPattern = "</script><script type='text/javascript'>([^<]+)</script></div>"
        aResult = oParser.parse(sHtmlContent,sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'file:"([^"]+)",flashplayer:'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + self._url
                
        if api_call:
            return True, api_call

        return False, False