# -*- coding: utf-8 -*-
# Basic Implementaion

import re
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import isMatrix, siteManager, VSlog
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'anilist_co'
SITE_NAME = '[COLOR orange]AniListDB[/COLOR]'
SITE_DESC = 'Anime database.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

query = '''
query ($sort: [MediaSort], $page: Int) {
  Page(page: $page, perPage: 20) {
    media(sort: $sort, type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
      coverImage {
        extraLarge
      }
      popularity
      averageScore
      startDate {
        year
      }
      description
    }
  }
}
'''

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'animes')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimes', "أنمي", '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'news')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimesNews', "جديد", '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'popular')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimesPop', "رائج", 'pop.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'top')
    oGui.addDir(SITE_IDENTIFIER, 'showAnimesTop', "الافضل", 'top.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesNews():
    variables = {
                'sort': 'START_DATE_DESC',
                'page': 1
                }
    showAnimes(term=variables)

def showAnimesTop():
    variables = {
                "sort": "SCORE_DESC",
                "page": 1
                }
    showAnimes(variables)

def showAnimesTrending():
    variables = {
                "sort": "TRENDING_DESC",
                "page": 1
                }
    showAnimes(variables)

def showAnimesPop():
    variables = {
                "sort": "POPULARITY_DESC",
                "page": 1
                }
    showAnimes(variables)

def _call(variables=''):

    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.addJSONEntry('query', query)
    oRequestHandler.addJSONEntry('variables', variables)
    oRequestHandler.setRequestType(1)
    data = oRequestHandler.request(jsonDecode=True)

    return data

def showAnimes(term=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if term == '':
        term = {
                "sort": "TRENDING_DESC",
                "page": 1 
                }

    iPage = 1
    if oInputParameterHandler.exist('page'):
        iPage = oInputParameterHandler.getValue('page')
        term.update({"page": iPage}) 

    result = _call(term)

    try:
        total = len(result)

        if total > 0:
            for item in result['data']['Page']['media']:

                sTitle = item['title']['romaji']
                sDisplayTitle = f"{sTitle} [COLOR orange]({item['title']['english']})[/COLOR]"
                sThumb = item['coverImage']['extraLarge']
                sDesc = item['description']
                sDesc = re.sub(r'<.*?>', '', sDesc)
                sYear = item['startDate']['year']

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)


                if isMatrix():
                    oOutputParameterHandler.addParameter('searchtext', sTitle)
                else:
                    oOutputParameterHandler.addParameter('searchtext', cUtil().CleanName(sTitle))

                cGui.CONTENT = "tvshows"
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName('globalSearch')
                oGuiElement.setFunction('searchMovie')
                oGuiElement.setTitle(sDisplayTitle)
                oGuiElement.setFileName(sTitle)
                oGuiElement.setIcon('animes.png')
                oGuiElement.setMeta(4)
                oGuiElement.setThumbnail(sThumb)
                oGuiElement.setPoster(sThumb)
                oGuiElement.setCat(3)
                oGuiElement.setDescription(sDesc)
                oGuiElement.setYear(sYear)

                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            if int(iPage) > 0:
                iNextPage = int(iPage) + 1
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('page', iNextPage)
                oOutputParameterHandler.addParameter('term', term)
                oGui.addNext(SITE_IDENTIFIER, 'showAnimes', 'Page ' + str(iNextPage), oOutputParameterHandler)

    except TypeError:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]No results were found.[/COLOR]')

    oGui.setEndOfDirectory()
