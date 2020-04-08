#-*- coding: utf-8 -*-
#zombi
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
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'watanflix'
SITE_NAME = 'watanflix'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://watanflix.com'


SERIE_AR = ('http://watanflix.com/ar/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')
KID_CARTOON = ('http://watanflix.com/ar/category/%D8%A3%D8%B7%D9%81%D8%A7%D9%84', 'showSerie')


SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('https://watanflix.com/ar/search?q=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
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
        sUrl = 'https://watanflix.com/ar/search?q='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
  

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["كوميدي","https://watanflix.com/ar/type/%D9%83%D9%88%D9%85%D9%8A%D8%AF%D9%8A"] )
    liste.append( ["دراما","https://watanflix.com/ar/type/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7"] )
    liste.append( ["حارة-شامية","https://watanflix.com/ar/type/%D8%AD%D8%A7%D8%B1%D8%A9-%D8%B4%D8%A7%D9%85%D9%8A%D8%A9"] )
    liste.append( ["تاريخي-سيرة-ذاتيه-وثائقي","https://watanflix.com/ar/type/%D8%AA%D8%A7%D8%B1%D9%8A%D8%AE%D9%8A-%D8%B3%D9%8A%D8%B1%D8%A9-%D8%B0%D8%A7%D8%AA%D9%8A%D9%87-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A"] )
    liste.append( ["غموض-تشويق","https://watanflix.com/ar/type/%D8%BA%D9%85%D9%88%D8%B6-%D8%AA%D8%B4%D9%88%D9%8A%D9%82"] )


    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()  
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 #.+?([^<]+)

    sPattern = 'data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[1])
            sThumbnail = str(aEntry[3])
            sInfo = str(aEntry[0]).decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showSHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 #.+?([^<]+)

    sPattern = 'data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
				
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[1])
            sThumbnail = str(aEntry[3])
            sInfo = str(aEntry[0]).decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showSHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)" rel="next">&raquo;</a></li></ul></div>'
	 #.+?([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

def showSHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #.+? ([^<]+)
              
        
    sPattern = '<div style="overflow: hidden">.+?<a href="([^<]+)" target="_blank" class="linkPlay">.+?<img src="([^<]+)"  style=" margin: -13% 0 -10% 0; width: 100%;">.+?<i class="play-icon"></i>.+?</a>.+?</div>.+?<div><p><b>.+?</b><br/>([^<]+)</p></div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sMovieTitle = str(aEntry[2]).replace("</b>","").replace("<b>","")
            
            sThumbnail = str(aEntry[1])
            url = str(aEntry[0])
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
    oGui.setEndOfDirectory()                

