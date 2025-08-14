#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib import helpers, random_ua
from urllib.parse import unquote
from six.moves import urllib_parse

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'Filemoon')

    def _getMediaLinkForGuest(self, autoPlay = False):
        oParser = cParser()
        self._url = self._url.replace('filemoon.sx','filemoon.in')
        VSlog(self._url)
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
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = r'<iframe\s*src="([^"]+)'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            oRequest = cRequestHandler(aResult[1][0])
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self._url)
            oRequest.addHeaderEntry('sec-fetch-dest', 'iframe')
            sHtmlContent = oRequest.request()
               
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?)</script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)

        headers = {'User-Agent': UA}
        sPattern = r'sources:\s*\[\s*{\s*file:\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            headers.update({
                    'Referer': self._url,
                    'Origin': urllib_parse.urljoin(self._url, '/')[:-1]})
            api_call = aResult[1][0] + helpers.append_headers(headers)

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                headers.update({
                    'Referer': self._url,
                    'Origin': urllib_parse.urljoin(self._url, '/')[:-1]})
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                api_call = dialog().VSselectqual(qua, url) + helpers.append_headers(headers)
        
        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
