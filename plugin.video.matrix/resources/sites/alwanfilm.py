# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager
 
SITE_IDENTIFIER = 'alwanfilm'
SITE_NAME = 'Alwanfilm'
SITE_DESC = 'arabic vod'

URL_MAIN = 'https://alwanfilm.com/'

MOVIE_CLASSIC = (URL_MAIN + '/genre/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%85%d9%84%d9%88%d9%86%d8%a9/', 'showMovies')

REPLAYTV_PLAY = (URL_MAIN + '/genre/%d9%85%d8%b3%d8%b1%d8%ad%d9%8a%d8%a7%d8%aa-%d9%85%d9%84%d9%88%d9%86%d8%a9/', 'showMovies')

MOVIE_ANNEES = (True, 'showYears')

FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1932, 1975)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/release/' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

  # .+? ([^<]+) (.+?) .+?

    sPattern = 'data-src="([^<]+)" alt="([^<]+)" data.+?<a href="([^<]+)"><div '
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
 
            sTitle = aEntry[1].replace('"',"").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[2]
            sDesc = ''
            sYear = ''
            sThumb = aEntry[0]
            sDub = ''
            m = re.search('باﻷلوان', sTitle)
            if m:
                sDub = str(m.group(0))
                sTitle = sTitle.replace(sDub,'')
            sDisplayTitle = ('%s [%s]') % (sTitle, sDub)


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

  # .+? ([^<]+) 
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        
        return aResult[1][0]

    return False

	 
def showServer():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    
    #(.+?) 
    sId = ''
    Host = URL_MAIN.split('//')[1]

    sPattern = "data-post='(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sId = aResult[1][0]
    sUrl = 'https://alwanfilm.com/wp-json/dooplayer/v2/'+sId+'/movie/2'
    oRequestHandler = cRequestHandler(sUrl)
    import requests
    sgn = requests.Session()
    headers = {'Host': Host,
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl,
     'Connection': 'keep-alive'}
    data = sgn.get(sUrl, headers=headers).content
    sHtmlContent = data.decode('utf8',errors='ignore')
    
    # (.+?) .+? ([^<]+)        	
    sPattern = '"embed_url":"(.+?)",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            url = aEntry
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
       
    oGui.setEndOfDirectory()