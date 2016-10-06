#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.siteHandler import cSiteHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb
import os
import urllib
import xbmc

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'
color_cherches = cConfig().getSetting('color_cherches')
color_films = cConfig().getSetting('color_epl')
color_series = cConfig().getSetting('color_liga')
color_anims = cConfig().getSetting('color_cl')
color_tvs = cConfig().getSetting('color_tvs')
color_sports = cConfig().getSetting('color_sports')
color_docs = cConfig().getSetting('color_docs')
color_videos = cConfig().getSetting('color_videos')
color_replaytvs = cConfig().getSetting('color_replaytvs')

class cHome:
        

    def load(self):
        oGui = cGui()

        if (cConfig().getSetting('home_cl') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportCl', '[COLOR '+color_films+']'+cConfig().getlanguage(30120)+'[/COLOR]', 'cl.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_epl') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportEpl', '[COLOR '+color_films+']'+cConfig().getlanguage(30121)+'[/COLOR]', 'epl.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_liga') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportLiga', '[COLOR '+color_series+']'+cConfig().getlanguage(30122)+'[/COLOR]', 'liga.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_calcio') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportCalcio', '[COLOR '+color_series+']'+cConfig().getlanguage(30101)+'[/COLOR]', 'calcio.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_bundes') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportBundes', '[COLOR '+color_series+']'+cConfig().getlanguage(30102)+'[/COLOR]', 'bundes.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_ligue') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportLigue', '[COLOR '+color_series+']'+cConfig().getlanguage(30103)+'[/COLOR]', 'ligue.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_foot') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showFoot', '[COLOR '+color_series+']'+cConfig().getlanguage(30104)+'[/COLOR]', 'foot.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_basket') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportBasket', '[COLOR '+color_series+']'+cConfig().getlanguage(30107)+'[/COLOR]', 'basket.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_tennis') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportTennis', '[COLOR '+color_series+']'+cConfig().getlanguage(30105)+'[/COLOR]', 'tennis.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_motors') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'sportMotors', '[COLOR '+color_series+']'+cConfig().getlanguage(30108)+'[/COLOR]', 'motors.png', oOutputParameterHandler)

        if (cConfig().getSetting('home_more') == 'true'):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'showMore', '[COLOR '+color_series+']'+cConfig().getlanguage(30112)+'[/COLOR]', 'more.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cFav', 'getFavourites', '[COLOR teal]'+cConfig().getlanguage(30210)+'[/COLOR]', 'mark.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSources', cConfig().getlanguage(30116), 'host.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        if (cConfig().getSetting("active-view") == 'true'):
            xbmc.executebuiltin('Container.SetViewMode(%s)' % cConfig().getSetting('accueil-view'))


    
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

    def showFoot(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'footNews', '[COLOR '+color_videos+']'+cConfig().getlanguage(30114)+'[/COLOR]', 'bein.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'footGenres', '[COLOR '+color_videos+']'+cConfig().getlanguage(30115)+'[/COLOR]', 'bein.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def showMore(self):
        oGui = cGui()

        # Affiche les Nouveautés Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'moreNews', '[COLOR '+color_videos+']'+cConfig().getlanguage(30114)+'[/COLOR]', 'bein.png', oOutputParameterHandler)

        # Affiche les Genres Vidéos
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'moreGenres', '[COLOR '+color_videos+']'+cConfig().getlanguage(30115)+'[/COLOR]', 'bein.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    

    def sportCl(self):
        self.__callpluging('SPORT_CL', color_sports, 'cl.png')

    def sportEpl(self):
        self.__callpluging('SPORT_EPL', color_sports, 'epl.png')

    def sportLiga(self):
        self.__callpluging('SPORT_LIGA', color_sports, 'liga.png')

    def sportCalcio(self):
        self.__callpluging('SPORT_CALCIO', color_sports, 'calcio.png')

    def sportBundes(self):
        self.__callpluging('SPORT_BUNDES', color_sports, 'bundes.png')

    def sportLigue(self):
        self.__callpluging('SPORT_LIGUE', color_sports, 'ligue.png')

    def sportFoot(self):
        self.__callpluging('SPORT_FOOT', color_sports, 'foot.png')

    def footNews(self):
        self.__callpluging('FOOT_NEWS', color_sports, 'foot.png')

    def footGenres(self):
        self.__callpluging('FOOT_GENRES', color_sports, 'foot.png')

    def moreNews(self):
        self.__callpluging('MORE_NEWS', color_sports, 'foot.png')

    def moreGenres(self):
        self.__callpluging('MORE_GENRES', color_sports, 'foot.png')

    def sportBasket(self):
        self.__callpluging('SPORT_BASKET', color_sports, 'basket.png')

    def sportTennis(self):
        self.__callpluging('SPORT_TENNIS', color_sports, 'tennis.png')

    def sportMotors(self):
        self.__callpluging('SPORT_MOTORS', color_sports, 'motors.png')

    def sportMore(self):
        self.__callpluging('SPORT_MORE', color_sports, 'more.png')

    def sportSports(self):
        self.__callpluging('SPORT_SPORTS', color_sports, 'sport.png')

    def showSearch(self):

        if (cConfig().getSetting("history-view") == 'true'):
            readdb = 'True'
        else:
            readdb = 'False'

        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search1')
        oOutputParameterHandler.addParameter('readdb', readdb)
        sLabel1 = cConfig().getlanguage(30077)+": "+cConfig().getSetting('search1_label')
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', sLabel1, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search2')
        oOutputParameterHandler.addParameter('readdb', readdb)
        sLabel2 = cConfig().getlanguage(30089)+": "+cConfig().getSetting('search2_label')
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', sLabel2, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search3')
        oOutputParameterHandler.addParameter('readdb', readdb)
        sLabel3 = cConfig().getlanguage(30090)+": "+cConfig().getSetting('search3_label')
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', sLabel3, 'search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search4')
        oOutputParameterHandler.addParameter('readdb', readdb)
        sLabel4 = cConfig().getlanguage(30091)+": "+cConfig().getSetting('search4_label')
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', sLabel4, 'search.png', oOutputParameterHandler)


        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
        oOutputParameterHandler.addParameter('disp', 'search10')
        oOutputParameterHandler.addParameter('readdb', readdb)
        oGui.addDir(SITE_IDENTIFIER, 'searchMovie', '[COLOR orange]Recherche: Alluc_ee[/COLOR]', 'search.png', oOutputParameterHandler)

        #history
        if (cConfig().getSetting("history-view") == 'true'):

            row = cDb().get_history()
            if row:
                oGui.addText(SITE_IDENTIFIER, "[COLOR azure]Votre Historique[/COLOR]")
            for match in row:

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                oOutputParameterHandler.addParameter('searchtext', match[1])
                oOutputParameterHandler.addParameter('disp', match[2])
                oOutputParameterHandler.addParameter('readdb', 'False')
                oGui.addDir(SITE_IDENTIFIER, 'searchMovie', "- "+match[1], 'search.png', oOutputParameterHandler)

            if row:

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
                oGui.addDir(SITE_IDENTIFIER, 'delSearch', '[COLOR red]Supprimer l\'historique[/COLOR]', 'search.png', oOutputParameterHandler)


        oGui.setEndOfDirectory()

    def searchMovie2(self):
        oInputParameterHandler = cInputParameterHandler()
        sDisp = oInputParameterHandler.getValue('disp')
        oHandler = cRechercheHandler()
        liste = oHandler.getAvailablePlugins(sDisp)
        self.__callsearch(liste, sDisp)

    def delSearch(self):
        cDb().del_history()
        return True


    def __callpluging(self, sVar, sColor, sIcon):
        oGui = cGui()
        oPluginHandler = cSiteHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sVar)
        for aPlugin in aPlugins:
            try:
                #exec "import "+aPlugin[1]
                #exec "sSiteUrl = "+aPlugin[1]+"."+sVar
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aPlugin[0])
                icon = 'sites/%s.png' % (aPlugin[2])
                oGui.addDir(aPlugin[2], aPlugin[3], '[COLOR '+sColor+']'+aPlugin[1]+'[/COLOR]', icon, oOutputParameterHandler)
            except:
                pass

        oGui.setEndOfDirectory()

    def searchMovie(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sSearchText = oInputParameterHandler.getValue('searchtext')
        sReadDB = oInputParameterHandler.getValue('readdb')
        sDisp = oInputParameterHandler.getValue('disp')

        oHandler = cRechercheHandler()
        oHandler.setText(sSearchText)
        oHandler.setDisp(sDisp)
        aPlugins = oHandler.getAvailablePlugins()

        if (sReadDB != 'False' and aPlugins == True):
            meta = {}
            meta['title'] = oHandler.getText()
            meta['disp'] = oHandler.getDisp()
            cDb().insert_history(meta)

        oGui.setEndOfDirectory()
