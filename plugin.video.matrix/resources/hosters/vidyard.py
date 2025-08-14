#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import urllib.parse as urllib
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidyard', 'VidYard')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        headers = {'User-Agent': UA,
                   'Origin': self._url.rsplit('/', 1)[0],
                   'Referer': self._url
                   }
        s = requests.session()

        if not '.json' in self._url:
            parsed_uri = urllib.urlparse(self._url)
            base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            link = re.escape(self._url)
            id = re.compile(r'.com/(.*?)\\').findall(link)
            id2 = re.compile(r'.com/(.*)').findall(link)
            if id !=[]:
                api = base+'player/'+id[0]+'.json'
            elif id2 !=[]:
                api = base+'player/'+id2[0]+'.json'
            data = s.get(api, allow_redirects=True, headers=headers, verify=False)
            data.encoding = 'utf-8'
            data = data.text
            _1080p = re.compile('"profile":"1080p","url":"(.*?)","mimeType"').findall(data)
            _720p = re.compile('"profile":"720p","url":"(.*?)","mimeType"').findall(data)
            _480p = re.compile('"profile":"480p","url":"(.*?)","mimeType"').findall(data)
            _360p = re.compile('"profile":"360p","url":"(.*?)","mimeType"').findall(data)
            if _1080p !=[]:
                resolved = _1080p[0]+'|Referer='+base
            elif _720p !=[]:
                resolved = _720p[0]+'|Referer='+base
            elif _480p !=[]:
                resolved = _480p[0]+'|Referer='+base
            elif _360p !=[]:
                resolved = _360p[0]+'|Referer='+base
            else:
                resolved = ''
        elif '.json' in self._url:
            data = s.get(self._url, allow_redirects=True, headers=headers, verify=False)
            data.encoding = 'utf-8'
            data = data.text
            _1080p = re.compile('"profile":"1080p","url":"(.*?)","mimeType"').findall(data)
            _720p = re.compile('"profile":"720p","url":"(.*?)","mimeType"').findall(data)
            _480p = re.compile('"profile":"480p","url":"(.*?)","mimeType"').findall(data)
            _360p = re.compile('"profile":"360p","url":"(.*?)","mimeType"').findall(data)
            if _1080p !=[]:
                resolved = _1080p[0]+'|Referer='+base
            elif _720p !=[]:
                resolved = _720p[0]+'|Referer='+base
            elif _480p !=[]:
                resolved = _480p[0]+'|Referer='+base
            elif _360p !=[]:
                resolved = _360p[0]+'|Referer='+base
            else:
                resolved = ''
        else:
            resolved = ''

        if resolved:
            return True, resolved

        return False, False

