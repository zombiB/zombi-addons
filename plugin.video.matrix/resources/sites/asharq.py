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
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'asharq'
SITE_NAME = 'asharq'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DOC_NEWS = ('https://now.asharq.com/doc', 'showMovies')
DOC_SERIES = ('https://now.asharq.com/doc', 'showMovies')

 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)
    

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
    sPattern = 'class="imgContainer"><img src="([^<]+)" alt=.+?class="card-description">([^<]+)</p></div>.+?<a href="([^<]+)" class="card-title">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 

            sTitle = aEntry[3]
            sThumb = aEntry[0]
            siteUrl = URL_MAIN + aEntry[2]
            sDesc = aEntry[1]

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    oGui.setEndOfDirectory() 
    
def showMoviesLinks(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    VSlog(sUrl)
 
# ([^<]+) .+? (.+?)
    sPattern = 'class="d-flex mt-4"><a href="([^<]+)" class="btn btn-main btn-lg">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = sMovieTitle
            
            sThumb = sThumb
            siteUrl = URL_MAIN+aEntry
            sDesc = sDesc
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
# ([^<]+) .+? (.+?)
    sPattern = '<div class="imgContainer"><img src="(.+?)" alt=.+?<a href="(.+?)" class="card-title">(.+?)</a><p class="card-shortdescription">(.+?)</'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2]
            
            sThumb = aEntry[0]
            siteUrl = URL_MAIN+aEntry[1]
            sDesc = aEntry[3]
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesLinks', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li >.+?<a href="(.+?)">'
	 # .+? ([^<]+) (.+?)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        
        return URL_MAIN+'/'+aResult[1][0]


    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    oParser = cParser()
      # (.+?) ([^<]+) .+?
    sPattern =  ',"Link":.+?},"(.+?)","(.+?)",' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
       for aEntry in aResult[1]:
            url = aEntry[1]
            quality = aEntry[0]
            sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, quality)
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url
			
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


                
    oGui.setEndOfDirectory()