import requests, re
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog, dialog
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidtube', 'VidTube')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = ''
        sSession = requests.session()
        oParser = cParser()

        sUrl = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            sUrl = self._url.split('|Referer=')[0]

        headers = {'User-Agent': UA, 'Referer': sReferer}
        if '/d/' in sUrl:
            sHtmlContent = sSession.get(sUrl, headers=headers).text

            quality_pattern = re.compile(r'<b class="text-.*?">\s*(.*?)\s*</b>')
            link_pattern = re.compile(r'<a class="btn.*?" href="(.*?)">')

            qualities = quality_pattern.findall(sHtmlContent)
            links = link_pattern.findall(sHtmlContent)
            url = []
            qua = []
            for i in zip(qualities, links):
                url.append(str(i[1]))
                qua.append(str(i[0]))

            nUrl = sUrl.split("/d/")[0] + dialog().VSselectqual(qua, url)
            sHtmlContent = sSession.get(nUrl, headers=headers).text
            
            sPattern =  '<div class="mb-4">\s*<a href="([^"]+)"' 
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                api_call = aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + sUrl

        else:

            sHtmlContent = sSession.get(sUrl, headers=headers).text

            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHtmlContent = cPacker().unpack(aResult[1][0])
            
            sPattern = 'file:"([^"]+)".+?label:"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url)  + '|User-Agent=' + UA + '&Referer=' + sUrl

            sPattern =  'sources:*\[{file:"([^"]+)"' 
            aResult = oParser.parse(sHtmlContent,sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:            
                    api_call = aEntry + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=' + self._url.rsplit('/', 1)[0]

        if api_call:
            return True, api_call

        return False, False