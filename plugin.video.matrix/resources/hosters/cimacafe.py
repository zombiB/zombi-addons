#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from resources.lib import random_ua
import requests, re

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimacafe', 'CimaCafe')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oParser = cParser() 

        headers = {'User-Agent': UA,
                   'Referer': self._url
                   }
        if 'egbist' in self._url:
             headers.update({"Sec-Fetch-Dest": "iframe"})
             
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        if 'JuicyCodes.Run' in sHtmlContent:
            sHtmlContent = helpers.get_juiced_data(sHtmlContent)

        sPattern = 'iframe src=["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            return True, aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + self._url

        else:
            sPattern = 'file: ["\']([^"\']+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0]

            sPattern = 'file:["\']([^"\']+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][1]

            pattern = r'key:"(.*?)",keyId:"(.*?)"'
            match = re.search(pattern, sHtmlContent)
            if match:
                key = match.group(1)
                keyId = match.group(2)
                license_key = f'org.w3.clearkey|{keyId}:{key}'

                if api_call:
                    return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&license=' + license_key

        return False, False