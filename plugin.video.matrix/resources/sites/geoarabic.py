# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'geoarabic'
SITE_NAME = 'Geoarabic'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

DOC_NEWS = ('https://www.geoarabic.com/search/label/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')
DOC_GENRES = (True, 'showGenres')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
   
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+?
    sPattern = "<a href=([^<]+)><img alt='([^<]+)' class='lazyload' data-src='([^<]+)' data-srcset.+?<span itemprop='keywords'>([^<]+)</span></a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("'", "")
            
            sThumb = aEntry[2].replace('w50-h26', 'w400-h720')
            siteUrl = aEntry[0].replace('"', '')
            sDesc = aEntry[3] 
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)" id='
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('facebook','')
    # ([^<]+) (.+?)
               

    videoId = "a"
    Vid = "a"     

    sPattern = '<td id="(.+?)">(.+?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] is True:
        for aEntry in aResult[1]:

            videoId = aEntry[0]
            Vid = aEntry[1]
            url = ""
            if 'no_video' in Vid:
               videoId = ""
            if 'ID' in videoId:
               url = 'http://www.youtube.com/watch?v=' + Vid
            if 'IDGoogle' in videoId:
               url = 'https://drive.google.com/file/d/' + Vid + '/preview'
            if '2ID' in videoId:
               url = 'http://www.youtube.com/watch?v=' + Vid
            if '2IDOk' in videoId:
               url = 'http://ok.ru/videoembed/' + Vid
            if 'IDOk' in videoId:
               url = 'http://ok.ru/videoembed/' + Vid
            if 'IDRutube' in videoId:
               url = 'https://rutube.ru/play/embed/' + Vid
            if 'IDDaily' in videoId:
               url = 'https://www.dailymotion.com/embed/video/' + Vid
            if '2IDDaily' in videoId:
               url = 'https://www.dailymotion.com/embed/video/' + Vid
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

                
    oGui.setEndOfDirectory()