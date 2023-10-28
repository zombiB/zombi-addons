#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Plugin from ResolveURL
# Yonn1981 https://github.com/Yonn1981/Repo
#

import json
import re
import requests
from six.moves import urllib_parse

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog, VSlog

from resolveurl.lib.pyaes import openssl_aes


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamrapid', 'Rabbitstream/Dokicloud')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        mainurl = self._url

        referer = urllib_parse.urljoin(self._url, '/')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Referer': referer}
        
        import requests
        s = requests.Session()  
   
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Referer': referer}
        r = s.get(self._url, headers=headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()

        sPattern = '<script type="text/javascript" src="(.+?)"></script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            surl = aResult[1][0]
            surl = referer + surl

        import requests
        response = requests.get("https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt")
        key = response.text

        host = mainurl.split("/e")[0]
        host = host.split("//")[1]
        mid = mainurl.split('?')[0]
        mid = mid.split("embed-4")[1]
        mid = mid.replace('/', '/getSources?id=')
        aurl = 'https://'+host+'/ajax/embed-4'+mid

        import requests
        s = requests.Session()  
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Referer': referer, 'X-Requested-With': 'XMLHttpRequest'}
        r = s.get(aurl, headers=headers)
        sHtmlContent = r.content.decode('utf8')
        oParser = cParser()

        sPattern = '"sources":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sources = aResult[1][0]
            
        # Working?
        table = json.loads(key)
        decrypted_key = ""
        offset = 0
        encrypted_string = sources
        for start, end in table:
            decrypted_key += encrypted_string[start - offset:end - offset]
            encrypted_string = encrypted_string[:start - offset] + encrypted_string[end - offset:]
            offset += end - start

        OpenSSL_AES = openssl_aes.AESCipher()
        sources = json.loads(OpenSSL_AES.decrypt(encrypted_string, decrypted_key))

        sPattern = "'file': '(.+?)',"
        aResult = oParser.parse(sources, sPattern)

        if aResult[0]:
            source = aResult[1][0]

        url_stream = source

        SubTitle = ''
        sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
                # initialisation des tableaux
            url = []
            qua = []
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            SubTitle = dialog().VSselectsub(qua, url)

        if url_stream:
            if ('http' in SubTitle):
                return True, url_stream, SubTitle
            else:
                return True, url_stream


        return False, False

def extract_real_key(sources, key):
    table = json.loads(key)
    decrypted_key = ""
    offset = 0
    encrypted_string = sources
    for start, end in table:
        decrypted_key += encrypted_string[start - offset:end - offset]
        encrypted_string = encrypted_string[:start - offset] + encrypted_string[end - offset:]
        offset += end - start
        VSlog(decrypted_key)
    return decrypted_key, encrypted_string