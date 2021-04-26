#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
import unicodedata
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
import re
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Lien direct'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'lien_direct'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''
        
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
    def gethost(self, sUrl):
        sPattern = 'https*:\/\/(.+?)\/.+?'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''   

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = self.__sUrl.replace("ddsdd","upbbom")
        api_call = self.__sUrl.replace("ffsff","moshahda")
        api_call = self.__sUrl.replace("rrsrr","cimanow")
        #full moviz lien direct final nowvideo
            

        if 'pixsil' in api_call:
            api_call = api_call.split('|')[0] + '|Referer=http://www.mangacity.org/jwplayer/player.swf'
 	   
        if 'moshahda' in api_call:


            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA + '&Referer=https://moshahda.online' 
 

       
        if 'akwam.download' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false' 
        if 'cimanow' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|AUTH=TLS&verifypeer=false' + '&User-Agent=' + UA + '&Referer=' + 'https://en.cimanow.cc'
       
        if '+' in api_call:
            api_call = api_call.replace("[","%5B").replace("]","%5D").replace("+","%20")
        	
        if 'bittube.video/videos/' in api_call:
            api_call = api_call + '-1080.mp4' 
            api_call = api_call.replace("/videos/embed/","/download/videos/")
	   
        if 'goal4live.com' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA 



        if 'fushaar' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            api_call = api_call + '|User-Agent=' + UA  + '&Referer=' + self.__sUrl
        if 'egybest' in api_call:
            import requests
            oParser = cParser()
            sHtmlContent=requests.get(api_call).content
        	
            sPattern =  ',RESOLUTION=(.+?),.+?(http.+?.m3u8)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
               url=[]
               qua=[]
               for i in aResult[1]:
                  url.append(str(i[1]))
                  qua.append(str(i[0]).split('x')[1]+"p")
               api_call = dialog().VSselectqual(qua, url)

            
        #Special pour hd-stream.in et film-streaming.co
        if '/embed/' in api_call:
            oRequest = cRequestHandler(api_call)
            sHtmlContent = oRequest.request()
            sPattern =  'src="(.+?)" scrolling="(.+?)">'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                #initialisation des tableaux
                url=[]
                qua=[]
                api_call = ''
                #Replissage des tableaux
                for i in aResult[1]:
                    url.append(str(i[0]).split('?link=', 1)[1].split('&channel_id', 1)[0])
                    qua.append(str(i[1]))

                #Afichage du tableau
                api_call = dialog().VSselectqual(qua, url)
        if 'playlist.m3u8' in api_call:
            base = re.sub(r'(playlist.m3u8*.+)','',api_call)
            core = api_call.split('playlist.m3u8', 1)[0]
            oRequest = cRequestHandler(api_call)
            sHtmlContent = oRequest.request()
            sPattern =  ',NAME="(.+?)",.+?(chunklist.+?.m3u8)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                #initialisation des tableaux
                url=[]
                qua=[]
                api_call = ''
                #Replissage des tableaux
                for i in aResult[1]:
                    url.append( core +'chunklist'+str(i[1]))
                    qua.append(str(i[0]))

                #Afichage du tableau
                api_call = dialog().VSselectqual(qua, url)
            sPattern =  ',NAME="(.+?)",.+?(http.+?.m3u8)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                #initialisation des tableaux
                url=[]
                qua=[]
                api_call = ''
                #Replissage des tableaux
                for i in aResult[1]:
                    url.append('http'+str(i[1]))
                    qua.append(str(i[0]))

                #Afichage du tableau
                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call 
            
        return False, False