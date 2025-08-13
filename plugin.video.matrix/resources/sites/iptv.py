# -*- coding: utf-8 -*-

import re, base64
import six, time
import requests
from resources.lib.mCaptcha.mserver import CaptchaServer
from resources.lib.comaddon import addon, siteManager, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.util import urlHostName
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib import random_ua

UA = random_ua.get_ua()

sSession = requests.session()

SITE_IDENTIFIER = 'iptv'
SITE_NAME = '[COLOR orange]Premium IPTV[/COLOR]'
SITE_DESC = 'Watch Live television'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
sHost = base64.b64decode('ZXZpbC5uZWVndS8vOnB0dGg=').decode("utf-8")
URL_MAIN = sHost[::-1]

iHost = base64.b64decode('MDAwMzowNi45LjMyMS42NzEvLzpwdHRo').decode("utf-8")
iHost = iHost[::-1]

URL_WEB = f'{URL_MAIN}:8080/get.php?username=accountname&password=accountpassword&type=m3u_plus'

TV_TV = (True, 'showMenuTV')

icon = 'tv.png'
sRootArt = ''
addons = addon()

class track:
    def __init__(self, length, title, path, icon, data=''):
        self.length = length
        self.title = title
        self.path = path
        self.icon = icon
        self.data = data

def load():
    oGui = cGui()

    if (addons.getSetting('hoster_iptv_username') == '') and (addons.getSetting('hoster_iptv_password') == ''):
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', '[COLOR %s]%s[/COLOR]' % ('orange', 'Requires a Premium or Account'), 'none.png', oOutputParameterHandler)

    else:
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', addons.VSlang(30115), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuTV():
    oGui = cGui()

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
            length, title = line.split('#EXTINF:')[1].split(',', 1)
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

    if (addons.getSetting('hoster_iptv_username') == '') and (addons.getSetting('hoster_iptv_password') == ''):
        if (addons.getSetting('hoster_iptv_account_email') == '') and (addons.getSetting('hoster_iptv_account_password') == ''):
            oOutputParameterHandler = cOutputParameterHandler()
            oGui.addDir(SITE_IDENTIFIER, 'opensetting', '[COLOR %s]%s[/COLOR]' % ('orange', 'Requires a Premium or Free Account'), 'none.png', oOutputParameterHandler)
        else:
            get_Bearer()
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://')
            oGui.addText(SITE_IDENTIFIER, '[COLOR orange]Renew Completed, Go Back and try Again[/COLOR]')

    else:
        Iuser = addons.getSetting('hoster_iptv_username')
        Ipass = addons.getSetting('hoster_iptv_password')

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl').replace('P_L_U_S', '+').replace('accountname', Iuser).replace('accountpassword', Ipass)

        if sUrl == 'TV':
            sUrl = URL_WEB.replace('P_L_U_S', '+').replace('accountname', Iuser).replace('accountpassword', Ipass)

        playlist = parseM3U(sUrl=sUrl)
        if not playlist:
            if (addons.getSetting('hoster_iptv_account_email') == '') and (addons.getSetting('hoster_iptv_account_password') == ''):
                oOutputParameterHandler = cOutputParameterHandler()
                oGui.addDir(SITE_IDENTIFIER, 'opensetting', '[COLOR %s]%s[/COLOR]' % ('orange', 'Requires a Premium or Free Account'), 'none.png', oOutputParameterHandler)
            else:
                get_Bearer()
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://')
                oGui.addText(SITE_IDENTIFIER, '[COLOR orange]Renew Completed, Go Back and try Again[/COLOR]')

        else:
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            groups = set()
            current_group = None

            for line in sHtmlContent.splitlines():
                if line.startswith("#EXTINF"):
                    match = re.search(r'group-title="([^"]+)"', line)
                    if match:
                        current_group = match.group(1)
                        groups.add(current_group)

            for group in sorted(groups, key=str.lower):
                sTitle = group
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sGroup', sTitle)
                oGui.addDir(SITE_IDENTIFIER, 'showGroup', sTitle.replace('⚽',''), 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGroup():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sGroup = oInputParameterHandler.getValue('sGroup')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    groups = {}
    current_group = None
    current_name = None
    current_logo = None

    for line in sHtmlContent.splitlines():
        if line.startswith("#EXTINF"):
            match_group = re.search(r'group-title="([^"]+)"', line)
            match_name = re.search(r'tvg-name="([^"]+)"', line)
            match_logo = re.search(r'tvg-logo="([^"]+)"', line)
            if match_group:
                current_group = match_group.group(1)
            if match_name:
                current_name = match_name.group(1)
            if match_logo:
                current_logo = match_logo.group(1)
                if 'http' not in current_logo:
                    current_logo = 'special://home/addons/plugin.video.matrix/resources/art/tv.png'

        elif line.startswith("http"):
            if current_group == sGroup:
                if current_group not in groups:
                    groups[current_group] = []
                groups[current_group].append((current_name, current_logo, line))

    for name, logo, link in groups.get(sGroup, []):
        sThumb = logo
        sTitle = name
        sHosterUrl = link.replace('+', 'P_L_U_S')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumb)
        oGui.addMisc(SITE_IDENTIFIER, 'play__', sTitle, 'foot.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def play__(): 
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    if 'youtube' in sUrl:
        oHoster = cHosterGui().checkHoster(sUrl)

        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

    else:
        oHoster = cHosterGui().getHoster('direct_link')
        if oHoster:
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)

    oGui.setEndOfDirectory()

