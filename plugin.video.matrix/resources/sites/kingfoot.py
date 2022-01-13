#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.util import Unquote, Quote, QuotePlus
import xbmcgui
import re
import unicodedata
 
SITE_IDENTIFIER = 'kingfoot'
SITE_NAME = 'kingfoot'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://king-shoot.tv/'



SPORT_LIVE = ('https://king-shoot.tv/today-matches/', 'showMovies')



FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = ''+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
            
    sPattern =  'href="https://.+?/today-matches/(.+?)" />' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 

# ([^<]+) .+? (.+?)
    import requests
    s = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
    r = s.get('https://web-api.golato.net/webapi/matches/'+m3url, headers=headers)
    sHtmlContent = r.content.decode('utf8')
    sPattern = '"id":"(.+?)","sitemap":1,"api_matche_id":"(.+?)",.+?,"home_en":"(.+?)",.+?,"away_en":"(.+?)",'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[2] +' - '+ aEntry[3]
            sThumbnail = ""
            siteUrl =  "https://king-shoot.tv/gen-matche/"+aEntry[0]+'/'+aEntry[1]
            sInfo = ''
			
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('murl', aEntry[0])
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters4', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showHosters4():
    import requests,re,json
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    murl = oInputParameterHandler.getValue('murl')
    
    oRequestHandler = cRequestHandler(sUrl)
    hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','Origin' : '1xnews.online','referer' : sUrl}
    VSlog(sUrl)
    rurl = 'https://1xnews.online/home/matche/'+murl 
    St=requests.Session()              
    oRequestHandler = cRequestHandler(rurl)
    sHtmlContent = St.get(rurl).content.decode('utf-8')

    sPattern = '"link":"(.+?)","server_name":"(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[0]
            if '.php?' in url:
                oRequestHandler = cRequestHandler(url)
                hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','Origin' : 'dalbouh.club','referer' : 'https://1xnews.online/'}
                data = {'watch':'1'}
                St=requests.Session()
                sHtmlContent = St.get(url,headers=hdr)
                sHtmlContent2 = sHtmlContent.content
                oParser = cParser()
                sPattern =  'src="(.+?)"'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                   url = aResult[1][0]
                oRequestHandler = cRequestHandler(url)
                hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','Origin' : 'dalbouh.club','referer' : 'https://dalbouh.club/'}
                data = {'watch':'1'}
                St=requests.Session()
                sHtmlContent = St.get(url,headers=hdr)
                sHtmlContent2 = sHtmlContent.content
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                   url = aResult[1][0]
            if 'multi.html' in url:
                url2 = url.split('=') 
                live = url2[1].replace("&ch","")
                ch = url2[2]
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  "var src = (.+?),"
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                    url2 = aResult[1][0].split('hls:')
                    url2 = url2[1].split('+')
                    url2 = url2[0].replace("'","")
                    url = url2+live+'/'+ch+'.m3u8'
            if '/dash/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = St.get(url).content
                regx = '''var s = '(.+?)';.+?url="(.+?)".+?s;'''
                var = re.findall(regx,sHtmlContent4,re.S)
                if var:
                   a = var[0][0]
                   a = a.replace('\\','')
                   b = var[0][1]
                   url = 'https://video-a-sjc.xx.fbcdn.net/hvideo-ash66'+a
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + 'https://king-shoot.com/'
            sMovieTitle = aEntry[1]
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    sPattern = "'link': u'(.+?)',"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            if '.php?' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                   url = aResult[1][0]
            if 'multi.html' in url:
                url2 = url.split('=') 
                live = url2[1].replace("&ch","")
                ch = url2[2]
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  "var src = (.+?),"
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
                    url2 = aResult[1][0].split('hls:')
                    url2 = url2[1].split('+')
                    url2 = url2[0].replace("'","")
                    url = url2+live+'/'+ch+'.m3u8'
            if '/dash/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = St.get(url).content
                regx = '''var s = '(.+?)';.+?url="(.+?)".+?s;'''
                var = re.findall(regx,sHtmlContent4,re.S)
                if var:
                   a = var[0][0]
                   a = a.replace('\\','')
                   b = var[0][1]
                   url = 'https://video-a-sjc.xx.fbcdn.net/hvideo-ash66'+a
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + 'https://king-shoot.com/'
            sMovieTitle = 'link'
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)


    oGui.setEndOfDirectory()
	
def showHosters2():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sUrl2 = sUrl.split('mubasher=')[1]
    sUrl2 = sUrl2.split('&key')[0]
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #recup du lien mp4
    sPattern =  'source: "(.+?)",' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = aResult[1][0].replace('"+live+"',sUrl2) + '|User-Agent=' + UA + '&Referer=' + sUrl
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()
