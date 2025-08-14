# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, addon, isMatrix, VSlog
from resources.lib.util import cUtil
from resources.lib.tmdb import cTMDb

SITE_IDENTIFIER = 'xprime'
SITE_NAME = 'X-Prime'
SITE_DESC = 'english vod'

URL_MAIN = 'https://www.themoviedb.org/'

MOVIE_EN = ('trending/movie/week', 'showMovies')
KID_MOVIES = ('discover/movie?with_genres=16', 'showMovies')
MOVIE_TOP = ('movie/top_rated', 'showMovies')
MOVIE_POP = ('movie/popular', 'showMovies')
MOVIE_GENRES = ('genre/movie/list', 'showGenreMovie')

SERIE_EN = ('trending/tv/week', 'showSeries')

URL_SEARCH_MOVIES = ('https://api.themoviedb.org/3/search/movie?include_adult=false&query=', 'showMovies')
URL_SEARCH_SERIES = ('https://api.themoviedb.org/3/search/tv?include_adult=false&query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', '%s (TMDB)' % addons.VSlang(30330), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30425), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انيميشن', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30426), 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30427), 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30429), 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'discover/tv?watch_region=US&sort_by=vote_average.desc')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30431), 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'search/movie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', addons.VSlang(30423), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'search/tv')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', addons.VSlang(30424), '1/Search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText.replace(' ', '+'))
        oGui.setEndOfDirectory()
        return

