# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.Styling import getGenreIcon
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
	
SITE_IDENTIFIER = 'ifushaar'
SITE_NAME = 'iFushaar'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_FAM = (URL_MAIN + 'gerne/family/', 'showMovies')
MOVIE_EN = (URL_MAIN + 'packs/افلام-اجنبية/', 'showMovies')
MOVIE_FAM = (URL_MAIN + 'archive/افلام-عائلية/', 'showMovies')
MOVIE_TRE = (URL_MAIN + '#trending', 'showMovies')
MOVIE_REC = (URL_MAIN + '#latest', 'showMovies')
MOVIE_TOP = (URL_MAIN + '#most-viewed', 'showMovies')

MOVIE_GENRES = (URL_MAIN, 'moviesGenres')
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FAM[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عائلية', icons + '/Family.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TRE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TRE[1], 'أفلام (شائع)', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_REC[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_REC[1], 'أفلام (الاحدث)', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'أفلام (الاكثر مشاهدة)', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', icons + '/Genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def moviesGenres():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
      
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<a>حسب التصنيف</a>'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^<]+)">([^<]+)</a>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = aEntry[1].replace("افلام","").replace("أفلام","").strip()
            siteUrl = aEntry[0]

			

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showMovies', sTitle, getGenreIcon(sTitle), '', '', oOutputParameterHandler)
    
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
    sPattern = '<li class="video-grid".+?<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)'

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
 
            sTitle = aEntry[1].replace("تحميل","").replace("مشاهدة","").replace("مشاهده","").replace("مباشره","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("فلم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("اولاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("أون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
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

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            

        progress_.VSclose(progress_)
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()



def __checkForNextPage(sHtmlContent):
    sPattern = 'rel="next" href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return aResult[1][0]

    return False


def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    St=requests.Session()
    sHtmlContent1 = oRequestHandler.request()

    oParser = cParser()
    sPattern = '</div><a href="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent1, sPattern)

    if aResult[0]:
                    for aEntry in aResult[1]:
                               
                            aurl = aEntry
                            if aurl.startswith('//'):
                                aurl = 'http:' + aurl

                            cook = oRequestHandler.GetCookies()
                            hdr = {'Sec-Fetch-Mode' : 'navigate','Cookie' : cook,'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58','Referer' : sUrl}
                            sHtmlContent = St.get(aurl,headers=hdr)
                            sHtmlContent = sHtmlContent.content
                            
                            sPattern = 'data-src="([^"]+)'
                            oParser = cParser()
                            aResult = oParser.parse(sHtmlContent, sPattern)

                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry
                                    sHosterUrl = url

                                    sTitle = sMovieTitle
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        sDisplayTitle = sTitle
                                        oHoster.setDisplayName(sDisplayTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()
