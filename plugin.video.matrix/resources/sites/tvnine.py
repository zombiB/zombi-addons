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
 
SITE_IDENTIFIER = 'tvnine'
SITE_NAME = 'Tv96'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = ('https://www.tv96.tv', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

   
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+? (.+?)

    sPattern = '<div class="containerMatch"><a href="(.+?)" target=.+?<div style="font-weight: bold">(.+?)</div>.+?<div class="matchTime">(.+?)</div>.+?<div style="font-weight: bold">(.+?)</div>'



    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1]+' vs '+aEntry[3]
            sYear = ""
            sThumb = ""
            siteUrl = aEntry[0]
            sDesc = aEntry[2]+' GMT+1'
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()                   
    UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1' 
    # (.+?) # ([^<]+) .+? 
    if 'data-embed=' in sHtmlContent :
        sPattern = 'data-embed="(.+?)">(.+?)</li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
    else :
        sPattern = 'onclick="location.href=(.+?);">(.+?)</li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("'","")
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
            data = oRequestHandler.request()

            oParser = cParser()
    # (.+?) # ([^<]+) .+? 
            sPattern = 'source: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if '.png' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = 'hls: "(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url 
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   if ".php" in url:
                       oRequestHandler = cRequestHandler(url)
                       data = oRequestHandler.request() 
                       sPattern = "source: '(.+?)',"
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0] is True:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url+ "|Referer=" + URL_MAIN
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = url + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster != False:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                   sHosterUrl = url.replace("https://tv.hd44.net/p/phone.html?src=","") 
 
                   UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1' 
                   sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)  
    # (.+?) # ([^<]+) .+? 
            sPattern = 'hls: "(.+?)"'
				
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
            sPattern = "hls: '(.+?)'"
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url+ "|Referer=" + URL_MAIN 
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = '(http.+?m3u8)'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = url + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)   
    # (.+?) # ([^<]+) .+? 
            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
            if aResult[0] is True:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url+ "|Referer=" + URL_MAIN
                   sMovieTitle = sTitle
                   if 'vimeo' in url:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
           

             
    oGui.setEndOfDirectory() 
	