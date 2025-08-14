#-*- coding: utf-8 -*-

import re, json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, addon, VSlog
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib import random_ua

UA = random_ua.get_phone_ua()
 
SITE_IDENTIFIER = 'lodynet'
SITE_NAME = 'Lodynet'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركية-مترجم/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/افلام-هندية/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام-اسيوية-a/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/انيمي/', 'showMovies')

SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركي/', 'showSerie')
SERIE_TR_AR = (f'{URL_MAIN}dubbed-turkish-series-g/', 'showSerie')
SERIE_HEND = (f'{URL_MAIN}category/مسلسلات-هندية-مترجمة/', 'showSerie')
SERIE_HEND_AR = (f'{URL_MAIN}dubbed-indian-series-p5/', 'showSerie')
SERIE_ASIA = (f'{URL_MAIN}tag/new-asia/', 'showMovies')
SERIE_CN = (f'{URL_MAIN}category/مسلسلات-صينية-مترجمة/', 'showSerie')
SERIE_KR = (f'{URL_MAIN}korean-series-a/', 'showSerie')
SERIE_THAI = (f'{URL_MAIN}مشاهدة-مسلسلات-تايلندية/', 'showSerie')
SERIE_PAK = (f'{URL_MAIN}category/المسلسلات-باكستانية/', 'showSerie')
SERIE_LATIN = (f'{URL_MAIN}category/مسلسلات-مكسيكية-a/', 'showSerie')

URL_SEARCH = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSearchSerie')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات هندية مدبلجة', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات باكستانية', 'paki.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات لاتنية', 'latin.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie' ,'مسلسلات صينية', '1/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie' ,'مسلسلات كورية', '1/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie' ,'مسلسلات تايلاندية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أقسام الموقع', 'listes.png', oOutputParameterHandler)	
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return	

def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showSearchSerie(sUrl)
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
 
    oParser = cParser()
    sPattern = '<li class="LodyBlock">\s*<a href="([^"]+)".+?alt="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if 'فيلم'  not in aEntry[1]:
                continue
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace("&#8217;", "'")
            sTitle = re.sub('[^a-zA-Z]', ' ', sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '>الرئيسية</a></li>'
    sEnd = '<div class="SiteSlider">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '#' in aEntry[0] or 'الطلبات' in aEntry[1] or 'ممثل' in aEntry[1]:
                continue 
            sTitle = aEntry[1]
            if 'رياح' in sTitle  or 'لون' in sTitle:
                continue
            siteUrl = aEntry[0]	

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            if 'برامج' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showSearchSerie', sTitle, '1/TVShows.png', '', '', oOutputParameterHandler)
            elif 'اغاني' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, '1/TVShows.png', '', '', oOutputParameterHandler)
            elif 'مسلسل' in sTitle:
                oGui.addMisc(SITE_IDENTIFIER, 'showSerie', sTitle, '1/TVShows.png', '', '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, '1/Movies.png', '', '', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()

def showSearchSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li class="LodyBlock">\s*<a href="([^"]+)".+?alt="([^"]+)".+?data-src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if 'فيلم'  in aEntry[1]:
                continue
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li class="LodyBlock">\s*<a href="([^"]+)".+?alt="([^"]+)".+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[1]).replace("&#8217;", "'")
            sTitle = re.sub('[^a-zA-Z0-9]', ' ', sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
			
            if 'مسلسل' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:    
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li class="LodyBlock TermBlock">\s*<a href="([^"]+)".+?alt="([^"]+)".+?.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = (cUtil().CleanSeriesName(aEntry[1])).replace('حصرياً','').replace('التايلندي','').replace('التايلاندي','').replace('الصيني','').replace('الباكستاني','')
            siteUrl = aEntry[0]
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[2])
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            sThumb = ""
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sPattern = '<li class="LodyBlock">\s*<a href="([^"]+)".+?alt="([^"]+)".+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]
            sThumb = sThumb
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a class="next page-numbers" href="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:       
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
       
    sPattern = r"SwitchServer\(this, '([^']+)'\)\">([^<]+)<\/span>"
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry[0])
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(f'{sMovieTitle} [{aEntry[1]}]')
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'data-embed="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:

            url = str(aEntry)
            if url.startswith('//'):
               url = 'http:' + url

            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    sPattern = r'var\s+ServerDownload\s*=\s*(\[\{.*?\}\]);'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            try:
                jsonDown = json.loads(aEntry)
                for item in jsonDown:
                    url = item["Link"]
                    sName = item["Name"]
                    sDisplayTitle = f'{sMovieTitle} -{cUtil().unescape(sName)}'
                    if url.startswith('//'):
                        url = 'http:' + url

                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            except:
                VSlog('Failed to get json')

    if 'class="DownloadLinks">' in sHtmlContent:
        sStart = '<div class="DownloadLinks">'
        sEnd = '</div></div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<a href="(.+?)" target='
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            for aEntry in aResult[1]:

                url = str(aEntry)
                if url.startswith('//'):
                    url = 'http:' + url

                sHosterUrl = url
                if 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        if 'id="DownloadAreaMobile"' in sHtmlContent:
            sStart = '<div id="DownloadAreaMobile">'
            sEnd = '<div id="SpaceBottomNotices">'
            sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

            sPattern = 'href="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)	
            if aResult[0]:
                for aEntry in aResult[1]:
                    
                    url = str(aEntry)
                    if url.startswith('//'):
                        url = 'http:' + url
                    
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
        
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				                
    oGui.setEndOfDirectory()