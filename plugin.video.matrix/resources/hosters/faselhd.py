#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'faselhd'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'faselhd'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        VSlog("getMediaLink")
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        data = oRequest.request()
#############################################################
#
# big thx to Rgysoft for this code
# From this url https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/blob/master/IPTVPlayer/tsiplayer/host_faselhd.py
#################################################################
	#
        if 'adilbo_HTML_encoder' in data:
			t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
			t_int = re.findall('/g.....(.*?)\)', data, re.S)
			if t_script and t_int:
				script = t_script[0].replace("'",'')
				script = script.replace("+",'')
				script = script.replace("\n",'')
				sc = script.split('.')
				page = ''
				for elm in sc:
						c_elm = base64.b64decode(elm+'==')
						t_ch = re.findall('\d+', c_elm, re.S)
						if t_ch:
							nb = int(t_ch[0])+int(t_int[0])
							page = page + chr(nb)
				t_url = re.findall('file":"(.*?)"', page, re.S)
				if t_url:
					api_call = t_url[0].replace('\\','').replace("['",'').replace("']",'')


				if (api_call):
					return True, api_call+'|User-Agent=' + UA 
					
				return False, False