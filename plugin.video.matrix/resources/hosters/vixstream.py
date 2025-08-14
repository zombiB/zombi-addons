#-*- coding: utf-8 -*-

import base64
import urllib.parse
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vixstream', 'VixStream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        VSlog(self._url)

        sRefer = urlHostName(self._url)

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', sRefer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = 'var\s*_[0-9a-f]+\s*=\s*"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            key = '_0x3e68eb'
            decrypted_html = self.decrypt(aResult[1][0], key)

            sPattern = 'sources:\s*\[{file:"([^"]+)'
            aResult = oParser.parse(decrypted_html, sPattern)
            if aResult[0]:  
                api_call = aResult[1][0]

        if api_call:
            return True, f'{api_call}|User-Agent={UA}&Referer=https://{sRefer}/'

        return False, False

    def decrypt(self, encoded_string, key):
        decoded_string = base64.b64decode(encoded_string).decode('latin1')
        hex_encoded_string = ''.join(['%' + format(ord(char), '02x') for char in decoded_string])
        url_decoded_string = urllib.parse.unquote(hex_encoded_string)
        decrypted_string = ''.join([chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(url_decoded_string)])
        return decrypted_string