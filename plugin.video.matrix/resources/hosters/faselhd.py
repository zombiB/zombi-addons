#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'faselhd')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        api_call = ''
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('referer','https://www.faselhd.top/')
        data = oRequest.request()

        oParser = cParser()
        sPattern = '"file":"(.+?)","'
        aResult = oParser.parse(data, sPattern)
      # (.+?) ([^<]+) .+?
        if aResult[0] is True:
            url2 = aResult[1][0]
            oRequestHandler = cRequestHandler(url2)
            sHtmlContent2 = oRequestHandler.request()
            core = url2.replace('\\','').replace("['",'').replace("']",'')
            

            sPattern = ',RESOLUTION=(.+?),.+?(http.+?m3u8)'
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0] is True:
            
            #initialisation des tableaux
                url=[]
                qua=[]
            
            #Replissage des tableaux
                for i in aResult[1]:
                    url.append(str(i[1]))
                    qua.append(str(i[0]).split('x')[1]+"p")
                api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url 
#############################################################
#
# big thx to Rgysoft for this code
# From this url https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/blob/master/IPTVPlayer/tsiplayer/host_faselhd.py
#################################################################
	#
        if 'adilbo' in data:
        	t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        	t_int = re.findall('/g.....(.*?)\)', data, re.S)
        	if t_script and t_int:
        	    script = t_script[0].replace("'",'')
        	    script = script.replace("+",'')
        	    script = script.replace("\n",'')
        	    sc = script.split('.')
        	    page = ''
        	    for elm in sc:
                        c_elm = base64.b64decode(elm+'==').decode()
                        t_ch = re.findall('\d+', c_elm, re.S)
                        if t_ch:
                        	nb = int(t_ch[0])+int(t_int[0])
                        	page = page + chr(nb)
        	    t_url = re.findall('file":"(.*?)"', page, re.S)
        	    if t_url:
                	api_call = t_url[0].replace('\\','').replace("['",'').replace("']",'')
                	core = api_call
                	oRequest = cRequestHandler(api_call)
                	sHtmlContent = oRequest.request()
                	sPattern =  ',RESOLUTION=(.+?),.+?index(.+?)token='
                	oParser = cParser()
                	aResult = oParser.parse(sHtmlContent, sPattern)
                	if aResult[0] is True:
        	            url=[]
        	            qua=[]
        	            base= ''
        	            for i in aResult[1]:
                        	base= 'index' + str(i[1])
                        	url.append(core.replace('master.m3u8?',base))
                        	qua.append(str(i[0]))
        	            api_call = dialog().VSselectqual(qua, url)
 
        	    if api_call:
                	return True, api_call + '|User-Agent=' + UA
                	
        	    return False, False