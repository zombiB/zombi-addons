#-*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re
import requests
import base64, json
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mcloud', 'mCloud/VizCLoud')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('#')[0]
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

        api_call = decodeVidstream(self._url)
        api_call = api_call.replace('\\','')+"|Referer=https://mcloud.bz/"

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False

def decodeVidstream(query):
	from requests.compat import urlparse
	link = ''
	ref = query
	hd ={'user-agent':  UA,'Referer': ref}
	domain = urlparse(query).netloc
	domain = 'vidplay.site' if 'vidplay' in domain else domain
	futokenurl = 'https://'+domain+'/futoken'
	futoken = requests.get(futokenurl, verify=False).text

	k=re.findall("k='([^']+)'",futoken,re.DOTALL)[0]
	if 'vidplay' in query:
		query = query.split('/e/')[1].split('?')

	else:
		query = query.split('e/')[1].split('?')
          
	v = encode_id(query[0])
	a = [k];
	for i in range(len(v)):
		w = ord(k[i % len(k)])
		z = ord(v[i])
		x=int(w)+int(z)
		a.append(str(x))#

	urlk = 'https://'+domain+'/mediainfo/'+",".join(a)+'?'+query[1]

	ff=requests.get(urlk, headers=hd,verify=False).text
	if 'status":200' in ff:
		srcs = (json.loads(ff)).get('result',None).get('sources',None)
		for src in srcs:
			fil = src.get('file',None)
			if 'm3u8' in fil:
				link = fil+'|User-Agent='+UA+'&Referer='+ref
				break
	
	return link

def encode_id(id_):
	def endEN(t, n) :
		return t + n;
	
	def rLMxL(t, n):
		return t < n;
	
	def VHtgA (t, n) :
		return t % n;
	
	def DxlFU(t, n) :
		return rLMxL(t, n);
	
	def dec2(t, n) :
		o=[]
		s=[]
		u=0
		h=''
		for e in range(256):
			s.append(e)
	
		for e in range(256):
			u = endEN(u + s[e],ord(t[e % len(t)])) % 256
			o = s[e];
			s[e] = s[u];
			s[u] = o;
		e=0
		u=0
		c=0
		for c in range(len(n)):
			e = (e + 1) % 256
			o = s[e]
			u = VHtgA(u + s[e], 256)
			s[e] = s[u];
			s[u] = o;
			try:
				h += chr((n[c]) ^ s[(s[e] + s[u]) % 256]);
			except:
				h += chr(ord(n[c]) ^ s[(s[e] + s[u]) % 256]);

		return h
		
	
	klucze = requests.get('https://raw.githubusercontent.com/matecky/bac/keys/keys.json', verify=False).json()
	k1 = klucze[0]
	k2 = klucze[1]
	cbn = dec2(k1,id_)
	cbn = cbn.encode('Latin_1')
	cbn = dec2(k2,cbn)
	cbn = cbn.encode('Latin_1')

	vrfx = base64.b64encode(cbn)#
	v = vrfx.decode('utf-8')
	v = v.replace('/','_')
	return v	