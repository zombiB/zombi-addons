#-*- coding: utf-8 -*-
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
#from resources.lib.handler.pluginHandler import cPluginHandler
#from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.siteHandler import cSiteHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb

from resources.lib.comaddon import addon, window

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'

#temp d'execution
# import time, random

# l = range(100000)

# tps1 = time.clock()
# random.shuffle(l)
# l.sort()
# tps2 = time.clock()
# print(tps2 - tps1)


addons = addon()

class cHome:

    addons = addons

    def load(self):
        oGui = cGui()

        if (addons.getSetting('home_update') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showUpdate', '%s (%s)' % (addons.VSlang(30418), addons.getSetting('service_futur')), 'update.png', oOutputParameterHandler)



        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', addons.VSlang(30076), 'search.png', oOutputParameterHandler)



        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir('freebox', 'load', addons.VSlang(30115), 'tv.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', addons.VSlang(30120), 'film.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', addons.VSlang(30121), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', addons.VSlang(30112), 'doc.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showIslam', addons.VSlang(70009), 'islm.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showRamadan', addons.VSlang(70006), 'rmdn.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showKid', addons.VSlang(70012), 'tfl.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', addons.VSlang(30122), 'anime.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSport', addons.VSlang(30113), 'sport.png', oOutputParameterHandler)



        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', addons.VSlang(30117), 'brmg.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showNets', addons.VSlang(30114), 'none.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cTrakt', 'getLoad', addons.VSlang(30214), 'trakt.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', addons.VSlang(30202), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', addons.VSlang(30300), 'library.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', addons.VSlang(30207), 'fav.png', oOutputParameterHandler)

        if (addons.getSetting("history-view") == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', addons.VSlang(30308), 'annees.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'showSources', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir('globalParametre', 'showSources', '[COLOR teal]'+addons.VSlang(30023)+'[/COLOR]', 'param.png', oOutputParameterHandler)


        view = False
        if (addons.getSetting("active-view") == 'true'):
            view = addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)


    def showUpdate(self):
        try:
            from resources.lib.about import cAbout
            cAbout().checkdownload()
        except:
            pass
        return

    def showSearchText(self):
        oGui = cGui()
        sSearchText = oGui.showKeyBoard(heading=addons.VSlang(30076))
        if sSearchText:
            self.showSearch(sSearchText)
            oGui.setEndOfDirectory()
        else :
            return False

    def showSearch(self, searchtext=cInputParameterHandler().getValue('searchtext')):

        if not searchtext:
            return self.showSearchText()

        #n'existe plus mais pas sure.
        #xbmcgui.Window(10101).clearProperty('search_text')
        window(10101).clearProperty('search_text')

        oGui = cGui()

        #print xbmc.getInfoLabel('ListItem.Property(Category)')

        oGui.addText('globalSearch', addons.VSlang(30077) % (searchtext), 'none.png')

        #utilisation de guielement pour ajouter la bonne catégorie

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(addons.VSlang(30078))
        oGuiElement.setFileName(addons.VSlang(30078))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(1)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(addons.VSlang(30079))
        oGuiElement.setFileName(addons.VSlang(30079))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(2)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('searchtext', searchtext)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName('globalSearch')
        oGuiElement.setFunction('showSearch')
        oGuiElement.setTitle(addons.VSlang(30080))
        oGuiElement.setFileName(addons.VSlang(30080))
        oGuiElement.setIcon('search.png')
        oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(3)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        # oOutputParameterHandler = cOutputParameterHandler()
        # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        # oOutputParameterHandler.addParameter('searchtext', searchtext)
        # oOutputParameterHandler.addParameter('disp', 'search10')
        # oOutputParameterHandler.addParameter('readdb', 'True')
        # oGui.addDir('globalSearch', 'showSearchText', '[COLOR orange]Recherche: Alluc_ee[/COLOR]', 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30112), addons.VSlang(30101)), 'film.png', oOutputParameterHandler)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30112), addons.VSlang(30121)), 'mslsl.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30112), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSport(self):
        oGui = cGui()

        # Affiche les Nouveautés Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_FOOT')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30113), addons.VSlang(30134)), 'foot.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30113), addons.VSlang(70011)), 'sport.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_WWE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30113), addons.VSlang(30135)), 'wwe.png', oOutputParameterHandler)

        # Affiche les Genres Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30113), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        # Affiche les Sources Documentaires
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showIslam(self):
        oGui = cGui()


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_QURAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging',addons.VSlang(70003), 'quran.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_SHOWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70009), addons.VSlang(30117)), 'brmg.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_NASHEED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70009), addons.VSlang(70004)), 'nsheed.png', oOutputParameterHandler)

        #Genres 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70009), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        #Sources 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ISLAM_ISLAM')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showRamadan(self):
        oGui = cGui()

        #series
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70006), addons.VSlang(30121)), 'mslsl.png', oOutputParameterHandler)

        #tv shows
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_SHOWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70006), addons.VSlang(30117)), 'brmg.png', oOutputParameterHandler)

        #islam
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_ISLAM')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70006), addons.VSlang(70009)), 'islm.png', oOutputParameterHandler)

        #Genres 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70006), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        #Sources 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_RAMADAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showKid(self):
        oGui = cGui()

        #CARTOON
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'KID_CARTOON')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70012), addons.VSlang(70005)), 'crtoon.png', oOutputParameterHandler)

        #MOVIE
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'KID_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70012), addons.VSlang(30120)), 'anim.png', oOutputParameterHandler)

        #Genres 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(70012), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        #Sources 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'RAMADAN_RAMADAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = cGui()

        #new
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30114), addons.VSlang(30101)), 'news.png', oOutputParameterHandler)

        #Genres
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30114), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        #Sources 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'NETS_NETS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = cGui()
        #arabic
        oOutputParameterHandler = cOutputParameterHandler()
        #self.__callpluging('MOVIE_NEWS', 'films_news.png')
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30107)), 'arab.png', oOutputParameterHandler)
        #agnab
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30108)), 'agnab.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_HI')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30103)), 'hend.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TURK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30109)), 'turk.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_ASIAN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_PACK')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(70013)), 'pack.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_POP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(30315)), 'pop.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_TOP')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30120), addons.VSlang(70001)), 'top.png', oOutputParameterHandler)



        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'films_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_DUBBED')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(70002)), 'mdblg.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_AR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30107)), 'arab.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_EN')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30108)), 'agnab.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_ASIA')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30104)), 'asia.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_HEND')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30103)), 'hend.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_TR')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30109)), 'turk.png', oOutputParameterHandler)

        # Affiche les Genres 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30121), addons.VSlang(30105)), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'mslsl.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30122), addons.VSlang(30121)), 'mslsl.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_MOVIES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30122), addons.VSlang(30120)), 'film.png', oOutputParameterHandler)


        #non utiliser ANIM_MOVIES

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30122), addons.VSlang(30105)), 'animes_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'animes_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30117), addons.VSlang(30101)), 'brmg.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_PLAY')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30117), addons.VSlang(70010)), 'msrh.png', oOutputParameterHandler)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (addons.VSlang(30117), addons.VSlang(30105)), 'replay_genres.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(SITE_IDENTIFIER, 'callpluging', addons.VSlang(30138), 'replay_host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showSources(self):
        oGui = cGui()

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins()
        for aPlugin in aPlugins:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            icon = 'sites/%s.png' % (aPlugin[1])
            oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showHistory(self):

        oGui = cGui()

        row = cDb().get_history()
        if row:
            oGui.addText(SITE_IDENTIFIER, addons.VSlang(30416))
        else:
            oGui.addText(SITE_IDENTIFIER)
        for match in row:
            oOutputParameterHandler = cOutputParameterHandler()

            #code to get type with disp
            type = addons.getSetting('search' + match[2][-1:] + '_type')
            if type:
                oOutputParameterHandler.addParameter('type', type)
                #xbmcgui.Window(10101).setProperty('search_type', type)
                window(10101).setProperty('search_type', type)

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oOutputParameterHandler.addParameter('searchtext', match[1])
            #oOutputParameterHandler.addParameter('disp', match[2])
            #oOutputParameterHandler.addParameter('readdb', 'False')

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')
            oGuiElement.setTitle('- ' + match[1])
            oGuiElement.setFileName(match[1])
            oGuiElement.setCat(match[2])
            oGuiElement.setIcon('search.png')
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, SITE_IDENTIFIER, 'cHome', 'delSearch', addons.VSlang(30412))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if row:

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', addons.VSlang(30413), 'search.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def delSearch(self):
        cDb().del_history()
        return True


    def callpluging(self):
        oGui = cGui()

        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')

        oPluginHandler = cSiteHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        for aPlugin in aPlugins:
            try:
                #exec "import "+aPlugin[1]
                #exec "sSiteUrl = "+aPlugin[1]+"."+sVar
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                icon = 'sites/%s.png' % (aPlugin[2])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, oOutputParameterHandler)
            except:
                pass

        oGui.setEndOfDirectory()
