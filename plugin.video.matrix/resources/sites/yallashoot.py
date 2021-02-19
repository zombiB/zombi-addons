#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'yallashoot'
SITE_NAME = 'yalla-shoot.com'
SITE_DESC = 'sport vod'

URL_MAIN = 'http://www.yalla-shoot.com/live/'
URL_MAIN_link = 'http://www.yalla-shoot.com/live/video.php'
SPORT_FOOT = ('https://www.yalla-shoot.com/live/video.php', 'showMovies')
SPORT_SPORTS = ('http://', 'load')
SPORT_GENRES = ('http://', 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)  
            
    oGui.setEndOfDirectory()
   
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["مباريات كاملة","http://www.yalla-shoot.com/live/video.php?type=3"] )
    liste.append( ["أهداف ","http://www.yalla-shoot.com/live/video.php?type=1"] )
    liste.append( ["الأشواط ","http://www.yalla-shoot.com/live/video.php?type=4"] )
    liste.append( ["ملخصات","http://www.yalla-shoot.com/live/video.php?type=2"] )
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&quot;', '"')
	 # .+? ([^<]+) 
    sPattern = '<div class="col-md-3 col-sm-6 goals-item"><a href="([^<]+)"><div class="panel panel-default"><div class="panel-body"><div class="goals-img"><i class="fa fa-play-circle-o"></i><img src="([^<]+)" /></div></div><div class="panel-footer"><h4 data-toggle="tooltip" data-placement="top" title="([^<]+)">([^<]+)</h4>'
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = str(aEntry[0])
            sTitle = str(aEntry[3])
            sInfo = ""
            sThumbnail = aEntry[1]
            if not 'http' in sUrl:
                sUrl = str(URL_MAIN) + sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<li><a href='(.+?)'>التالى</a></li>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN_link+aResult[1][0]
        return aResult

    return False
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    oParser = cParser()
    #print sHtmlContent
 
    sPattern = '<iframe.+?src="(.+?)"' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            if 'ok.php' in url:
                url = url.split('ok.php?id=', 1)[1]
                url = 'http://ok.ru/videoembed/' + url
            
                
            sHosterUrl = url
			

            sHosterUrl = sHosterUrl.replace('http://yalla6.xyz/goals/youtube.php?ytid=','https://www.youtube.com/embed/').replace('?autoplay=0','').replace('?autoplay=1','')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_) 
 
    sPattern = '<a href="([^<]+)" target="_blank"' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            if 'ok.php' in url:
                url = url.split('ok.php?id=', 1)[1]
                url = 'http://ok.ru/videoembed/' + url
            
                
            sHosterUrl = url
			

            sHosterUrl = sHosterUrl.replace('http://yalla6.xyz/goals/youtube.php?ytid=','https://www.youtube.com/embed/').replace('?autoplay=0','').replace('?autoplay=1','')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_) 


                
    oGui.setEndOfDirectory()    