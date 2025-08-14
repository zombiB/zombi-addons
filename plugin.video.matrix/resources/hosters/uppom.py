#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from resources.lib.util import Unquote
from resources.lib.packer import cPacker
import re
import requests

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

   def __init__(self):
      iHoster.__init__(self, 'uppom', 'Uppom')

   def setUrl(self, sUrl):
      self._url2 = sUrl
      self._url = str(sUrl).replace(".html","")

      if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

   def _getMediaLinkForGuest(self, autoPlay=False):
      VSlog(self._url)
      oParser = cParser()
      
      if '|Referer=' in self._url:
         sReferer = self._url.split('|Referer=')[1]
         self._url = self._url.split('|Referer=')[0]
      else:
         sReferer = self._url

      Sgn = requests.Session()
      
      if 'key=' in self._url:
         return True, f'{self._url}|Referer={sReferer}'

      protocol = 'https' if 'https' in self._url else 'http'
      d = re.findall(f'{protocol}://(.*?)/([^<]+)', self._url)
      
      if not d:
         return False, False

      sHost, sID = d[0]
      sID = sID.split('/')[0] if '/' in sID else sID
      sLink = f'{protocol}://{sHost}/{sID}'

      headers = {
         'Origin': f'{protocol}://{sHost}',
         'Referer': sLink,
         'User-Agent': UA
      }

      sHtmlContent = Sgn.get(self._url, headers=headers).text
      data = helpers.get_hidden(sHtmlContent)
      data.update({"method_free": "Free Download >>"})
      
      _r = Sgn.post(sLink, headers=headers, data=data)
      sHtmlContent = _r.content.decode('utf8', errors='ignore')
      url = _r.headers.get('location')
      
      if url and url != self._url:
         return True, url.replace(' ', '%20') + helpers.append_headers(headers)

      data = {
         'op': 'download2',
         'id2': sID,
         'rand': '',
         'referer': sLink
      }
      _r = Sgn.post(sLink, headers=headers, data=data)
      sHtmlContent = _r.content.decode('utf8', errors='ignore')

      sPattern = 'id="direct_link".+?href="([^"]+)'
      aResult = oParser.parse(sHtmlContent, sPattern)
      
      if aResult[0]:
         api_call = aResult[1][0].replace(' ', '%20') + helpers.append_headers(headers)
      else:
         sLink = f'{protocol}://{sHost}/embed-{sID}.html'
         sHtmlContent = Sgn.get(sLink, headers=headers).text
         sPattern = r'(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
         aResult = oParser.parse(sHtmlContent, sPattern)
         
         if aResult[0]:
               sHtmlContent = cPacker().unpack(aResult[1][0])
         
         sPattern = r'file:["\']([^"\']+)'
         aResult = oParser.parse(sHtmlContent, sPattern)
         
         if aResult[0]:
               api_call = aResult[1][0]
      
      if api_call:
         return True, api_call

      return False, False
