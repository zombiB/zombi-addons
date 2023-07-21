# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
# zombi.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.search import cSearch
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import addon, window, addon, VSlog

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

class cHome:

    addons = addon()
    
    def load(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30076), icons + '/Search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), icons + '/TMDB.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), icons + '/Movies.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), icons + '/TVShows.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), icons + '/Documentary.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showIslam', self.addons.VSlang(70009), icons + '/Islamic.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showRamadan', self.addons.VSlang(70006), icons + '/Ramadan.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showKid', self.addons.VSlang(70012), icons + '/Kids.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), icons + '/Anime.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSport', self.addons.VSlang(30113), icons + '/Sport.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30117), icons + '/Programs.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getBookmarks', self.addons.VSlang(30207), icons + '/Bookmarks.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cViewing', 'showMenu', self.addons.VSlang(30125), icons + '/ContinueWatching.png', oOutputParameterHandler)
		
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), icons + '/User.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'ShowTools', self.addons.VSlang(30033), icons + '/Tools.png', oOutputParameterHandler)

        if (self.addons.getSetting('history-view') == 'true'):
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), icons + '/History.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30138), icons + '/Sources.png', oOutputParameterHandler)

        view = False
        if (self.addons.getSetting('active-view') == 'true'):
            view = self.addons.getSetting('accueil-view')
               
        oGui.setEndOfDirectory(view)

    def showSearchText(self):
        oGui = cGui()
        sSearchText = oGui.showKeyBoard(heading=self.addons.VSlang(30076))
        if sSearchText:
            self.showSearch(sSearchText)
            oGui.setEndOfDirectory()
        else:
            return False

    def showSearch(self, searchtext=None):
        
        ADDON = addon()
        CurrentCacheStatus = ADDON.getSetting('RequestCache')
        VSlog('CurrentCacheStatus: ' + ADDON.getSetting('RequestCache'))
        ## Turnoff Matrix Cache
        ADDON.setSetting('RequestCache','False')
        VSlog('After trying to switch it off CacheStatus: ' + ADDON.getSetting('RequestCache'))
        
        if not searchtext:
            searchtext=cInputParameterHandler().getValue('searchtext')

        if not searchtext:
            return self.showSearchText()

        window(10101).clearProperty('search_text')

        oGui = cGui()
        oGui.addText('globalSearch', self.addons.VSlang(30077) % searchtext, icons + '/None.png')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setIcon(icons + '/Search.png')
        oGuiElement.setMeta(0)

        # Recherche globale films
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)
        oGuiElement.setTitle(self.addons.VSlang(30078))
        oGuiElement.setFileName(self.addons.VSlang(30078))
        oGuiElement.setCat(1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        # Recherche globale séries
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)
        oGuiElement.setTitle(self.addons.VSlang(30079))
        oGuiElement.setFileName(self.addons.VSlang(30079))
        oGuiElement.setCat(2)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        # Recherche globale divers
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)
        oGuiElement.setTitle(self.addons.VSlang(30080))
        oGuiElement.setFileName(self.addons.VSlang(30080))
        oGuiElement.setCat(5)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        ADDON.setSetting('RequestCache',CurrentCacheStatus)
        VSlog('Reverting to original setting CurrentCacheStatus: ' + ADDON.getSetting('RequestCache'))
        
        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30120)), icons + '/Movies.png', oOutputParameterHandler)
		
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30121)), icons + '/TVShows.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)


        oGui.setEndOfDirectory()

    def showSport(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_FOOT')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30134)), icons + '/Sport.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(70011)), icons + '/Live.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_WWE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30135)), icons + '/WWE.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showIslam(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_QURAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging',self.addons.VSlang(70003), icons + '/Quran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_SHOWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(30117)), icons + '/Programs.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_NASHEED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(70004)), icons + '/Anasheed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70009), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showRamadan(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70006), self.addons.VSlang(30121)), icons + '/TVShows.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showKid(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'KID_CARTOON')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70012), self.addons.VSlang(70005)), icons + '/Cartoon.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'KID_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70012), self.addons.VSlang(30120)), icons + '/Anime.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'KID_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(70012), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_FAM')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(33107)), icons + '/Family.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), icons + '/Arabic.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_DUBBED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70002)), icons + '/Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30108)), icons + '/Movies.png', oOutputParameterHandler)
		
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TURK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30109)), icons + '/Turkish.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ASIAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)), icons + '/Asian.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_KR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301041)), icons + '/Korean.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_KR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301042)), icons + '/Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_CN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301043)), icons + '/Chinese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_JP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301044)), icons + '/Japanese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_THAI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301045)), icons + '/Thai.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_VIET')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301046)), icons + '/Vietnamese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301047)), icons + '/Taiwanese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30103)), icons + '/Hindi.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_CLASSIC')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30501)), icons + '/MoviesClassic.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_PACK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70013)), icons + '/Pack.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_POP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30315)), icons + '/MoviesPopular.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TOP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(70001)), icons + '/Top.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30106)), icons + '/Calendar.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_LANGS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(301061)), icons + '/Language.png', oOutputParameterHandler)
		
        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_DUBBED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(70002)), icons + '/Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30107)), icons + '/Arabic.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30108)), icons + '/TVShows.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30109)), icons + '/Turkish.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(31110)), icons + '/TVShowsTurkish-Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_KR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301041)), icons + '/Korean.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ASIA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30104)), icons + '/Asian.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_KR_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301042)), icons + '/TVShowsKorean-Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_CN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301043)), icons + '/Chinese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_JP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301044)), icons + '/Japanese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_THAI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301045)), icons + '/Thai.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_VIET')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301046)), icons + '/Vietnamese.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(301047)), icons + '/Taiwanese.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_PAK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30111)), icons + '/Pakistani.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HEND')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30103)), icons + '/Hindi.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HEND_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30136)), icons + '/TVShowsHindi-Dubbed.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_LATIN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30137)), icons + '/TVShows.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30121)), icons + '/TVShows.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30120)), icons + '/Movies.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30101)), icons + '/Programs.png', oOutputParameterHandler)


        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_PLAY')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(70010)), icons + '/Theater.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30105)), icons + '/Genres.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showUsers(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', icons + '/TMDB.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), icons + '/Trakt.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteuptobox', 'load', 'Uptobox', 'sites/siteuptobox.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteonefichier', 'load', self.addons.VSlang(30327), 'sites/siteonefichier.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def ShowTools(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), icons + '/Tools.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30300), icons + '/Library.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30202), icons + '/Download.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), icons + '/HosterDirect.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def opensetting(self):
        addon().openSettings()
			
    def showHistory(self):
        oGui = cGui()

        from resources.lib.db import cDb
        with cDb() as db:
            row = db.get_history()

        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416))
        else:
            oGui.addText(SITE_IDENTIFIER)
        oOutputParameterHandler = cOutputParameterHandler()
        for match in row:
            sTitle = match['title']
            sCat = match['disp']

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', sTitle)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')

            try:
                oGuiElement.setTitle('- ' + sTitle)
            except:
                oGuiElement.setTitle('- ' + str(sTitle, 'utf-8'))

            oGuiElement.setFileName(sTitle)
            oGuiElement.setCat(sCat)
            oGuiElement.setIcon(icons + '/Search.png')
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, 'cHome', 'delSearch', self.addons.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.addons.VSlang(30413), icons + '/Search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def delSearch(self):
        from resources.lib.db import cDb
        with cDb() as db:
            db.del_history()
        return True

    def callpluging(self):
        
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        for aPlugin in aPlugins:
            try:
                icon = 'sites/%s.png' % (aPlugin[2])
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass
        
        oGui.setEndOfDirectory()

    def showHostDirect(self):  # fonction de recherche
        oGui = cGui()
        sUrl = oGui.showKeyBoard(heading=self.addons.VSlang(30045))
        if (sUrl != False):

            oHoster = cHosterGui().checkHoster(sUrl)
            if (oHoster != False):
                oHoster.setDisplayName(self.addons.VSlang(30046))
                oHoster.setFileName(self.addons.VSlang(30046))
                cHosterGui().showHoster(oGui, oHoster, sUrl, '')

        oGui.setEndOfDirectory()
