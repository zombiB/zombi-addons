#-*- coding: utf-8 -*-
#Venom.
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'us_bein_en'
SITE_NAME = '[COLOR red]English[/COLOR] [COLOR white]USA[/COLOR]'
SITE_DESC = 'sport vod'

URL_MAIN = 'http://www.beinsports.com/'
SPORT_EPL = ('http://www.beinsports.com/us/premier-league/videos', 'showMovies')
SPORT_LIGA = ('http://www.beinsports.com/us/laliga/videos', 'showMovies')
SPORT_CL = ('http://www.beinsports.com/us/uefa-champions-league/videos', 'showMovies')
SPORT_CALCIO = ('http://www.beinsports.com/us/serie-a/videos', 'showMovies')
SPORT_BUNDES = ('http://www.beinsports.com/us/bundesliga/videos', 'showMovies')
SPORT_LIGUE = ('http://www.beinsports.com/us/ligue-1/videos', 'showMovies')
SPORT_BASKET = ('http://www.beinsports.com/us/basketball/videos', 'showMovies')
SPORT_TENNIS = ('http://www.beinsports.com/us/tennis/videos', 'showMovies')
SPORT_MOTORS = ('http://www.beinsports.com/us/motorsports/videos', 'showMovies')


FOOT_NEWS = ('http://www.beinsports.com/us/soccer/videos', 'showMovies')
MORE_NEWS = ('http://www.beinsports.com/us/other-sports/videos', 'showMovies')
MORE_GENRES = ('http://', 'showMore')
FOOT_GENRES = ('http://', 'showGenres')
SPORT_SPORTS = ('http://', 'load')


URL_SEARCH = ('http://www.beinsports.com/us/search?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://frenchstream.org/les-plus-vues')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Sports', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.beinsports.com/ar/search?q='+sSearchText+'&ft=%22%D8%A7%D9%84%D9%81%D9%8A%D8%AF%D9%8A%D9%88%22'  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return   
    
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["CONMEBOL WCQ","http://www.beinsports.com/us/conmebol-world-cup-qualifiers/videos"] )
    liste.append( ["UEFA Europa League","http://www.beinsports.com/us/uefa-europa-league/videos"] )
    liste.append( ["MLS","http://www.beinsports.com/us/mls/videos"] )
    liste.append( ["Eredivisie","http://www.beinsports.com/us/eredivisie/videos"] )
    liste.append( ["CONCACAF WCQ","http://www.beinsports.com/us/concacaf-world-cup-qualifiers/videos"] )
    
    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()  
    
    
def showMore():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["Six Nations","http://www.beinsports.com/us/six-nations/videos"] )
    liste.append( ["College Football","http://www.beinsports.com/us/college-football/videos"] )
    liste.append( ["MMA","http://www.beinsports.com/us/mma/videos"] )
    liste.append( ["NBA","http://www.beinsports.com/us/nba/videos"] )
    liste.append( ["Rugby","http://www.beinsports.com/us/rugby/videos"] )
    liste.append( ["Handball","http://www.beinsports.com/us/handball/videos"] )
    liste.append( ["Summer Olympics","http://www.beinsports.com/us/summer-olympics/videos"] )
    liste.append( ["Athletics","http://www.beinsports.com/us/athletics/videos"] )
    liste.append( ["Boxing","http://www.beinsports.com/us/boxing/videos"] )
    liste.append( ["Cycling","http://www.beinsports.com/us/cycling/videos"] )
    
    
    
  
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'bein.png', oOutputParameterHandler)
       
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
    sPattern = '<img data-src="(.+?)".+?<span class="time">(.+?)</span>.+?<figcaption>.+?<a href="(.+?)">(.+?)</a>'
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sUrl = str(aEntry[2])
            if not 'http' in sUrl:
                sUrl = str(URL_MAIN) + sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[3], 'doc.png', aEntry[0], aEntry[1], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="pagination__link">.+?<a href="(.+?)" aria-label="Next">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
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
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               

    sPattern = '<meta itemprop="embedURL" content="(.+?)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    
