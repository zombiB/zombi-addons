from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
import unicodedata

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamwish', 'Streamwish')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        self._url = self._url.replace('/f/','/e/').replace('/d/','/e/')
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            self._url = self._url.split('|Referer=')[0]
        api_call = ''

        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry("User-Agent", UA)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        if 'Page is loading' in sHtmlContent:
            oRequest = cRequestHandler(self.get_redirect_url())
            oRequest.addHeaderEntry("User-Agent", UA)
            oRequest.addHeaderEntry('Referer', sReferer)
            oRequest.enableCache(False)
            sHtmlContent = oRequest.request()


        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent = cPacker().unpack(data)

        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 

        sPattern = 'MDCore.wurl=["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0] 
            if api_call.startswith('//'):
                api_call = 'http:' + api_call

        sPattern = r'"(hls2|hls3|hls4)"\s*:\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult and aResult[0]:
            link_map = {item[0]: item[1] for item in aResult[1]}

            base_url = f'https://{urlHostName(self._url)}'
            for key in ["hls4", "hls2", "hls3"]:
                if key in link_map:
                    link = link_map[key]
                    if not link.startswith("http"):
                        link = base_url + link
                    api_call = link

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False

    def get_redirect_url(self):
        import random
        from urllib.parse import urlparse, urlunparse
        dmca = [
            'hgplaycdn.com',
            'habetar.com',
            'yuguaab.com',
            'guxhag.com',
            'auvexiug.com',
            'xenolyzb.com',
        ]

        main = [
            'kravaxxa.com',
            'davioad.com',
            'haxloppd.com',
            'tryzendm.com',
            'dumbalag.com',
        ]

        rules = [
            'dhcplay.com',
            'hglink.to',
            'test.hglink.to',
            'wish-redirect.aiavh.com',
        ]

        parsed = urlparse(self._url)
        hostname = parsed.hostname

        if hostname in rules:
            destination = random.choice(main)
        else:
            destination = random.choice(dmca)

        final_url = urlunparse(('https', destination, parsed.path, '', parsed.query, ''))
        return final_url