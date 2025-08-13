# -*- coding: utf-8 -*-

import re
import string

from resources.lib.comaddon import progress, addon, VSlog, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'freebox'
SITE_NAME = '[COLOR orange]Free TV[/COLOR]'
SITE_DESC = 'Watch Livetelevision'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_WEB = 'https://7pal.short.gy/alxstream'

TV_GROUPS = ('http://venom/', 'showGroups')

TV_CHANNELS = ('http://venom/', 'showAllChannels')

Streams = 'api/streams.json'
Channels = 'api/channels.json'
Categories = 'api/categories.json'
Languages = 'api/languages.json'
Countries = 'api/countries.json'
Logos = 'api/logos.json'
Regions = 'api/regions.json'

TV_TV = (True, 'showMenuTV')

UA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'

icon = 'tv.png'
sRootArt = ''
ADDON = addon()


class track:
    def __init__(self, length, title, path, icon, data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data

def getChannels():
    addons = addon()

    oRequestHandler = cRequestHandler(f'{URL_MAIN}{Channels}')
    ChannelsJSON = oRequestHandler.request(jsonDecode=True)

    oRequestHandler = cRequestHandler(f'{URL_MAIN}{Streams}')
    StreamsJSON = oRequestHandler.request(jsonDecode=True)

    oRequestHandler = cRequestHandler(f'{URL_MAIN}{Countries}')
    CountriesJSON = oRequestHandler.request(jsonDecode=True)

    oRequestHandler = cRequestHandler(f'{URL_MAIN}{Logos}')
    LogosJSON = oRequestHandler.request(jsonDecode=True)

    logo_map = {logo['channel']: logo['url'] for logo in LogosJSON if 'channel' in logo and 'url' in logo}

    ChannelsList = []
    sLang = addons.getSetting('livetv_lang')
    sLang_speaking_countries = [
        country["code"] for country in CountriesJSON if sLang in country.get("languages", [])
    ]

    for ch in ChannelsJSON:
        if any(lang in ch.get('country', []) for lang in sLang_speaking_countries):
            for stream in StreamsJSON:
                if stream['channel'] == ch['id']:
                    try: 
                        Cat = ch['categories'][0]
                    except:
                        Cat = 'Undefined'
                    channel_logo = logo_map.get(ch['id'], ch.get('logo', ''))
                    channel = {
                        'name': ch['name'],
                        'logo': channel_logo,
                        'country': ch['country'],
                        'cat': Cat,
                        'url': stream['url'],
                        'referrer': stream['referrer'],
                        'ua': stream['user_agent']
                    }
                    ChannelsList.append(channel)

    return ChannelsList

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', addons.VSlang(30115), 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TV_GROUPS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_GROUPS[1], addons.VSlang(70016), 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', TV_CHANNELS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_CHANNELS[1], addons.VSlang(70017), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGroups():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    ChannelsList = getChannels()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    CatsList = []
    Count = 0
    for aEntry in ChannelsList:
        CatsList.append(aEntry['cat'])
        
    CatsList = list(set(CatsList))
    
    CatsCounter = dict(zip(CatsList, [0]*len(CatsList)))
    
    for Cat in CatsList:
        for Ch in ChannelsList:
            if Ch['cat'] == Cat:
                CatsCounter[Cat] = CatsCounter[Cat] + 1

    for aEntry in CatsList:
        if aEntry not in [None,""," "]:
            sTitle = aEntry.title() + ' (' + str(CatsCounter[aEntry]) + ')'
            oOutputParameterHandler.addParameter('siteUrl',  sUrl) 
            oOutputParameterHandler.addParameter('sTitle',  sTitle) 
            oOutputParameterHandler.addParameter('sTitle2',  aEntry.title()) 
            
            oOutputParameterHandler.addParameter('sThumb',  '') 
            
            oGui.addDir(SITE_IDENTIFIER, 'showChannels', sTitle, 'genres.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showChannels():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    SelectedCat = oInputParameterHandler.getValue('sTitle2')
    
    ChannelsList = getChannels()

    for aEntry in ChannelsList:
      
        if SelectedCat in aEntry['cat'].title():
            
            sHosterUrl = aEntry['url']
   
            if aEntry['referrer'] not in [None, 'none', '']:
                sHosterUrl = sHosterUrl + '|Referrer=' + aEntry['referrer']
     
            if aEntry['ua'] not in [None, 'none', '']:
                sHosterUrl = sHosterUrl + '|User-Agent=' + aEntry['ua']
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', sHosterUrl):
                oHoster = cHosterGui().getHoster('direct_link') 
            if oHoster:
                oHoster.setDisplayName(aEntry['name'])
                oHoster.setFileName(SelectedCat)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, aEntry['logo'])

    oGui.setEndOfDirectory()

def showAllChannels():
    oGui = cGui()

    ChannelsList = getChannels()
    for aEntry in ChannelsList:

        sHosterUrl = aEntry['url']
        if aEntry['referrer'] not in [None, 'none', '']:
            sHosterUrl = sHosterUrl + '|Referrer=' + aEntry['referrer']
        if aEntry['ua'] not in [None, 'none', '']:
            sHosterUrl = sHosterUrl + '|User-Agent=' + aEntry['ua']
        
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', sHosterUrl):
            oHoster = cHosterGui().getHoster('direct_link') 
        if oHoster:
            oHoster.setDisplayName(aEntry['name'])
            oHoster.setFileName(aEntry['name'])
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, aEntry['logo'])

    oGui.setEndOfDirectory()

