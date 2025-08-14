#-*- coding: utf-8 -*-

import requests
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, siteManager
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidhls', 'vidHLS')

    def setUrl(self, sUrl):
        self._url = str(sUrl).replace(".html","")


    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        api_call = ''
        sUrl = self._url
        if '|Referer=' in sUrl:
            Referer = sUrl.split('|Referer=')[1]
            sUrl = sUrl.split('|Referer=')[0]
        else:
            sUrl = sUrl
            Referer = siteManager().getUrlMain('moviztime')

        sdata = sUrl.split('data=')[1]

        Sgn=requests.Session()

        hdr = {'Sec-Fetch-Mode': 'navigate',
        	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        	'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        	'User-Agent': UA,
        	'Upgrade-Insecure-Requests': '1',
            'Host':'vidhls.com',
        	'Referer': Referer}
        prm={
                "data": sdata}
        _r = Sgn.get(sUrl,headers=hdr)
        sHtmlContent = _r.content.decode('utf8',errors='ignore').replace('\\','')
        oParser = cParser() 

        sPattern = '"videoServer":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            VidServ = aResult[1][0]

        sPattern = '"videoUrl":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            Url2 = aResult[1][0]
            Url2 = 'https://vidhls.com'+Url2+'?s='+VidServ
          
            headers = {'Referer':'https://vidhls.com/'}
            r = Sgn.get(Url2, headers=headers)
            sHtmlContent = r.text

            sPattern = 'RESOLUTION=(\d+x\d+)\s*(http[s]?://\S+)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
                    api_call = aEntry[1]

        if api_call:
            return True, f'{api_call}|Referer={self._url}' 

        return False, False