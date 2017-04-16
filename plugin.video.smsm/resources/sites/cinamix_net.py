#-*- coding: utf-8 -*-
#zombi.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata

SITE_IDENTIFIER = 'cinamix_net'
SITE_NAME = 'cimamix.net'
SITE_DESC = 'vod'

URL_MAIN = 'http://www.cimamix.co'
MOVIE_AR = ('http://cimamix.co/c/8/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/1.html', 'showMovies')
MOVIE_ANIME = ('http://cimamix.co/c/12/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%83%D8%B1%D8%AA%D9%88%D9%86/1.html', 'showMovies')
MOVIE_HI = ('http://cimamix.co/c/11/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D9%87%D9%86%D8%AF%D9%8A%D8%A9/1.html', 'showMovies')
MOVIE_EN = ('http://cimamix.co/c/10/%D8%A7%D9%81%D9%84%D8%A7%D9%85_%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9/1.html', 'showMovies')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)   
            
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
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<img src="(.+?)" width=".+?" title="(.+?)".+?href="(.+?)">'
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sUrl = str(aEntry[2]).replace('http://cimamix.co/f/', 'http://cimamix.co/play/')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', aEntry[1], 'doc.png', aEntry[0], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)">&rsaquo;</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
	
def showLinks():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li><a href="([^<]+)" rel="#iframe"[^<]+>([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()   

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','([^<]+)')
               
        
    sPattern = 'id="player"></div> <script type="text/rocketscript">(.+?)</script>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print sPattern

    if (aResult[0] == True):
        sHosterUrl = cPacker().unpack(aResult[1][0])
        print sHosterUrl
        

        
        sPattern2 = '"file":"(.+?)","label":"(.+?)P",' 
        aResult = oParser.parse(sHosterUrl, sPattern2)
	
        if (aResult[0] == True):
			total = len(aResult[1])
			dialog = cConfig().createDialog(SITE_NAME)
			for aEntry in aResult[1]:
				cConfig().updateDialog(dialog, total)
				if dialog.iscanceled():
					break
            
				url = str(aEntry[0])
				Squality = str(aEntry[1])
				sTitle = '[' + Squality + '] ' + sMovieTitle
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = cUtil().DecoTitle(sTitle)
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    
