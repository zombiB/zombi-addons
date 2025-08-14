#-*- coding: utf-8 -*-

import json
import re, requests
import base64
import hashlib
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from Cryptodome.Cipher import AES
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'jimmy', 'JimmyX')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = self._url

        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': sReferer}
        
        s = requests.Session()  
   
        r = s.get(self._url, headers=headers)
        sHtmlContent = r.text

        key = ''.join("GDPlayer-JASm(8234_)9312HJASi23lakka")
        key = bytes(key, 'utf-8')       

        edata = re.search(r"_decx\('([^']+)", sHtmlContent).group(1)
        if edata:
            edata = json.loads(edata)
            ct = base64.b64decode(edata['ct'])
            salt = bytes.fromhex(edata['s'])
            iv = bytes.fromhex(edata['iv'])

            md = hashlib.md5()
            md.update(key)
            md.update(salt)
            cache0 = md.digest()

            md = hashlib.md5()
            md.update(cache0)
            md.update(key)
            md.update(salt)
            cache1 = md.digest()

            key = cache0 + cache1

            cipher = AES.new(key, AES.MODE_CBC, iv)
            ddata = cipher.decrypt(ct)
            ddata = ddata.decode('utf-8').replace("\\", "")
            r = re.search(r'''url:\s*"([^"]+)"''', ddata) 
            surl = r.group(1)
            sHtmlContent = r = s.get(surl, headers=headers).json()
            api_call = sHtmlContent.get('sources')[0].get('file').replace(' ', '%20')
            if api_call.startswith('//'):
                api_call = 'https:' + api_call

            if api_call:
                return True, api_call

        return False, False