def showMenuTV():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_WEB)
    oGui.addDir(SITE_IDENTIFIER, 'showWeb', addons.VSlang(30332), 'tv.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def parseM3U(sUrl=None):  
    
    if not sUrl:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    inf = oRequestHandler.request().split('\n')

    playlist = []
    song = track(None, None, None, None)
    ValidEntry = False

    for line in inf:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            parts = line.split('#EXTINF:')[1].split(',', 1)
            if len(parts) == 2:
                length, title = parts
            else:
                length = parts[0]
                title = ''
            try:
                licon = line.split('#EXTINF:')[1].partition('tvg-logo=')[2]
                icon = licon.split('"')[1]
            except:
                icon = 'tv.png'
            ValidEntry = True
            song = track(length, title, None, icon)

        elif len(line) != 0:
            if ValidEntry and (not (line.startswith('!') or line.startswith('#'))):
                ValidEntry = False
                song.path = line
                playlist.append(song)
                song = track(None, None, None, None)

    return playlist

def showWeb():  
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sUrl == 'TV':
        sUrl = URL_WEB

    playlist = parseM3U(sUrl=sUrl)

    if oInputParameterHandler.exist('AZ'):
        sAZ = oInputParameterHandler.getValue('AZ')
        string = filter(lambda t: t.title.strip().capitalize().startswith(sAZ), playlist)
        playlist = sorted(string, key=lambda t: t.title.strip().capitalize())
    else:
        playlist = sorted(playlist, key=lambda t: t.title.strip().capitalize())

    if not playlist:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://')
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Error getting playlist[/COLOR]')

    else:
        total = len(playlist)
        progress_ = progress().VScreate(SITE_NAME)
        for track in playlist:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sThumb = track.icon
            if not sThumb:
                sThumb = 'special://home/addons/plugin.video.matrix/resources/art/tv.png'

            url2 = track.path.replace('+', 'P_L_U_S')

            thumb = ''.join([sRootArt, sThumb])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', url2)
            oOutputParameterHandler.addParameter('sMovieTitle', track.title)
            oOutputParameterHandler.addParameter('sThumbnail', thumb)

            oHoster = cHosterGui().getHoster('direct_link')
        
            if oHoster:
                oHoster.setDisplayName(track.title)
                oHoster.setFileName(track.title)
                cHosterGui().showHoster(oGui, oHoster, url2, sThumb)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for i in string.digits:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    for i in string.ascii_uppercase:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        oGui.addDir(SITE_IDENTIFIER, 'showTV', i, 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<title>(.+?)</title><link>(.+?)</link>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        progress_ = progress().VScreate(SITE_NAME)

        if oInputParameterHandler.exist('AZ'):
            sAZ = oInputParameterHandler.getValue('AZ')
            string = filter(lambda t: t[0].strip().capitalize().startswith(sAZ), aResult[1])
            string = sorted(string, key=lambda t: t[0].strip().capitalize())
        else:
            string = sorted(aResult[1], key=lambda t: t[0].strip().capitalize())

        total = len(string)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in string:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[0])
            oOutputParameterHandler.addParameter('sThumbnail', 'tv.png')

            oHoster = cHosterGui().getHoster('direct_link')
        
            if oHoster:
                oHoster.setDisplayName(track.title)
                oHoster.setFileName(track.title)
                cHosterGui().showHoster(oGui, oHoster, aEntry[1], 'tv.png')

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def play__():
    addons = addon()
    oGui = cGui()

    Iuser = addons.getSetting('hoster_iptvt_username')
    Ipass = addons.getSetting('hoster_iptvt_password')
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+').replace('username', Iuser).replace('password', Ipass)
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sDesc = oInputParameterHandler.getValue('sDesc')

    if '[' in sUrl and ']' in sUrl:
        sUrl = getRealUrl(sUrl)

    if 'youtube' in sUrl:
        oHoster = cHosterGui().checkHoster(sUrl)

        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

    else:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sTitle)
        sUrl = sUrl.replace(' ', '%20')
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)

        from resources.lib.player import cPlayer
        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        
        return False, False

    oGui.setEndOfDirectory()


