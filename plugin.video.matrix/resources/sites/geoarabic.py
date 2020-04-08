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
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'geoarabic'
SITE_NAME = 'geoarabic'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.geoarabic.com/'

DOC_NEWS = ('https://www.geoarabic.com/search/label/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')
DOC_GENRES = (True, 'showGenres')




URL_SEARCH = ('?s=', 'showMovies')
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
   


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["natgeoad","https://www.geoarabic.com/search/label/%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D9%86%D8%A7%D8%B4%D9%8A%D9%88%D9%86%D8%A7%D9%84%20%D8%AC%D9%8A%D9%88%D8%BA%D8%B1%D8%A7%D9%81%D9%8A%D9%83"] )
    liste.append( ["natgeoad kids","https://www.geoarabic.com/search/label/%D9%86%D8%A7%D8%B4%D9%8A%D9%88%D9%86%D8%A7%D9%84%20%D8%AC%D9%8A%D9%88%D8%BA%D8%B1%D8%A7%D9%81%D9%8A%D9%83%20%D9%83%D9%8A%D8%AF%D8%B2"] )
    liste.append( ["jazeeradoc-tv-channels","https://www.geoarabic.com/search/label/%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D8%A7%D9%84%D8%AC%D8%B2%D9%8A%D8%B1%D8%A9%20%D8%A7%D9%84%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9"] )
    liste.append( ["natgeowild","https://www.geoarabic.com/search/label/%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D9%86%D8%A7%D8%AA%20%D8%AC%D9%8A%D9%88%20%D9%88%D8%A7%D9%8A%D9%84%D8%AF"] )
    liste.append( ["othertv","https://www.geoarabic.com/search/label/%D8%A7%D9%81%D9%84%D8%A7%D9%85%20%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9"] )

    
	            
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
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+?
    sPattern = "<a href=([^<]+)><img alt='([^<]+)' class='lazyload' data-src='([^<]+)' data-srcset.+?<span itemprop='keywords'>([^<]+)</span></a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].decode("utf8").replace("'", "")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sThumbnail = aEntry[2].replace('w50-h26', 'w400-h720')
            siteUrl = aEntry[0].replace('"', '')
            sInfo = aEntry[3] 
			



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 

 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)" id='
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('facebook','')
    # ([^<]+) (.+?)
               

    Id = "a"
    Vid = "a"     

    sPattern = '<td id="(.+?)">(.+?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break

				Id = str(aEntry[0])
				Vid = str(aEntry[1])
				url = ""
				if 'no_video' in Vid:
					Id = ""
				if 'ID' in Id:
					url = 'http://www.youtube.com/watch?v=' + Vid
				if 'IDGoogle' in Id:
					url = 'https://drive.google.com/file/d/' + Vid + '/preview'
				if '2ID' in Id:
					url = 'http://www.youtube.com/watch?v=' + Vid
				if '2IDOk' in Id:
					url = 'http://ok.ru/videoembed/' + Vid
				if 'IDOk' in Id:
					url = 'http://ok.ru/videoembed/' + Vid
				if 'IDRutube' in Id:
					url = 'https://rutube.ru/play/embed/' + Vid
				if 'IDDaily' in Id:
					url = 'https://www.dailymotion.com/embed/video/' + Vid
				if '2IDDaily' in Id:
					url = 'https://www.dailymotion.com/embed/video/' + Vid
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()