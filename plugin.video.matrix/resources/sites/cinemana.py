# -*- coding: utf-8 -*-
# Yonn1981 https://github.com/Yonn1981/Repo

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib import random_ua
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
 
SITE_IDENTIFIER = 'cinemana'
SITE_NAME = 'Cinemana'
SITE_DESC = 'arabic vod'

UA = random_ua.get_ua()

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movies/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/page/arabic-movies/', 'showMovies')
SERIE_GENRES = (True, 'seriesGenres')
MOVIE_GENRES = (True, 'moviesGenres')

SERIE_EN = (URL_MAIN + '/watch=category/مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (URL_MAIN + '/watch=category/مسلسلات-عربية/', 'showSeries')
SERIE_TR = (URL_MAIN + '/watch=category/مسلسلات-تركية/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/watch=category/مسلسلات-اسيوية/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/watch=category/مسلسلات-هندية/', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + 'watch=category/مسلسلات-رمضان-2024/', 'showSeries')

SPORT_WWE = (URL_MAIN + '/watch=category/مصارعة-حرة/', 'showMovies')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/?search=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/?search=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية',  icons + '/TVShowsKorean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية',  icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية',  icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة',  icons + '/WWE.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)',  icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)',  icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/?search=مسلسل+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText+'&type=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'search/?search=مسلسل&genre=47'])
    liste.append(['انيميشن', URL_MAIN + 'search/?search=مسلسل&genre=309'])
    liste.append(['مغامرات', URL_MAIN + 'search/?search=مسلسل&genre=153'])
    liste.append(['تاريخي', URL_MAIN + 'search/?search=مسلسل&genre=25'])
    liste.append(['كوميديا', URL_MAIN + 'search/?search=مسلسل&genre=8'])
    liste.append(['موسيقى', URL_MAIN + 'search/?search=مسلسل&genre=131'])
    liste.append(['رياضي', URL_MAIN + 'search/?search=مسلسل&genre=17986'])
    liste.append(['دراما', URL_MAIN + 'search/?search=مسلسل&genre=27'])
    liste.append(['رعب', URL_MAIN + 'search/?search=مسلسل&genre=225'])
    liste.append(['عائلى', URL_MAIN + 'search/?search=مسلسل&genre=237'])
    liste.append(['فانتازيا', URL_MAIN + 'search/?search=مسلسل&genre=73'])
    liste.append(['حروب', URL_MAIN + 'search/?search=مسلسل&genre=79'])
    liste.append(['الجريمة', URL_MAIN + 'search/?search=مسلسل&genre=26'])
    liste.append(['رومانسى', URL_MAIN + 'search/?search=مسلسل&genre=37'])
    liste.append(['خيال علمى', URL_MAIN + 'search/?search=مسلسل&genre=91'])
    liste.append(['اثارة', URL_MAIN + 'search/?search=مسلسل&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', URL_MAIN + 'search/?search=مسلسل&genre=342'])
    liste.append(['وثائقى', URL_MAIN + 'search/?search=مسلسل&genre=195'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'search/?search=فيلم&genre=47'])
    liste.append(['انيميشن', URL_MAIN + 'search/?search=فيلم&genre=309'])
    liste.append(['مغامرات', URL_MAIN + 'search/?search=فيلم&genre=153'])
    liste.append(['تاريخي', URL_MAIN + 'search/?search=فيلم&genre=25'])
    liste.append(['كوميديا', URL_MAIN + 'search/?search=فيلم&genre=8'])
    liste.append(['موسيقى', URL_MAIN + 'search/?search=فيلم&genre=131'])
    liste.append(['رياضي', URL_MAIN + 'search/?search=فيلم&genre=17986'])
    liste.append(['دراما', URL_MAIN + 'search/?search=فيلم&genre=27'])
    liste.append(['رعب', URL_MAIN + 'page/افلام-رعب/'])
    liste.append(['عائلى', URL_MAIN + 'search/?search=فيلم&genre=237'])
    liste.append(['فانتازيا', URL_MAIN + 'search/?search=فيلم&genre=73'])
    liste.append(['حروب', URL_MAIN + 'search/?search=فيلم&genre=79'])
    liste.append(['الجريمة', URL_MAIN + 'search/?search=فيلم&genre=26'])
    liste.append(['رومانسى', URL_MAIN + 'search/?search=فيلم&genre=37'])
    liste.append(['خيال علمى', URL_MAIN + 'search/?search=فيلم&genre=91'])
    liste.append(['اثارة', URL_MAIN + 'search/?search=فيلم&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', URL_MAIN + 'search/?search=فيلم&genre=342'])
    liste.append(['وثائقى', URL_MAIN + 'search/?search=فيلم&genre=195'])

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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="ItemBlock">.+?<a href="(.+?)".+?style="(.+?)"></div>.+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            if "مسلسل"  in aEntry[2]:
                continue
 
            if "حلقة"  in aEntry[2]:
                continue
 
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
            siteUrl = aEntry[0]
            sDesc = ""
            sThumb = aEntry[1].replace("background-image: url(","").replace(");","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')
                else:
                    sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="ItemBlock">.+?<a href="(.+?)".+?style="(.+?)"></div>.+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if "فلم"  in aEntry[2]:
                continue
            if "فيلم"  in aEntry[2]:
                continue
            if "movie"  in aEntry[2]:
                continue

            siteUrl = aEntry[0]           
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[1].replace("background-image: url(","").replace(");","")
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('الحلقة')[0].split('حلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            if sTitle not in itemList:
                itemList.append(sTitle)			
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

    if not sSearch:
        oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNext = aResult[1][0]
        if 'http' not in sNext:
            sNext = URL_MAIN + aResult[1][0]
        return sNext

    return False
	
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="(.+?)" title=.+?class=.+?>(.+?)</a>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace(" ","").replace("EP"," E")
            if "|" in aEntry[1]:
                Ss = aEntry[1].replace(" ","").split("|")[0]
            else:
                Ss = "S1"
            sTitle = Ss+' '+sEp+' '+sMovieTitle
            sTitle = sTitle.replace("|","")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 
	 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<a data-like="likeCount" data-id="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0]:
        sId = aResult[1][0]
        sId = sId

    sPattern = 'data-server="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        for aEntry in aResult[1]:

            cook = oRequestHandler.GetCookies()
            oRequestHandler = cRequestHandler(URL_MAIN + 'wp-content/themes/EEE/Inc/Ajax/Single/Server.php')
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
            oRequestHandler.addHeaderEntry('cookie', cook)
            oRequestHandler.addParameters('post_id', sId)
            oRequestHandler.addParameters('server', aEntry)
            oRequestHandler.setRequestType(1)
            sHtmlContent = oRequestHandler.request()

            sPattern =  '<iframe.+?src="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry.split('\\')[0]
                    if url.startswith('//'):
                       url = 'http:' + url
            
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				            
    oGui.setEndOfDirectory()