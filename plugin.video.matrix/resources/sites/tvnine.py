# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', icons + '/Sport.png', oOutputParameterHandler)
    
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

    sPattern = '<div class="containerMatch"><a href="(.+?)"><div class="row">.+?<img alt="Image" src="(.+?)" style.+?<div style="font-weight: bold">(.+?)</div>.+?<div class="matchTime">(.+?)</div>.+?<div style="font-weight: bold">(.+?)</div>'



    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[2]+' vs '+aEntry[4]
            sYear = ""
            sThumb = aEntry[1]
            siteUrl = aEntry[0]
            sDesc = aEntry[3]+' GMT+1'
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
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
        VSlog(aResult)
    else :
        sPattern = 'onclick="location.href=(.+?);">(.+?)</li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0]:
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
            if aResult[0]:
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
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = 'hls.loadSource(.+?);'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
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
                   sHosterUrl = url.replace('("',"").replace('")',"")
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = 'hls: "(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
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
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
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
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if 'jsdelivr' in url:
                       continue
                   if 'sotchoum' in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1]
                   if 'href.li' in url:
                      url = url.replace("https://href.li/?","") 
                   if 'realbit' in url:
                      url = getHosterIframe(url,sUrl) 
                   if 'sportsonline' in url:
                      url = getHosterIframe(url,sUrl) 
                   if 'dinnn' in url:
                      url = getHosterIframe(url,sUrl)  
                   if ".php" or ".html" in url:
                       oRequestHandler = cRequestHandler(url)
                       data = oRequestHandler.request() 
                       sPattern = "source: '(.+?)',"
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                       sPattern = '<iframe src="(.+?)" height'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                       sPattern = 'source: "(.+?)",'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                   sHosterUrl = url.replace("https://tv.hd44.net/p/phone.html?src=","") 
 
                   UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1' 
                   sHosterUrl = sHosterUrl   
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)  
    # (.+?) # ([^<]+) .+? 
            sPattern = 'hls: "(.+?)"'
				
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
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
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
            sPattern = "hls: '(.+?)'"
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
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
                   sHosterUrl = url 
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
    # (.+?) # ([^<]+) .+? 
            sPattern = '(http.+?m3u8)'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)   
    # (.+?) # ([^<]+) .+? 
            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 
                   if 'href.li' in url:
                      url = url.replace("https://href.li/?","") 
                   if ".php" or ".html" in url:
                       oRequestHandler = cRequestHandler(url)
                       data = oRequestHandler.request() 
                       sPattern = "source: '(.+?)',"
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          oOutputParameterHandler = cOutputParameterHandler()
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
                       sPattern = '<iframe src=["\']([^"\']+)["\']'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:                  
                              url2 = aEntry.replace("https://href.li/?","") 
                              if url2.startswith('//'):
                                 url2 = 'https:' + url2
                              if '?src=' in url2:
                                 url2 = url2.split('?src=')[1] 
                              sHosterUrl = url2
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                              if 'sportsonline' in sHosterUrl:
                                sHosterUrl = getHosterIframe(url2,url) 
                                sHosterUrl = sHosterUrl + "|Referer=" + url  
                              if 'dynamic' in url2:
                                sHosterUrl = url2 + "|Referer=" + url 
                              if 'mangomolo' in sHosterUrl:
                                oRequestHandler = cRequestHandler(sHosterUrl)
                                data = oRequestHandler.request() 
                                sPattern = 'src: ["\']([^"\']+)["\']'
                                aResult = oParser.parse(data, sPattern)
                                if aResult[0]:
                                    for aEntry in aResult[1]:           
                                        sHosterUrl = aEntry
                              if 'live7' in sHosterUrl:
                                oRequestHandler = cRequestHandler(sHosterUrl)
                                data = oRequestHandler.request() 
                                sPattern = '<iframe src=["\']([^"\']+)["\']'
                                aResult = oParser.parse(data, sPattern)
                                if aResult[0]:
                                    oOutputParameterHandler = cOutputParameterHandler()
                                    for aEntry in aResult[1]:           
                                        sHosterUrl = aEntry  + "|Referer=https://www.live7.pro/"          

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
                       sPattern = 'source: "(.+?)",'
                       aResult = oParser.parse(data, sPattern)
                       if aResult[0]:
                          for aEntry in aResult[1]:
            
                              url = aEntry
                              if url.startswith('//'):
                                 url = 'https:' + url
                              if '?src=' in url:
                                 url = url.split('?src=')[1] 
                              sHosterUrl = url
                              sMovieTitle = sTitle
                              if 'vimeo' in sHosterUrl:
                                  sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                              oHoster = cHosterGui().checkHoster(sHosterUrl)
                              if oHoster:
                                  oHoster.setDisplayName(sMovieTitle)
                                  oHoster.setFileName(sMovieTitle)
                                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
                                  
                   sHosterUrl = url.replace("https://tv.hd44.net/p/phone.html?src=","") 
                   if 'sportsonline' in sHosterUrl:
                        continue                   
                   sHosterUrl = sHosterUrl   
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

            sPattern = '["\']hls["\']:\s*["\']([^"\']+)["\']'
				
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
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
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                      
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

            sPattern = 'hls:\s*["\']([^"\']+)["\']'
				
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
 
                   if 'googleusercontent' in url:
                       continue
                   if '.webp' in url:
                       continue
                   if '.jpg' in url:
                       continue
                   if '.' not in url:
                       continue
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                      
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

            sPattern = 'url.+?(http.+?m3u8)'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
                   if 'm3u8' not in url:
                       continue
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler) 

            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
            
                   url = aEntry
                   if url.startswith('//'):
                      url = 'https:' + url
                   if '?src=' in url:
                      url = url.split('?src=')[1] 
                   sHosterUrl = url
                   sMovieTitle = sTitle
                   if 'vimeo' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

            sPattern = "document.write(.+?)</script>"
            aResult = oParser.parse(data, sPattern)
            
            if aResult[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               for aEntry in aResult[1]:
                   sContent = aEntry.replace("(unescape('","").replace("'))","")
                   import urllib
                   sHtmlContent = urllib.parse.unquote(sContent)

                   sPattern = '<video src=["\']([^"\']+)["\']'
                   aResult = re.findall(sPattern, sHtmlContent)

                   if aResult:
                        url = aResult[0]
                        sMovieTitle = sTitle
                        if '.m3u8' in url:
                            sHosterUrl = url
            
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

           

             
    oGui.setEndOfDirectory() 

def getHosterIframe(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    referer = url
    if 'channel' in referer:
         referer = referer.split('channel')[0]

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
            return code + '|Referer=' + referer
        except Exception as e:
            pass
    
    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  
                url = "https:" + url
            referer2 = url.split('embed')[0]
            url = getHosterIframe(url, referer)
            if url:
                return url + "|Referer=" + referer2 

    sPattern = 'src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            referer = url
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return True, sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = aResult[0]
        if '.m3u8' in sHosterUrl:
            return True, sHosterUrl 

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return True, aResult[0] + '|referer=' + url

    sPattern = 'source\s*["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    return False
	