#coding: utf-8
import base64
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, addon, siteManager
from resources.sites.faselhd import decode_page
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'FaselHD', 'gold')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        sReferer = siteManager().getUrlMain('faselhd')
        VSlog(self._url)

        oParser = cParser()   
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        if 'adilbo' in sHtmlContent:
            sHtmlContent = decode_page(sHtmlContent)
        else:
            try:
                patterns = [
                    r'</button><script type="text/javascript">(.*?)</script><button',
                    r'</video><script>(.*?)</script'
                ]

                all_results = []
                for sPattern in patterns:
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0]:
                        all_results.extend(aResult[1])

                for coded in all_results:
                    # Don't use this, just for test
                    oRequest = cRequestHandler("https://webcrack-one.vercel.app/api")
                    oRequest.addHeaderEntry('user-agent',UA)
                    oRequest.enableCache(False)
                    oRequest.addParameters('code', coded)
                    oRequest.setRequestType(1)
                    sHtmlContent = oRequest.request(jsonDecode=True)['code'].replace('\\"', '"')

            except:
                VSlog('Failed Api')
        
        sPattern =  'data-url="([^<]+)">([^<]+)</button>' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sLink = []
                sQual = []
                for aEntry in aResult[1]:
                    sLink.append(str(aEntry[0]))
                    sQual.append(str(aEntry[1].upper()))
            api_call = dialog().VSselectqual(sQual, sLink)

        sPattern =  'videoSrc = ["\']([^"\']+)["\']' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                api_call = aEntry
        
        if api_call:
            return True, f'{api_call}|Referer={sReferer}&User-Agent={UA}'

        return False, False
