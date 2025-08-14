#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from six.moves import urllib_parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'directplay', 'Direct-Link')

    def setUrl(self, url):
        self._url = str(url).replace('||', '%20')

    def _getMediaLinkForGuest(self, autoPlay = False):
        if '|Referer=' in self._url:
            sQuote = True
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]
        else:
            sQuote = False
            sReferer = self._url

        if 'googleusercontent.com' in self._url or 'video-downloads' in self._url:
            dialog().VSinfo(f'قد لا يقبل التشغيل المباشر ، جرب تحميل وتشغيل')

        if self._url:
            if sQuote:
                return True, urllib_parse.quote(self._url, '/:?=&') + f'|Referer={sReferer}'
            else:
                return True, self._url.replace('+', '%2B')

        return False, False
