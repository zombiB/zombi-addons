# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, isMatrix, siteManager, addon

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
 
SITE_IDENTIFIER = 'ahdaf'
SITE_NAME = 'Ahdaf'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_FOOT = (URL_MAIN, 'showMovies')
 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات', icons + '/Sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
    if not isMatrix():
       sHtmlContent = sHtmlContent.decode("windows-1256").encode("utf-8")
    if isMatrix():
       sHtmlContent = sHtmlContent.encode('cp1252').decode('cp1256')
 
# ([^<]+) .+?
    sPattern = '<td class="alt1Active" align="right" id=".+?">.+?a href="([^<]+)"><strong>([^<]+)</strong></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            sThumb = ''
            siteUrl = URL_MAIN + '/' +aEntry[0]
            sDesc = '' 
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
 
    oGui.setEndOfDirectory()
 
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')


    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
    if not isMatrix():
       sHtmlContent = sHtmlContent.decode("windows-1256").encode("utf-8")
    if isMatrix():
       sHtmlContent = sHtmlContent.encode('cp1252').decode('cp1256')
    # (.+?) ([^<]+)
    sPattern = '<a href="([^<]+)" id="thread_title_.+?">([^<]+)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            sThumb = '' 
            siteUrl = URL_MAIN +'/'+ aEntry[0]
            sDesc = '' 
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)  
        
           
       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
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
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

		
    oGui.setEndOfDirectory()