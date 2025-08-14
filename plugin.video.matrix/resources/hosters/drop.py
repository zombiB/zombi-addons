import time
from resources.lib import captcha_lib, helpers, random_ua
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re, requests

UA = random_ua.get_pc_ua()

MAX_TRIES = 3

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'drop', 'DropDownload')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        if 'No such file with this filename' not in sHtmlContent:
            tries = 0
            while tries < MAX_TRIES:
                data = helpers.get_hidden(sHtmlContent)
                data.update({"method_free": "Free Download >>"})
                data.update(captcha_lib.do_captcha(sHtmlContent))
                time.sleep(16)
                headers.update({'Origin': self._url.rsplit('/', 1)[0]})
                sHtmlContent = s.post(self._url, data, headers=headers).text
                r = re.search(r'''<a\s*href="([^"]+)"\s*class="btn-download''', sHtmlContent, re.DOTALL)
                if r:
                    return True, r.group(1).replace(' ', '%20') + helpers.append_headers(headers)
                tries += 1

        return False, False