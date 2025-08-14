import re
from resources.lib.comaddon import dialog, addon, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.tmdb import cTMDb
from resources.lib.db import cDb
from resources.sites.themoviedb_org import SITE_IDENTIFIER as SITE_TMDB

SITE_IDENTIFIER = 'cRecommendations'
SITE_NAME = 'Recommendations'

class cRecommendations:
    DIALOG = dialog()
    ADDON = addon()

    def showMoviesRecommendations(self):
        oGui = cGui()
        grab = cTMDb()
        try:
            with cDb() as DB:
                row = DB.get_catWatched('1', 5)

                if not row:
                    oGui.setEndOfDirectory()
                    return
                
                for data in row:
                    sTitle = data['title']
                    if bool(re.search(r"[\u0600-\u06FF]", sTitle)) is False:
                        sId = data['tmdb_id']
                        if sId == '0' or sId == '' or sId is False:
                            result = grab.getUrl('search/movie', 1, 'query=' + sTitle)
                            for i in result['results']:

                                i = grab._format(i, '', "movie")
                                sId = i['tmdb_id']

                        if sId != '0':
                            oOutputParameterHandler = cOutputParameterHandler()
                            oOutputParameterHandler.addParameter('sTmdbId', sId)
                            oOutputParameterHandler.addParameter('siteUrl', 'movie/'+str(sId)+'/recommendations')
                            oGui.addMovie(SITE_TMDB, 'showMovies', f"{self.ADDON.VSlang(70029)} {sTitle}", 'films.png', '', '', oOutputParameterHandler)
        except:
            pass

        cGui.CONTENT = 'files'
        oGui.setEndOfDirectory()

    def showShowsRecommendations(self):
        oGui = cGui()
        grab = cTMDb()
        try:
            with cDb() as DB:
                row = DB.get_catWatched('2', 5)

                if not row:
                    oGui.setEndOfDirectory()
                    return
                
                for data in row:
                    sTitle = data['title']
                    if bool(re.search(r"[\u0600-\u06FF]", sTitle)) is False:
                        sTitle = re.sub(r"S\d{1,2}", "", sTitle)
                        sId = data['tmdb_id']
                        if sId == '0' or sId == '' or sId is False:
                            result = grab.getUrl('search/tv', 1, 'query=' + sTitle)
                            for i in result['results']:

                                i = grab._format(i, '', "tvshow")
                                sId = i['tmdb_id']
                        if sId != '0':
                            oOutputParameterHandler = cOutputParameterHandler()
                            oOutputParameterHandler.addParameter('sTmdbId', sId)
                            oOutputParameterHandler.addParameter('siteUrl', 'tv/'+str(sId)+'/recommendations')
                            oGui.addTV(SITE_TMDB, 'showSeries', f"{self.ADDON.VSlang(70029)} {sTitle}", '1/TVShows.png', '', '', oOutputParameterHandler)
        except:
            pass
            
        cGui.CONTENT = 'files'
        oGui.setEndOfDirectory()