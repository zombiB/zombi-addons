# -*- coding: utf-8 -*-

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.util import cUtil
from resources.lib.parser import cParser
from resources.lib import random_ua
 
SITE_IDENTIFIER = 'cinemana'
SITE_NAME = 'Cinemana'
SITE_DESC = 'arabic vod'

UA = random_ua.get_ua()

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}movies/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}page/arabic-movies/', 'showMovies')
SERIE_GENRES = (True, 'seriesGenres')
MOVIE_GENRES = (True, 'moviesGenres')

SERIE_EN = (f'{URL_MAIN}watch=category/مسلسلات-اجنبي/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}watch=category/مسلسلات-عربية/', 'showSeries')
SERIE_TR = (f'{URL_MAIN}watch=category/مسلسلات-تركية/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}watch=category/مسلسلات-اسيوية/', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}watch=category/مسلسلات-هندية/', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}watch=category/مسلسلات-رمضان-2025/', 'showSeries')

SPORT_WWE = (f'{URL_MAIN}watch=category/مصارعة-حرة/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', '1/WWE.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', '1/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}&type=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}search/?search=مسلسل&genre=47'])
    liste.append(['انيميشن', f'{URL_MAIN}search/?search=مسلسل&genre=309'])
    liste.append(['مغامرات', f'{URL_MAIN}search/?search=مسلسل&genre=153'])
    liste.append(['تاريخي', f'{URL_MAIN}search/?search=مسلسل&genre=25'])
    liste.append(['كوميديا', f'{URL_MAIN}search/?search=مسلسل&genre=8'])
    liste.append(['موسيقى', f'{URL_MAIN}search/?search=مسلسل&genre=131'])
    liste.append(['رياضي', f'{URL_MAIN}search/?search=مسلسل&genre=17986'])
    liste.append(['دراما', f'{URL_MAIN}search/?search=مسلسل&genre=27'])
    liste.append(['رعب', f'{URL_MAIN}search/?search=مسلسل&genre=225'])
    liste.append(['عائلى', f'{URL_MAIN}search/?search=مسلسل&genre=237'])
    liste.append(['فانتازيا', f'{URL_MAIN}search/?search=مسلسل&genre=73'])
    liste.append(['حروب', f'{URL_MAIN}search/?search=مسلسل&genre=79'])
    liste.append(['الجريمة', f'{URL_MAIN}search/?search=مسلسل&genre=26'])
    liste.append(['رومانسى', f'{URL_MAIN}search/?search=مسلسل&genre=37'])
    liste.append(['خيال علمى', f'{URL_MAIN}search/?search=مسلسل&genre=91'])
    liste.append(['اثارة', f'{URL_MAIN}search/?search=مسلسل&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', f'{URL_MAIN}search/?search=مسلسل&genre=342'])
    liste.append(['وثائقى', f'{URL_MAIN}search/?search=مسلسل&genre=195'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', f'{URL_MAIN}search/?search=فيلم&genre=47'])
    liste.append(['انيميشن', f'{URL_MAIN}search/?search=فيلم&genre=309'])
    liste.append(['مغامرات', f'{URL_MAIN}search/?search=فيلم&genre=153'])
    liste.append(['تاريخي', f'{URL_MAIN}search/?search=فيلم&genre=25'])
    liste.append(['كوميديا', f'{URL_MAIN}search/?search=فيلم&genre=8'])
    liste.append(['موسيقى', f'{URL_MAIN}search/?search=فيلم&genre=131'])
    liste.append(['رياضي', f'{URL_MAIN}search/?search=فيلم&genre=17986'])
    liste.append(['دراما', f'{URL_MAIN}search/?search=فيلم&genre=27'])
    liste.append(['رعب', f'{URL_MAIN}page/افلام-رعب/'])
    liste.append(['عائلى', f'{URL_MAIN}search/?search=فيلم&genre=237'])
    liste.append(['فانتازيا', f'{URL_MAIN}search/?search=فيلم&genre=73'])
    liste.append(['حروب', f'{URL_MAIN}search/?search=فيلم&genre=79'])
    liste.append(['الجريمة', f'{URL_MAIN}search/?search=فيلم&genre=26'])
    liste.append(['رومانسى', f'{URL_MAIN}search/?search=فيلم&genre=37'])
    liste.append(['خيال علمى', f'{URL_MAIN}search/?search=فيلم&genre=91'])
    liste.append(['اثارة', f'{URL_MAIN}search/?search=فيلم&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', f'{URL_MAIN}search/?search=فيلم&genre=342'])
    liste.append(['وثائقى', f'{URL_MAIN}search/?search=فيلم&genre=195'])

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

    sPattern = r'<div class="ItemBlock">.+?href="([^"]+)".+?url\((https?://[^\)]+)\).+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if any(keyword in aEntry[2] for keyword in ["مسلسل", "حلقة", "موسم"]):
                continue
            
            sTitle = cUtil().CleanMovieName(aEntry[2])
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', aEntry[2])
            if m:
                sYear = str(m.group(0))
                if 'عرض' in sTitle:
                    sTitle = sTitle.replace('عرض','')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
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
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            
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

    sPattern = r'<div class="ItemBlock">.+?href="([^"]+)".+?url\((https?://[^\)]+)\).+?<h3>(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    itemList = []
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if any(keyword in aEntry[2] for keyword in ["فلم", "فيلم", "movie"]):
                continue

            siteUrl = aEntry[0]           
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', aEntry[2])
            if m:
                sYear = str(m.group(0))

            if sTitle not in itemList:
                itemList.append(sTitle)			
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                if any(keyword in aEntry[2] for keyword in ["فلم", "فيلم", "movie"]):
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
        
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-tap="([^"]+)".+?class=".*?">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

            sSeason = aEntry[1].strip()
            sTitle = re.sub(r"S\d{2}|S\d", "", sMovieTitle)
            sTitle = f'{sTitle} S{sSeason}'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
 
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

    else:
        sPattern = r'<a href="([^"]+)"\s*title=".*?"\s*class=".*?">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
    
                sEp = str(m.group(1)) if (m := re.search(r"EP\s*(\d+)", aEntry[1])) else None
                sSeason = str(m.group(1)) if (m := re.search(r"S\s*(\d+)", aEntry[1])) else '01'
                sTitle = re.sub(r"S\d{2}|S\d", "", sMovieTitle)
                sTitle = f'{sTitle} S{sSeason.strip()} E{sEp.strip()}'
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sSeason = oInputParameterHandler.getValue('sSeason')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = (oRequestHandler.request()).replace('class="tab-pane fade direction-right  active in "','seasonEps').replace('class="tab-pane fade direction-right "','seasonEps')

    sStart = f'seasonEps id="{sSeason}">'
    sEnd = '</ul>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = r'<a href="([^"]+)"\s*title=".*?"\s*class=".*?">(.+?)</a>' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = str(m.group(1)) if (m := re.search(r"EP\s*(\d+)", aEntry[1])) else None
            sTitle = f'{sMovieTitle} E{sEp}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

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

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<a data-like="likeCount" data-id="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0]:
        sId = aResult[1][0]

    sPattern = 'data-server="([^"]+)">(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            Serv = aEntry[0]
            sHost = aEntry[1]
            sTitle = f'{sMovieTitle} [COLOR coral]{sHost}[/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('Serv', Serv)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)

            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, sTitle, oOutputParameterHandler)
				            
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Serv = oInputParameterHandler.getValue('Serv')
    sId = oInputParameterHandler.getValue('sId')

    oParser = cParser()
    oRequestHandler = cRequestHandler(f'{URL_MAIN}wp-content/themes/EEE/Inc/Ajax/Single/Server.php')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addParameters('post_id', sId)
    oRequestHandler.addParameters('server', Serv)
    oRequestHandler.enableCache(False)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0]
        if sHosterUrl.startswith('//'):
            sHosterUrl = f'http:{sHosterUrl}'

        if URL_MAIN in sHosterUrl or 'cinemana' in sHosterUrl:
            oRequestHandler = cRequestHandler(sHosterUrl)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl)
            oRequestHandler.setTimeout(120)
            sHtmlContent = oRequestHandler.request()

            sPattern =  'source\s*src=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sHosterUrl = f'{aResult[1][0]}|Referer={sUrl}'
                if sHosterUrl.startswith('//'):
                    sHosterUrl = f'http:{sHosterUrl}'
            else:
                sPattern =  'iframe.+?src=["\']([^"\']+)["\']'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    if sHosterUrl.startswith('//'):
                        sHosterUrl = f'http:{sHosterUrl}'

            if 'userload' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={sUrl}'
            if 'mystream' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={sUrl}'  

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()