#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://aparat.cam/embed-xxxxx.html

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'arabveturk', 'arabveturk')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        url = self._url
        VideoType = 2 # dl mp4 lien existant non utilisé ici
        VideoType = 1 # m3u8
        VSlog(self._url)

        if VideoType == 1:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = 'file:"(http.+?m3u8)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                api_call = aResult[1][0]


            if api_call:
                return True, api_call

        return False,False