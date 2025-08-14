# -*- coding: utf-8 -*-

import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
 
SITE_IDENTIFIER = 'aracinema_co'
SITE_NAME = 'ARA-Drama'
SITE_DESC = 'arabic vod'
 
sHost = base64.b64decode(siteManager().getUrlMain2(SITE_IDENTIFIER)).decode("utf-8")
sHost = sHost[::-1]

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = sHost

MOVIE_ASIAN = (f'{URL_MAIN}category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%84%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_KR = (f'{URL_MAIN}type/k-movies/', 'showMovies')
MOVIE_CN = (f'{URL_MAIN}type/c-movies/', 'showMovies')
MOVIE_JP = (f'{URL_MAIN}type/j-movie/', 'showMovies')
MOVIE_THAI = (f'{URL_MAIN}type/t-movies/', 'showMovies')
MOVIE_TA = (f'{URL_MAIN}type/فيلم-تايواني/', 'showMovies')
MOVIE_VIET = (f'{URL_MAIN}type/فيلم-فيتنامي/', 'showMovies')
MOVIE_GENRES = (f'{URL_MAIN}category/الافلام-الآسيوية/', 'moviesGenres')
MOVIE_ANNEES = (f'{URL_MAIN}category/الافلام-الآسيوية/', 'showYears')

SERIE_ASIA = (f'{URL_MAIN}category/serie/', 'showSerie')
SERIE_KR = (f'{URL_MAIN}category/serie/korea/', 'showSerie')
SERIE_CN = (f'{URL_MAIN}category/serie/chinese-taiwan/', 'showSerie')
SERIE_JP = (f'{URL_MAIN}category/serie/japanese/', 'showSerie')
SERIE_THAI = (f'{URL_MAIN}category/serie/tailand/', 'showSerie')
SERIE_GENRES = (f'{URL_MAIN}category/serie/', 'seriesGenres')
SERIE_ANNEES = (f'{URL_MAIN}category/serie/', 'showSerieYears')

REPLAYTV_PLAY = (f'{URL_MAIN}category/k-shows/', 'showSerie')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSerie')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30330), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_KR[1], 'أفلام كورية', '1/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CN[1], 'أفلام صينية', '1/Chinese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_JP[1], 'أفلام يابانية', '1/Japanese.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_THAI[1], 'أفلام تايلندية', '1/Thai.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TA[1], 'أفلام تايوانية', 'ta.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIET[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIET[1], 'أفلام فيتنامية', '1/Vietnamese.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', '1/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], 'مسلسلات صينية', '1/Chinese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات يابانية', '1/Japanese.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات تايلندية', '1/Thai.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_PLAY[1], 'برامج ترفيهية', '1/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/الافلام-الآسيوية/')
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'أفلام (بالسنوات)', '1/Calendar.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}category/serie/')
    oGui.addDir(SITE_IDENTIFIER, 'showSerieYears', 'مسلسلات (بالسنوات)', '1/Calendar.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return

def showYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '>كل السنوات</option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '>(.+?)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}stat/فيلم/?yr={sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '>كل السنوات</option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '>(.+?)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in reversed(aResult[1]):
 
            sYear = aEntry
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}yr/{sYear}') 
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', sYear, '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '>كل الأنواع</option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'value="(.+?)">([^<]+)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in (aResult[1]):
            sTitle = aEntry[1]  
            sGenres = aEntry[1].replace(' ','-')
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}tag/{sGenres}/?stat=فيلم') 
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def seriesGenres():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sStart = '>كل الأنواع</option>'
    sEnd = '</select>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'value="(.+?)">([^<]+)</option>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            sTitle = aEntry[1] 
            sGenres = aEntry[1].replace(' ','-')
            oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}tag/{sGenres}') 
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sPattern ='<a class="first_A" href="([^<]+)" title="([^<]+)">.+?<img src="([^<]+)" alt.+?<i class="fa fa-calendar-o"></i>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[1]:
                continue
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace("&#8217;","'")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""
            sYear = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sPattern ='<article id="post-.+?href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt=.+?<i class="icon-folder-open mi"></i>([^<]+)</a>.+?<i class="icon-calendar mi"></i>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[3]
            sYear = aEntry[4]

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

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sPattern ='<a class="first_A" href="([^"]+)" title="([^"]+)".+?src="([^"]+)"\s*alt.+?</i>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanSeriesName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = aEntry[3]
            sYear = ''

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
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()

    sNote = ''

    sPattern = '<p class="<h3>القصة :</h3><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sNote = aResult[1][0]
            
    sPattern =  'href="([^<]+)" title="">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
	
    sPattern = '<a class="first_A" href="([^<]+)" title="([^<]+)"><img src="([^<]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = (cUtil().ConvertSeasons(aEntry[1])).replace("الحلقة "," E").replace("مترجم","").replace("والأخيرة","")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = sNote
            sYear = ''
			
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request()
    
    sDesc = ''

    sPattern = '<h3>القصة :</h3><p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sDesc = aResult[1][0]

    sPattern = '<a class="vc_general vc_btn3 vc_btn3-size-lg vc_btn3-shape-square vc_btn3-style-flat vc_btn3-color-danger" href="(.+?)" title'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            siteUrl = aResult[1][0].split('?')[1]
            siteUrl = f'{URL_MAIN}?{siteUrl}'

            oRequest = cRequestHandler(siteUrl)
            sHtmlContent1 = oRequest.request()

    if sDesc:
        oGui.addLink(SITE_IDENTIFIER, 'showHosters','القصة', sThumb, sDesc, oOutputParameterHandler)


    sPattern =  '<a class="first_A" href="([^<]+)" title=' 
    aResult = oParser.parse(sHtmlContent1,sPattern)
    if aResult[0]:
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
               
    sPattern = "data-url='(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            url = url.replace("?rel=0","")
            if url.startswith('//'):
                url = f'http:{url}'
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
            if 'mystream' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
    oGui.setEndOfDirectory()     
 
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="current">.+?</span><a href="([^<]+)" class="page"'
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
    oRequestHandler.disableSSL()
    sHtmlContent = oRequestHandler.request() 

    sPattern =  '<a class="first_A" href="([^<]+)" title=' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
                    
    sPattern = "data-url='(.+?)' >"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            url = url.replace("?rel=0","")
            if url.startswith('//'):
                url = f'http:{url}'
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}' 
            if 'mystream' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}' 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster :
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)				
                
    oGui.setEndOfDirectory()