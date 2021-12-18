# -*- coding: utf-8 -*-
#zombi.(@geekzombi)
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, isMatrix
 
SITE_IDENTIFIER = 'ahdaf'
SITE_NAME = 'ahdaf'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.ahdaf-kooora.com/'

SPORT_FOOT = (URL_MAIN, 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'رياضة', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    if not isMatrix():
       sHtmlContent = sHtmlContent.decode("windows-1256").encode("utf-8")
    if isMatrix():
       sHtmlContent = sHtmlContent.encode('cp1252').decode('cp1256')
 
# ([^<]+) .+?
    sPattern = '<td class="alt1Active" align="right" id=".+?">.+?<a href="([^<]+)"><strong>([^<]+)</strong></a>'

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
 
            sTitle = aEntry[1]
            sThumbnail = aEntry[0]
            siteUrl = URL_MAIN + aEntry[0]
            sInfo = '' 
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
 
    oGui.setEndOfDirectory()
 
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    if not isMatrix():
       sHtmlContent = sHtmlContent.decode("windows-1256").encode("utf-8")
    if isMatrix():
       sHtmlContent = sHtmlContent.encode('cp1252').decode('cp1256')
    # (.+?) ([^<]+)
    sPattern = '<a href="([^<]+)" id="thread_title_.+?">([^<]+)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            sThumbnail = aEntry[0]
            siteUrl = URL_MAIN + aEntry[0]
            sInfo = '' 
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)        
           
       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    if not isMatrix():
       sHtmlContent = sHtmlContent.decode("windows-1256").encode("utf-8")
    if isMatrix():
       sHtmlContent = sHtmlContent.encode('cp1252').decode('cp1256')

         # (.+?) ([^<]+)   
    sPattern = '<a href="(.+?)".+?">([^<]+)<'
    aResult1 = re.findall(sPattern, sHtmlContent)
    sPattern = '<a href="(.+?)" target="_blank">(.+?)<br />'
    aResult2 = re.findall(sPattern, sHtmlContent)
    sPattern = '<a href="(.+?)" target="_blank">(.+?)</a>'
    aResult3 = re.findall(sPattern, sHtmlContent)
    aResult = aResult1 + aResult2+ aResult3
	
    if aResult:
        for aEntry in aResult:
            
            sMovieTitle = aEntry[1]
            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
                           
            if 'goo.gl' in sHosterUrl or 'bit.ly' in sHosterUrl:
                try:
                    import requests
                    url = sHosterUrl
                    session = requests.Session()  # so connections are recycled
                    resp = session.head(url, allow_redirects=True)
                    sHosterUrl = resp.url
                except:
                    pass
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

		
    oGui.setEndOfDirectory()