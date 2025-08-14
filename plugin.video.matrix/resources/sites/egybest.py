# -*- coding: utf-8 -*-

import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon, siteManager
from resources.sites.wecima import showHosters
from resources.sites.faselhd import decode_page
from resources.lib.util import cUtil

UA = "okhttp/5.0.0-alpha.6"

SITE_IDENTIFIER = 'egybest'
SITE_NAME = 'EgyBest'
SITE_DESC = 'arabic vod'

sHost = base64.b64decode('L2lwYS9jaWxidXAvdG5hdHNlYnlnZS9udC5oY2VsZi5mZWRjYmEvLzpzcHR0aA==').decode("utf-8")
URL_MAIN = sHost[::-1]

mHost = base64.b64decode('cUJBSXpOQjVjbXpoaUhwbVV5UTRBa3lyRmtXZ2JsMnA=').decode("utf-8")
mHost_Ext = mHost[::-1]

MOVIE_EN = (f'{URL_MAIN}networks/media/show/7093-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}networks/media/show/7462-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}networks/media/show/7097-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}networks/media/show/7095-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}networks/media/show/7096-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}genres/animes/all/{mHost_Ext}?page=1', 'showMovies')
ANIM_MOVIES = (f'{URL_MAIN}networks/media/show/7094-vide-created-vide-movie/{mHost_Ext}?page=1', 'showMovies')
MOVIE_POP = (f'{URL_MAIN}genres/popularmovies/all/{mHost_Ext}?page=1', 'showMovies')

SERIE_EN = (f'{URL_MAIN}networks/media/show/7865-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}networks/media/show/7866-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_AR = (f'{URL_MAIN}networks/media/show/7007-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_TR = (f'{URL_MAIN}networks/media/show/7867-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}networks/media/show/7868-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
REPLAYTV_NEWS = (f'{URL_MAIN}networks/media/show/7461-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_NETFLIX = (f'{URL_MAIN}networks/media/show/213/{mHost_Ext}?page=1', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}networks/media/show/8006-vide-created-vide-serie/{mHost_Ext}?page=1', 'showSeries')
SERIE_DUBBED = (f'{URL_MAIN}genres/latestanimes/all/{mHost_Ext}?page=1', 'showSeries')

ANIM_NEWS = (f'{URL_MAIN}networks/media/show/7869/{mHost_Ext}?page=1', 'showSeries')
DOC_SERIES = (f'{URL_MAIN}networks/media/show/213/{mHost_Ext}?page=1', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}search/', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', '1/Ramadan.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/1/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)
     
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', '1/Documentary.png', oOutputParameterHandler) 
        
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', '1/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}/{mHost_Ext}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}/{mHost_Ext}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if mHost_Ext not in sUrl:
        sUrl = f'{sUrl}/{mHost_Ext}'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Accept', "application/json")
    oRequestHandler.addHeaderEntry('Host', "abcdef.flech.tn")
    oRequestHandler.addHeaderEntry('packagename', "com.egyappwatch")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('User-Agent', "EasyPlex (Android 11; Mi 5s; Xiaomi capricorn; en)")
    sHtmlContent_Main = oRequestHandler.request(jsonDecode=True)
    if sSearch:
        sHtmlContent = sHtmlContent_Main.get('search')
    else:
        sHtmlContent = sHtmlContent_Main.get('data')

    for aEntry in sHtmlContent:
            
            sType = aEntry.get('type')
            if sType == 'Serie':
                continue
            sTitle = aEntry.get('title') if aEntry.get('title') else aEntry.get('name', "")
            siteUrl = f'{URL_MAIN}media/detail/{aEntry.get("id")}/{mHost_Ext}'
            sThumb = aEntry.get('poster_path')
            sDesc = aEntry.get('overview') if aEntry.get('overview') else ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle.replace('مترجم',''), '', sThumb, sDesc, oOutputParameterHandler)


    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent_Main)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if mHost_Ext not in sUrl:
        sUrl = f'{sUrl}/{mHost_Ext}'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Accept', "application/json")
    oRequestHandler.addHeaderEntry('Host', "abcdef.flech.tn")
    oRequestHandler.addHeaderEntry('packagename', "com.egyappwatch")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('User-Agent', "EasyPlex (Android 11; Mi 5s; Xiaomi capricorn; en)")
    sHtmlContent_Main = oRequestHandler.request(jsonDecode=True)
    if sSearch:
        sHtmlContent = sHtmlContent_Main.get('search')
    else:
        sHtmlContent = sHtmlContent_Main.get('data')

    for aEntry in sHtmlContent:
            
            sType = aEntry.get('type')
            if sType == 'Movie':
                continue
            sTitle = aEntry.get('title') if aEntry.get('title') else aEntry.get('name', "")
            siteUrl = f'{URL_MAIN}series/show/{aEntry.get("id")}/{mHost_Ext}'
            sThumb = aEntry.get('poster_path')
            sDesc = aEntry.get('overview') if aEntry.get('overview') else ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
                
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle.replace('مترجم',''), '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent_Main)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
		
