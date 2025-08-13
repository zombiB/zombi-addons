# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib import random_ua
from resources.lib.util import urlHostName
import base64, re
from urllib.parse import urlparse, parse_qs

UA = random_ua.get_ua()

class cHoster(iHoster):
    STUPID_KEY = "xHb0ZvME5q8CBcoQi6AngerDu3FGO9fkUlwPmLVY_RTzj2hJIS4NasXWKy1td7p"
    NONCE_REGEX = re.compile(r'_xt\s*=\s*"([^"]+)"')

    def __init__(self):
        iHoster.__init__(self, 'videa', 'Videa')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay=False):
        VSlog(self._url)

        oParser = cParser()
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        match = self.NONCE_REGEX.search(sHtmlContent)
        if not match:
            return False, False

        nonce = match.group(1)
        paramL, paramS = nonce[:32], nonce[32:]
        result = ''.join(paramS[it - (self.STUPID_KEY.index(paramL[it]) - 31)] for it in range(32))

        seed = self.get_random_string()
        video_id = parse_qs(urlparse(self._url).query).get("v", [""])[0]

        REQUEST_URL = f'https://{urlHostName(self._url)}/player/xml?platform=desktop'
        request_url = f"{REQUEST_URL}&v={video_id}&lang=hu&_s={seed}&_t={result[:16]}&start=0"

        oRequestHandler = cRequestHandler(request_url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        oRequestHandler.addHeaderEntry('Origin', f'https://{urlHostName(self._url)}')
        sHtmlContent = oRequestHandler.request()

        if sHtmlContent.startswith("<?xml"):
            doc = sHtmlContent
        else:
            key = result[16:] + seed + oRequestHandler.getResponseHeader()["x-videa-xs"]
            b64dec = base64.b64decode(sHtmlContent)
            doc = self.rc4(b64dec, key).decode('utf-8', errors='ignore')

        sSubtitle = {}
        sSubs = re.findall(r'<subtitle\s*src="([^"]+)"\s*title="([^"]+)"', doc)
        if sSubs:
            sSubtitle = {sLang: 'https:' + sUrl.replace('&amp;', '&') for sUrl, sLang in sSubs}

        sPattern = r'<video_source\s*name="([^"]+)".+?>([^<]+)</video_source>'
        aResult = oParser.parse(doc, sPattern)
        if aResult[0]:
            url = []
            qua = []

            for aEntry in reversed(aResult[1]):
                sQual = str(aEntry[0])
                vLink = str(aEntry[1])
                hash_match = re.search(fr'<hash_value_{sQual}>([^<]+)</hash_value_{sQual}>', doc)
                if not hash_match:
                    return False, False

                hash_value = hash_match.group(1)
                expires_value = re.search(r'exp="([^"]+)"', doc).group(1)
                api_call = f"https:{vLink}?md5={hash_value}&expires={expires_value}"

                url.append(str(api_call))
                qua.append(str(sQual))

            api_call = dialog().VSselectqual(qua, url) 

        if api_call:
            if sSubs:
                return True, api_call + '|User-Agent=' + UA, sSubtitle
            return True, api_call + '|User-Agent=' + UA

        return False, False

    def get_random_string(self, length=8):
        import random, string
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def rc4(self, data, key):
        S = list(range(256))
        j = 0
        out = []
        key = [ord(c) for c in key]

        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            out.append(byte ^ S[(S[i] + S[j]) % 256])

        return bytes(out)