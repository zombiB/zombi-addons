# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'alfajertv'
SITE_NAME = 'Alfajertv'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/genre/english-movies/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/genre/arabic-movies/', 'showMovies')

MOVIE_FAM = (URL_MAIN + '/genre/family/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/genre/indian-movies/', 'showMovies')
MOVIE_TOP = (URL_MAIN + '/imdb/', 'showTopMovies')

MOVIE_TURK = (URL_MAIN + '/genre/turkish-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/genre/animation/', 'showMovies')
SERIE_TR = (URL_MAIN + '/genre/turkish-series/', 'showSeries')
SERIE_EN = (URL_MAIN + '/genre/english-series/', 'showSeries')
SERIE_AR = (URL_MAIN + '/genre/arabic-series/', 'showSeries')

REPLAYTV_PLAY = (URL_MAIN + '/genre/plays/', 'showMovies')

RAMADAN_SERIES = (URL_MAIN + '/genre/ramadan2023/', 'showSeries')
URL_SEARCH = (URL_MAIN + '/?s=', 'showMoviesSearch')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMoviesSearch')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
       
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)
                       
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?

    sPattern = '<a href="([^<]+)"><img src="([^<]+)" alt="([^<]+)" /><span class="movies">.+?class="year">(.+?)</span>.+?<p>(.+?)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[1]#.replace("-185x278","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            sYear = aEntry[3]
            sDesc = aEntry[4]
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?

    sPattern = '<a href="([^<]+)"><img src="([^<]+)" alt="([^<]+)" /><span class="tvshows">.+?class="year">(.+?)</span>.+?<p>(.+?)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[1]#.replace("-185x278","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)            
            sYear = aEntry[3]	
            sDesc = aEntry[4]
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
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

    sPattern = '<img src="([^<]+)" alt="([^<]+)">.+?</div><a href="([^<]+)"><div class="see">.+?<span>([^<]+)</span> <span>.+?class="texto">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[2]
            s1Thumb = aEntry[0]#.replace("-185x278","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)  
            sYear = aEntry[3]
            sDesc = aEntry[4]
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showTopMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?

    sPattern = "<div class='poster'><a href='([^<]+)'><img src='([^<]+)' alt='([^<]+)'></a>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[1]#.replace("-185x278","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)            
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
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

    sPattern = '<article id=".+?" class="item tvshows "><div class="poster"><img src="([^<]+)" alt="([^<]+)"><div class="rating"><span class="icon-star2"></span>([^<]+)</div><div class="mepo"> </div><a href="(.+?)"><div class="see">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[3]
            s1Thumb = aEntry[0]#.replace("-185x278","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)  
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   		
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
# ([^<]+) .+? 
    sPattern = '<div class="imagen"><a href="([^<]+)"><img src="([^<]+)"></a></div><div class="numerando">([^<]+)</div><div class="episodiotitle"><a href=".+?">(.+?)</a> <span class="date">'

    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = sMovieTitle+' S'+aEntry[2].replace("- ","E")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[1]#.replace("-185x278","").replace("-300x170","")
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            
            sDesc =  sDesc

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

       
    oGui.setEndOfDirectory()

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="(.+?)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return False
	
