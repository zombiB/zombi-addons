#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import xbmcgui
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'koraonline'
SITE_NAME = 'koraonline'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://kora-online.tv/'



SPORT_LIVE = ('https://kora-online.tv/', 'showMovies')



URL_SEARCH = ('', 'showMovies')
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
 
# ([^<]+) .+? 

    sPattern = '<a class="link" href="([^<]+)" title="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1].replace("بث مباشر","")
            sThumbnail = ""
            siteUrl = aEntry[0]
            sInfo = ""
            sTitle = sTitle.split('بتاريخ')[0]



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters4', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 


def __checkForNextPage(sHtmlContent):
    sPattern = ''
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        return aResult

    return False 
 

def showHosters4():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    oParser = cParser()

    sPattern = 'allow="(.+?)".+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            url = aEntry[1]
            if 'embed' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request();
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent2,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
					url = url.split('?link=', 1)[1]
            if '/dash/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = oRequestHandler.request();
                oParser = cParser()
                sPattern =  'var link = "(.+?)";'
                aResult = oParser.parse(sHtmlContent4,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
                sPattern =  "dash: '(.+?)'};"
                aResult = oParser.parse(sHtmlContent4,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
            sHosterUrl = url
            if 'm3u8' in url:
				sHosterUrl = url.split('?link=', 1)[1]
            sMovieTitle = '1'
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_) 
 # (.+?) # ([^<]+) .+? 

    sPattern = 'setURL([^<]+)">([^<]+)</button>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            url = str(aEntry[0]).replace("('",'').replace("')","")
            if 'm3u8' in url:
				url = url.split('?ch=', 1)[1]
            if url.startswith('//'):
                url = 'http:' + url
            if '/embed/' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent3 = oRequestHandler.request();
                oParser = cParser()
                sPattern =  'src="(.+?)" scrolling="no">'
                aResult = oParser.parse(sHtmlContent3,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
            if '.php' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent4 = oRequestHandler.request();
                oParser = cParser()
                sPattern =  'var link = "(.+?)";'
                aResult = oParser.parse(sHtmlContent4,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]+ '&Referer=' + "https://kora-online.tv"
                sPattern =  "dash: '(.+?)'};"
                aResult = oParser.parse(sHtmlContent4,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
                sPattern =  'src="(.+?)"'
                aResult = oParser.parse(sHtmlContent4,sPattern)
                if (aResult[0] == True):
					url = aResult[1][0]
            sHosterUrl = url
            sMovieTitle = str(aEntry[1])
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_)



                
    oGui.setEndOfDirectory()