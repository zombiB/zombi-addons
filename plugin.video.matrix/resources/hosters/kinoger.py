#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
from Cryptodome.Cipher import AES
import binascii, json

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'kinoger', 'Kinoger')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        vID = self._url.split('#')[1]
        sHost = self._url.split('#')[0]

        sUrl = f'{sHost}api/v1/video?id={vID}'
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', sHost)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        edata = binascii.unhexlify(sHtmlContent[:-1])
        key = b'\x6b\x69\x65\x6d\x74\x69\x65\x6e\x6d\x75\x61\x39\x31\x31\x63\x61'
        iv = b'\x31\x32\x33\x34\x35\x36\x37\x38\x39\x30\x6f\x69\x75\x79\x74\x72'

        cipher = AES.new(key, AES.MODE_CBC, iv) 
        ddata = cipher.decrypt(edata) 
        ddata = ddata.rstrip(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10').decode('utf-8') 
        ddata = json.loads(ddata)

        api_call = ddata.get('source')
        if api_call: 
            return True, f'{api_call}|Referer={sHost}&Origin={sHost[:-1]}&User-Agent={UA}'

        return False, False