"""
Fonction diverse:
#   - getRealUrl = Regex pour Iptv(Officiel)
#   - showDailymotionStream = Lis les liens de streaming de Daylimotion qui sont speciaux
#   - getBrightcoveKey = Recupere le token pour les liens proteger par Brightcove (RMC Decouvert par exemple)
"""


def getRealUrl(chain):
    oParser = cParser()

    UA2 = UA
    url = chain
    regex = ''
    param = ""
    head = None

    r = re.search('\[[DECODENRJ]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = decodeNrj(r.group(1))

    r = re.search('\[[BRIGHTCOVEKEY]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = getBrightcoveKey(r.group(1))

    r = re.search('\[[REGEX]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        regex = r.group(1)

    r = re.search('\[[UA]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        UA2 = r.group(1)

    r = re.search('\[[URL]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        url = r.group(1)

    r = re.search('\[[HEAD]+\](.+?)(?:(?:\[[A-Z]+\])|$)',chain)
    if r:
        head = r.group(1)

    # post metehod ?
    r = re.search('\[[POSTFORM]+\](.+?)(?:(?:\[[A-Z]+\])|$)', chain)
    if r:
        param = r.group(1)

    oRequestHandler = cRequestHandler(url)
    if param:
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'identity')
        oRequestHandler.addParametersLine(param)
    if head:
        import json
        head = json.loads(head)
        for a in head:
            oRequestHandler.addHeaderEntry(a,head[a])
    sHtmlContent = oRequestHandler.request()

    if regex:
        aResult2 = oParser.parse(sHtmlContent, regex)
        if aResult2:
            url = aResult2[1][0]

    url = url + '|User-Agent=' + UA2

    return url


def decodeNrj(d):
    oRequestHandler = cRequestHandler(d)
    sHtmlContent = oRequestHandler.request()

    title = re.search('data-program_title="([^"]+)"', sHtmlContent).group(1)
    ids = re.search('data-ref="([^"]+)"', sHtmlContent).group(1)

    url = 'https://www.nrj-play.fr/compte/live?channel=' + d.split('/')[3] + '&channel=' + d.split('/')[3] + '&title='
    url += title + '&channel=' + d.split('/')[3] + '&ref=' + ids + '&formId=formDirect'

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    dataUrl = re.search('"contentUrl" content="([^"]+)"', sHtmlContent).group(1)

    return dataUrl


def getBrightcoveKey(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "rmcdecouverte" in sUrl:
        url = re.search('<script type="application/javascript" src="([^"]+)"></script>', sHtmlContent).group(1)

        oRequestHandler = cRequestHandler("https://" + sUrl.split('/')[2] + url)
        sHtmlContent = oRequestHandler.request()
        result = re.search('N="([^"]+)",y="([^"]+)"\)', sHtmlContent)
        player = result.group(1)
        video = result.group(2)

        oRequestHandler = cRequestHandler("https://static.bfmtv.com/ressources/next-player/cleo-player/playerBridge.js")
        sHtmlContent = oRequestHandler.request().lower()

        ID = sUrl.split('/')[2].split('.')[0]
        account = re.search("\n(.+?): '" + ID + "'", sHtmlContent).group(1).replace('            ', '')

    else:
        result = re.search('<div class="video_block" id="video_player_.+?" accountid="([^"]+)" playerid="([^"]+)" videoid="([^"]+)"', sHtmlContent)

        account = result.group(1)
        player = result.group(2)
        video = result.group(3)

    url = 'http://players.brightcove.net/%s/%s_default/index.min.js' % (account, player)
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    policyKey = re.search('policyKey:"(.+?)"', sHtmlContent).group(1)

    url = "https://edge.api.brightcove.com/playback/v1/accounts/%s/videos/%s" % (account, video)
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Accept', "application/json;pk=" + policyKey)
    sHtmlContent = oRequestHandler.request()
    url = re.search('"sources":.+?src":"([^"]+)"', sHtmlContent).group(1)

    return url
