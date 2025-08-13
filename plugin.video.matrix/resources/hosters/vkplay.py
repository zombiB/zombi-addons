#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vkplay', 'vkPlay')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        
        sLive = self._url.split('embed/')[1]
        api_url = "https://api.vkplay.live/v1/blog/"
        url = api_url+sLive+'/public_video_stream'

        api_call = False
        sReferer = ""
        if '|Referer=' in self._url:
            url = self._url.split('|Referer=')[0]
            sReferer = self._url.split('|Referer=')[1]
        else:
            url = self._url
            sReferer =  self._url

        oParser = cParser()
        oRequest = cRequestHandler(url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern =  '"url":"([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:
                if '.m3u8' not in aEntry:
                    continue
                if 'hls' not in aEntry:
                    continue
                if 'http' not in aEntry:
                    continue
                url = aEntry

            # Need proper work 
            VSlog(url)
            api_call = url

            if api_call:
                return True, api_call

            return False, False
