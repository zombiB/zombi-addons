# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
import resources.lib.cloudscraper2 as cper
import xbmcgui

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'bigwarp', 'BigWarp')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        sReferer = self._url
        api_call = ''

     
         

        # ✅ Unpack any packed JS
        oParser = cParser(self._url)
        sPattern = r'(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                unpacked = cPacker().unpack(aEntry)
                if unpacked:
                    sHtmlContent += unpacked
                else:
                    VSlog("Unpack failed or returned empty")

        # ✅ Try common video patterns
        patterns = [
            r'sources\s*:\s*\[\s*\{.*?file\s*:\s*["\'](http[^"\']+)',
            r'file\s*:\s*"([^"]+\.mp4)"',
            r'"(http[^"]+\.m3u8)"',
            r'src\s*:\s*"([^"]+\.mp4)"',
        ]

        for pat in patterns:
            res = oParser.parse(sHtmlContent, pat)
            if res[0]:
                api_call = res[1][0]
                break

        if api_call:
            if not api_call.startswith('http'):
                base = self._url.rsplit('/', 1)[0]
                api_call = base + '/' + api_call.lstrip('/')
            return True, api_call + '|Referer=' + sReferer

        VSlog("❌ No video source found")
        return False, False
