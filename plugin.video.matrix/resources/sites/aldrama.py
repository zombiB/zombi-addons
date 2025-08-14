# -*- coding: utf-8 -*-

import re
import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon, siteManager
from resources.sites.wecima import showHosters
from resources.sites.akwam import showHosters as showAkwam
from resources.sites.faselhd import decode_page
from resources.lib.util import cUtil

UA = "okhttp/4.8.0"

SITE_IDENTIFIER = 'aldrama'
SITE_NAME = 'Al-Drama'
SITE_DESC = 'arabic vod'

sHost = base64.b64decode('L2lwYS9tb2Muc29ycHliYXJhLnBwYS8vOnNwdHRo').decode("utf-8")
URL_MAIN = sHost[::-1]

mHost = base64.b64decode('LzMxZGFjYjEyZmZlZi05NzliLTE3YjQtMmVmOS1kZmJhNjA1ZC81ODE1MzZERERFQ0FFNDVBRjY4QTlEM0M5QTVGNC8=').decode("utf-8")
mHost_Ext = mHost[::-1]

MOVIE_EN = (f'{URL_MAIN}poster/by/filtres/22/created/0{mHost_Ext}', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}poster/by/filtres/20/created/0{mHost_Ext}', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}poster/by/filtres/19/created/0{mHost_Ext}', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}poster/by/filtres/27/created/0{mHost_Ext}', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}poster/by/filtres/65/created/0{mHost_Ext}', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}poster/by/filtres/61/created/0{mHost_Ext}', 'showMovies')
MOVIE_POP = (f'{URL_MAIN}poster/by/filtres/25/created/0{mHost_Ext}', 'showMovies')
MOVIE_CLASSIC = (f'{URL_MAIN}poster/by/filtres/29/created/0{mHost_Ext}', 'showMovies')

SERIE_EN = (f'{URL_MAIN}poster/by/filtres/18/created/0{mHost_Ext}', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}poster/by/filtres/23/created/0{mHost_Ext}', 'showSeries')
SERIE_AR = (f'{URL_MAIN}poster/by/filtres/16/created/0{mHost_Ext}', 'showSeries')
SERIE_TR = (f'{URL_MAIN}poster/by/filtres/17/created/0{mHost_Ext}', 'showSeries')
REPLAYTV_NEWS = (f'{URL_MAIN}poster/by/filtres/28/created/0{mHost_Ext}', 'showSeries')
SERIE_NETFLIX = (f'{URL_MAIN}poster/by/filtres/81/created/0{mHost_Ext}', 'showSeries')
RAMADAN_SERIES = (f'{URL_MAIN}poster/by/filtres/88/created/0{mHost_Ext}', 'showSeries')

ANIM_NEWS = (f'{URL_MAIN}poster/by/filtres/55/created/0{mHost_Ext}', 'showSeries')
DOC_SERIES = (f'{URL_MAIN}poster/by/filtres/49/created/0{mHost_Ext}', 'showSeries')

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
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', '1/Classic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/Anime.png', oOutputParameterHandler)
    
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
 
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', '1/Programs.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}/0{mHost_Ext}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}/0{mHost_Ext}'
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
        sUrl = f'{sUrl}/0{mHost_Ext}'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    if sSearch:
        sHtmlContent = sHtmlContent.get('posters')

    for aEntry in sHtmlContent:
            
            sType = aEntry.get('type')
            if sType == 'serie':
                continue
            sTitle = aEntry.get('title')
            siteUrl = f'{URL_MAIN}movie/source/by/{aEntry.get("id")}{mHost_Ext}'
            sThumb = aEntry.get('image')
            sDesc = aEntry.get('description')
            sYear = aEntry.get('year')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


    sNextPage = __checkForNextPage(sUrl)
    if sNextPage:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
        sUrl = f'{sUrl}/0{mHost_Ext}'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)
    if sSearch:
        sHtmlContent = sHtmlContent.get('posters')

    for aEntry in sHtmlContent:
            
            sType = aEntry.get('type')
            if sType == 'movie':
                continue
            sTitle = aEntry.get('title')
            siteUrl = f'{URL_MAIN}season/by/serie/{aEntry.get("id")}{mHost_Ext}'
            sThumb = aEntry.get('image')
            sDesc = aEntry.get('description')
            sYear = aEntry.get('year')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
                
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sNextPage = __checkForNextPage(sUrl)
    if sNextPage:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for season in sHtmlContent:
        sSeason = season['title']
        season_id = sSeason
        sSeason = cUtil().ConvertSeasons(sSeason)
        sTitle = ("%s %s") % (sMovieTitle, sSeason.replace(" ", ""))      
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
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sel_season = [season for season in sHtmlContent if season['title'] == season_id]
    for season in sel_season:
        season_id = season['title']
        episodes = season['episodes']

        for episode in episodes:
            episode_id = episode['id']
            sEpisode = episode['title']
            siteUrl = f'{URL_MAIN}episode/source/by/{episode_id}{mHost_Ext}'
            sTitle = ("%s %s") % (sMovieTitle, sEpisode.replace('الحلقة ','E'))         
            sThumb = sThumb
            sDesc = sDesc

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('season_id', season_id)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
	
