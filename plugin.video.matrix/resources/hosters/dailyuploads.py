from resources.lib import captcha_lib, helpers, random_ua
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from six.moves import urllib_parse
import re, requests

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dailyuploads', 'DailyUploads')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        if 'File Not Found' not in sHtmlContent:
            data = helpers.get_hidden(sHtmlContent)
            data.update(captcha_lib.do_captcha(sHtmlContent))
            sHtmlContent = s.post(self._url, data, headers=headers).text
            api_call = re.search(r'<td.+?href="([^"]+)', sHtmlContent)
            if api_call:
                return True, urllib_parse.quote(api_call.group(1), '/:') + helpers.append_headers(headers)

        return False, False