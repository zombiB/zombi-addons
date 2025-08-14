# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.comaddon import progress
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnees videos.'

URL_MAIN = 'https://www.imdb.com/'
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'

MOVIE_WORLD = (URL_MAIN + 'search/title/?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
MOVIE_TOP250 = (URL_MAIN + 'search/title/?count=100&groups=top_250', 'showMovies')
MOVIE_ANNEES = (True, 'showMovieYears')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'أفضل الأفلام العالمية', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP250[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP250[1], 'افضل ۲٥۰ فلم', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'الأفضل (حسب السنة)', '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    import datetime

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1903, int(datetime.datetime.now().year) + 1)):
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'search/title?year=' + str(i) + ',' + str(i) + '&title_type=feature&explore=languages')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(i), '1/Calendar.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'img alt="([^"]+)" class="ipc-image".+?src="([^"]+)".+?<h3 class="ipc-title__text">([^<]+)</h3>.+?role="presentation">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2].split('.')[1].strip()
            sThumb = aEntry[1].split('._')[0] + '._V1_FMjpg_UX1000_.jpg'
            sYear = re.search('([0-9]{4})', aEntry[0]).group(1)
            sDesc = f'[COLOR fuchsia]{aEntry[0]}[/COLOR] \n \n {aEntry[3]}'

            oOutputParameterHandler.addParameter('siteUrl', 'none')
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('searchtext', str(sTitle))
            oGui.addMovie('globalSearch', 'showSearch', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory('500')
