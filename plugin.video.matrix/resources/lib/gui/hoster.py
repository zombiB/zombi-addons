#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

# Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer

from resources.lib.handler.requestHandler import cRequestHandler

from resources.lib.comaddon import dialog, addon, VSlog


class cHosterGui:

    SITE_NAME = 'cHosterGui'
    ADDON = addon()
    DIALOG = dialog()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False):

        oInputParameterHandler = cInputParameterHandler()

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        # oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())
        # oGuiElement.setThumbnail(sThumbnail)
        # if (oInputParameterHandler.exist('sMeta')):
            # sMeta = oInputParameterHandler.getValue('sMeta')
            # oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)

        # oGuiElement.setMeta(1)
        oGuiElement.setIcon('host.png')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('sTitle', oHoster.getDisplayName())
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', sMediaUrl)
        # oOutputParameterHandler.addParameter('sFav', 'play')
        # oOutputParameterHandler.addParameter('sCat', '4')

        # nouveaux pour la lecture.
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            oGuiElement.setCat(sCat)
            oOutputParameterHandler.addParameter('sCat', sCat)
        else:
            oGuiElement.setCat('4')

        # context playlit menu
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

        # context FAV menu
        oGui.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)

        # context Library menu
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        # bug
        oGui.addHost(oGuiElement, oOutputParameterHandler)

    def checkHoster(self, sHosterUrl):
        #securite
        if (not sHosterUrl):
            return False

        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.lower()

        #Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        #L'user a active l'url resolver ?
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
        if (('uppom' in sHostName)or ('upbom' in sHostName)):
            return self.getHoster('uppom')
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
        if ('vidsat' in sHostName):
            return self.getHoster('vidsat')
        if ('gateaflam' in sHostName):
            return self.getHoster('gateaflam')
        if ('mycima' in sHostName):
            return self.getHoster('mycima')
        if ('mp4upload' in sHostName):
            return self.getHoster('mpupload')
        if ('youdbox' in sHostName):
            return self.getHoster('youdbox')
        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')


        if ('alimorad.club' in sHostName):
            return self.getHoster('alimorad')
        if ('alkady' in sHostName):
            return self.getHoster('alkady')
        if ('k.vevents.net' in sHostName):
            return self.getHoster('kvevents')
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
        if ('vidbem' in sHostName):
            return self.getHoster('vidbm')
        if ('vidshar' in sHostName):
            return self.getHoster('vidshare')
        if ('vidshare' in sHostName):
            return self.getHoster('vidshare')
        if ('streamwire' in sHostName):
            return self.getHoster('streamwire')
        if ('vup' in sHostName):
            return self.getHoster('streamwire')
        if ('govid.co' in sHostName):
            return self.getHoster('govid')
        if ('french-vid' in sHostName or 'fembed.' in sHostName or 'yggseries' in sHostName or 'sendvid' in sHostName or 'vfsplayer' in sHostName or 'fsimg' in sHostName or 'fem.tohds' in sHostName):
            return self.getHoster('frenchvid')


        if ('vidzi' in sHostName):
            return self.getHoster('vidzi')
        if ('cloudy' in sHostName):
            return self.getHoster('cloudy')
        if ('filetrip' in sHostName):
            return self.getHoster('filetrip')
        if ('uptostream' in sHostName):
            return self.getHoster('uptostream')
        if (('dailymotion' in sHostName) or ('dai.ly' in sHostName)):

            return self.getHoster('dailymotion')
        if ('arabseed' in sHostName):
            return self.getHoster('arabseed')

        if ('vidhd' in sHostName):
            return self.getHoster('vidhd')
        if ('filez.' in sHostName):
            return self.getHoster('filez')

        if ('playr.4helal' in sHostName):
            return self.getHoster('playrhelal')
        if ('fastplay' in sHostName):
            return self.getHoster('fastplay')
        if ('streamingentiercom/videophp?type=speed' in sHosterUrl):
            return self.getHoster('speedvideo')
        if ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')
        if ('speedvid' in sHostName):
            return self.getHoster('speedvid')
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
        if ('onevideo' in sHostName):
            return self.getHoster('onevideo')
        if ('googlevideo' in sHostName):
            return self.getHoster('googlevideo')
        if ('picasaweb' in sHostName):
            return self.getHoster('googlevideo')
        if ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')
        if ('playreplay' in sHostName):
            return self.getHoster('playreplay')

        if ('streamin.to' in sHostName):
            return self.getHoster('streaminto')

        if ('vodlocker' in sHostName):
            return self.getHoster('vodlocker')
        if ('cima4up' in sHostName):
            return self.getHoster('cimaup')
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
        if ('letwatch' in sHostName):
            return self.getHoster('letwatch')
        if ('easyvid' in sHostName):
            return self.getHoster('easyvid')
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
        if ('idowatch' in sHostName):
            return self.getHoster('idowatch')
        if ('wstream.' in sHostName):
            return self.getHoster('wstream')
        if ('watchvideo' in sHostName):
             return self.getHoster('watchvideo')
        if ('drive.google.com' in sHostName):
            return self.getHoster('googledrive')
        if ('docs.google.com' in sHostName):
            return self.getHoster('googledrive')
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
        if ('stagevu' in sHostName):
            return self.getHoster('stagevu')
        if ('veehd.' in sHostName):
            return self.getHoster('veehd')
        if (('movshare' in sHostName) or ('wholecloud' in sHostName)):
            return self.getHoster('wholecloud')
        if ('gorillavid' in sHostName):
            return self.getHoster('gorillavid')
        if ('clipwatching' in sHostName):
            return self.getHoster('clipwatching')

        if ('vidfast' in sHostName):
            return self.getHoster('vidfast')
        if ('kvid' in sHostName):
            return self.getHoster('kvid')
        if ('vidlo' in sHostName):
            return self.getHoster('vidlo')
        if ('youwatch' in sHostName):
            return self.getHoster('youwatch')
        if ('videott' in sHostName):
            return self.getHoster('videott')
        if ('vidgot' in sHostName):
            return self.getHoster('vidgot')
        if ('estream.to' in sHostName):
            return self.getHoster('estream')
        if ('filescdn' in sHostName):
            return self.getHoster('filescdn')
        if ('hdvid' in sHostName):
            return self.getHoster('hdvid')
        if (('anonfile' in sHostName) or ('vidmoly' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')
        if ('bayfiles' in sHostName):


            return self.getHoster('bayfiles')
        if ('gounlimited' in sHostName):
            return self.getHoster('gounlimited')
        if ('Gounlimited' in sHostName):
            return self.getHoster('gounlimited')
        if ('mixdrop' in sHostName):
            return self.getHoster('mixdrop')
        if ('samaup' in sHostName):
            return self.getHoster('samaup')
        if ('vidabc' in sHostName):
            return self.getHoster('vidabc')
        if ('vshare' in sHostName):
            return self.getHoster('vshare')
        if ('giga' in sHostName):
            return self.getHoster('giga')
        if ('anavids' in sHostName):
            return self.getHoster('anavids')

        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamsforu')
        #if ('file-up' in sHostName):
            #return self.getHoster('fileup')

        if ('cloud2up' in sHostName):
            return self.getHoster('cloudup')
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
        if ('govid.me' in sHostName):
            return self.getHoster('govidme')
        if ('cloudvid.' in sHostName):
            return self.getHoster('cloudvid')




        if ('clickopen' in sHostName):
            return self.getHoster('clickopen')
        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')



        if ('goo.gl' in sHostName or 'bit.ly' in sHostName):
            return self.getHoster('allow_redirects')




        if ('streamz.cc' in sHostName):
            return self.getHoster('streamz')
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')
        if ('movs4u.club' in sHostName):
            return self.getHoster('movs4u')
        if ('mystream' in sHostName):
            return self.getHoster('mystream')
        if ('letsupload' in sHostName):
            return self.getHoster('letsupload')


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
        if ('ghost' in sHostName):
            return self.getHoster('ghost')
        if ('faselhd' in sHostName):
            return self.getHoster('faselhd')
        if ('streamable' in sHostName):
            return self.getHoster('streamable')


        if ('flashx' in sHostName):
            return self.getHoster('resolver')
        if (('thevideo.me' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName)):
            return self.getHoster('resolver')

        if ('vidbom' in sHostName):
            return self.getHoster('resolver')

        if (('cloudvideo' in sHostName) or ('streamcloud' in sHostName) or ('userscloud' in sHostName)):
            return self.getHoster('resolver')
        if ('clicknupload' in sHostName):
            return self.getHoster('resolver')
        if ('myvi.ru' in sHostName):
            return self.getHoster('resolver')
        if ('yandex' in sHostName):
            return self.getHoster('resolver')
        if ('jetload' in sHostName):
            return self.getHoster('resolver')



        if ('rapidgator' in sHostName):
            return self.getHoster('resolver')
        if ('streamcherry' in sHostName):
            return self.getHoster('resolver')


        #Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('onefichier')
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')
        if ('uplea.com' in sHostName):
            return self.getHoster('uplea')
        if ('uploaded' in sHostName or 'ul.to' in sHostName):
            return self.getHoster('uploaded')

        if ('kaydo.ws' in sHostName):
            return self.getHoster('lien_direct')
        if ('infinityload' in sHostName):
            return self.getHoster('lien_direct')
        if ('us.archive.' in sHostName):
            return self.getHoster('lien_direct')
        if ('ddsdd' in sHostName):
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

        if ('stardima.com' in sHostName):
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

        if ('nitroflare' in sHostName or 'megaup.net' in sHostName  or 'openload' in sHostName or 'multiup' in sHostName):
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
        sTitle = oInputParameterHandler.getValue('title')

        if not sTitle:
            sTitle = sFileName

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Hoster - play ' + sMediaUrl)

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        oDialog.VSinfo(sHosterName, 'Resolve')

        try:

            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink[0]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(sTitle)
                oGuiElement.getInfoLabel()

                oPlayer = cPlayer()

                # sous titres ?
                if len(aLink) > 2:
                    oPlayer.AddSubtitles(aLink[2])

                oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])
                return
            else:
                oDialog.VSerror(self.ADDON.VSlang(30020))
                return

        except:
            oDialog.VSerror(self.ADDON.VSlang(30020))
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

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            dialog().VSinfo(str(oHoster.getFileName()), 'Playlist')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