def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showSeries(sSearchText.replace(' ', '+'))
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch=''):
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/movie', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        sUrl = oInputParameterHandler.getValue('siteUrl')
        result = grab.getUrl(sUrl, iPage, term)

    try:
            for i in result['results']:
                if i['original_language'] == 'en':

                    i = grab._format(i, '', "movie")

                    sId, sTitle, simdb_id, sThumb, sDesc, sYear = i['tmdb_id'], i['title'], i['imdb_id'], i['poster_path'], i['plot'], i['year']

                    if not isMatrix():
                        sTitle = sTitle.encode("utf-8")
                    siteUrl = f'tmdbId={sId}&imdbId={simdb_id}'
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('simdb_id', simdb_id)
                    oOutputParameterHandler.addParameter('sTmdbId', sId)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oOutputParameterHandler.addParameter('sType', 'movie')
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]لم يتم العثور على نتائج.[/COLOR]')

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch=''):
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    iPage = 1
    term = ''
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')

    if oInputParameterHandler.exist('sSearch'):
        sSearch = oInputParameterHandler.getValue('sSearch')

    if sSearch:
        result = grab.getUrl('search/tv', iPage, 'query=' + sSearch)
        sUrl = ''

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if oInputParameterHandler.exist('genre'):
            term = 'with_genres=' + oInputParameterHandler.getValue('genre')

        if oInputParameterHandler.exist('session_id'):
            term += 'session_id=' + oInputParameterHandler.getValue('session_id')

        result = grab.getUrl(sUrl, iPage, term)

    oGui = cGui()

    try:
            for i in result['results']:
                if i['original_language'] == 'en':

                    i = grab._format(i, '', "tvshow")
                    sId, simdb_id, sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['tmdb_id'], i['imdb_id'], i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

                    if not isMatrix():
                        sTitle = sTitle.encode("utf-8")

                    sSiteUrl = 'tv/' + str(sId)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sId', sId)
                    oOutputParameterHandler.addParameter('sFanart', sFanart)
                    oOutputParameterHandler.addParameter('sTmdbId', sId)
                    oOutputParameterHandler.addParameter('simdb_id', simdb_id)
                    oOutputParameterHandler.addParameter('sYear', sYear)

                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                if sSearch:
                    oOutputParameterHandler.addParameter('sSearch', sSearch)
                if oInputParameterHandler.exist('genre'):
                    oOutputParameterHandler.addParameter('genre', oInputParameterHandler.getValue('genre'))
                oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]لم يتم العثور على نتائج.[/COLOR]')

    if not sSearch:
        oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()

    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sId = oInputParameterHandler.getValue('sId')
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sYear = oInputParameterHandler.getValue('sYear')

    if not sId:
        sId = sUrl.split('/')[-1]

    if not sFanart:
        sFanart = ''

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)

    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sMovieTitle))
    else:
        oOutputParameterHandler.addParameter('searchtext', sMovieTitle)

    result = grab.getUrl(sUrl)
    total = len(result)
    if total > 0:
        total = len(result['seasons'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['seasons']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sNbreEp, SSeasonNum = i['episode_count'], i['season_number']

            i = grab._format(i, '', "season")
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            sTitle = 'Season ' + str(SSeasonNum) + ' (' + str(sNbreEp) + ')'

            sUrl = 'tv/' + str(sId) + '/season/' + str(SSeasonNum)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sId', sId)
            oOutputParameterHandler.addParameter('sSeason', SSeasonNum)
            oOutputParameterHandler.addParameter('sFanart', sFanart)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('simdb_id', simdb_id)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesEpisode', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSeriesEpisode():
    grab = cTMDb()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sFanart = oInputParameterHandler.getValue('sFanart')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sYear = oInputParameterHandler.getValue('sYear')

    sSeason = oInputParameterHandler.getValue('sSeason')
    if not sSeason:
        sSeason = sUrl.split('/')[-1]

    if not sFanart:
        sFanart = ''

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sMovieTitle)
    search = '%s S%02d' % (sMovieTitle, int(sSeason))

    if not isMatrix():
        oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(search))
    else:
        oOutputParameterHandler.addParameter('searchtext', search)

    result = grab.getUrl(sUrl)

    total = len(result)
    if total > 0 and 'episodes' in result:
        total = len(result['episodes'])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for i in result['episodes']:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sEpNumber = i['episode_number']

            i = grab._format(i, '')
            sTitle, sGenre, sThumb, sFanart, sDesc, sYear = i['title'], i['genre'], i['poster_path'], i['backdrop_path'], i['plot'], i['year']

            if not isMatrix():
                sTitle = sTitle.encode("utf-8")

            sTitle = 'S%s E%s %s' % (sSeason, str(sEpNumber), sTitle)

            sExtraTitle = ' S' + "%02d" % int(sSeason) + 'E' + "%02d" % int(sEpNumber)

            oOutputParameterHandler.addParameter('siteUrl', sMovieTitle + '|' + sExtraTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            oOutputParameterHandler.addParameter('simdb_id', simdb_id)
            oOutputParameterHandler.addParameter('sSeason', sSeason)
            oOutputParameterHandler.addParameter('sEpisode', sEpNumber)
            oOutputParameterHandler.addParameter('sType', 'tv')
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sType = oInputParameterHandler.getValue('sType')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sYear = oInputParameterHandler.getValue('sYear')
    
    if simdb_id == '' or simdb_id is False:
        addons = addon()
        API_Key = addons.getSetting('api_tmdb')

        if sType == 'movie':
            sApi = f'https://api.themoviedb.org/3/movie/{sTmdbId}?api_key={API_Key}'
        else:
            sApi = f'https://api.themoviedb.org/3/tv/{sTmdbId}/external_ids?api_key={API_Key}'
        oRequestHandler = cRequestHandler(sApi)
        data = oRequestHandler.request(jsonDecode=True)

        simdb_id = data["imdb_id"]

    oRequestHandler = cRequestHandler('https://backend.xprime.tv/servers')
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    servers = sHtmlContent["servers"]
    for sServer in servers:
        oOutputParameterHandler = cOutputParameterHandler()
        if sServer.get("status") != "ok":
            continue
        sName = sServer.get("name")

        sDisplayTitle = f'{sMovieTitle} [COLOR coral]- {sName}[/COLOR]'      
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        oOutputParameterHandler.addParameter('simdb_id', simdb_id)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sServer', sName)
        oOutputParameterHandler.addParameter('sType', sType)
        oOutputParameterHandler.addParameter('sYear', sYear)

        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sEpisode = oInputParameterHandler.getValue('sEpisode')
    sSeason = oInputParameterHandler.getValue('sSeason')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sServer = oInputParameterHandler.getValue('sServer')
    simdb_id = oInputParameterHandler.getValue('simdb_id')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    sType = oInputParameterHandler.getValue('sType')
    sYear = oInputParameterHandler.getValue('sYear')

    query_params = {"name": sMovieTitle.replace(' ','%20') or ""}
    if sServer == "primebox":
        if sYear is not False:
            query_params["fallback_year"] = sYear
        if sSeason is not False and sEpisode is not False:
            query_params["season"] = sSeason
            query_params["episode"] = sEpisode
    else:
        if sYear is not False:
            query_params["year"] = sYear
        if sTmdbId:
            query_params["id"] = sTmdbId
            query_params["imdb"] = simdb_id
        if sSeason is not False and sEpisode is not False:
            query_params["season"] = sSeason
            query_params["episode"] = sEpisode

    final_url = f'https://backend.xprime.tv/{sServer}' + "?" + "&".join(f"{k}={v}" for k, v in query_params.items())

    oRequestHandler = cRequestHandler(final_url)
    data = oRequestHandler.request(jsonDecode=True)

    if sServer == "primebox":
        streams = data.get("streams", {})
            
        qualities = data.get("available_qualities", [])
        for quality in qualities:
            url = streams.get(quality)
            if url:
                sHosterUrl = f'{url}|Referer=https://xprime.tv&Origin=https://xprime.tv'
                sDisplayTitle = f'{sMovieTitle} [{quality}]'

            oHoster = cHosterGui().getHoster('directplay') 
            if oHoster:  
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        url = data.get("url")
        if url:
            sHosterUrl = f'{url}|Referer=https://xprime.tv&Origin=https://xprime.tv'
            sDisplayTitle = f'{sMovieTitle}'

        oHoster = cHosterGui().getHoster('directplay') 
        if oHoster:  
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
