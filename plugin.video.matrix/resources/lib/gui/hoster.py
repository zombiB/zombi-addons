# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog, xbmc




class cHosterGui:

    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False):
        oOutputParameterHandler = cOutputParameterHandler()
        oInputParameterHandler = cInputParameterHandler()

        # Gestion NextUp
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')
				
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())

        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4':  # Si on vient de passer par un menu "Saison" ...
                sCat = '8'   # ...  On est maintenant au niveau "Episode"
        else:
            sCat = '5'     # Divers
        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)

        oGuiElement.setIcon('host.png')
				
        title = oGuiElement.getCleanTitle()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)    # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)    # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # context playlist menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        if oHoster.isDownloadable():
            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'UptomyAccount', self.ADDON.VSlang(30325))

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = '1fichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'UptomyAccount', '1fichier')

        # context Library menu
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid=True):
        # securite
        if not sHosterUrl:
            return False

        # Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.lower()

        # Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl
        if debrid:

                
            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                return self.getHoster('alldebrid')

            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')

                else:
                    return self.getHoster("lien_direct")

            # L'user a active l'url resolver ?
            if self.ADDON.getSetting('UserResolveurl') == 'true':
                import resolveurl
                hmf = resolveurl.HostedMediaFile(url=sHosterUrl)
                if hmf.valid_url():
                    tmp = self.getHoster('resolver')
                    RH = sHosterUrl.split('/')[2]
                    RH = RH.replace('www.', '')
                    tmp.setRealHost(RH[:3].upper())
                    return tmp
        supported_player = ['streamz', 'streamax', 'gounlimited', 'xdrive', 'mixdrop', 'mixloads', 'vidoza', 'rutube', 'vk', 'vkontakte', 'vkcom',
                    'megawatch', 'playvidto', 'vidzi', 'filetrip', 'uptostream', 'livestream', 'flashx', 'filez','speedvid', 'netu',  'mail.ru', 
                    'onevideo', 'playreplay', 'vimeo', 'prostream', 'vidfast', 'uqload', 'letwatch', 'letsupload', 'filepup', 'vimple.ru', 'wstream', 'watchvideo', 'vidwatch', 'up2stream', 'vidbm', 'tune', 'vidup', 'vidbull', 'vidlox', 'videobin', 'stagevu', 'movshare',
                    'gorillavid','daclips', 'estream', 'hdvid', 'vshare', 'giga', 'vidbom', 'upvideo', 'upvid', 'cloudvid', 'megadrive', 'downace', 'clickopen',
                    'iframe-secured', 'iframe-secure', 'jawcloud', 'kvid', 'soundcloud', 'mixcloud', 'ddlfr', 'pdj', 'vidzstore', 'hd-stream', 'rapidstream','jetload','dustreaming', 'vupload', 'viki', 'flix555', 'onlystream', 'upstream', 'pstream', 'vudeo', 'cimanow',  
                    'supervideo', 'voe', 'dood', 'vidia', 'streamtape', 'femax', 'vidbem', 'sibnet', 'vidplayer', 'userload', 'aparat', 'evoload', 'abcvideo', 
                    'plynow', 'myvi.tv', 'playtube', 'dwfull', 'uptobox', 'uplea', 'vidload','cloudhost', 'ninjastream', 'vidhid', 'moshahda', 'vidspeeds', 'yourupload', 'yadi.sk', 'extremenow', 'youdbox', 'arabveturk', 'holavid','mycima']

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))
        # Gestion classique
        if ('sama-share' in sHostName):
            return self.getHoster('samashare')
        if ('yodbox' in sHostName):
            return self.getHoster('youdbox')
        if ('anafast' in sHostName):
            return self.getHoster('anafasts')
        if ('filerio' in sHostName):
            return self.getHoster('filerio')
        if ('brightcove' in sHostName):
            return self.getHoster('brightcove')
        if ('upbam' in sHostName):
            return self.getHoster('uppom')
        if ('uppom' in sHostName):
            return self.getHoster('uppom')
        if ('uppboom' in sHostName):
            return self.getHoster('uppom')
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
        if ('mp4upload' in sHostName):
            return self.getHoster('mpupload')
        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')
        if ('l.vevents.net' in sHostName):
            return self.getHoster('vevents')
        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')
        if ('jwplatform' in sHostName):
            return self.getHoster('anonfile')
        if ('vidto.me' in sHostName):
            return self.getHoster('vidto')
        if ('hibridvod' in sHostName):
            return self.getHoster('hibridvod')
        if ('vedbom' in sHostName):
            return self.getHoster('vidbm')
        if ('vadbom' in sHostName):
            return self.getHoster('vidbm')
        if ('vidbam' in sHostName):
            return self.getHoster('vidbm')
        if ('vedpom' in sHostName):
            return self.getHoster('vidbem')
        if ('vadshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vidshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vedshaar' in sHostName):
            return self.getHoster('vidshare')
        if ('vedsharr' in sHostName):
            return self.getHoster('vidshare')
        if ('vedshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vidshare' in sHostName):
            return self.getHoster('vidshare')
        if ('detectiveconanar' in sHostName):
            return self.getHoster('detectiveconanar')
        if ('streamwire' in sHostName):
            return self.getHoster('streamwire')
        if ('vup' in sHostName):
            return self.getHoster('streamwire')
        if ('kopatube' in sHostName):
            return self.getHoster('govid')
        if ('kobatube' in sHostName):
            return self.getHoster('govid')
        if ('gvid.rest' in sHostName):
            return self.getHoster('govid')
        if ('goved' in sHostName):
            return self.getHoster('govidme')
        if ('govid.co' in sHostName):
            return self.getHoster('govid')
        if ('cloudy' in sHostName):
            return self.getHoster('cloudy')
        if ('seeeed' in sHostName):
            return self.getHoster('arabseed')
        if ('vidhd' in sHostName):
            return self.getHoster('vidhd')
        if ('oktube' in sHostName):
            return self.getHoster('vidhd')
        if ('fastplay' in sHostName):
            return self.getHoster('fastplay')
        if ('4shared' in sHostName):
            return self.getHoster('shared')
        if ('videoraj' in sHostName):
            return self.getHoster('videoraj')
        if ('videohut' in sHostName):
            return self.getHoster('videohut')
        if ('googlevideo' in sHostName):
            return self.getHoster('googlevideo')
        if ('picasaweb' in sHostName):
            return self.getHoster('googlevideo')
        if ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')
        if ('vidmoly' in sHostName):
            return self.getHoster('vidmoly')
        if ('mediafire' in sHostName):
            return self.getHoster('mediafire')
        if ('www.amazon' in sHostName):
            return self.getHoster('amazon')
        if ('thevid' in sHostName):
            return self.getHoster('thevid')
        if ('drive.google.com' in sHostName):
            return self.getHoster('resolver')
        if ('docs.google.com' in sHostName):
            return self.getHoster('resolver')
        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')
        if ('sendit' in sHostName):
            return self.getHoster('sendit')
        if ('veehd.' in sHostName):
            return self.getHoster('veehd')
        if ('vidlo' in sHostName):
            return self.getHoster('vidlo')
        if ('myviid' in sHostName):
            return self.getHoster('myvid')
        if ('myvid' in sHostName):
            return self.getHoster('myvid')
        if ('youwatch' in sHostName):
            return self.getHoster('youwatch')
        if ('videott' in sHostName):
            return self.getHoster('videott')
        if ('vidgot' in sHostName):
            return self.getHoster('vidgot')
        if ('filescdn' in sHostName):
            return self.getHoster('filescdn')
        if (('anonfile' in sHostName) or ('govid.xyz' in sHostName) or ('vidmoly' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')
        if ('vidabc' in sHostName):
            return self.getHoster('vidabc')
        if (('anavids' in sHostName) or ('anavidz' in sHostName)):
            return self.getHoster('anavids')
        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamsforu')
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
        if ('govid.me' in sHostName):
            return self.getHoster('govidme')
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')
        if ('movs4u.club' in sHostName):
            return self.getHoster('movs4u')
        if ('arabramadan' in sHostName):
            return self.getHoster('arabramadan')
        if ('player.4show' in sHostName):
            return self.getHoster('arabramadan')
        if ('faselhd' in sHostName):
            return self.getHoster('faselhd')
        if ('stardima' in sHostName):
            return self.getHoster('stardima')
        if ('streamable' in sHostName):
            return self.getHoster('streamable')

        if ('vidbom' in sHostName):
            return self.getHoster('resolver')

        if (('cloudvideo' in sHostName) or ('streamcloud' in sHostName) or ('userscloud' in sHostName)):
            return self.getHoster('cloudvid')
        if ('clicknupload' in sHostName):
            return self.getHoster('resolver')
        if ('myvi.ru' in sHostName):
            return self.getHoster('resolver')
        if ('yandex' in sHostName):
            return self.getHoster('yadisk')
        if ('megaup.' in sHostName):
            return self.getHoster('megaup')
        if ('streamcherry' in sHostName):
            return self.getHoster('resolver')
        #Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('1fichier')

        if ('kaydo.ws' in sHostName):
            return self.getHoster('lien_direct')
        if ('megaupload.' in sHostName):
            return self.getHoster('lien_direct')
        if ('king-shoot.xyz' in sHostName):
            return self.getHoster('lien_direct')
        if ('fansubs' in sHostName):
            return self.getHoster('lien_direct')
        if ('us.archive.' in sHostName):
            return self.getHoster('lien_direct')
        if ('ddsdd' in sHostName):
            return self.getHoster('lien_direct')
        if ('ffsff' in sHostName):
            return self.getHoster('lien_direct')
        if ('rrsrr' in sHostName):
            return self.getHoster('lien_direct')
        if ('fbcdn.net' in sHostName):
            return self.getHoster('lien_direct')
        if ('blogspot.com' in sHostName):
            return self.getHoster('lien_direct')
        if ('videodelivery' in sHostName):
            return self.getHoster('lien_direct')
        if ('bittube' in sHostName):
            return self.getHoster('lien_direct')
        if ('amazonaws.com' in sHostName):
            return self.getHoster('lien_direct')
        if ('streamtec' in sHostName):
            return self.getHoster('lien_direct')

        if ('.googleusercontent.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('archive.org/download' in sHostName):
            return self.getHoster('lien_direct')

        if ('ak-download' in sHostName):
            return self.getHoster('lien_direct')

        if ('akwam' in sHostName):
            return self.getHoster('lien_direct')

        if ('akoams.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('.stream.fushaar.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('gcdn' in sHostName):
            return self.getHoster('lien_direct')

        if ('egybest' in sHostName):
            return self.getHoster('lien_direct')

        if ('alarabiya' in sHostName):
            return self.getHoster('lien_direct')

        if ('kingfoot' in sHostName):
            return self.getHoster('lien_direct')

        # vidtodo et clone
        val = next((x for x in ['vidtodo', 'vixtodo', 'viddoto', 'vidstodo'] if x in sHostName), None)
        if val:
            return self.getHoster("vidtodo")

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('lien_direct')
            except:
                pass
            else:
                return self.getHoster('dailymotion')


        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp?type=speed' in sHosterUrl):
            return self.getHoster('speedvideo')
        if ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')

        # frenchvid et clone
        val = next((x for x in ['french-vid', 'yggseries', 'fembed', 'fem.tohds', 'feurl', 'fsimg', 'core1player',
                                'vfsplayer', 'gotochus', 'sendvid', "femax"] if x in sHostName), None)
        if val:
            return self.getHoster("frenchvid")

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')

        if ('.m3u8' in sHosterUrl):
            return self.getHoster('lien_direct')

        if ('.mp3' in sHosterUrl):
            return self.getHoster('lien_direct')

        if ('.mp4' in sHostName):
            return self.getHoster('lien_direct')

        if ('.mpd' in sHostName):
            return self.getHoster('lien_direct')

        if ('nitro.download' in sHosterUrl or 'Facebook'  or 'facebook' or 'infinityload' or 'turbobit' or 'fastdrive' in sHosterUrl or 'openload' in sHosterUrl or 'multiup' in sHosterUrl):
            return False

            
        if any(x in sHosterUrl for x in ['mp4', 'avi', 'flv', 'm3u8', 'webm', 'mkv', 'mpd']):
            return self.getHoster('lien_direct')
        return False
		
    def getHoster(self, sHosterFileName):
        mod = __import__('resources.hosters.' + sHosterFileName, fromlist=['cHoster'])
        klass = getattr(mod, 'cHoster')
        return klass()

    def play(self):
        oGui = cGui()
        oDialog = dialog()

        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('sTitle')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sCat = oInputParameterHandler.getValue('sCat')
		
        sMeta = oInputParameterHandler.getValue('sMeta')
        if not sTitle:
            sTitle = sFileName

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        try:
            mediaDisplay = sMediaUrl.split('/')
            VSlog('Hoster - play : %s/ ... /%s' % ('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster - play : ' + sMediaUrl)
				

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        oDialog.VSinfo(sHosterName, 'Resolve')

        try:

            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink[0] or aLink[1]:  # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0]:  # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        oDialog.VSinfo(sHosterName, 'Resolve')
                        oHoster.setUrl(sMediaUrl)
                        aLink = oHoster.getMediaLink()

                if aLink[0]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setFileName(sFileName)
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setCat(sCat)
                    oGuiElement.setMeta(int(sMeta))
                    oGuiElement.getInfoLabel()
    
                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer()
    
                    # sous titres ?
                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])
    
                    return oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])

            oDialog.VSerror(self.ADDON.VSlang(30020))
            return

        except Exception as e:
            oDialog.VSerror(self.ADDON.VSlang(30020))
            import traceback
            traceback.print_exc()
            return

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Hoster - playlist ' + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if aLink[0]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            from resources.lib.player import cPlayer
            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            dialog().VSinfo(str(oHoster.getFileName()), 'Playlist')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        from resources.lib.handler.requestHandler import cRequestHandler
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
