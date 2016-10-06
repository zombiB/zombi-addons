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

SITE_IDENTIFIER = 'us_bein_es'
SITE_NAME = '[COLOR yellow]Spanish[/COLOR] [COLOR white]USA[/COLOR]'
SITE_DESC = 'sport vod'

URL_MAIN = 'http://www.beinsports.com'
SPORT_EPL = ('http://www.beinsports.com/us-es/premier-league/v%C3%ADdeos', 'showMovies')
SPORT_LIGA = ('http://www.beinsports.com/us-es/laliga/v%C3%ADdeos', 'showMovies')
SPORT_CL = ('http://www.beinsports.com/us-es/uefa-champions-league/v%C3%ADdeos', 'showMovies')
SPORT_CALCIO = ('http://www.beinsports.com/us-es/serie-a/v%C3%ADdeos', 'showMovies')
SPORT_BUNDES = ('http://www.beinsports.com/us-es/bundesliga/v%C3%ADdeos', 'showMovies')
SPORT_LIGUE = ('http://www.beinsports.com/us-es/ligue-1/v%C3%ADdeos', 'showMovies')
SPORT_TENNIS = ('http://www.beinsports.com/us-es/tenis/v%C3%ADdeos', 'showMovies')
SPORT_MOTORS = ('http://www.beinsports.com/us-es/deporte-motor/v%C3%ADdeos', 'showMovies')


FOOT_NEWS = ('http://www.beinsports.com/us-es/futbol/v%C3%ADdeos', 'showMovies')
MORE_NEWS = ('http://www.beinsports.com/us-es/other-sports/v%C3%ADdeos', 'showMovies')
MORE_GENRES = ('http://', 'showMore')
FOOT_GENRES = ('http://', 'showGenres')
SPORT_SPORTS = ('http://', 'load')


URL_SEARCH = ('http://www.beinsports.com/ar/search?q=', 'showMovies')
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
    liste.append( ["ELIMINATORIAS CONMEBOL","http://www.beinsports.com/us-es/eliminatorias-conmebol/v%C3%ADdeos"] )
    liste.append( ["UEFA Europa League","http://www.beinsports.com/us-es/uefa-europa-league/v%C3%ADdeos"] )
    liste.append( ["MLS","http://www.beinsports.com/us-es/mls/v%C3%ADdeos"] )
    liste.append( ["NASL","http://www.beinsports.com/us-es/nasl/v%C3%ADdeos"] )
    liste.append( ["Eliminatorias CONCACAF","http://www.beinsports.com/us-es/eliminatorias-concacaf/v%C3%ADdeos"] )
    
    
	            
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


    liste.append( ["MMA","http://www.beinsports.com/us-es/mma/v%C3%ADdeos"] )
    liste.append( ["NBA","http://www.beinsports.com/us-es/nba/v%C3%ADdeos"] )
    liste.append( ["Rugby","http://www.beinsports.com/us-es/rugby/v%C3%ADdeos"] )
    liste.append( ["BOXEO","http://www.beinsports.com/us-es/boxeo/v%C3%ADdeos"] )
    liste.append( ["Ciclismo","http://www.beinsports.com/us-es/ciclismo/v%C3%ADdeos"] )
    
    
    
  
	            
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
            sUrl = aEntry[2]
            if not 'http' in sUrl:
                sUrl = URL_MAIN+sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[3]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[3], 'bein.png', aEntry[0], aEntry[1], oOutputParameterHandler)

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
    
