# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'hdseed'
SITE_NAME = 'Hdseed'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://hdseed.net/'

KID_MOVIES = (URL_MAIN + '/genre/movies/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeriesSearch')

URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام', 'crtoon.png', oOutputParameterHandler)
   

    oGui.setEndOfDirectory()

def showSearchMovies():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN +'/?s='+sSearchText
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
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<article.+?<a href="([^<]+)">.+?<img src="([^<]+)" alt=.+?<div class="Title">([^<]+)</div>'
		
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
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجم عربي","مترجم").replace("مترجم","[COLOR yellow]مترجم[/COLOR]").replace("المسلسل العائلي","").replace("كرتون","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
               sThumb = 'https:' + sThumb
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
	
      # (.+?) ([^<]+) .+?
	
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="(.+?)" />'
	
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
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # (.+?) .+? ([^<]+)

    sPattern =  'class="Video on on_iframe TrvideoFirst">(.+?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] is True:
       total = len(aResult[1])
       for aEntry in aResult[1]:     
            import base64  
            sHtmlContent2 = base64.b64decode(aEntry)
    # (.+?)    .+?    
            sPattern = 'src="(.+?)".+?allowfullscreen'
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0] is True:
               for aEntry in aResult[1]:
                   sHosterUrl = str(aEntry) 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
                
    oGui.setEndOfDirectory()				