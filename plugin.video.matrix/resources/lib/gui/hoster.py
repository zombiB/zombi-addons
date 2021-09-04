# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog, addon, VSlog, xbmc

import re

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
        sFav = oInputParameterHandler.getValue('sFav')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())

        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4': # Si on vient de passer par un menu "Saison" ...
               sCat = '8'   #     ...  On est maintenant au niveau "Episode"
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
		
        if sCat == "1":
            title = re.sub('\[.*\]|\(.*\)','', oHoster.getDisplayName())
        elif xbmc.getInfoLabel('ListItem.tagline'):
            title = xbmc.getInfoLabel('ListItem.tagline')
        else:
            title = oHoster.getDisplayName()
				

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
            accept = ['uptobox', 'uptostream', 'onefichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'UptomyAccount', self.ADDON.VSlang(30325))

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = 'onefichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'UptomyAccount', '1fichier')

        # context Library menu
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid = True):
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

        #Gestion classique
        if ('yadi.sk' in sHostName):

            return self.getHoster('yadisk')
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
        if ('vidsat' in sHostName):
            return self.getHoster('vidsat')
        if ('mycima' in sHostName):
            return self.getHoster('mycima')
        if ('mp4upload' in sHostName):
            return self.getHoster('mpupload')
        if ('youdbox' in sHostName):
            return self.getHoster('youdbox')
        if ('aparat' in sHostName):
            return self.getHoster('aparat')
        if ('yourupload' in sHostName):
            return self.getHoster('yourupload')
        if ('vidspeeds' in sHostName):
            return self.getHoster('vidspeeds')
        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')
        if ('l.vevents.net' in sHostName):
            return self.getHoster('vevents')
        if ('moshahda' in sHostName):
            return self.getHoster('moshahda')
        if ('vidoza.' in sHostName):
            return self.getHoster('vidoza')
        if (('youtube' in sHostName) or ('youtu.be' in sHostName)):
            return self.getHoster('youtube')
        if ('onlystream' in sHostName):
            return self.getHoster('onlystream')
        if ('rutube' in sHostName):
            return self.getHoster('rutube')
        if ('jwplatform' in sHostName):
            return self.getHoster('anonfile')
        if ('vk.com' in sHostName):
            return self.getHoster('vk')
        if ('vkontakte' in sHostName):
            return self.getHoster('vk')
        if ('vkcom' in sHostName):
            return self.getHoster('vk')
        if ('vidhid' in sHostName):
            return self.getHoster('vidhid')
        if ('vidto.me' in sHostName):
            return self.getHoster('vidto')
        if ('vidtodo.' in sHostName):
            return self.getHoster('vidtodo')
        if ('vidbm' in sHostName):
            return self.getHoster('vidbm')
        if ('vedbom' in sHostName):
            return self.getHoster('vidbm')
        if ('vedpom' in sHostName):
            return self.getHoster('vidbem')
        if ('vidbem' in sHostName):
            return self.getHoster('vidbem')
        if ('vedshaar' in sHostName):
            return self.getHoster('vidshare')
        if ('vedsharr' in sHostName):
            return self.getHoster('vidshare')
        if ('vedshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vidshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vidshare' in sHostName):
            return self.getHoster('vidshare')
        if ('streamwire' in sHostName):
            return self.getHoster('streamwire')
        if ('vup' in sHostName):
            return self.getHoster('streamwire')
        if ('kopatube' in sHostName):
            return self.getHoster('govid')
        if ('kobatube' in sHostName):
            return self.getHoster('govid')
        if ('govid.co' in sHostName):
            return self.getHoster('govid')
        if ('french-vid' in sHostName or 'fembed.' in sHostName or 'yggseries' in sHostName or 'sendvid' in sHostName or 'vfsplayer' in sHostName or 'fsimg' in sHostName or 'fem.tohds' in sHostName):
            return self.getHoster('frenchvid')
        if ('vidzi' in sHostName):
            return self.getHoster('vidzi')
        if ('cloudy' in sHostName):
            return self.getHoster('cloudy')
        if ('uptostream' in sHostName):
            return self.getHoster('uptostream')
        if (('dailymotion' in sHostName) or ('dai.ly' in sHostName)):
            return self.getHoster('dailymotion')
        if ('arabseed' in sHostName):
            return self.getHoster('arabseed')
        if ('vidhd' in sHostName):
            return self.getHoster('vidhd')
        if ('oktube' in sHostName):
            return self.getHoster('vidhd')
        if ('fastplay' in sHostName):
            return self.getHoster('fastplay')
        if ('4shared' in sHostName):
            return self.getHoster('shared')
        if (('netu' in sHostName) or ('hqq' in sHostName) or ('waaw' in sHostName)):
            return self.getHoster('netu')
        if ('waaw' in sHostName):
            return self.getHoster('netu')
        if ('mail.ru' in sHostName):
            return self.getHoster('mailru')
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
        if ('playreplay' in sHostName):
            return self.getHoster('playreplay')
        if ('ninjastream' in sHostName):
            return self.getHoster('ninjastream')
        if ('ok.ru' in sHostName):
            return self.getHoster('ok_ru')
        if ('vimeo.com' in sHostName):
            return self.getHoster('vimeo')
        if ('vidmoly' in sHostName):
            return self.getHoster('vidmoly')
        if ('playtube' in sHostName):
            return self.getHoster('playtube')
        if ('mediafire' in sHostName):
            return self.getHoster('mediafire')
        if ('supervideo' in sHostName):
            return self.getHoster('supervideo')
        if ('uqload.' in sHostName):
            return self.getHoster('uqload')
        if ('userload' in sHostName):
            return self.getHoster('userload')
        if ('www.amazon' in sHostName):
            return self.getHoster('amazon')
        if ('filepup' in sHostName):
            return self.getHoster('filepup')
        if ('thevid' in sHostName):
            return self.getHoster('thevid')
        if ('jawcloud' in sHostName):
            return self.getHoster('jawcloud')
        if ('vimple.ru' in sHostName):
            return self.getHoster('vimple')
        if ('wstream.' in sHostName):
            return self.getHoster('wstream')
        if ('drive.google.com' in sHostName):
            return self.getHoster('resolver')
        if ('docs.google.com' in sHostName):
            return self.getHoster('resolver')
        if ('vidwatch' in sHostName):
            return self.getHoster('vidwatch')
        if ('up2stream' in sHostName):
            return self.getHoster('up2stream')
        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')
        if ('tune' in sHostName):
            return self.getHoster('tune')
        if ('sendit' in sHostName):
            return self.getHoster('sendit')
        if ('sendvid' in sHostName):
            return self.getHoster('sendvid')
        if ('vidup' in sHostName):
            return self.getHoster('vidup')
        if ('vidbull' in sHostName):
            return self.getHoster('vidbull')
        if ('vidlox' in sHostName):
            return self.getHoster('vidlox')
        if ('veehd.' in sHostName):
            return self.getHoster('veehd')
        if (('movshare' in sHostName) or ('wholecloud' in sHostName)):
            return self.getHoster('wholecloud')
        if ('vidfast' in sHostName):
            return self.getHoster('vidfast')
        if ('kvid' in sHostName):
            return self.getHoster('kvid')
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
        if ('hdvid' in sHostName):
            return self.getHoster('hdvid')
        if (('anonfile' in sHostName) or ('govid.xyz' in sHostName) or ('vidmoly' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')
        if ('gounlimited' in sHostName):
            return self.getHoster('gounlimited')
        if ('Gounlimited' in sHostName):
            return self.getHoster('gounlimited')
        if ('mixdrop' in sHostName):
            return self.getHoster('mixdrop')
        if ('megaup' in sHostName):
            return self.getHoster('megaup')
        if ('evoload' in sHostName):
            return self.getHoster('evoload')
        if ('vidabc' in sHostName):
            return self.getHoster('vidabc')
        if ('vshare' in sHostName):
            return self.getHoster('vshare')
        if ('giga' in sHostName):
            return self.getHoster('giga')
        if (('anavids' in sHostName) or ('anavidz' in sHostName)):
            return self.getHoster('anavids')
        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamsforu')
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
        if ('govid.me' in sHostName):
            return self.getHoster('govidme')
        if ('cloudvid.' in sHostName):
            return self.getHoster('cloudvid')
        if (('goo.gl' in sHostName) or ('bit.ly' in sHostName)):
            return self.getHoster('allow_redirects')
        if ('streamzz.to' in sHostName):
            return self.getHoster('streamz')
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')
        if ('movs4u.club' in sHostName):
            return self.getHoster('movs4u')
        if ('tune' in sHostName):
            return self.getHoster('tune')
        if ('mystream' in sHostName):
            return self.getHoster('mystream')
        if ('prostream' in sHostName):
            return self.getHoster('prostream')
        if ('dood' in sHostName):
            return self.getHoster('dood')
        if ('streamtape' in sHostName):
            return self.getHoster('streamtape')
        if ('arabramadan' in sHostName):
            return self.getHoster('arabramadan')
        if ('player.4show' in sHostName):
            return self.getHoster('arabramadan')
        if ('upstream' in sHostName):
            return self.getHoster('upstream')
        if ('faselhd' in sHostName):
            return self.getHoster('faselhd')
        if ('streamable' in sHostName):
            return self.getHoster('streamable')


        if ('flashx' in sHostName):
            return self.getHoster('flashx')
        if (('thevideo.me' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName)):
            return self.getHoster('resolver')

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
        if ('jetload' in sHostName):
            return self.getHoster('resolver')
        if ('streamcherry' in sHostName):
            return self.getHoster('resolver')
        #Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('onefichier')
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')
        if ('uploaded' in sHostName or 'ul.to' in sHostName):
            return self.getHoster('uploaded')

        if ('kaydo.ws' in sHostName):
            return self.getHoster('lien_direct')
        if ('king-shoot.xyz' in sHostName):
            return self.getHoster('lien_direct')
        if ('infinityload' in sHostName):
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

        if ('egybest' in sHostName):
            return self.getHoster('lien_direct')

        if ('kingfoot' in sHostName):
            return self.getHoster('lien_direct')

        if ('livestream.com' in sHostName):
            return self.getHoster('lien_direct')

        if ('nitroflare' in sHostName or 'letsupload' in sHostName  or 'fastdrive' in sHostName   or 'openload' in sHostName or 'multiup' in sHostName):
            return False

        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm.mpd'):
            return self.getHoster('lien_direct')
        #Cas special si parametre apres le lien_direct
        if (sHosterUrl.split('?')[0][-4:] in '.mp4.avi.flv.m3u8.webm.mpd'):
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        exec ("from resources.hosters." + sHosterFileName + " import cHoster", globals())
        return cHoster()

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

            if aLink[0] or aLink[1] : # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0] :   # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        oDialog.VSinfo(sHosterName, 'Resolve')
                        oHoster.setUrl(sMediaUrl)
                        aLink = oHoster.getMediaLink()

                if aLink[0] :
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setCat(sCat)
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
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