def set_setting(id, value):

    if not isinstance(value, six.string_types):
        value = str(value)
    addons.setSetting(id, value)

def get_Bearer():

    sBearer, sUser, sPass = account_login()
    set_setting('bearer_token', sBearer)
    set_setting('hoster_iptv_username', sUser)
    set_setting('hoster_iptv_password', sPass)
    set_setting('last_bearer_create', str(int(time.time())))
    renewSubs(sBearer)

    return sBearer

def account_login():
    Iuser = addons.getSetting('hoster_iptv_account_email')
    Ipass = addons.getSetting('hoster_iptv_account_password')

    url = f"{iHost}/auth/login"
    user = Iuser
    password = Ipass
    captcha = get_captcha()
    payload = {
        'email': user,
        'password': password,
        'recaptcha': captcha
        }

    headers = {
        "host": f"{iHost}",
        "proxy-connection": "keep-alive",
        "accept": "application/json",
        "authorization": "Bearer",
        "user-agent": UA,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": URL_MAIN,
        "referer": f"{URL_MAIN}/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9"
    }

    response = sSession.post(url, data=payload, headers=headers).json()
    return response["access"]["token"], response["user"]["iptv_user"], response["user"]["iptv_pass"] 

def renewSubs(Bearer):
    url = f"{iHost}/v1/subscriptions"
    code, token = get_code()
    payload = {"code": code,
            "token": token,
            "bouquetId": '384'}

    url = f"{iHost}/v1/subscriptions"

    headers = {
        "host": f"{iHost}",
        "proxy-connection": "keep-alive",
        "accept": "application/json",
        "authorization": f"Bearer {Bearer}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": URL_MAIN,
        "Referer": f"{URL_MAIN}/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9"
    }

    response = requests.post(url, data=payload, headers=headers)

def get_captcha():
    sUrl = f"{URL_MAIN}:80"
    RapidApi_Key = addon().getSetting('rapidapi')
    
    url = "https://captchakiller1.p.rapidapi.com/solvev2e"

    querystring = {"site":sUrl,"sitekey":"6LexPvMgAAAAALN68SVJjCdXthMxNSs9Sp6Q4Pdr","gdomain":"false","invisible":"false"}

    headers = {
        "x-rapidapi-key": RapidApi_Key,
        "x-rapidapi-host": "captchakiller1.p.rapidapi.com"
    }

    recaptcha = sSession.get(url, headers=headers, params=querystring).json()
    if 'result' in recaptcha:
        return recaptcha["result"]

    else:
        captcha_data = {
            "siteUrl": sUrl,
            "siteKey": "6LexPvMgAAAAALN68SVJjCdXthMxNSs9Sp6Q4Pdr",
            "captchaType": "captcha"
        }

        try:
            last_gen = int(addons.getSetting(f"{urlHostName(sUrl)}_mcreate"))
        except Exception:
            last_gen = 0

        if not addons.getSetting(f"{urlHostName(sUrl)}_mcaptcha") or last_gen < (time.time() - (5 * 60)):
            server = CaptchaServer(captcha_data)
            server.start_server()
            return addons.getSetting(f"{urlHostName(sUrl)}_mcaptcha")
        else:
            return addons.getSetting(f"{urlHostName(sUrl)}_mcaptcha")
    
def decode_base64(data):
    import json
    header_b64, payload_b64, signature = data.split('.')  
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '==').decode('utf-8'))
        return payload
    except Exception as e:
        return f"Error decoding Base64 string: {e}"

def get_code():
    url = f"{iHost}/v1/codes"

    headers = {
        "Origin": URL_MAIN,
        "Referer": f"{URL_MAIN}/",
        "User-Agent": UA
    }

    data = sSession.post(url, headers=headers).json()
    token = data["code"]["token"]
    datas = decode_base64(token)
    code = datas["code"]["code"]

    return code, token

def opensetting():
    addon().openSettings()