# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'shoofvod'
SITE_NAME = 'Shoofvod'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

RAMADAN_SERIES = (URL_MAIN + '/Cat-144-1', 'showSeries')
MOVIE_EN = (URL_MAIN + '/al_751319_1', 'showMovies')
MOVIE_AR = (URL_MAIN + '/Cat-100-1', 'showMovies')
MOVIE_HI = (URL_MAIN + '/Cat-132-1', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/Cat-48-1', 'showMovies')
MOVIE_ANIME = (URL_MAIN + '/Cat-57-1', 'showMovies')
DOC_NEWS = (URL_MAIN + '/Cat-23-1', 'showMovies')
SERIE_DUBBED = (URL_MAIN + '/Cat-129-1', 'showSeries')
SERIE_AR = (URL_MAIN + '/Cat-98-1', 'showSeries')
SERIE_TR = (URL_MAIN + '/Cat-128-1', 'showSeries')
SERIE_TR_AR = (URL_MAIN + '/Cat-129-1', 'showSeries')
SERIE_HEND = (URL_MAIN + '/Cat-130-1', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
REPLAYTV_NEWS = (URL_MAIN + '/Cat-39-1', 'showSeries')
THEATER = (URL_MAIN + '/Cat-44-1', 'showEps')
KID_CARTOON = (URL_MAIN + '/Cat-56-1', 'showSeries')

URL_SEARCH = (URL_MAIN + '/Search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler) 
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', icons + '/TVShowsTurkish-Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', icons + '/Cartoon.png', oOutputParameterHandler)   

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)
	
    oOutputParameterHandler.addParameter('siteUrl', THEATER[0])
    oGui.addDir(SITE_IDENTIFIER, 'showEps', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/Search/'+sSearchText

        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['مسلسلات سورية - لبنانية',URL_MAIN + '/Cat-93-1'] )

 
    for sTitle,sUrl in liste:
 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, icons + '/Genres.png', oOutputParameterHandler)
 
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
 
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class.+?<div class="title"><h4>([^<]+)</h4></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")


            siteUrl = URL_MAIN+aEntry[0]
            siteUrl = siteUrl.replace('vidpage_','Play/')
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            if 'الحلقة' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
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
      # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class.+?<div class="title"><h4>([^<]+)</h4></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")
            siteUrl = URL_MAIN+aEntry[0]
            sThumb = aEntry[1]
            sDesc = ""
            sYear = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)">(.+?)</a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'التالي' in aEntry[1]:
                VSlog(URL_MAIN+aEntry[0])
                return URL_MAIN+aEntry[0]

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="col-md-3 col-sm-4 col-xs-4 col-xxs-6 item">.+?<a href="([^<]+)">.+?<img src="([^<]+)" class="img-responsive mrg-btm-5">.+?<div class="title"><h4>([^<]+)</h4></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والأخيرة","").replace("-","").replace("الحلقة "," E").replace("حلقة "," E")
            siteUrl = URL_MAIN+aEntry[0]
            siteUrl = siteUrl.replace('vidpage_','Play/')
            sThumb = aEntry[1]
            sDesc = ""

 

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters',  sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  'var url = "([^<]+)" +' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        m3url = URL_MAIN + '' + m3url 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
         # (.+?) ([^<]+) .+?       
    sPattern =  '<iframe src="(.+?)"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        m3url = 'http:' + m3url 
			
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
        sPattern = '<source src="(.+?)" type='
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if aResult[0]:
            for aEntry in aResult[1]:       
                url = aEntry
                if url.startswith('//'):
                   url = 'http:' + url
                sHosterUrl = url  
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                   oHoster.setDisplayName(sMovieTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