def showSeasons():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Accept', "application/json")
    oRequestHandler.addHeaderEntry('Host', "abcdef.flech.tn")
    oRequestHandler.addHeaderEntry('packagename', "com.egyappwatch")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('User-Agent', "EasyPlex (Android 11; Mi 5s; Xiaomi capricorn; en)")
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for season in sHtmlContent.get('seasons'):
        sSeason = season['season_number']
        season_id = sSeason
        sTitle = ("%s S%s") % (sMovieTitle, str(sSeason))      
        sThumb = sThumb
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('season_id', season_id)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)  

    oGui.setEndOfDirectory() 
  
def showEpisodes():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    season_id = oInputParameterHandler.getValue('season_id')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Accept', "application/json")
    oRequestHandler.addHeaderEntry('Host', "abcdef.flech.tn")
    oRequestHandler.addHeaderEntry('packagename', "com.egyappwatch")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('User-Agent', "EasyPlex (Android 11; Mi 5s; Xiaomi capricorn; en)")
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sel_season = [season for season in sHtmlContent['seasons'] if season['season_number'] == int(season_id)]
    for season in sel_season:
        season_id = season['season_number']
        episodes = season['episodes']

        for episode in episodes:
            episode_id = episode['episode_number']
            sEpisode = episode['name']
            sTitle = ("%s E%s") % (sMovieTitle, str(episode_id))         
            sThumb = episode['still_path']
            sDesc = sDesc

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('season_id', season_id)
            oOutputParameterHandler.addParameter('episode_id', episode_id)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
	
def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    season_id = oInputParameterHandler.getValue('season_id')
    episode_id = oInputParameterHandler.getValue('episode_id')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Accept', "application/json")
    oRequestHandler.addHeaderEntry('Host', "abcdef.flech.tn")
    oRequestHandler.addHeaderEntry('packagename', "com.egyappwatch")
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('User-Agent', "EasyPlex (Android 11; Mi 5s; Xiaomi capricorn; en)")
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if episode_id:
        for season in sHtmlContent['seasons']:
            if str(season['season_number']) == str(season_id):
                for episode in season['episodes']:
                    if str(episode['episode_number']) == str(episode_id):
                        sHtmlContent = episode['videos']
    else:
        sHtmlContent = sHtmlContent.get('videos')
    
    for aEntry in sHtmlContent:
            
            sHosterUrl = aEntry.get('link')
 
            if 'fasel' in sHosterUrl or 'fasoul' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace(sHosterUrl.split('video_player')[0], siteManager().getUrlMain('faselhd')).replace('$','&')
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)    

            if 'akwam' in sHosterUrl or 'animeiat' in sHosterUrl or 'wecima' in sHosterUrl or 'arabseed' in sHosterUrl:
                try:
                    from resources.lib.parser import cParser
                    oParser = cParser() 
                    oRequest = cRequestHandler(f'{URL_MAIN.split("/egybest")[0]}/test.php?api={sHosterUrl}')
                    oRequest.enableCache(False)
                    oRequest.addHeaderEntry('connection', 'Keep-Alive')
                    oRequest.setTimeout(60)
                    oRequest.addHeaderEntry('accept-encoding', 'gzip')
                    oRequest.addHeaderEntry('Host', "abcdef.flech.tn")
                    oRequest.addHeaderEntry('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 Safari/537.36")
                    data = oRequest.request()
                    
                    sPattern =  'href="([^"]+)">\s*<quality>(.+?)</quality>' 
                    aResult = oParser.parse(data, sPattern)
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            if 'wecima' in sHosterUrl:
                                sRefer = siteManager().getUrlMain('wecima')
                                sHosterUrl = f'{aEntry[0]}|Referer={sRefer}'
                            else:
                                sHosterUrl = aEntry[0]
                            sHost = aEntry[1].upper()
                            sTitle = f'{sMovieTitle} ({sHost})'
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                oHoster.setDisplayName(sTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)   
                except:
                    VSlog('Api Failed')

            else:
                try:
                    if aEntry.get('header') is not None:
                        sReferer = aEntry.get('header')
                        sHosterUrl = f'{sHosterUrl}|Referer={sReferer}'
                except:
                    pass
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)             

    oGui.setEndOfDirectory()       

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):

    sNextPage = sHtmlContent['next_page_url'] if sHtmlContent['next_page_url'] else ''
    if sNextPage:
        return sNextPage

    return False
