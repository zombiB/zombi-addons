#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog, addon
from resources.lib import helpers
from resources.lib.util import urlHostName
from resources.lib.mCaptcha.mserver import CaptchaServer
from six.moves import urllib_parse
import re
import requests
import time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frdl', 'FreeDownload')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        Sgn=requests.Session()

        response = requests.get(self._url)
        self._url = response.url

        headers = {
            'referer': self._url,
            'User-Agent': UA
                }

        sHtmlContent = Sgn.get(self._url, headers=headers).text
        data = helpers.get_hidden(sHtmlContent)
        data.update({"download_free": "1"})

        match = re.search(r'data-sitekey="([^"]+)"', sHtmlContent)
        if match:
            sitekey = match.group(1)

        token = self.get_captcha(sitekey)

        data.update({"cf-turnstile-response": token})

        waitingseconds = 61
        match = re.search(r'sec = (\d+);', sHtmlContent)
        if match:
            waitingseconds = int(match.group(1))+1

        dialog().VSinfo(f'الموقع يطلب الانتظار لمدة {waitingseconds} ثانية')
        time.sleep(waitingseconds)

        _r = Sgn.post(self._url, data, headers=headers)
        sHtmlContent = _r.content.decode('utf8',errors='ignore')

        r = re.search(r'''sources:\s*\[{src:\s*["'](?P<url>[^"']+)''', sHtmlContent, re.DOTALL)
        if r:
            api_call = urllib_parse.quote(r.group(1), '/:?=&') + helpers.append_headers(headers)

        else:
            pattern = r'<a href="([^"]+)"[^>]*type="button" class="btn[^"]*">'
            r = re.search(pattern, sHtmlContent)
            if r:
                api_call = urllib_parse.quote(r.group(1), '/:?=&') + helpers.append_headers(headers)

        if api_call:
            return True, api_call

        return False, False

    def get_captcha(self, sitekey):
        captcha_data = {
            "siteUrl": self._url,
            "siteKey": sitekey,
            "captchaType": "cf_re"
        }

        try:
            last_gen = int(addon().getSetting(f"{urlHostName(self._url)}_mcreate"))
        except Exception:
            last_gen = 0

        if not addon().getSetting(f"{urlHostName(self._url)}_mcaptcha") or last_gen < (time.time() - (1 * 60)):
            server = CaptchaServer(captcha_data)
            server.start_server()
            return addon().getSetting(f"{urlHostName(self._url)}_mcaptcha")
        else:
            return addon().getSetting(f"{urlHostName(self._url)}_mcaptcha")