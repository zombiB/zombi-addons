# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.util import Quote
 
SITE_IDENTIFIER = 'yallalive'
SITE_NAME = 'Yallalive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN, 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
   
    oGui.setEndOfDirectory()
	
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
	# (.+?) .+? 
    sPattern = '<a class="alba_sports_events_link" href="(.+?)" target="_blank" title.+?<div class="event_inner"><div class="team-aria team-first"><div class="team"><div class="alba-team_logo"><img alt="(.+?)" title=.+?<div class="matchTime">(.+?)</div>.+?<img alt="(.+?)" title='


    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1] +' - '+ aEntry[3]
            sThumb = ""
            siteUrl =  aEntry[0]
            sDesc = aEntry[2]+ " KSA"
			
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
 
    oGui.setEndOfDirectory()
			
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')                    
       
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "redirectUrl='(.+?)';"
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sUrl = aResult[1][0]


    oRequestHandler = cRequestHandler(sUrl)
    hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','Origin' : 'yallalive.id','Referer' : 'https://yallalive.id/'}
    St=requests.Session()              
    sHtmlContent = St.get(sUrl,headers=hdr).content.decode('utf-8')        

    # (.+?) .+? ([^<]+)
    sPattern = 'href="(.+?)" target="search_iframe">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = sMovieTitle+' '+aEntry[1]
            url = aEntry[0]
            if '.m3u8' in url:           
                url = url.split('=')[1] 
            if '.php' in url:           
                oRequestHandler = cRequestHandler(url)
                hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36','referer' : 'https://riyadh.himtree.com/'}
                St=requests.Session()
                sHtmlContent = St.get(url,headers=hdr)
                sHtmlContent2 = sHtmlContent.content 
                sPattern =  'src="(.+?)"'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
                sPattern =  '(http[^<]+m3u8)'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
                sPattern =  "source: '(.+?)',"
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
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
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + URL_MAIN
            Referer = aEntry[0].split('live')[0]
            VSlog(sHosterUrl)   
            if 'amazonaws.com'  in sHosterUrl:
                sHosterUrl = url + '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer='+Referer
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = "'link': u'(.+?)',"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            if '.php?' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'source: "(.+?)",'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
                   url = aResult[1][0]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = St.get(url).content
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if aResult[0]:
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
                if aResult[0]:
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
            sHosterUrl = url+ '|User-Agent=' + "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" + '&Referer=' + URL_MAIN
            sMovieTitle = 'link'
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle+' '+sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    oGui.setEndOfDirectory()