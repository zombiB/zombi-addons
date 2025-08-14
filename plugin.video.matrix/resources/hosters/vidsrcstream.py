#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
import re
import requests
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidsrcstream', 'VidsrcStream')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url
        SubTitle = ''

        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            if '/search/' in SubTitle:
                try:
                    headers = { "User-Agent": "VLSub 0.10.2",
                            "X-Requested-With": "XMLHttpRequest"}
                    data = requests.get(SubTitle, headers=headers).json()
                    SubTitle = [item['SubDownloadLink'].replace(".gz", "").replace("download/", "download/subencoding-utf8/") for item in data]
                except:
                    VSlog('Failed to process subtitle')
                    
        if '|Referer=' in self._url:
            referer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        if 'm3u8' in self._url or 'vidsrc.pro' in self._url or '.mp4' in self._url:
            if '/soaper/' in self._url:
                import urllib.parse
                inner_url = self._url.split('soaper/')[1]
                main_url = self._url.split('soaper/')[0]
                encoded_inner_url = urllib.parse.quote(inner_url, safe='')
                self._url = f'{main_url}soaper/{encoded_inner_url}'
                
            return True, f'{self._url}|Referer={referer}&verifypeer=false', SubTitle
        
        headers = {'User-Agent': UA,
                   'Referer': referer
                   }
        s = requests.session()

        req = s.get(self._url, headers=headers)

        hls_url = re.search(r'file:"([^"]*)"', req.text).group(1)
        hls_url = re.sub(r'\/\/\S+?=', '', hls_url).replace('#2', '')

        try:
            hls_url = base64.b64decode(hls_url).decode('utf-8') 
        except Exception: 
            return self._getMediaLinkForGuest(self._url + f'?Referer={referer}')

        set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
        if set_pass.startswith("//"):
            set_pass = f"https:{set_pass}"           

        if hls_url:
            return True, hls_url + '|User-Agent=' + UA + '&Referer=' + referer

        return False, False
