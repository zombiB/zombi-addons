# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import urllib.request as urllib2
import ssl
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'giga', 'Giga')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        myContext = ssl._create_unverified_context()

        req = urllib2.Request(self._url)
        handle = urllib2.urlopen(req, context=myContext)
        sHtmlContent = handle.read()
        handle.close()

        oParser = cParser()
        sPattern = "var mp4v = '(.+?)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return True, aResult[1][0]
        
        else:
            sPattern = '<a id="downloadb" class="btn btn-default.+?href="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                return True, aResult[1][0]

        return False, False
