from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.lib.comaddon import progress
from resources.hosters.hoster import iHoster
import re,urllib2,urllib,xbmc


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'samaup'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'samaup'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        if '.cc' in sUrl:
            self.__sUrl = self.__sUrl.replace(".cc",".org")
        if 'embed' in sUrl:
            self.__sUrl = self.__sUrl.replace("embed-","")
        self.__sUrl = self.__sUrl.split('-')[0]

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        #methode1 
        #lien indirect
        if 'samaup' in sHtmlContent:
            POST_Data              = {}
            POST_Data['op']        = re.findall('input type="hidden" name="op" value="([^<>"]*)"',sHtmlContent)[0]
            #POST_Data['usr_login'] = re.findall('input type="hidden" name="usr_login" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['id']        = re.findall('input type="hidden" name="id" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['fname']     = re.findall('input type="hidden" name="fname" value="([^<>"]*)"',sHtmlContent)[0]
            #POST_Data['referer']   = re.findall('input type="hidden" name="referer" value="([^<>"]*)"',sHtmlContent)[0]
            #POST_Data['hash']      = re.findall('input type="hidden" name="hash" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['method_free']   = re.findall('<input type="submit" name="method_free" class=".+?" value="([^<>"]*)">',sHtmlContent)[0]
            
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            headers = {'User-Agent': UA ,
                       'Host' : 'www.samaup.org',
                       'Referer' : self.__sUrl ,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Content-Type': 'application/x-www-form-urlencoded'}
            
            postdata = urllib.urlencode(POST_Data)
            
            req = urllib2.Request(self.__sUrl,postdata,headers)
            
            xbmc.sleep(10*1000)
            
            response = urllib2.urlopen(req)
            sHtmlContent = response.read()
            #print sHtmlContent
            response.close()

        #methode1 
        #lien indirect
        if 'samaup' in sHtmlContent:
            POST_Data              = {}
            POST_Data['op']        = re.findall('input type="hidden" name="op" value="([^<>"]*)"',sHtmlContent)[0]
            #POST_Data['usr_login'] = re.findall('input type="hidden" name="usr_login" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['id']        = re.findall('input type="hidden" name="id" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['referer']     = re.findall('input type="hidden" name="referer" value="([^<>"]*)"',sHtmlContent)[0]
            #POST_Data['referer']   = re.findall('input type="hidden" name="referer" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['rand']      = re.findall('input type="hidden" name="rand" value="([^<>"]*)"',sHtmlContent)[0]
            POST_Data['method_free']   = re.findall('input type="hidden" name="method_free" value="([^<>"]*)">',sHtmlContent)[0]
            
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            headers = {'User-Agent': UA ,
                       'Host' : 'www.samaup.org',
                       'Referer' : self.__sUrl ,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Content-Type': 'application/x-www-form-urlencoded'}
            
            postdata = urllib.urlencode(POST_Data)

            
            req = urllib2.Request(self.__sUrl,postdata,headers)
            
            xbmc.sleep(10*1000)
            
            response = urllib2.urlopen(req)
            sHtmlContent = response.read()
            response.close()

             #print sHtmlContent
                         
            #fh = open('c:\\test.txt', "w")
            #fh.write(sHtmlContent)
            #fh.close()
     
        sPattern = '<div id="direct_link"><a href="(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call 

        return False, False