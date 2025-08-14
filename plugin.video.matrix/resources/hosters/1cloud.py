#-*- coding: utf-8 -*-
# Adopted from ResolveURL https://github.com/Gujal00/ResolveURL

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib import random_ua
import binascii
import re

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, '1cloud', 'OneCloud')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Origin', self._url.rsplit('/', 1)[0])
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        api_call = ''
        aResult = re.search(r'"([^"]+)","DOWNLOAD', sHtmlContent, re.IGNORECASE)
        if aResult:
            api_call = ''.join([chr(((x if isinstance(x, int) else ord(x)) ^ 15) ^ 117) for x in binascii.unhexlify(aResult.group(1))])

        if api_call:
            return True, api_call

        return False, False
