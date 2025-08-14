# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import xbmcplugin
import xbmc
import re
import xbmcgui
import json
import xbmcaddon
from resources.lib.comaddon import addon, dialog, VSlog, KodiVersion, addonManager
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.upnext import UpNext
from resources.lib.util import cUtil, Unquote
from resources.lib.trakt import cTrakt

class cPlayer(xbmc.Player):

    ADDON = addon()

    def __init__(self, *args):

        sPlayerType = self.__getPlayerType()
        xbmc.Player.__init__(self, sPlayerType)

        self.Subtitles_file = []
        self.SubtitleActive = False

        oInputParameterHandler = cInputParameterHandler()
        self.sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        self.sTitle = oInputParameterHandler.getValue('sFileName')
        if self.sTitle:
            self.sTitle = Unquote(self.sTitle)
        self.sCat = oInputParameterHandler.getValue('sCat')
        self.sSaison = oInputParameterHandler.getValue('sSeason')
        self.sEpisode = oInputParameterHandler.getValue('sEpisode')
        self.tvShowTitle = oInputParameterHandler.getValue('tvShowTitle')

        self.sSite = oInputParameterHandler.getValue('siteUrl')
        self.sSource = oInputParameterHandler.getValue('sourceName')
        self.sFav = oInputParameterHandler.getValue('sourceFav')
        self.saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        self.nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        self.movieUrl = oInputParameterHandler.getValue('movieUrl')
        self.movieFunc = oInputParameterHandler.getValue('movieFunc')
        self.sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        self.sImdbId = oInputParameterHandler.getValue('sImdbId')
        self.sYear = oInputParameterHandler.getValue('sYear') if oInputParameterHandler.exist('sYear') else xbmc.getInfoLabel('ListItem.Year')

        self.playBackEventReceived = False
        self.playBackStoppedEventReceived = False
        self.forcestop = False

        VSlog('player initialized')

    def clearPlayList(self):
        oPlaylist = self.__getPlayList()
        oPlaylist.clear()

    def __getPlayList(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

    def addItemToPlaylist(self, oGuiElement):
        oGui = cGui()
        oListItem = oGui.createListItem(oGuiElement)
        self.__addItemToPlaylist(oGuiElement, oListItem)

    def __addItemToPlaylist(self, oGuiElement, oListItem):
        oPlaylist = self.__getPlayList()
        oPlaylist.add(oGuiElement.getMediaUrl(), oListItem)

    def AddSubtitles(self, files):
        if type(files) is list or type(files) is tuple:
            self.Subtitles_file = files
        else:
            self.Subtitles_file.append(files)

    def run(self, oGuiElement, sUrl):
        if self.ADDON.getSetting('use_trakt_addon') == 'true':
            if self.sImdbId:
                ids = json.dumps({u'imdb': self.sImdbId})
                xbmcgui.Window(10000).setProperty('script.trakt.ids', ids)
            elif not self.sTmdbId:
                if self.sTitle or self.tvShowTitle:
                    if self.sCat:
                        ctrakt = cTrakt()
                        sType = ctrakt.convertCatToType(self.sCat)
                        if sType != -1:
                            self.sTmdbId = int(ctrakt.getTmdbID(self.sTitle, sType, oGuiElement.getItemValue('year')))
            if self.sTmdbId:
                ids = json.dumps({u'tmdb': self.sTmdbId})
                xbmcgui.Window(10000).setProperty('script.trakt.ids', ids)

        # Starting a video without stopping the previous one
        if self.isPlaying():
            sEpisode = str(oGuiElement.getEpisode())
            if sEpisode:
                # the previous video should be marked as VIEWED
                numEpisode = int(sEpisode)
                prevEpisode = numEpisode - 1
                sPrevEpisode = '%02d' % prevEpisode
                self._setWatched(sPrevEpisode)
            else:
                self._setWatched()
        self.totalTime = 0
        self.currentTime = 0

        sPluginHandle = cPluginHandler().getPluginHandle()

        oGui = cGui()
        listitem = oGui._createListItem(oGuiElement)
        listitem.setPath(oGuiElement.getMediaUrl())

        # Subtitles
        if self.Subtitles_file:
            try:
                listitem.setSubtitles(self.Subtitles_file)
                VSlog('Load SubTitle :' + str(self.Subtitles_file))
                self.SubtitleActive = True
            except:
                VSlog("Can't load subtitle:" + str(self.Subtitles_file))

        player_conf = self.ADDON.getSetting('playerPlay')

        kodiver = KodiVersion()
        listitem = xbmcgui.ListItem(path=sUrl.encode('utf-8')) 
        if '.m3u8' in sUrl or '&ct=6&' in sUrl:
            if kodiver < 21:
                listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
            mime_type = 'application/vnd.apple.mpegurl'
        elif '.mpd' in sUrl:
            if kodiver < 21:
                listitem.setProperty('inputstream.adaptive.manifest_type', 'mpd')
            mime_type = 'application/dash+xml'
        elif '.mkv' in sUrl:
            if kodiver < 21:
                listitem.setProperty('inputstream.adaptive.manifest_type', 'mkv')
            mime_type = 'video/x-matroska'
        elif '.mp4' in sUrl:
            if kodiver < 21: 
                listitem.setProperty('inputstream.adaptive.manifest_type', 'mp4') 
            mime_type = 'video/mp4'
        elif '.ism' in sUrl:
            if kodiver < 21:
                listitem.setProperty('inputstream.adaptive.manifest_type', 'ism')
            mime_type = 'application/vnd.ms-sstr+xml'
        else:
            mime_type = None

        media_type = 'movie' if self.sCat == '1' else 'tv'
        if media_type == 'movie':
            self.sTitle = self.sTitle
        else:
            self.sTitle = self.tvShowTitle
        try:
            self.fetch_imdb_id_from_title(media_type)
            info_tag = listitem.getVideoInfoTag()
            if self.sTitle or self.tvShowTitle:
                info_tag.setTitle(self.sTitle or self.tvShowTitle)
            info_tag.setYear(int(self.sYear) if self.sYear else 0)
            info_tag.setMediaType(media_type)
            if self.sImdbId:
                info_tag.setIMDBNumber(self.sImdbId)
            if media_type == 'tv':
                info_tag.setSeason(int(self.sSaison) if self.sSaison else 1)
                info_tag.setEpisode(int(self.sEpisode) if self.sEpisode else 1)
        except Exception as e:
            VSlog(f"Failed to set InfoTagVideo: {e}")

        if mime_type: 
            if any(ext in sUrl for ext in ['.m3u8', '&ct=6&', '.mpd']):
                listitem.setProperty('inputstream', 'inputstream.adaptive')
            
            addonManager().enableAddon('inputstream.adaptive')
            listitem.setMimeType(mime_type) 
            listitem.setContentLookup(False) 

            if '|' in sUrl:
                if '&license=' in sUrl:
                    sUrl, license_key = sUrl.split('&license=')
                    strhdr = sUrl.split('|')[1]
                    listitem.setProperty('inputstream.adaptive.drm_legacy', license_key)
                else:
                    strhdr = sUrl.split('|')[1]
                    listitem.setProperty('inputstream.adaptive.license_key', '|%s' % strhdr)

                listitem.setProperty('inputstream.adaptive.stream_headers', strhdr.encode('utf-8'))

                if kodiver > 21.8:
                    listitem.setProperty('inputstream.adaptive.common_headers', strhdr)
                elif kodiver > 19.8:
                    listitem.setProperty('inputstream.adaptive.manifest_headers', strhdr)
                    # listitem.setProperty('inputstream.adaptive.stream_params', strhdr)

            listitem.setPath(sUrl.encode('utf-8'))

            if self.Subtitles_file:
                try:
                    listitem.setSubtitles(self.Subtitles_file)
                    self.SubtitleActive = True
                except:
                    VSlog("Can't load subtitle:" + str(self.Subtitles_file))

            xbmcplugin.setResolvedUrl(sPluginHandle, True, listitem)

        elif player_conf == '0':
            self.play(sUrl, listitem)
            VSlog('Player use Play() method')

        elif player_conf == 'neverused':
            xbmc.executebuiltin('PlayMedia(' + sUrl + ')')
            VSlog('Player use PlayMedia() method')

        else:
            xbmcplugin.setResolvedUrl(sPluginHandle, True, listitem)
            VSlog('Player use setResolvedUrl() method')

        for _ in range(20):
            if self.playBackEventReceived:
                break
            xbmc.sleep(1000)

        if self.getAvailableSubtitleStreams():
            if self.ADDON.getSetting('srt-view') == 'true':
                self.showSubtitles(True)
            else:
                self.showSubtitles(False)
                dialog().VSinfo('الترجمة متوفرة', 'الترجمة', 4)

        waitingNext = 0

        while self.isPlaying() and not self.forcestop:
            try:
                self.currentTime = self.getTime()

                waitingNext += 1
                if waitingNext == 10:
                    self.totalTime = self.getTotalTime()
                    self.infotag = self.getVideoInfoTag()
                    UpNext().nextEpisode(oGuiElement)

            except Exception as err:
                VSlog("Exception run: {0}".format(err))

            xbmc.sleep(1000)

        if not self.playBackStoppedEventReceived:
            self.onPlayBackStopped()

        if player_conf == '0':
            r = xbmcplugin.addDirectoryItem(handle=sPluginHandle, url=sUrl, listitem=listitem, isFolder=False)
            return r

        VSlog('Closing player')
        return True

    def startPlayer(self, window=False):
        oPlayList = self.__getPlayList()
        self.play(oPlayList, windowed=window)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    # Attention, no stop, if you start a second video without closing the first
    def onPlayBackStopped(self):
        VSlog('player stopped')

        # received twice, we don't take it into account
        if self.playBackStoppedEventReceived:
            return
        self.playBackStoppedEventReceived = True

        self._setWatched(self.sEpisode)

    # MARK AS VIEWED
    # uses the information from the video that has just been played
    # which is not the one that was launched if several videos have been chained
    # sEpisode = the previous episode in case of a chain of episodes
    def _setWatched(self, sEpisode=''):
        try:
            with cDb() as db:
                if self.isPlaying():
                    self.totalTime = self.getTotalTime()
                    self.currentTime = self.getTime()
                    self.infotag = self.getVideoInfoTag()

                if self.totalTime > 0:
                    pourcent = float('%.2f' % (self.currentTime / self.totalTime))

                    saisonViewing = False

                    # calculates the reading time
                    # In the case where we have seen the entire content, percent = 0.0
                    # But we have still finished so the current time is equal to the total time.

                    VALUE_WATCHTIME = 0.90
                    TRAKT_ID = "script.trakt"

                    if self.ADDON.getSetting('use_trakt_addon') == 'true':
                        traktAddon = xbmcaddon.Addon(TRAKT_ID)
                        VALUE_WATCHTIME = int(traktAddon.getSetting("rate_min_view_time")) / 100

                    if (pourcent > VALUE_WATCHTIME) or (pourcent == 0.0 and self.currentTime == self.totalTime):

                        # Mark VU in the matrix BDD
                        sTitleWatched = self.infotag.getOriginalTitle()
                        if sTitleWatched:
                            if sEpisode :   # change of episode following an automatic sequence, end of the previous episode
                                sTitle = '%s S%sE%s' % (self.tvShowTitle, self.sSaison, sEpisode)
                            else:
                                sTitle = self.sTitle
                            meta = {}
                            meta['cat'] = self.sCat
                            meta['title'] = sTitle
                            meta['titleWatched'] = sTitleWatched
                            if self.movieUrl and self.movieFunc:
                                meta['siteurl'] = self.movieUrl
                                meta['fav'] = self.movieFunc
                            else:
                                meta['siteurl'] = self.sSite
                                meta['fav'] = self.sFav

                            meta['tmdbId'] = self.sTmdbId
                            meta['site'] = self.sSource

                            if self.sSaison:
                                meta['season'] = self.sSaison
                            meta['seasonUrl'] = self.saisonUrl
                            meta['seasonFunc'] = self.nextSaisonFunc
                            db.insert_watched(meta)

                            # Reset the recovery point
                            db.del_resume(meta)

                            # Output of CURRENT READINGS for movies, for series the deletion is manual
                            if self.sCat == '1':
                                db.del_viewing(meta)
                            elif self.sCat == '8':  # At the end of reading an episode, we put the season in "Currently reading"
                                saisonViewing = True

                        # Mark VU in personal accounts
                        self.__setWatchlist(sEpisode)

                    # Save reading point for replay
                    elif self.currentTime > 180.0:
                        sTitleWatched = self.infotag.getOriginalTitle()
                        if sTitleWatched:
                            meta = {}
                            meta['title'] = self.sTitle
                            meta['titleWatched'] = sTitleWatched
                            meta['site'] = self.sSite
                            meta['point'] = self.currentTime
                            meta['total'] = self.totalTime
                            db.insert_resume(meta)

                            # recovery point in external accounts
                            self.__setProgress(sEpisode, self.currentTime, self.totalTime)

                            # Now Playing
                            meta['cat'] = self.sCat
                            meta['site'] = self.sSource
                            meta['sTmdbId'] = self.sTmdbId

                            # Reading an episode, we save the season
                            if self.sCat == '8':
                                saisonViewing = True
                            else:  # Reading a movie

                                # 'miscellaneous' under 45 minutes can be 'adult' type
                                # no backup until better
                                if self.sCat == '5' and self.totalTime < 2700:
                                    pass
                                else:
                                    if self.movieUrl and self.movieFunc:
                                        meta['siteurl'] = self.movieUrl
                                        meta['fav'] = self.movieFunc
                                    else:
                                        meta['siteurl'] = self.sSite
                                        meta['fav'] = self.sFav

                                    db.insert_viewing(meta)

                    # Reading an episode, we put the season "Currently reading"
                    if saisonViewing:
                        meta['cat'] = '4'  # Season
                        meta['sTmdbId'] = self.sTmdbId
                        tvShowTitleWatched = cUtil().titleWatched(self.tvShowTitle).replace(' ', '')
                        if self.sSaison:
                            meta['season'] = self.sSaison
                            meta['title'] = self.tvShowTitle + " S" + self.sSaison
                            meta['titleWatched'] = tvShowTitleWatched + "_S" + self.sSaison
                        else:
                            meta['title'] = self.tvShowTitle
                            meta['titleWatched'] = tvShowTitleWatched
                        meta['site'] = self.sSource
                        meta['siteurl'] = self.saisonUrl
                        meta['fav'] = self.nextSaisonFunc
                        db.insert_viewing(meta)

        except Exception as err:
            VSlog("ERROR Player_setWatched : {0}".format(err))

    def onAVStarted(self):
        VSlog('player started')

        # If we receive the event again, it's because there's a bug, we stop everything
        if self.playBackEventReceived:
            self.forcestop = True
            return

        self.playBackEventReceived = True

        with cDb() as db:
            # Resume reading
            if self.isPlayingVideo() and self.getTime() < 180:  # if greater than 3 minutes, recovery management is provided by KODI
                self.infotag = self.getVideoInfoTag()
                sTitleWatched = self.infotag.getOriginalTitle()
                if sTitleWatched:
                    meta = {'titleWatched': sTitleWatched}
                    resumePoint, total = db.get_resume(meta)
                    if resumePoint:
                        h = resumePoint//3600
                        ms = resumePoint-h*3600
                        m = ms//60
                        s = ms-m*60
                        ret = dialog().VSselect(['استئناف من %02d:%02d:%02d' %(h, m, s), 'العرض من البداية'], 'استئناف العرض')
                        if ret == 0:
                            self.seekTime(resumePoint)
                        elif ret == 1:
                            self.seekTime(0.0)
                            # Reset the recovery point
                            db.del_resume(meta)

    def __setWatchlist(self, sEpisode=''):
        # Checking whether the Trakt addon is used or not, if yes, we exit the function.
        if self.ADDON.getSetting('use_trakt_addon') == 'true':
            return
        
        # Reading tracking in Trakt if account
        if self.ADDON.getSetting('bstoken') == '':
            return
        plugins = __import__('resources.lib.trakt', fromlist=['trakt']).cTrakt()
        function = getattr(plugins, 'getAction')
        function(Action="SetWatched", sEpisode=sEpisode)

    def __setProgress(self, sEpisode='', currentTime=0, totalTime=0):
        if self.ADDON.getSetting('use_trakt_addon') == 'true':
            return

        if self.ADDON.getSetting('bstoken') == '':
            return
        
        if totalTime == 0:
            return
        
        progress = currentTime/ totalTime
        
        plugins = __import__('resources.lib.trakt', fromlist=['trakt']).cTrakt()
        function = getattr(plugins, 'getAction')
        function(Action="SetProgress", sEpisode=sEpisode, progress=progress)

    def __getPlayerType(self):
        sPlayerType = self.ADDON.getSetting('playerType')

        try:
            if sPlayerType == '0':
                VSlog('playertype from config: auto')
                return xbmc.PLAYER_CORE_AUTO

            if sPlayerType == '1':
                VSlog('playertype from config: mplayer')
                return xbmc.PLAYER_CORE_MPLAYER

            if sPlayerType == '2':
                VSlog('playertype from config: dvdplayer')
                return xbmc.PLAYER_CORE_DVDPLAYER
        except:
            return False

    def fetch_imdb_id_from_title(self, media_type):
        oOutputParameterHandler = cOutputParameterHandler()
        if not self.sImdbId or not self.sTmdbId:
            try:
                if self.ADDON.getSetting('use_omdb') == 'true':
                    from resources.lib.omdb import cOMDb
                    tmdb = cOMDb()
                else:
                    from resources.lib.tmdb import cTMDb
                    tmdb = cTMDb()

                meta = tmdb.search_movie_name(self.sTitle, self.sYear) if media_type == 'movie' else tmdb.search_tvshow_name(self.sTitle, self.sYear)

                imdb_id = meta.get('external_ids', {}).get('imdb_id') or meta.get('imdb_id')
                try:
                    tmdb_id = meta.get('id')
                except:
                    VSlog('Not supported')

                if imdb_id and not self.sImdbId:
                    self.sImdbId = imdb_id
                    oOutputParameterHandler.addParameter('sImdbId', imdb_id)
                    VSlog(f"IMDb ID fetched via TMDb/OMDb wrapper: {self.sImdbId}")
                    
                if tmdb_id and not self.sTmdbId:
                    self.sTmdbId = tmdb_id
                    oOutputParameterHandler.addParameter('sTmdbId', tmdb_id)
                    VSlog(f"TMDb ID fetched via TMDb/OMDb wrapper: {self.sTmdbId}")

            except Exception as e:
                VSlog(f"Metadata fallback failed: {e}")
