#-*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from resources.lib import captcha_lib
from six.moves import urllib_parse
import re
import requests
import time

UA = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frdl', 'FreeDownload')

    def _getMediaLinkForGuest(self, autoPlay = False):
         VSlog(self._url)
         api_call = ''
         Sgn=requests.Session()

         headers = {
               'referer': self._url,
               'User-Agent': UA
                  }

         sHtmlContent = Sgn.get(self._url, headers=headers).text
         data = helpers.get_hidden(sHtmlContent)
         data.update(captcha_lib.do_captcha(sHtmlContent))
         time.sleep(31)

         _r = Sgn.post(self._url, data, headers=headers)
         sHtmlContent = _r.content.decode('utf8',errors='ignore')

         r = re.search(r'class="done.+?href="([^"]+)', sHtmlContent, re.DOTALL)
         if r:
            api_call = urllib_parse.quote(r.group(1), '/:') + helpers.append_headers(headers)
         
         if api_call:
             return True, api_call

         return False, False