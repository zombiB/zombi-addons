# -*- coding: utf-8 -*-

from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog

class cHosterGui:
    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False):
        oHoster.setUrl(sMediaUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        oInputParameterHandler = cInputParameterHandler()

        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        sSeason = oInputParameterHandler.getValue('sSeason')
        sEpisode = oInputParameterHandler.getValue('sEpisode')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')

        if not sRes:
            sRes = oHoster.getRes()

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')

        # Category
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4':  # "Season" ...
                sCat = '8'   # ... "Episode"
        else:
            sCat = '5'     # Divers

        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(sMeta)

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setIcon('host.png')
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        sMediaFile = oHoster.getMediaFile()
        if sMediaFile:  # Afficher le nom du fichier plutot que le titre
            oGuiElement.setMediaUrl(sMediaFile)
            if self.ADDON.getSetting('display_info_file') == 'true':
                oHoster.setDisplayName(sMediaFile)
                oGuiElement.setTitle(oHoster.getFileName())  # permet de calculer le cleanTitle
                oGuiElement.setRawTitle(oHoster.getDisplayName())  # remplace le titre par le lien
            else:
                oGuiElement.setTitle(oHoster.getDisplayName())
        else:
            oGuiElement.setTitle(oHoster.getDisplayName())


        title = oGuiElement.getCleanTitle()
        tvShowTitle = oGuiElement.getItemValue('tvshowtitle')

        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('tvShowTitle', tvShowTitle)
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)


        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)  # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)  # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
        oOutputParameterHandler.addParameter('realHoster', oHoster.getRealHost())

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Reading List
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Media
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'upToMyAccount', self.ADDON.VSlang(30325))
                    break

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = '1fichier' 
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'upToMyAccount', '1fichier')

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid=True):
        # security
        if not sHosterUrl:
            return False

        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.split('?')[0]
        sHosterUrl = sHosterUrl.lower()

        try:
            from urllib.parse import urlparse
            sHostName = urlparse(sHosterUrl).hostname or sHosterUrl
        except Exception:
            sHostName = sHosterUrl

        if debrid: 

            if self.ADDON.getSetting('Userresolveurl') == 'true':
                import resolveurl
                hmf = resolveurl.HostedMediaFile(url=sHosterUrl)
                if hmf.valid_url():
                    tmp = self.getHoster('resolver')
                    RH = sHosterUrl.split('/')[2]
                    RH = RH.replace('www.', '')
                    tmp.setRealHost(RH.split('.')[0].upper())
                    return tmp

            # alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                f = self.getHoster('alldebrid')

                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f

            # realbrid ?
            if self.ADDON.getSetting('hoster_realdebrid_premium') == 'true':
                f = self.getHoster('realdebrid')

                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f

            # debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("direct_link")

        supported_player = ['film77', 'streamable', 'stardima', 'filescdn', 'videott', 'vidlo', 'sendit', 'vidmoly', 
                            'fastplay', 'extremenow', 'yourupload', 'vidspeeds', 'voe', 'faselhd', 'naqoos', 'frdl',
                            'streamax', 'facebook', 'mixdrop', 'mixloads', 'vidoza', 'rutube', 'speedvid', 'krakenfiles', 
                            'playreplay', 'uqload', 'qiwi', 'gofile', 'mail.ru', 'videas', 'vidyard', '1cloud', 'uploady',
                            'letwatch', 'mp4upload', 'filepup', 'wstream', 'watchvideo', 'vidwatch', 'tune', 'extrashare',
                            'vidup', 'vidbull', 'cloudhost', 'videobin', 'stagevu', 'soraplay', 'supervideo', 'streamhub',
                            'hdvid', 'vidload', 'giga', 'vidbom', 'cloudvid', 'megadrive', 'clickopen', 'gettyshare',
                            'turbovid', 'soundcloud', 'mixcloud', 'ddlfr', 'vupload', 'dwfull', 'vidzstore', 'pdj', 
                            'dustreaming', 'onlystream', 'upstream', 'vudeo', 'vidia', 'vidbem', 'onevideo', 
                            'sibnet', 'userload', 'aparat', 'abcvideo', 'streamvid', 'darkibox', 'hexupload', 'dailyuploads',
                            'myvi', 'viewsb', 'yourvid', 'terabox', 'streamsilk', 'vixstream', 'vid3rb', 'bigwarp',
                            'forafile', 'filepv', 'ultra4vid', 'abstream', 'videa', 'streamup', 'upzur']

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))

        # Vidshare Clone
        vidshare = next((x for x in ['vadshar', 'vidshar', 'vedshaar', 'vedsharr', 'vedshar', 'vedshar', 'vidshare', 'viidshar', 'vid1shar', '2vid2cdnshar', 'v2d2shr', 
                            'v1d1shr', 'v3dsh1r', 'vds3r', 'v3dshr', 'vndsh1r', 'vd12s3r', 'v31dshr', 'vds1r', 'vdonlineshr', 'v4dshnr', 'vd1sher',
                            'vd13r', 'vd1sr', 'v1dsr', 'vd2sr', 'v1d2sr', 'v2d3sr', 'vd4sr', 'vadsr', 'van1dsr', 'vv1dsr', 'viidhdr', 'va1dsr', 'vd5sr',
                            '1vid1shar'] if x in sHostName), None)
        if vidshare:
            return self.getHoster('vidshare')

        # Vidbom Clone
        vidbom = next((x for x in ['vidbom', 'vidbm', 'vadbam', 'vedbom', 'vadbom', 'vidbam', 'vedbam', 'viboom', 'vid1bom', 'viid2beem', 'viid1boom', 
                            'ved2om', 'vid2bom', 'viidboom', 'vig1bm', 'v3db1oom', 'ved1om', 'vvid1om', 'vigom', 've1dp3m', 'vdp1em', 'viid1bem', 'vuidbeaam',
                            'v2ddb3m', '2vbiim', 'vdb123m', 'vd123bm', 'v3dbeam', 'v3dbtom', 'v7d20bm', 'v7d20bm', 'vdtom', 'vendm', 'vandbm', 'vand1bm', 
                            'vrdb2m', 'vdbt3om', 'vd22tom', 'ven1dm', 'vrdtem', 'vrd1tem', 'v5db2m', 'vdb1m', 'vendbm', 'v6b3m', 'vd1bm', 'vdb2m', 'v1db2m', 
                            'v2db3m', 'vd3bm', 'venb1m', 'v1enbm', 'vndtom', 'v1dbm', 'vd5bm', 'vdbtm'] if x in sHostName), None)
        if vidbom:
            return self.getHoster('vidbom')

        # Uppom Clone
        uppom = next((x for x in ['upbaam', 'upbam', 'uppom', 'uppboom', 'uupbom', 'upgobom', 'upptobom', 'up2b9om', 'up1bom', 'up3bom', 'u1pb3m', 
                            'u2pbemm', 'up1beem', 'bmbm.shop', '4bmto', '2bm.shop', 't0bm4.shop', '4bem2022', 'bm025', 'bm2024', 'b245m.shop', 'b2m1.shop',
                            'online20.shop', 'line50.shop', 'fo0.shop', 'online20stream', '4view.shop', 'team20.shop', 'travel15.shop', 'sigh15.shop', 
                            'video15.shop', 'streaming15.shop', 'onlin12estream', 'tostream20', 'streaming200', 'top15top', 'uppbom'] if x in sHostName), None)
        if uppom:
            return self.getHoster('uppom')

        # Govidme Clone
        govidme = next((x for x in ['govad', 'govid.me', 'goveed', 'go2ved', 'go1ved', 'go-veid', 'g1v3d', 'goo1vd', 'g2ev4d', 'ge1verd', 'g1oov1d', 
                            'ga1ov3d', '1gafv3d', 'go12d', 'go1v2d', 'gonvd1', 'gaonv3d', 'gonv20d', 'goevd', 'goanvd', 'goanv1d', 'gonvnd', 'gvnd', 
                            'gaonvd', 'go1evd', 'goverd', 'gnvd', 'go1vend', 'go1vd', 'go2vd', 'go4vd', 'gov7d', 'gon1vd', 'goov9d','goov1d', 'goov2d', 
                            'gov9d', 'gov8d', 'g1ovd', 'goveed1'] if x in sHostName), None)
        if govidme:
            return self.getHoster('govidme')
        
        # Streamwish Clone
        streamwish = next((x for x in ['streamwish', 'khadhnayad', 'ajmidyad', 'yadmalik', 'kharabnah', 'hayaatieadhab', 'sfastwish', 'eghjrutf', 'eghzrutw',
                            'wishfast', 'fviplions', 'egtpgrvh', 'mdy48tn97', 'embedwish', 'fsdcmo.sbs', 'anime4low', 'cdnwish-down', 'heavenlyvideo', 'strwish',
                            'flaswish', 'streamzid', 'cimawish', 'egopxutd', 'obeywish', 'trgsfjll', 'mdbekjwqa', 'uqloads', 'm3lomatik', 'cdnwish', 'ma2d',
                            'mohahhda', 'asnwish', 'jodwish', 'cinemathek', 'swhoi', 'dancima', 'warda', 'gsfqzmqu', 'swdyu', 'cinemabest.online', 'zidwish',
                            'wishonly', 'playerwish', 'katomen', 'hlswish', 'swishsrv', 'iplayerhls', 'hlsflast', '4yftwvrdz7', 'eb8gfmjn71', 'cybervynx',
                            'edbrdl7pab', 'stbhg', 'dhcplay', 'hailindihg', 'zuvioeb', 'musalsalatuk', 'hglink', 'tryzendm', 'wish-redirect',
                            'dumbalag', 'haxloppd', 'davioad', 'kravaxxa'] if x in sHostName), None)
        if streamwish:
            return self.getHoster('streamwish')

        # Frenchvid Clone
        frenchvid = next((x for x in ['french-vid', 'diasfem', 'yggseries', 'fembed', 'fem.tohds', 'feurl', 'fsimg', 'core1player',
                                'vfsplayer', 'gotochus', 'suzihaza', "femax"] if x in sHostName), None)
        if frenchvid:
            return self.getHoster("frenchvid")

        # Filelions Clone
        filelions = next((x for x in ['filelions', 'ajmidyadfihayh', 'alhayabambi', 'bazwatch', 'cilootv', 'motvy55', 'bazlions', 'lylxan',
                                'fdewsdc.sbs', '5drama.vip', 'cdnlion-down', 'demonvideo', 'zidlions', 'vidhide', 'streamfile', 'vidnow', 'tuktukcinema29.buzz',
                                'gsfomqu', 'codeda', 'ma3refa.store', 'coolciima', 'nejma', 'cinmabest.site', 'zidhide', 'dhtpre', '6sfkrspw4u',
                                'peytonepre', 'ryderjet', 'e4xb5c2xnz', 'smoothpre', 'cinmabest', 'movearnpre', 'gradehgplus', 'jaycinema', 'videoland',
                                'mivalyo'] if x in sHostName), None)
        if filelions:
            return self.getHoster("filelions")

        # Vidguard Clone
        vidguard = next((x for x in ['vidguard', 'fertoto', 'vgembed', 'vgfplay', 'vembed', 'vid-guard', 'jetload', 'embedv', 'fslinks', 'bembed', 'listeamed',
                                     'gsfjzmqu', '6tnutl8knw', 'dhmu4p2hkp', 'cinmbest'] if x in sHostName), None)
        if vidguard:
            return self.getHoster("vidguard")

        # Vidtodo clone
        vidtodo = next((x for x in ['vidtodo', 'vixtodo', 'viddoto', 'vidstodo'] if x in sHostName), None)
        if vidtodo:
            return self.getHoster('vidtodo')

        # Filemoon Clone
        filemoon = next((x for x in ['filemoon', 'moonmov', 'allviid', 'all-vid', 'techradar', 'albrq', 'kerapoxy', 'kinoger', 'smdfs40r', '81u6xl9d',
                                     '1azayf9w', 'ghbrisk', 'bf0skv', '8mhlloqo', '222i8x', 'l1afav', '96ar', 'xcoic', 'f51rm'] if x in sHostName), None)
        if filemoon:
            return self.getHoster("filemoon")

        # Voe Clone
        voe = next((x for x in ['voe', 'kathleenmemberhistory', 'timberwoodanotia', 'stevenimaginelittle', 'availedsmallest', 'monorhinouscassaba', 'jamiesamewalk',
                                'graceaddresscommunity', 'shannonpersonalcost', 'michaelapplysome','brucevotewithin', 'robertplacespace', 'jamessoundcost',
                                'robertordercharacter', 'maxfinishseveral', 'chuckle-tube', 'kristiesoundsimply', 'adrianmissionminute', 'jilliandescribecompany'] if x in sHostName), None)
        if voe:
            return self.getHoster("voe")

        # Vidlo Clone
        vidlo = next((x for x in ['vidlo', 'c13-look', '7c3-look'] if x in sHostName), None)
        if vidlo:    
            return self.getHoster('vidlo')

        # Dood Clone
        vidlo = next((x for x in ['DoodStream', 'dooood', 'flixeo', 'ds2play', 'dood', 'd0o0d', 'ds2video', 'do0od', 'd0000d', 'd000d', 'doood', 'vidply',
                                  'do7go', 'doply.net', 'vide0.net', 'vvide0', 'd-s.io'] if x in sHostName), None)
        if vidlo:    
            return self.getHoster('dood')

        # Chillx Clone
        # chillx = next((x for x in ['chillx', 'vectorx', 'boltx', 'bestx'] if x in sHostName), None)
        # if chillx:    
        #    return self.getHoster('chillx')

        # Mixdrop Clone
        mixdrop = next((x for x in ['mixdroop', 'mdfx9dc8n', 'mdzsmutpcvykb', 'mxdrop'] if x in sHostName), None)
        if mixdrop:    
            return self.getHoster('mixdrop')

        # Mcloud Clone
        mcloud = next((x for x in ['mcloud', 'vizcloud', 'vidstream', 'vidplay', '55a0716b8c', 'e69975b881', 'c8365730d4', 'vid2faf'] if x in sHostName), None)
        if mcloud:    
            return self.getHoster('mcloud')

        # Arabseed Clone
        arabseed = next((x for x in ['reviewtech', 'reviewrate', 'seeeed', 'techinsider', 'gamezone.cam', 'gameshop4u', 'gamehub'] if x in sHostName), None)
        if arabseed:    
            return self.getHoster('arabseed')

        # Streamhide Clone
        streamhide = next((x for x in ['guccihide', 'streamhide', 'fanakishtuna', 'ahvsh', 'animezd', 'anime7u', 'vidroba'] if x in sHostName), None)
        if streamhide:    
            return self.getHoster('streamhide')

        # X-Video Clone
        xvideo = next((x for x in ['filerio', 'vod540', 'hd-cdn', 'anyvid', 'vod7', 'segavid', 'vidblue', 'arabveturk', 'filegram', 'tv30.online', 'miravd',
                                   'mwdy', 'vidsp.net', 'mp4plus', 'okprime', '1vid.xyz', 'vidker', 'filehd', 'egybestvid', 'vidoba', 'arab-drama',
                                   'hdup20', 'turkvearab'] if x in sHostName), None)
        if xvideo:    
            return self.getHoster('xvideo')

        # Kinoger Clone
        kinoger = next((x for x in ['.upn.one', '.upns.online', 'uns.bio', 'wasuytm', 'rpmvid', 'filedecrypt'] if x in sHostName), None)
        if kinoger:    
            return self.getHoster('kinoger')


        # False Links
        false_links = next((x for x in ['nitroflare', 'tubeload.', 'Facebook', 'fastdrive', 'megaup.net', 'openload', 'vidhd', 'oktube', 'mdiaload', 'fikper', 'turbobit', '1fichier', 'multiup.io',
                                        'mega.nz', 'rapidgator', 'ddownload', 'bowfile', 'uptobox', 'uptostream', 'wahmi', 'doodrive', 'highload', 'anonfiles', 'jawcloud', 'dailyuploads',
                                        'videomega', 'prostream', 'fembed', 'filegage', 'streamlare', 'katfile', 'usersdrive', 'uploadbank', 'fastupload', 'fireload', 'vikingfile', 'workupload',
                                        'buzzheavier', 'samaup', 'uplo.top', 'filespayout', 'send.cm', 'sbthe.com', '10gb.vn'] if x in sHostName), None)
        if false_links:    
            return False

        if ('short.ink' in sHostName):
            return self.getHoster('shortlink')

        if ('oneupload' in sHostName) or ('tipfly' in sHostName):
            return self.getHoster('oneupload')

        if ('vidsrc.stream' in sHostName):
            return self.getHoster('vidsrcstream')

        if ('multiembed' in sHostName):
            return self.getHoster('multiembed')

        if ('cimacafe' in sHostName) or ('media200' in sHostName) or ('media300' in sHostName):
            return self.getHoster('cimacafe')

        if ('bgwp.cc' in sHosterUrl):
            return self.getHoster('bigwarp')

        if ('hexload' in sHostName):
            return self.getHoster('hexupload')

        if ('dzen' in sHostName):
            return self.getHoster('dzen')

        if ('extreamnow' in sHostName):
            return self.getHoster('extremenow')

        if ('2embed.me' in sHostName):
            return self.getHoster('2embedme')

        if ('remotestre.am' in sHostName):
            return self.getHoster('remotestream')

        if ('drop.download' in sHostName):
            return self.getHoster('drop')

        if ('clicknupload' in sHostName):
            return self.getHoster('clicknupload')

        if ('.aflam' in sHosterUrl):
            return self.getHoster('mixloads')

        if ('sbfull' in sHostName) or ('sbrapid' in sHostName) or ('sbhight' in sHostName) or ('sbface' in sHostName):
            return self.getHoster('viewsb')

        if ('upstream' in sHosterUrl) or ('ups2up' in sHosterUrl):
            return self.getHoster('upstream')

        if ('wolfstream' in sHosterUrl):
            return self.getHoster('aparat')
              
        if ('vanfem' in sHostName):
            return self.getHoster('fembed')

        if ('asjp1j93c1' in sHostName) or ('cd189tryo7' in sHostName):
            return self.getHoster('forafile')

        if ('vidtube' in sHostName) or ('vtbe' in sHostName):
            return self.getHoster('vidtube')

        if ('updown' in sHostName):
            return self.getHoster('updown')

        if ('diasfem' in sHosterUrl):
            return self.getHoster('fembed')
       
        if ('streamtape' in sHostName) or ('streamnoads' in sHostName) or ('tapenoads' in sHostName) or ('advertisertape' in sHostName) or ('adblocktape' in sHostName) or ('streamta.site' in sHosterUrl):
            return self.getHoster('streamtape')
       
        if ('lanesh' in sHosterUrl):
            return self.getHoster('lanesh')

        if ('lulustream' in sHosterUrl) or ('luluvdo' in sHostName) or ('luluvid' in sHostName) or ('lulu.st' in sHostName) or ('732eg54de642sa' in sHostName) or ('goodstream') in sHostName:
            return self.getHoster('lulustream')

        if ('rubystream' in sHosterUrl) or ('tuktukmulti' in sHostName) or ('stmruby' in sHostName) or ('streamruby' in sHostName) or ('rubystm' in sHostName) or ('rubyvid' in sHostName):
            return self.getHoster('rubystream')

        if ('they.tube' in sHostName):
            return self.getHoster('theytube')

        if ('asiawiki' in sHostName):
            return self.getHoster('asiadtv')

        if ('asiatvplayer' in sHostName):
            return self.getHoster('asiadtv')

        if ('vimeo' in sHostName):
            return self.getHoster('vimeo')

        if ('rrsrrs' in sHostName) or ('cimanow.net' in sHosterUrl):
            return self.getHoster('cimanow')

        if ('embed.scdn.' in sHostName):
            return self.getHoster('faselhd')
        
        if ('/run/' in sHosterUrl):
            return self.getHoster('mycima')
                 
        if ('rumble' in sHostName):
            return self.getHoster('rumble')

        if ('file-upload' in sHostName):
            return self.getHoster('fileupload')

        if ('download.gg' in sHostName):
            return self.getHoster('downloadgg')
           						
        if ('vidspeed' in sHostName):
            return self.getHoster('vidspeeds')
				
        if ('linkbox' in sHostName) or ('sharezweb' in sHostName) or ('lbx.to' in sHostName):
            return self.getHoster('linkbox')
           
        if ('mediafire' in sHostName):
            return self.getHoster('mediafire')

        if ('rabbitstream' in sHostName) or ('dokicloud' in sHostName):
            return self.getHoster('streamrapid')

        if ('veehd.' in sHostName):
            return self.getHoster('veehd')

        if ('eeggyy' in sHosterUrl):
            return self.getHoster('egybest')

        if ('vidhls' in sHosterUrl):
            return self.getHoster('vidhls')

        if ('play.imovietime' in sHosterUrl):
            return self.getHoster('moviztime')

        if ('shoffree' in sHostName) or ('egy-best' in sHostName) or ('site-panel.click' in sHostName) or ('anime4up' in sHostName) or ('anme4up7' in sHostName) or ('egybest' in sHostName):
            return self.getHoster('shoffree')

        if ('streamsforu' in sHostName or 'ylass' in sHostName or 'rsc.cdn' in sHostName or 'btolat' in sHostName):
            return self.getHoster('streamz')
				
        if ('archive.org/embed/"' in sHostName):
            return self.getHoster('archive')
				
        if (('anavids' in sHostName) or ('anavidz' in sHostName)):
            return self.getHoster('anavids')

        if (('anonfile' in sHostName) or ('govid.xyz' in sHostName) or ('file.bz' in sHostName) or ('myfile.is' in sHostName) or ('upload.st' in sHostName)):
            return self.getHoster('anonfile')

        if (('cloudvideo' in sHostName) or ('streamcloud' in sHostName) or ('userscloud' in sHostName)):
            return self.getHoster('cloudvid')
                                 
        if ('nowvid' in sHostName) or ('vegaasvid' in sHostName):
            return self.getHoster('govid')
                      
        if ('4shared' in sHostName):
            return self.getHoster('shared')
				
        if ('fajer.live' in sHostName):
            return self.getHoster('fajerlive')

        if ('cimaclub' in sHostName):
            return self.getHoster('cimaclub')
                       
        if ('govid' in sHostName) or ('drkvid' in sHosterUrl) or ('gvid.' in sHosterUrl) or ('govid.' in sHostName) or ('kopatube' in sHostName) or ('kobatube' in sHostName) or ('darkveed' in sHostName) or ('downvol' in sHosterUrl) or ('telvod' in sHosterUrl):
            return self.getHoster('govid')
            
        if ('vid4up' in sHostName):
            return self.getHoster('vidforup')
                       
        if ('fajer.video' in sHostName):
            return self.getHoster('fajer')
            
        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')

        if ('anafast' in sHostName) or ('anamov' in sHostName) or ('anaturk' in sHostName):
            return self.getHoster('anafasts')

        if ('myvi.' in sHostName):
            return self.getHoster('myvi')

        if ('yodbox' in sHostName) or ('youdbox' in sHostName) or ('youdboox' in sHostName):
            return self.getHoster('youdbox')

        if ('yandex' in sHostName) or ('yadi.sk' in sHostName):
            return self.getHoster('yadisk')

        if ('vedpom' in sHostName) or ('vidbem' in sHostName):
            return self.getHoster('vidbem')

        if ('vkplay' in sHostName):
            return self.getHoster('vkplay')

        if ('sharecast' in sHostName):
            return self.getHoster('sharecast')

        if ('live7' in sHostName):
            return self.getHoster('live7')

        if ('voodc' in sHostName):
            return self.getHoster('voodc')

        if ('vk.com' in sHostName) or ('vkontakte' in sHostName) or ('vkcom' in sHostName) or ('vk.ru' in sHostName) or ('vkvideo' in sHostName):
            return self.getHoster('vk')

        if ('megaup.net' in sHostName):
            return self.getHoster('megaup')

        if ('liiivideo' in sHostName) or ('qfilm' in sHostName) or ('almstba' in sHostName):
            return self.getHoster('qfilm')

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('direct_link')
            except:
                pass
            else:
                return self.getHoster('dailymotion')
            
        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp?type=speed' in sHosterUrl) or ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('googlevideo' in sHostName) or ('picasaweb' in sHostName) or ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')

        if ('sendvid' in sHostName):
            return self.getHoster('sendme')

        if ('upvid' in sHostName) or ('opvid' in sHostName) or ('illvid' in sHostName):
            return self.getHoster('upvid')

        if ('dynamicrevival' in sHostName) or ('cordneutral' in sHostName):
            return self.getHoster('dynamic')

        if ('hdup' in sHostName):
            return self.getHoster('hdup')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')

        if ('netu' in sHostName) or ('waaw' in sHostName) or ('hqq' in sHostName) or ('doplay' in sHostName) or ('vizplay' in sHostName):
            return self.getHoster('netu')

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')
   
        if ('torrent' in sHosterUrl) or ('magnet:' in sHosterUrl):
            return self.getHoster('torrent')

        # Direct Links
        line_direct = next((x for x in ['hadara.ps', 'megaupload.', 'fansubs', 'us.archive.', 'ddsdd', 'ffsff', 'rrsrr', 'fbcdn.net', 'blogspot.com', 'videodelivery', 'bittube', 'amazonaws.com',
                                        '.googleusercontent.com', 'archive.org/download', 'iptvtree', 'ugeen', 'ak-download', 'nextcdn', 'akwam', 'onesav', 'akoams.com', '.vimeocdn.', 'bokracdn', 
                                        'gcdn', 'alarabiya', 'kingfoot', 'livestream', 'myfiles.alldebrid.com', 'clientsportals', 'workers.dev'] if x in sHostName), None)
        if line_direct:    
            return self.getHoster('direct_link')

        # lien direct ?
        if any(sHosterUrl.endswith(x) for x in ['.mp4', '.avi', '.flv', '.m3u8', '.webm', '.mkv', '.mpd']):
            return self.getHoster('direct_link')

        if ('tuktuk' in sHosterUrl) or ('volvovideo' in sHostName) or ('lumiawatch' in sHostName) or ('demonvid' in sHostName):
            return self.getHoster('tuktuk')

        if ('avideo.host' in sHosterUrl):
            return self.getHoster('avideo')

        if ('vido' in sHosterUrl):
            return self.getHoster('vido') 

        if ('hd-cdn' in sHosterUrl):
            return self.getHoster('hdcdn') 

        else:
            # If no builtin resolver then let's try resolveURL:
            f = self.getHoster('resolver')
            f.setRealHost(sHostName)
            return f     
               
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

            if aLink and (aLink[0] or aLink[1]):
                if not aLink[0]: 
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        oDialog.VSinfo(sHosterName, 'Resolve')
                        oHoster.setUrl(aLink[1])
                        aLink = oHoster.getMediaLink()

                if aLink[0]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setFileName(sFileName)
                    oGuiElement.setCat(sCat)
                    oGuiElement.setMeta(sMeta)
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.getInfoLabel()

                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer()

                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])

                    return oPlayer.run(oGuiElement, aLink[1])

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
