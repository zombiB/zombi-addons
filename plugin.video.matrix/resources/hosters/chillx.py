#-*- coding: utf-8 -*-

import json
import re, requests
import base64
import hashlib

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import helpers
from Cryptodome.Cipher import AES
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'chillx', 'Chillx')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sRefer = self._url
        if '|Referer=' in self._url:
            sRefer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        headers = {'User-Agent': UA,
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                   'Accept-Language':'en-US,en;q=0.5',
                   'Referer': sRefer}
        
        s = requests.Session()  
   
        r = s.get(self._url, headers=headers)
        sHtmlContent = r.text

        key_response = requests.get("https://rowdy-avocado.github.io/multi-keys/")
        key_data = key_response.json()
        key = key_data['chillx']
        key = ''.join(key)
        key = bytes(key, 'utf-8')       

        edata = re.search(r"\s*=\s*'([^']+)", sHtmlContent).group(1)
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
            r = re.search(r'"?file"?:\s*"([^"]+)"', ddata) \
                or re.search(r'"video_player".+?file:\s*"([^"]+)', ddata)
            if r:
                headers.update({'Origin': self._url.rsplit("/",3)[0], 'verifypeer': 'false'})
                return True, r.group(1) + helpers.append_headers(headers)

        return False, False

