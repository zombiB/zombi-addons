#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'yallashoot'
SITE_NAME = 'yallashoot'
SITE_DESC = 'sport vod'

URL_MAIN = 'https://www.yalla-shoot.com/match'
URL_MAIN_link = URL_MAIN + '/live/video.php'
SPORT_FOOT = (URL_MAIN + '/video.php', 'showMovies')
SPORT_SPORTS = ('http://', 'load')
SPORT_GENRES = ('http://', 'showGenres')
SPORT_GENRES = (True, 'showGenres')

def load():
    oGui = cGui() 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات ', 'sport.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'أقسام أخرى', 'genres.png', oOutputParameterHandler)
    
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
	            
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 
    sPattern = '<div class="col-md-3 col-sm-6 goals-item"><a href="([^<]+)"><div class="panel panel-default"><div class="panel-body"><div class="goals-img"><i class="fa fa-play-circle-o"></i><img src="([^<]+)" /></div></div><div class="panel-footer"><h4 data-toggle="tooltip" data-placement="top" title="([^<]+)">([^<]+)</h4>'
   
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
				
            sUrl = aEntry[0]
            sTitle = aEntry[3]
            sInfo = ""
            sThumbnail = aEntry[1]
            if not 'http' in sUrl:
                sUrl = str(URL_MAIN) + sUrl
					
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

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
 
    sPattern = '<iframe.+?src="(.+?)"' 
    aResult1 = re.findall(sPattern, sHtmlContent)
    sPattern = '<a href="([^<]+)" target="_blank"' 
    aResult2 = re.findall(sPattern, sHtmlContent)
    aResult = aResult1 + aResult2
    if aResult:
        for aEntry in aResult:
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            if 'ok.php' in url:
                url = url.split('ok.php?id=', 1)[1]
                url = 'http://ok.ru/videoembed/' + url                            
            sHosterUrl = url
            sHosterUrl = sHosterUrl.replace('http://yalla6.xyz/goals/youtube.php?ytid=','https://www.youtube.com/embed/')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                
    oGui.setEndOfDirectory()    