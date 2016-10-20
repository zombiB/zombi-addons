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
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'yallashoot'
SITE_NAME = 'yalla-shoot.com'
SITE_DESC = 'sport vod'

URL_MAIN = 'http://www.yalla-shoot.com/app/'
SPORT_NEWS = ('http://www.yalla-shoot.com/app/#page3', 'showMovies')
SPORT_SPORTS = ('http://www.yalla-shoot.com/app/', 'showMovies')
SPORT_SPORTS = ('http://', 'load')


URL_SEARCH = ('http://www.yalla-shoot.com/app/', 'showMovies')
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
	#([^<]+).+?
    sPattern = 'href="([^<]+)">.+?/><br>([^<]+)</td>.+?>([^<]+)</span> <br>.+?<img.+?width="30"/><br>([^<]+)</td>'

	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sTitle = str(aEntry[1])+''+str(aEntry[2])+''+str(aEntry[3])
            sUrl = str(aEntry[0])
            if not 'http' in sUrl:
                sUrl = str(URL_MAIN) + sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', aEntry[0], aEntry[2], oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
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
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
    oParser = cParser()
               
        
    sPattern = '<font color=red>(.+?)</font><br>' 
    sPattern = sPattern + '|' + '</iframe><br><font color=red>(.+?)</font><br><IFRAME'
    sPattern = sPattern + '|' + 'iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
               oOutputParameterHandler = cOutputParameterHandler()
               oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]'+ aEntry[0] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)
                        
            elif aEntry[1]:
                 oOutputParameterHandler = cOutputParameterHandler()
                 oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]'+ aEntry[1] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)

            elif aEntry[2]:
                 sHosterUrl = 'http:' +str(aEntry[2])
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle)
                     oHoster.setFileName(sMovieTitle)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()    
