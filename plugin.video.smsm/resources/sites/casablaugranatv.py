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

SITE_IDENTIFIER = 'casablaugranatv'
SITE_NAME = 'casablaugranatv'
SITE_DESC = 'sport vod'

URL_MAIN = 'http://www.casablaugranatv.pro'
SPORT_NEWS = ('http://www.casablaugranatv.pro/search?max-results=8', 'showMovies')
SPORT_SPORTS = ('http://www.casablaugranatv.pro/search?max-results=8', 'showMovies')
SPORT_GENRES = ('http://', 'showGenres')
SPORT_SPORTS = ('http://', 'load')


URL_SEARCH = ('http://www.casablaugranatv.pro/search?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Sports', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.casablaugranatv.pro/search?q='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["LA LIGA 16-17","http://www.casablaugranatv.pro/search/label/LA%20LIGA%2016-17"] )
    liste.append( ["دوري أبطال أوروبا 17-2016","http://www.casablaugranatv.pro/search/label/%D8%AF%D9%88%D8%B1%D9%8A%20%D8%A3%D8%A8%D8%B7%D8%A7%D9%84%20%D8%A3%D9%88%D8%B1%D9%88%D8%A8%D8%A7%2017-2016"] )
    liste.append( ["دوري أبطال أوروبا 15-2016","http://www.casablaugranatv.pro/search/label/%D8%AF%D9%88%D8%B1%D9%8A%20%D8%A3%D8%A8%D8%B7%D8%A7%D9%84%20%D8%A3%D9%88%D8%B1%D9%88%D8%A8%D8%A7%2015-2016"] )
    liste.append( ["LA LIGA 15-16","http://www.casablaugranatv.pro/search/label/LA%20LIGA%2015-16"] )
    liste.append( ["LA COPA DEL REY","http://www.casablaugranatv.pro/search/label/LA%20COPA%20DEL%20REY"] )
    liste.append( ["FULL MATCHES-مباريات كاملة","http://www.casablaugranatv.pro/search/label/FULL%20MATCHES"] )
    liste.append( ["وثائقيات","http://www.casablaugranatv.pro/search/label/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A7%D8%AA"] )
    liste.append( ["السوبر الاسباني","http://www.casablaugranatv.pro/search/label/%D8%A7%D9%84%D8%B3%D9%88%D8%A8%D8%B1%20%D8%A7%D9%84%D8%A7%D8%B3%D8%A8%D8%A7%D9%86%D9%8A"] )
    liste.append( ["EL CLASICO","http://www.casablaugranatv.pro/search/label/EL%20CLASICOOO"] )

    
	            
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
    sPattern = "<a content='([^<]+)'></a>.+?rel='prettyPhoto' title='([^<]+)'></a></span><span class='magazine-read-more-link'><a href='([^<]+)'></a></span>"
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
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', aEntry[0], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="pagination__link">.+?<a href="(.+?)" aria-label="Next">.+?<span aria-hidden="true"><i class="icon-angle-left"></i></span>'
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
               
        
    sPattern = '<span style="color: #cc0000;">([^<]+)</span>' 
    sPattern = sPattern + '|' + 'style="text-align: right;"><a href="([^<]+)"><span'
    sPattern = sPattern + '|' + '<iframe allowfullscreen.+?src="(.+?)"'
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
                 sUrl = str(aEntry[1])
                 oOutputParameterHandler = cOutputParameterHandler()
                 oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR blue]'+ aEntry[1] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)

            elif aEntry[2]:
                 sHosterUrl = 'http:' +str(aEntry[2])
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle)
                     oHoster.setFileName(sMovieTitle)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory() 
	
