# -*- coding: utf-8 -*-

from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog
# from Cryptodome.Cipher import ARC4
from urllib.parse import urlparse
import re
import requests, base64, json

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []

    def GetUrls(self, url):
        sHtmlContent = GetHtml(url)
        sPattern = '<form action="([^"]+)'
        result = re.findall(sPattern, sHtmlContent)
        if result:
            NewUrl = f'https://multiup.io{result[0]}'.replace('/fr/download', '/en/mirror').replace('/en/download', '/en/mirror').replace('/download', '/en/mirror')
            sHtmlContent = GetHtml(NewUrl)

        sPattern = 'nameHost="([^"]+)"\s*link="([^"]+)'
        r = re.findall(sPattern, sHtmlContent)
        if not r:
            return False

        for aEntry in r:
            false_links = next((x for x in ['nitroflare', 'tubeload.', 'Facebook', 'fastdrive', 'megaup.net', 'openload', 'vidhd', 'oktube', 'mdiaload', 'fikper', 'turbobit', '1fichier',
                                            'mega.nz', 'rapidgator', 'ddownload', 'bowfile', 'uptobox', 'uptostream', 'wahmi', 'doodrive', 'highload', 'anonfiles', 'jawcloud', 'dailyuploads', 
                                            'videomega', 'prostream', 'fembed', 'filegage', 'streamlare', 'katfile', 'usersdrive', 'uploadbank', 'fastupload', 'fireload', 'vikingfile', 'workupload',
                                            'UseeNet', 'chomikuj', 'filefactory'] if x in aEntry[0]), None)
            if false_links:    
                continue
            sHosterUrl = aEntry[1]
            sLabel = 'Multiup - ' + aEntry[0]
            self.list.append(f'url={sHosterUrl}, label={sLabel}')

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
    import xbmcgui
    Yes = xbmcgui.Dialog().yesno(
        'موقع الملفات MultiUP محمي',
        'هل تريد تجربة الحصول على الروابط قد يكون الأمر بطيئًا.. لا يُنصح بذلك..',
        'إلغاء'
        )
    if Yes:
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
    return ' '
        
class cMegamax:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self, url):
        try:
            sHosterUrl = url.replace('download','iframe').replace(' ','')
            if 'leech' in sHosterUrl or '/e/' in sHosterUrl:
                return False
            oRequestHandler = cRequestHandler(sHosterUrl)
            oRequestHandler.enableCache(False)
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
                                    'X-Inertia-Partial-Component':'files/mirror/video',
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
        except:
            VSlog('Error to retrieve links')
            return []

