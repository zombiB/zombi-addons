#-*- coding: utf-8 -*-
# Plugin modified from ResolveURL

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamtape', 'Streamtape')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        oParser = cParser()
        api_call = ''

        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            oRequest0 = cRequestHandler(SubTitle)
            sHtmlContent0 = oRequest0.request().replace('\\','')

            sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
            aResult = oParser.parse(sHtmlContent0, sPattern)
            if aResult[0]:

                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
                SubTitle = dialog().VSselectsub(qua, url)
        else:
            SubTitle = ''

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        
        src = re.findall(r'''ById\('.+?=\s*(["']//[^;<]+)''', sHtmlContent)
        if src:
            src_url = ''
            parts = src[-1].replace("'", '"').split('+')
            for part in parts:
                p1 = re.findall(r'"([^"]*)', part)[0]
                p2 = 0
                if 'substring' in part:
                    subs = re.findall(r'substring\((\d+)', part)
                    for sub in subs:
                        p2 += int(sub)
                src_url += p1[p2:]
            src_url += '&stream=1'
            src_url = 'https:' + src_url if src_url.startswith('//') else src_url
            api_call = src_url

        if api_call:
            if ('http' in SubTitle):
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url, SubTitle
            else:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False