def showServerold():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)
    oParser = cParser()
    Host = URL_MAIN.split('//')[1]
     # (.+?) ([^<]+) .+?
    sPattern = 'id=\"player-option-1\" data-type=\"movie\" data-post=\"(.+?)\" data-nume=\"(.+?)\">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
       for aEntry in aResult[1]:
           pUrl = URL_MAIN + '/wp-admin/admin-ajax.php'
           post = aEntry[0]
           nume = aEntry[1]
           pdata = 'action=doo_player_ajax&post='+post+'&nume='+nume+'&type=movie'
           UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
           oRequest = cRequestHandler(pUrl)
           oRequest.setRequestType(1)
           oRequest.addHeaderEntry('User-Agent', UA)
           oRequest.addHeaderEntry('Referer', sUrl)
           oRequest.addHeaderEntry('Host', 'show.alfajertv.com')
           oRequest.addHeaderEntry('Accept', '*/*')
           oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
           oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
           oRequest.addParametersLine(pdata)
           sHtmlContent2 = oRequest.request() 
           #VSlog(sHtmlContent)
           
           sPattern = "<iframe.+?src='(.+?)' frameborder"
           aResult = oParser.parse(sHtmlContent2, sPattern)
           #VSlog(aResult)
           if aResult[0]:
               for aEntry in aResult[1]:            
                   url = aEntry.replace("%2F","/").replace("%3A",":").replace("https://show.alfajertv.com/jwplayer/?source=","").replace("&type=mp4","").split("&id")[0]
                   VSlog(url)
                   if 'hadara.ps' in aEntry :
                        url = url + "|Referer=" + aEntry + "| User-Agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                   sHosterUrl = url
                   VSlog(sHosterUrl)
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
           
           sPattern = 'domain=(.+?)\".+?href=\"(.+?)\".+?quality\">(.+?)</.+?<td>.+?</td><td>(.+?)</td>'
           oParser = cParser()
           aResult = oParser.parse(sHtmlContent, sPattern)
           VSlog(aResult)
           
           if aResult[0]:
               for aEntry in aResult[1]: 
                    oRequest = cRequestHandler(aEntry[1])
                    sHtmlContent3 = oRequest.request()
                    VSlog(sHtmlContent3)
                    oParser = cParser()
                    sPattern = 'rel=\"nofollow\" href=\"(.+?)\" class'
                    aResult = oParser.parse(sHtmlContent3, sPattern)
                    VSlog(aResult)
                    
                    if aResult[0]:
                       for aEntry in aResult[1]:            
                           url = aEntry[1]
                           if url.startswith('//'):
                              url = 'http:' + url
                    
                           sHosterUrl = url
                           if 'userload' in sHosterUrl:
                               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                           if 'mystream' in sHosterUrl:
                               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                           oHoster = cHosterGui().checkHoster(sHosterUrl)
                           if oHoster:
                              oHoster.setDisplayName(aEntry[0] +'-' + aEntry[2]+'-' + aEntry[3] )
                              oHoster.setFileName(sMovieTitle)
                              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
    
	
def showServer():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)
    oParser = cParser()
    Host = URL_MAIN.split('//')[1]
     # (.+?) ([^<]+) .+?
    sPattern = 'id=\"player-option-\d\" data-type=\"(.+?)\" data-post=\"(.+?)\" data-nume=\"(.+?)\">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)
    if aResult[0]:
       for aEntry in aResult[1]:
           pUrl = URL_MAIN + '/wp-admin/admin-ajax.php'
           post = aEntry[1]
           nume = aEntry[2]
           datatype= aEntry[0]
           pdata = 'action=doo_player_ajax&post='+post+'&nume='+nume+'&type='+datatype
           UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
           oRequest = cRequestHandler(pUrl)
           oRequest.setRequestType(1)
           oRequest.addHeaderEntry('User-Agent', UA)
           oRequest.addHeaderEntry('Referer', sUrl)
           oRequest.addHeaderEntry('Host', 'show.alfajertv.com')
           oRequest.addHeaderEntry('Accept', '*/*')
           oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
           oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
           oRequest.addParametersLine(pdata)
           sHtmlContent2 = oRequest.request() 
           VSlog(sHtmlContent)
           
           sPattern = "<iframe.+?src='(.+?)' frameborder"
           aResult = oParser.parse(sHtmlContent2, sPattern)
           VSlog(aResult)
           if aResult[0]:
               for aEntry in aResult[1]:            
                   url = aEntry.replace("%2F","/").replace("%3A",":").replace("https://show.alfajertv.com/jwplayer/?source=","").replace("&type=mp4","").split("&id")[0]
                   VSlog(url)
                   if 'hadara.ps' in aEntry :
                        url = url + "|Referer=" + aEntry + "| User-Agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                   sHosterUrl = url
                   VSlog(sHosterUrl)
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
           
    sPattern = 'domain=(.+?)\".+?href=\"(.+?)\".+?quality\">(.+?)</.+?<td>.+?</td><td>(.+?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)

    if aResult[0]:
       for aEntry in aResult[1]: 
            oRequest = cRequestHandler(aEntry[1])
            sHtmlContent3 = oRequest.request()
            VSlog(sHtmlContent3)
            oParser = cParser()
            sPattern = 'rel=\"nofollow\" href=\"(.+?)\" class'
            aResult = oParser.parse(sHtmlContent3, sPattern)
            VSlog(aResult)
            
            if aResult[0]:
               for aEntry in aResult[1]:            
                   url = aEntry[1]
                   if url.startswith('//'):
                      url = 'http:' + url
            
                   sHosterUrl = url
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      oHoster.setDisplayName(aEntry[0] +'-' + aEntry[2]+'-' + aEntry[3] )
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()