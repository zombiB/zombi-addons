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
from resources.lib.Styling import getGenreIcon

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
SITE_IDENTIFIER = 'filmihq'
SITE_NAME = 'FilmiHQ'
SITE_DESC = 'arabic vod'

UA = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.48 Mobile Safari/537.36'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'search?q=%D9%81%D9%8A%D9%84%D9%85', 'showMovies')
MOVIE_HI = (URL_MAIN + 'genre/indian-movies.html', 'showMovies')
SERIE_EN = (URL_MAIN + 'search?q=مسلسل', 'showSeries')
SERIE_TR = (URL_MAIN + 'genre/turkish-series.html', 'showSeries')

SERIE_GENRES = (True, 'seriesGenres')
MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (URL_MAIN + '/search?q=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?q=فيلم+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?q=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', icons + '/Genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', icons + '/Genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?q=مسلسل+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?q=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'genre/action.html'])
    liste.append(['انيميشن', URL_MAIN + 'genre/animation.html'])
    liste.append(['مغامرات', URL_MAIN + 'genre/adventure.html'])
    liste.append(['تاريخي', URL_MAIN + 'genre/history.html'])
    liste.append(['كوميديا', URL_MAIN + 'genre/comedy.html'])
    liste.append(['موسيقى', URL_MAIN + 'genre/music.html'])
    liste.append(['رياضي', URL_MAIN + 'genre/music.html'])
    liste.append(['دراما', URL_MAIN + 'genre/drama.html'])
    liste.append(['رعب', URL_MAIN + 'genre/horror.html'])
    liste.append(['عائلي', URL_MAIN + 'genre/family.html'])
    liste.append(['فانتازيا', URL_MAIN + 'genre/fantasy.html'])
    liste.append(['حروب', URL_MAIN + 'genre/war.html'])
    liste.append(['الجريمة', URL_MAIN + 'genre/crime.html'])
    liste.append(['رومانسي', URL_MAIN + 'genre/romance.html'])
    liste.append(['خيال علمي', URL_MAIN + 'genre/science-fiction.html'])
    liste.append(['اثارة', URL_MAIN + 'genre/thriller.html'])
    liste.append(['وثائقي', URL_MAIN + 'genre/documentary.html'])
    liste.append(['نيتفليكس', URL_MAIN + 'genre/netflix.html'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, getGenreIcon(sTitle), oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'genre/action.html'])
    liste.append(['انيميشن', URL_MAIN + 'genre/animation.html'])
    liste.append(['مغامرات', URL_MAIN + 'genre/adventure.html'])
    liste.append(['تاريخي', URL_MAIN + 'genre/history.html'])
    liste.append(['كوميديا', URL_MAIN + 'genre/comedy.html'])
    liste.append(['موسيقى', URL_MAIN + 'genre/music.html'])
    liste.append(['رياضي', URL_MAIN + 'genre/music.html'])
    liste.append(['دراما', URL_MAIN + 'genre/drama.html'])
    liste.append(['رعب', URL_MAIN + 'genre/horror.html'])
    liste.append(['عائلي', URL_MAIN + 'genre/family.html'])
    liste.append(['فانتازيا', URL_MAIN + 'genre/fantasy.html'])
    liste.append(['حروب', URL_MAIN + 'genre/war.html'])
    liste.append(['الجريمة', URL_MAIN + 'genre/crime.html'])
    liste.append(['رومانسي', URL_MAIN + 'genre/romance.html'])
    liste.append(['خيال علمي', URL_MAIN + 'genre/science-fiction.html'])
    liste.append(['اثارة', URL_MAIN + 'genre/thriller.html'])
    liste.append(['وثائقي', URL_MAIN + 'genre/documentary.html'])
    liste.append(['نيتفليكس', URL_MAIN + 'genre/netflix.html'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, getGenreIcon(sTitle), oOutputParameterHandler)

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
    sPattern = 'data-container="body" title="(.+?)".+?"latest-movie-img-container lazy" style="(.+?)".+?<span class="label label-primary">(.+?)</span>.+?<a href="(.+?)">' 

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
 
            if "مسلسل"  in aEntry[0]:
                continue
 
            if "حلقة"  in aEntry[0]:
                continue

            if "انمي"  in aEntry[0]:
                continue 
            
            sTitle = aEntry[0].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
 
 
            siteUrl = aEntry[3]
            sDesc = aEntry[2]
            sThumb = aEntry[1].replace("background-image: url(","").replace("); display: inline-block;","").replace("'","")
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
    sPattern = 'data-container="body" title="(.+?)".+?"latest-movie-img-container lazy" style="(.+?)".+?<span class="label label-primary">(.+?)</span>.+?<a href="(.+?)">' 

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

            if "فيلم"  in aEntry[0]:
                continue

            siteUrl = aEntry[3]
            
            sTitle = aEntry[0].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[1].replace("background-image: url(","").replace("); display: inline-block;","").replace("'","")
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
    sPattern = 'class ="pagination">.+?class="active"><a href=".+?</li><li><a href="([^"]+)'
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

    sPattern = '<div class="movie-heading overflow-hidden"> <span>([^<]+)</span>(.+?)<script type = "text/javascript" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            if "EN Server" in aEntry[0]:
                continue
 
            if "No Subtitle" in aEntry[0]:
                continue

            if "Non Subtitled Servers" in aEntry[0]:
                continue

            if "Non Sub Servers" in aEntry[0]:
                continue

            sSeason = aEntry[0]
            sHtmlContent = aEntry[1]
 # ([^<]+) .+?

            sPattern = 'href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
	
            if aResult[0] :
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = aEntry[0]
                    sTitle = sSeason
                    sTitle = sTitle+" "+aEntry[2].replace('حلقة','E')
                    sThumb = aEntry[1]
                    sDesc = ""
			


                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
       
    oGui.setEndOfDirectory() 
	 
def showHosters():
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

    sPattern = '<div class="video-embed-container"><iframe class="responsive-embed-item" src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)


    if aResult[0] :
        for aEntry in aResult[1]:
            url = aEntry.split('mp4')[0]
            sTitle = " "
            if url.startswith('//'):
                url = 'http:' + url
				
					
            if 'filmihq' in url:
                continue
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
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

    sStart = '<div class="season">'
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'filmihq' in aEntry:
                oRequestHandler = cRequestHandler(aEntry)                        
                sHtmlContent = oRequestHandler.request()
                sPattern = '<iframe.+?src="([^"]+)'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:               
                        sHosterUrl = aEntry
                        sTitle = " "
                        if 'filmihq' in sHosterUrl:
                            continue
                        if 'userload' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                        if 'moshahda' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                        if 'mystream' in sHosterUrl:
                            sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            sDisplayTitle = sTitle
                            oHoster.setDisplayName(sDisplayTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()