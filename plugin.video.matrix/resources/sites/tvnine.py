﻿#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'tvnine'
SITE_NAME = 'tv96'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.tv96.tv'

SPORT_LIVE = ('https://www.tv96.tv', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
               
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
 
# ([^<]+) .+? (.+?)

    sPattern = '<div class="containerMatch"><a href="(.+?)" target=.+?<div style="font-weight: bold">(.+?)</div>.+?<div class="matchTime">(.+?)</div>.+?<div style="font-weight: bold">(.+?)</div>'



    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1]+' vs '+aEntry[3]
            sThumbnail = ""
            siteUrl = aEntry[0]
            sInfo = aEntry[2]
			
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # (.+?) # ([^<]+) .+? 
    sPattern = 'data-embed="(.+?)">(.+?)</li>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = ''
            oRequestHandler = cRequestHandler(siteUrl)
            data = oRequestHandler.request()
            oParser = cParser()
    # (.+?) # ([^<]+) .+? 
            sPattern = 'source: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if (aResult[0] == True):
               total = len(aResult[1])
               progress_ = progress().VScreate(SITE_NAME)
               for aEntry in aResult[1]:
                   progress_.VSupdate(progress_, total)
                   if progress_.iscanceled():
                       break
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)    
           
 
        progress_.VSclose(progress_)
             
    oGui.setEndOfDirectory() 
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'source: "(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            url = aEntry
            sHosterUrl = url
            sMovieTitle = sMovieTitle
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_)
                
    oGui.setEndOfDirectory()