class cVidNet:
    def __init__(self):
        self.name = "Vidsrc.net"
        self.mainUrl = "https://vidsrc.net"

    def server(self, video_type):
        if isinstance(video_type, str) and video_type.lower() == "movie":
            return {"id": self.name, "name": self.name, "src": f"{self.mainUrl}/embed/movie?tmdb={video_type}"}
        elif isinstance(video_type, dict) and video_type.get("type", "").lower() == "episode":
            return {"id": self.name, "name": self.name, "src": f"{self.mainUrl}/embed/tv?tmdb={video_type.get('show_id')}&season={video_type.get('season_number')}&episode={video_type.get('episode_number')}"}
        else:
            raise ValueError("Unsupported video type")

    def sSub(self, id):
            try:
                headers = { "User-Agent": "VLSub 0.10.2",
                                    "X-Requested-With": "XMLHttpRequest"}

                movie_id = id.replace('tt','')
                sUrl = f'https://rest.opensubtitles.org/search/imdbid-{movie_id}sublanguageid-ara'
              
                return sUrl

            except:
                return []

    def extract(self, link):

        sSubs = self.sSub(link.split('embed/')[1])

        oRequestHandler = cRequestHandler(link)
        oRequestHandler.addHeaderEntry('Referer', link)
        content = oRequestHandler.request()

        iframe_match = re.search(r'<iframe id="player_iframe".*?src="(.*?)"', content, re.DOTALL)
        if not iframe_match:
            raise Exception("Iframe not found")
        iframe_src = iframe_match.group(1)
        if iframe_src.startswith("//"):
            iframe_src = f"https:{iframe_src}"
        sReferer = f'https://{urlparse(iframe_src).netloc}/'

        oRequestHandler = cRequestHandler(iframe_src)
        oRequestHandler.addHeaderEntry('Referer', link)
        iframe_content = oRequestHandler.request()

        script_match = re.search(r"src: '(//vidsrc\.net/srcrcp/.*?)'", iframe_content)
        if not script_match:
            raise Exception("Script URL not found")
        script_url = script_match.group(1)
        if script_url.startswith("//"):
            script_url = f"https:{script_url}"

        oRequestHandler = cRequestHandler(script_url)
        oRequestHandler.addHeaderEntry('Referer', iframe_src)
        script_content = oRequestHandler.request()

        player_id_match = re.search(r"Playerjs.*file: ([a-zA-Z0-9]*?) ,", script_content)
        if not player_id_match:
            raise Exception("Player ID not found")
        player_id = player_id_match.group(1)

        encrypted_source_match = re.search(rf'<div id="{player_id}" style="display:none;">(.*?)</div>', script_content, re.DOTALL)
        if not encrypted_source_match:
            raise Exception("Encrypted source not found")
        encrypted_source = encrypted_source_match.group(1)

        decrypted_source = self.decode_url(player_id, encrypted_source)

        return {
        "source": decrypted_source,
        "subtitles": sSubs,
        "referer": sReferer,
        }
    
    def decode_url(self, enc_type, url):

        if enc_type == "NdonQLf1Tzyx7bMG":
            return self.bMGyx71TzQLfdonN(url)
        elif enc_type == "JoAHUMCLXV":
            return self.LXVUMCoAHJ(url)
        elif enc_type == "sXnL9MQIry":
            return self.Iry9MQXnLs(url)
        elif enc_type == "IhWrImMIGL":
            return self.IGLImMhWrI(url)
        elif enc_type == "xTyBxQyGTA":
            return self.GTAxQyTyBx(url)
        elif enc_type == "ux8qjPHC66":
            return self.C66jPHx8qu(url)
        elif enc_type == "eSfH1IRMyL":
            return self.MyL1IRSfHe(url)
        elif enc_type == "KJHidj7det":
            return self.detdj7JHiK(url)
        elif enc_type == "o2VSUnjnZl":
            return self.nZlUnj2VSo(url)
        elif enc_type == "Oi3v1dAlaM":
            return self.laM1dAi3vO(url)
        elif enc_type == "TsA2KGDGux":
            return self.GuxKGDsA2T(url)
        else:
            return None

    def bMGyx71TzQLfdonN(self, a):
        b = 3
        c = []
        for d in range(0, len(a), b):
            c.append(a[d:min(d + b, len(a))])
        return "".join(reversed(c))

    def Iry9MQXnLs(self, a):
        b = "pWB9V)[*4I`nJpp?ozyB~dbr9yt!_n4u"
        d = "".join(chr(int(a[i:i+2], 16)) for i in range(0, len(a), 2))
        c = ""
        for e, char in enumerate(d):
            c += chr(ord(char) ^ ord(b[e % len(b)]))
        e = ""
        for char in c:
            e += chr(ord(char) - 3)
        return self.decode_string(e)

    def IGLImMhWrI(self, a):
        b = a[::-1]
        c = "".join(chr(ord(char) + 13) if 'a' <= char <= 'm' or 'A' <= char <= 'M' else
                    chr(ord(char) - 13) if 'n' <= char <= 'z' or 'N' <= char <= 'Z' else char
                    for char in b)
        d = c[::-1]
        return self.decode_string(d)

    def GTAxQyTyBx(self, a):
        b = a[::-1]
        c = "".join(b[::2])
        return base64.b64decode(c).decode('utf-8')

    def C66jPHx8qu(self, a):
        b = a[::-1]
        c = "X9a(O;FMV2-7VO5x;Ao:dN1NoFs?j,"
        d = "".join(chr(int(b[i:i+2], 16)) for i in range(0, len(b), 2))
        e = "".join(chr(ord(d[i]) ^ ord(c[i % len(c)])) for i in range(len(d)))
        return e

    def MyL1IRSfHe(self, a):
        b = a[::-1]
        c = "".join(chr(ord(ch) - 1) for ch in b)
        d = "".join(chr(int(c[i:i+2], 16)) for i in range(0, len(c), 2))
        return d

    def detdj7JHiK(self, a):
        b = a[10:-16]
        c = "3SAY~#%Y(V%>5d/Yg\"\$G[Lh1rK4a;7ok"
        d = base64.b64decode(b).decode('utf-8')
        e = c * ((len(d) + len(c) - 1) // len(c))[:len(d)]
        f = "".join(chr(ord(d[i]) ^ ord(e[i])) for i in range(len(d)))
        return f

    def nZlUnj2VSo(self, a):
        b = {
            'x': 'a', 'y': 'b', 'z': 'c', 'a': 'd', 'b': 'e', 'c': 'f', 'd': 'g', 'e': 'h', 'f': 'i',
            'g': 'j', 'h': 'k', 'i': 'l', 'j': 'm', 'k': 'n', 'l': 'o', 'm': 'p', 'n': 'q', 'o': 'r',
            'p': 's', 'q': 't', 'r': 'u', 's': 'v', 't': 'w', 'u': 'x', 'v': 'y', 'w': 'z', 'X': 'A',
            'Y': 'B', 'Z': 'C', 'A': 'D', 'B': 'E', 'C': 'F', 'D': 'G', 'E': 'H', 'F': 'I', 'G': 'J',
            'H': 'K', 'I': 'L', 'J': 'M', 'K': 'N', 'L': 'O', 'M': 'P', 'N': 'Q', 'O': 'R', 'P': 'S',
            'Q': 'T', 'R': 'U', 'S': 'V', 'T': 'W', 'U': 'X', 'V': 'Y', 'W': 'Z'
        }
        return "".join(b.get(char, char) for char in a)

    def laM1dAi3vO(self, a):
        b = a[::-1] 
        c = c.replace("-", "+").replace("_", "/") 
        d = self.decode_string(c)
        e = ""
        f = 5 
        for ch in d:
            e += chr(ord(ch) - f) 
        return e

    def GuxKGDsA2T(self, a):
        b = a[::-1]
        c = b.replace("-", "+").replace("_", "/")
        d = self.decode_string(c)
        e = ""
        f = 7
        for ch in d:
            e += chr(ord(ch) - f)
        return e

    def LXVUMCoAHJ(self, a):
        b = a[::-1]
        c = b.replace("-", "+").replace("_", "/")
        d = self.decode_string(c)
        e = ""
        f = 3
        for ch in d:
            e += chr(ord(ch) - f)
        return e

    def decode_string(self, c):
        try:
            decoded_bytes = base64.b64decode(c)
            return decoded_bytes.decode('utf-8')
        except (UnicodeDecodeError):
            try:
                return decoded_bytes.decode('latin-1')
            except Exception as e:
                return None 

class cVidPro:
    def __init__(self):
        self.name = "embed.su"
        self.mainUrl = "https://embed.su"

    def sSub(self, id):
        try:
            headers = { "User-Agent": "VLSub 0.10.2",
                                "X-Requested-With": "XMLHttpRequest"}

            movie_id = id.replace('tt','')
            sUrl = f'https://rest.opensubtitles.org/search/imdbid-{movie_id}sublanguageid-ara'

            data = requests.get(sUrl, headers=headers).json()
            return [item['SubDownloadLink'].replace(".gz", "").replace("download/", "download/subencoding-utf8/") for item in data]

        except:
            return []

    def extract(self, sUrl):
        sSub = ''
        html_search = self.make_get_request(sUrl, f'{self.mainUrl}/')

        hash_value = ''
        match = re.search(r"atob\(`(.*?)`\)", html_search)
        if match:
            encoded_json = match.group(1)
            decoded_json = base64.b64decode(encoded_json).decode('utf-8')
            hashload = json.loads(decoded_json)
            hash_value = hashload["hash"]
       
        decode_hash = lambda a: base64.b64decode(a[::-1] + '==').decode('utf-8')
        parse_hash = json.loads(decode_hash(hash_value))

        url_direct = ''
        for item in parse_hash:
                url_direct = f"{self.mainUrl}/api/e/{item['hash']}"
                data_direct = self.make_get_request(url_direct, f'{self.mainUrl}/')
                data_direct = json.loads(data_direct) if data_direct else {}
                if not data_direct or 'source' not in data_direct:
                    continue
                
                else:
                    arabic_subtitles = None
                    for subtitle in data_direct["subtitles"]:
                        if subtitle["label"].lower() == "arabic":
                            arabic_subtitles = subtitle["file"]
                    sSub = arabic_subtitles if arabic_subtitles else data_direct["subtitles"][0]["file"]

                    nUrl = data_direct['source']
                    if '?url=' in nUrl:
                        nUrl = nUrl.split('?url=')[1]

                    return f"{nUrl}|Referer={self.mainUrl}/?sub.info={sSub}"

        if f"{self.mainUrl}/api/e/" in url_direct:
                json_response = self.make_get_request(url_direct, f'{self.mainUrl}/')
                json_data = json.loads(json_response) if json_response else {}
                if 'source' in json_data:
                    url_direct = json_data['source']
                else:
                    raise Exception('No source found in JSON response')

        q = ''
        match = re.search(r'\?base\=([A-z0-9.]+)', url_direct, re.IGNORECASE)
        if match:
                q = match.group(1)

        endpoint = ''
        match = re.search(r'proxy\/[A-z]+([A-z0-9_\/\.\-]+\.m3u8)', url_direct, re.IGNORECASE)
        if match:
                endpoint = match.group(1)

        if q and endpoint:
                return f"https://{q}{endpoint}|Referer={sUrl}"

    def make_get_request(self, url, referer):
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('Referer', referer)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0')
        return oRequestHandler.request()

class cVidVip:
    def __init__(self):
        self.list = []
        self.name = "Vidsrc.vip"
        self.mainUrl = "https://vidsrc.vip/"
        self.mainDL = "https://dl.vidsrc.vip"

    def extract(self, sUrl):
        if '/movie' in sUrl:
            sId = re.search(r'/movie/(\d+)', sUrl).group(1)
            nUrl = f'{self.mainDL}/movie/{sId}'
        else:
            sId = sUrl.split('tv/')[1].split('&server=')[0]
            nUrl = f'{self.mainDL}/tv/{sId}'

        oParser = cParser()
        oRequestHandler = cRequestHandler(nUrl)
        oRequestHandler.addHeaderEntry('Referer', self.mainUrl)
        oRequestHandler.addHeaderEntry('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Connection', 'keep-alive')
        oRequestHandler.addHeaderEntry('Host', self.mainDL.split('https://')[1])
        oRequestHandler.addHeaderEntry('Upgrade-Insecure-Requests', '1')
        sHtmlContent = oRequestHandler.request()

        sSub = ''
        sPattern = '<option value=["\']([^"\']+)["\']>Arabic'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sSub = (base64.b64decode(aResult[1][0]).decode('utf8',errors='ignore')).split('?u=')[1].split('&n=')[0]

        sPattern = "data-url='([^']+)'>Download</span>.+?<td>(.+?)</td>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                
                sHosterUrl = base64.b64decode(aEntry[0]).decode('utf8',errors='ignore')
                sQual = aEntry[1]
                
                self.list.append(f'url={sHosterUrl}?sub.info={sSub}, qual={sQual}')

            return self.list