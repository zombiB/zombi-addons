# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

 
import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
 
SITE_IDENTIFIER = 'moviztime'
SITE_NAME = 'MovizTime'
SITE_DESC = 'arabic vod'

UA = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.48 Mobile Safari/537.36'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = ',"url":"(.+?)","name":"وقت الافلام",'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]
    VSlog(URL_MAIN)

MOVIE_EN = (URL_MAIN + 'category/أفلام-أجنبية/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/أفلام-هندية/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/أفلام-آسيوية-مترجمة/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/أفلام-تركية/', 'showMovies')

SERIE_EN = (URL_MAIN + 'category/مسلسلات-أجنبية-مترجمة-d/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/مسلسلات-كورية/', 'showSeries')

SERIE_GENRES = (True, 'seriesGenres')
MOVIE_GENRES = (True, 'moviesGenres')

ANIM_MOVIES = (URL_MAIN + 'category/قائمة-الأنمي-b/أفلام-أنمي/', 'showMovies')
ANIM_NEWS = (URL_MAIN+'category/قائمة-الأنمي-b/مسلسلات-أنمي/' , 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + 'category/برامج-تلفزيونية/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies',icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/أفلام-أوروبية/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أوروبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية', icons + '/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/action/'])
    liste.append(['انيميشن', URL_MAIN + 'category/%d8%a3%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/'])
    liste.append(['كوميديا', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/comedy/'])
    liste.append(['قصة حقيقية', URL_MAIN + 'category/%d9%82%d8%b5%d8%a9-%d8%ad%d9%82%d9%8a%d9%82%d9%8a%d8%a9/'])
    liste.append(['دراما', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/drama/'])
    liste.append(['رعب', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%b1%d8%b9%d8%a8-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/'])
    liste.append(['عائلى', URL_MAIN + 'category/%d8%b9%d8%a7%d8%a6%d9%84%d9%8a/'])
    liste.append(['حروب', URL_MAIN + 'category/%d8%ad%d8%b1%d9%88%d8%a8/'])
    liste.append(['الجريمة', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%ac%d8%b1%d9%8a%d9%85%d8%a9/'])
    liste.append(['رومانسى', URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/'])
    liste.append(['خيال علمى', URL_MAIN + 'category/%d8%ae%d9%8a%d8%a7%d9%84-%d8%b9%d9%84%d9%85%d9%8a/'])
    liste.append(['اثارة', URL_MAIN + 'category/%d8%a7%d8%ab%d8%a7%d8%b1%d8%a9/'])
    liste.append(['وثائقى', URL_MAIN + 'category/%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a/'])
    liste.append(['غموض', URL_MAIN + 'category/%d8%ba%d9%85%d9%88%d8%b6/'])

    for sTitle, sUrl in liste:

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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    
      # (.+?) ([^<]+) .+?
    sPattern = '<p class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "مسلسل"  in aEntry[1]:
                continue
 
            if "حلقة"  in aEntry[1]:
                continue

            if "انمي"  in aEntry[1]:
                continue 
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
 
 
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]
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

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
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
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<p class="thumb">.+?href="([^"]+)" title="([^"]+)">.+?src="([^"]+)' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if "فيلم"  in aEntry[1]:
                continue

            siteUrl = aEntry[0]
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace('الموسم','S').replace('موسم','S').split('الحلقة')[0].replace('الأول','1').replace('الاول','1').replace('الثاني','2').replace('كامل','').replace('-','')
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)

    sPattern = '<div class="title">(.+?)</div>(.+?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] :
       
        for aEntry in aResult[1]:
            sServer = aEntry[0]
            sHtmlContent = aEntry[1]


            sPattern = "onclick=.+?.href='([^']+).+?>(.+?)</button>"


            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
	
            if aResult[0] :
                    for aEntry in aResult[1]:
 
                        siteUrl = aEntry[0]
                        sTitle = sServer
                        sTitle = sTitle+" "+aEntry[1].replace('الحلقة','E').replace('حلقة','E')
                        sThumb = sThumb		


                        sHosterUrl = siteUrl  
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sTitle)
                            oHoster.setFileName(sTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
       
    oGui.setEndOfDirectory() 
	 

def showHosters2():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
     # (.+?) ([^<]+) .+?

    sPattern = 'data-src="([^"]+)'
    oParser = cParser()
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

    oParser = cParser()
     # (.+?) ([^<]+) .+?

    sStart = '<span class="server_btn"'
    sEnd = '<div class="tabs_content"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="(.+?)" class="download_btn">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
                oRequestHandler = cRequestHandler(aEntry)                        
                sHtmlContent = oRequestHandler.request()
                oParser = cParser()
                sStart = '<section id="content">'
                sEnd = '</div>'
                sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
                
                sPattern = '<a href="(.+?)" class="download_btn"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                VSlog(sHosterUrl)
                if aResult[0]:
                    for aEntry in aResult[1]:               
                        sHosterUrl = aEntry

                        VSlog(sHosterUrl)
                        if 'movietime' in sHosterUrl:
                            oHoster = cHosterGui().getHoster('lien_direct')
                            if oHoster:
                                oHoster.setDisplayName(sMovieTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb)
                        else:
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sMovieTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
