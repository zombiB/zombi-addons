# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog

import re
import requests, base64
from urllib.parse import unquote

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        sHtmlContent = GetHtml(url)
        sPattern = '<form action="(.+?)" method="post"'
        result = re.findall(sPattern, sHtmlContent)
        if result:
           url = 'https://multiup.org' + ''.join(result[0])

        NewUrl = url.replace('https://www.multiup.org/fr/download', 'https://www.multiup.org/fr/mirror')\
                    .replace('https://www.multiup.eu/fr/download', 'https://www.multiup.org/fr/mirror')\
                    .replace('https://www.multiup.org/download', 'https://www.multiup.org/fr/mirror')

        sHtmlContent = GetHtml(NewUrl)

        sPattern = 'nameHost="([^"]+)".+?link="([^"]+)".+?class="([^"]+)"'
        r = re.findall(sPattern, sHtmlContent, re.DOTALL)

        if not r:
            return False

        for item in r:

            if 'bounce-to-right' in str(item[2]) and not 'download-fast' in item[1]:
                self.list.append(item[1])

        return self.list

class cJheberg:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):

        if url.endswith('/'):
            url = url[:-1]

        idFile = url.rsplit('/', 1)[-1]
        NewUrl = 'https://api.jheberg.net/file/' + idFile
        sHtmlContent = GetHtml(NewUrl)

        sPattern = '"hosterId":([^"]+),"hosterName":"([^"]+)",".+?status":"([^"]+)"'
        r = re.findall(sPattern, sHtmlContent, re.DOTALL)
        if not r:
            return False

        for item in r:
            if not 'ERROR' in item[2]:
                urllink = 'https://download.jheberg.net/redirect/' + idFile + '-' + item[0]
                try:
                    url = GetHtml(urllink)
                    self.list.append(url)
                except:
                    pass

        return self.list
    
# modif cloudflare
def GetHtml(url, postdata=None):

    if 'download.jheberg.net/redirect' in url:
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        url = oRequest.getRealUrl()
        return url
    else:
        sHtmlContent = ''
        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)

        if postdata != None:
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequest.addHeaderEntry('Referer', 'https://download.jheberg.net/redirect/xxxxxx/yyyyyy/')

        elif 'download.jheberg.net' in url:
            oRequest.addHeaderEntry('Host', 'download.jheberg.net')
            oRequest.addHeaderEntry('Referer', url)

        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()

        return sHtmlContent
        
class cMegamax:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        sHosterUrl = url.replace('download','iframe')
        oRequestHandler = cRequestHandler(sHosterUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('&quot;','"')
        oParser = cParser()
        
        sVer = ''
        sPattern = '"version":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in (aResult[1]):
                sVer = aEntry

        s = requests.Session()            
        headers = {'Referer':sHosterUrl,
                                'Sec-Fetch-Mode':'cors',
                                'X-Inertia':'true',
                                'X-Inertia-Partial-Component':'web/files/mirror/video',
                                'X-Inertia-Partial-Data':'streams',
                                'X-Inertia-Version':sVer}

        r = s.get(sHosterUrl, headers=headers).json()
        
        for key in r['props']['streams']['data']:
            sQual = key['label'].replace(' (source)','')
            for sLink in key['mirrors']:
                sHosterUrl = sLink['link']
                sLabel = sLink['driver'].capitalize()
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'https:' + sHosterUrl
        
                self.list.append(f'url={sHosterUrl}, qual={sQual}, label={sLabel}')
                                 
        return self.list 

class cVidsrcto:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()
        
        sPattern = 'data-id="(.*?)"'
        aResult = oParser.parse(sHtmlContent, sPattern) 
        if (aResult[0]):
          sources_code = aResult[1][0]
          sources = self.get_sources(sources_code)

          sPattern = "'.*?': '(.*?)'"
          aResult = oParser.parse(sources, sPattern)
          if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                source_url = self.get_source_url(source)
                self.list.append(source_url)
        return self.list 

    def get_sources(self, data_id) -> dict:
        req = requests.get(f"https://vidsrc.to/ajax/embed/episode/{data_id}/sources")
        data = req.json()

        return {video.get("title"): video.get("id") for video in data.get("result")}    

    def get_source_url(self, source_id) -> str:
        req = requests.get(f"https://vidsrc.to/ajax/embed/source/{source_id}")
        data = req.json()

        encrypted_source_url = data.get("result", {}).get("url")
        return self.decrypt_source_url(encrypted_source_url)

    def decrypt_source_url(self, source_url) -> str:
        encoded = self.decode_base64_url_safe(source_url)
        decoded = self.decode(encoded)
        decoded_text = decoded.decode('utf-8')

        return unquote(decoded_text)       
    
    def decode_base64_url_safe(self, s) -> bytearray:
        standardized_input = s.replace('_', '/').replace('-', '+')
        binary_data = base64.b64decode(standardized_input)

        return bytearray(binary_data)
    
    def decode(self, str) -> bytearray:
        key_bytes = bytes('8z5Ag5wgagfsOuhz', 'utf-8')
        j = 0
        s = bytearray(range(256))

        for i in range(256):
            j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
            s[i], s[j] = s[j], s[i]

        decoded = bytearray(len(str))
        i = 0
        k = 0

        for index in range(len(str)):
            i = (i + 1) & 0xff
            k = (k + s[i]) & 0xff
            s[i], s[k] = s[k], s[i]
            t = (s[i] + s[k]) & 0xff
            decoded[index] = str[index] ^ s[t]

        return decoded

class cVidsrcnet:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        oParser = cParser()
        req = requests.get(url)
        sources = re.findall(r'<div class="server" data-hash="(.*?)">(.+?)</div>', req.text)

        sPattern = "'(.*?)', '.*?'"
        aResult = oParser.parse(sources, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                source = aEntry
                req_1 = requests.get(f"https://rcp.vidsrc.me/rcp/{source}", headers={"Referer": url})

                encoded = re.search(r'data-h="(.*?)"', req_1.text).group(1)
                seed = re.search(r'<body data-i="(.*?)">', req_1.text).group(1)

                decoded_url = self.decode_src(encoded, seed)
                if decoded_url.startswith("//"):
                   decoded_url = f"https:{decoded_url}"

                req_2 = requests.get(decoded_url, allow_redirects=False, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
                location = req_2.headers.get("Location")
        
                if "vidsrc.stream" in location:
                  location= location + f"?Referer=https://rcp.vidsrc.me/rcp/{source}"
                  self.list.append(location)
                if "2embed.cc" in location:
                  location = ''
                  self.list.append(location)
                if "multiembed.mov" in location:
                  location= location + f"?Referer=https://rcp.vidsrc.me/rcp/{source}"
                  self.list.append(location)

        return self.list
       
    def decode_src(self, encoded, seed) -> str:
        '''decodes hash found @ vidsrc.me embed page'''
        encoded_buffer = bytes.fromhex(encoded)
        decoded = ""
        for i in range(len(encoded_buffer)):
            decoded += chr(encoded_buffer[i] ^ ord(seed[i % len(seed)]))
        return decoded
    