def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('connection', 'Keep-Alive')
    oRequestHandler.addHeaderEntry('accept-encoding', 'gzip')
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for aEntry in sHtmlContent:
            
            sHosterUrl = aEntry.get('url')
            if 'zplayer.io' in sHosterUrl:
                sHosterUrl = f'https://short.ink/{sHosterUrl.split("/?v=")[1]}'

            elif 'cimanow' in sHosterUrl or 'newcima' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={siteManager().getUrlMain("cimanow")}' 
                oHoster = cHosterGui().getHoster('mycima')
                if '/e/' in sHosterUrl:
                    oHoster = cHosterGui().getHoster('cimanow')
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)     

            elif 'faselhd' in sHosterUrl:
                try:
                    from resources.lib.parser import cParser
                    oParser = cParser() 
                    oRequest = cRequestHandler(sHosterUrl)
                    oRequest.enableCache(False)
                    oRequest.addHeaderEntry('referer', siteManager().getUrlMain("faselhd"))
                    data = oRequest.request()
                    if 'adilbo' in data:
                        data = decode_page(data)
                    
                    sPattern =  'data-url="([^<]+)">([^<]+)</button>' 
                    aResult = oParser.parse(data, sPattern)
                    if aResult[0]:
                        for aEntry in aResult[1]:
                            sHosterUrl = aEntry[0]
                            sHost = aEntry[1].upper()
                            sTitle = f'{sMovieTitle} ({sHost})'
                            oHoster = cHosterGui().getHoster('faselhd') 
                            if oHoster:
                                oHoster.setDisplayName(sTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)   
                except:
                    VSlog('Fasel Failed')
                    
            elif bool(re.search(r'mega.*max', sHosterUrl)):
                from resources.lib.multihost import cMegamax
                oOutputParameterHandler = cOutputParameterHandler()

                data = cMegamax().GetUrls(sHosterUrl)
                if data is not False:
                    for item in data:
                        sHosterUrl = item.split(',')[0].split('=')[1]
                        sQual = item.split(',')[1].split('=')[1]
                        sLabel = item.split(',')[2].split('=')[1]

                        sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'      
                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
            
            elif 'wecima' in sHosterUrl:
                oOutputParameterHandler = cOutputParameterHandler()

                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', f'{sMovieTitle} [COLOR gold] - WeCima[/COLOR]', '', sThumb, sDesc, oOutputParameterHandler)

            elif 'ak.sv' in sHosterUrl:
                oOutputParameterHandler = cOutputParameterHandler()

                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addMovie(SITE_IDENTIFIER, 'showAkwam', f'{sMovieTitle} [COLOR gold] - Akwam[/COLOR]', '', sThumb, sDesc, oOutputParameterHandler)

            else:
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

def __checkForNextPage(sUrl):
    pattern = r"created\/(\d+)\/"
    match = re.search(pattern, sUrl)
    if match:
        number = int(match.group(1)) + 1
        return re.sub(pattern, f"created/{number}/", sUrl)

    return False
