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
 
SITE_IDENTIFIER = 'beinmatch'
SITE_NAME = 'Beinmatch'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = (URL_MAIN, 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر و أهداف و ملخصات', 'sport.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()
   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+? (.+?)

    sPattern = '<button class="btn" onclick="goToMatch(.+?),([^<]+);">(.+?)</button>'



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
 
            sTitle =  aEntry[1].replace(')','').replace("'",'').replace('_',' ')
            sThumb = ""
            siteUrl = "https://beinmatch.one/home/live/"+aEntry[0].replace('(','')
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + aEntry[0]
            sDesc = aEntry[2]
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
    oRequestHandler.addHeaderEntry('authority', 'beinmatch.one')
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'source: "(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            sHosterUrl = url
            sMovieTitle = sMovieTitle
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            if 'vimeo' not in sHosterUrl:
                sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false&Referer=' + sUrl
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) # ([^<]+) .+? 
    sPattern = 'src="([^<]+)" frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            if '.php' in url:           
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request() 
                sPattern =  'src="(.+?)"'
                aResult = oParser.parse(sHtmlContent,sPattern)
                if aResult[0] is True:
                     url = aResult[1][0]
 
                     sHosterUrl = url
                     sMovieTitle = sMovieTitle  
                     if 'vimeo' in sHosterUrl:
                         sHosterUrl = sHosterUrl + "|Referer=" + sUrl
                     if 'vimeo' not in sHosterUrl:
                         sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false&Referer=' + sUrl                      
            

                     oHoster = cHosterGui().checkHoster(sHosterUrl)
                     if oHoster != False:
                               oHoster.setDisplayName(sMovieTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            sHosterUrl = url
            sMovieTitle = sMovieTitle
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            if 'vimeo' not in sHosterUrl:
                sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false&Referer=' + sUrl
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # (.+?) # ([^<]+) .+? 
    sPattern = ' <button class="btnServer" onclick="goToMatch(.+?), (.+?),'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = "link HD "+aEntry[1]
            siteUrl = "https://beinmatch.one/home/live/"+aEntry[0].replace("(","")
            siteUrl = siteUrl+'/'+aEntry[1]
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)        
           
             
    oGui.setEndOfDirectory() 
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'source: "(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            sHosterUrl = url
            sMovieTitle = sMovieTitle
            if 'vimeo' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + sUrl
            if 'vimeo' not in sHosterUrl:
                sHosterUrl = sHosterUrl + '|AUTH=TLS&verifypeer=false&Referer=' + sUrl
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()