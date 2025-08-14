#-*- coding: utf-8 -*-

import requests
import base64, json
from urllib.parse import unquote, urlparse, quote
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
from resources.sites.cinezone import rc4, reverse, subst, subst_, mapp

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mcloud', 'mCloud/VizCLoud')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('$')[0]
        self._url0 = str(url)

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        VSlog(self._url0)

        if ('sub.info' in self._url0):
            SubTitle = self._url0.split('sub.info=')[1]
            if '&t=' in SubTitle:
                SubTitle = SubTitle.split('&t=')[0]
            else:
                SubTitle = SubTitle
            oRequest0 = cRequestHandler(SubTitle)
            sHtmlContent0 = oRequest0.request().replace('\\','')
            oParser = cParser()

            sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
            aResult = oParser.parse(sHtmlContent0, sPattern)

            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
                SubTitle = dialog().VSselectsub(qua, url)
        else:
            SubTitle = ''


        url = urlparse(self._url)
        embed_id = self._url.rsplit('/e/')[1].split('?', 1)[0]
        source = url.hostname

        media_url = f"https://{source}/mediainfo/{embed_enc(embed_id, source)}?{url.query}&ads=0"
        req = requests.get(media_url).json()
        playlist = json.loads(embed_dec(req['result'], source))
        sources = playlist.get('sources')
        sources = [value.get("file") for value in sources]
        if sources:
            api_call = sources[0]
                    
        api_call = api_call.replace('\\','')

        if api_call:
            if ('http' in SubTitle):
                return True, quote(api_call, ':/?=&'), SubTitle
            else:
                return True, quote(api_call, ':/?=&')

        return False, False


def embed_enc(inp, source):
    source_keys = get_keys()
    try:
        keys = source_keys[source]
    except KeyError:
        keys = source_keys["vid2faf.site"]
    
    a = mapp(inp, keys[0], keys[1])
    a = reverse(a)
    a = rc4(keys[2], a)
    a = subst(a)
    a = reverse(a)
    a = mapp(a, keys[3], keys[4])
    a = rc4(keys[5], a)
    a = subst(a)
    a = rc4(keys[6], a)
    a = subst(a)
    a = reverse(a)
    a = mapp(a, keys[7], keys[8])
    a = subst(a)
    
    return a

def embed_dec(inp, source):
    source_keys = get_keys()
    try:
        keys = source_keys[source]
    except KeyError:
        keys = source_keys["vid2faf.site"]
    
    a = subst_(inp)
    a = mapp(a, keys[8], keys[7])
    a = reverse(a)
    a = subst_(a)
    a = rc4(keys[6], a)
    a = subst_(a)
    a = rc4(keys[5], a)
    a = mapp(a, keys[4], keys[3])
    a = reverse(a)
    a = subst_(a)
    a = rc4(keys[2], a)
    a = reverse(a)
    a = mapp(a, keys[1], keys[0])
    
    return a


def general_enc(key, inp):
    inp = quote(inp)
    e = rc4(key, inp)
    out = base64.b64encode(e.encode("latin-1")).decode()
    out = out.replace('/', '_').replace('+', '-')
    return out

def general_dec(key, inp):
    inp = inp.replace('_', '/').replace('-', '+')
    i = str(base64.b64decode(inp),"latin-1")
    e = rc4(key,i)
    e = unquote(e)
    return e

def get_keys():
    oRequestHandler = cRequestHandler("https://raw.githubusercontent.com/giammirove/videogatherer/main/dist/keys.json")
    res = oRequestHandler.request(jsonDecode=True)
    if res is not None:
        keys = res["keys"]
    else:
        raise Exception("Unable to fetch keys")
    return keys