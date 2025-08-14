# -*- coding: utf-8 -*-

import urllib.parse
import base64, json
import re, requests, time
import datetime
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.parser import cParser
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager
from resources.lib.util import urlHostName

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"

SITE_IDENTIFIER = 'koralive'
SITE_NAME = 'Koralive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

sHost = base64.b64decode('L21vYy5vaWVzYWJlcmlmLmJkdHItdGx1YWZlZC00MjAyLWViaXZlbGV0Ly86c3B0dGg=')
dHost = sHost.decode("utf-8")

URL_MAIN = dHost[::-1]

SPORT_LIVE = (f'{URL_MAIN}.json', 'showMatches')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showChannels', 'بث مباشر', 'foot.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', '')
    oGui.addDir(SITE_IDENTIFIER, 'showMatches', 'بث المباريات', 'foot.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
	
def showChannels():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('content-type', "application/json")
    oRequestHandler.addHeaderEntry('User-Agent', "Firebase/5/19.3.1/30/Android")
    oRequestHandler.enableCache(False)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    channels = sHtmlContent["channel"]
    oOutputParameterHandler = cOutputParameterHandler() 
    for key, value in channels.items():
        sTitle = value["channelName"]
        sThumb = value["tvgLogo"]
        siteUrl = value["url"]
        sDesc = ''
        
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, 'foot.png', sThumb, sDesc, oOutputParameterHandler)
         
    oGui.setEndOfDirectory()

def showMatches():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showChannels', 'قنوات مباشرة', 'foot.png', oOutputParameterHandler)
    oGui.addDir(SITE_IDENTIFIER, 'showMatches2', 'مباريات مباشرة اخرى', 'foot.png', oOutputParameterHandler)

    sHost = base64.b64decode('L3p5eC5uZGNtdWltZXJwaXBhLmlwYS8vOnNwdHRo')
    dHost = sHost.decode("utf-8")
    sUrl = dHost[::-1]
    import urllib.parse
    parsed_url = urllib.parse.urlparse(sUrl)
    sHost = parsed_url.netloc

    try:
        headers = {
            "user-agent": "Dart/3.3 (dart:io)",
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "host": sHost
        }

        sHtmlContent = requests.get(f'{sUrl}api/105/all', headers=headers).json()

        for channel in sHtmlContent["List"]:
            oOutputParameterHandler = cOutputParameterHandler() 

            mStatus = channel["live"]
            siteUrl = f'{sUrl}api1/{channel["matchId"]}'
            sTitle = f'{channel["name1"]} vs {channel["name2"]}'
            if str(mStatus) == 'True':
                sTitle = f'{sTitle} [COLOR red]● مباشر[/COLOR]'
            sThumb = channel["image1"]       
            sDesc = f'[COLOR orange]وقت المباراة[/COLOR] \n {channel["start_time"]}(+2) \n \n [COLOR orange]الدوري[/COLOR] \n {channel["ligue"]} \n \n [COLOR orange]حالة البث[/COLOR] \n {str(channel["finished"]).replace("False", "Live on Time").replace("True", "Ended")}'
            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showLinks2', sTitle, 'foot.png', sThumb, sDesc, oOutputParameterHandler)
    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange] تعذر الاتصال بالموقع [/COLOR]', 'none.png')

    oGui.setEndOfDirectory()

def showMatches2():
    oGui = cGui()

    sUrl = 'https://yalla-shoot-tv.one/'

    try:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        pattern = re.compile(r'<div class="match-container.+?href="([^"]+)".+?<div class="right-team">.+?src="([^"]+)" title="([^"]+)".+?<div class="match-timing">.+?>(.+?)</div>.+?<div class="left-team">.+?src="([^"]+)" title="([^"]+)".+?<div class="match-info">\s*<ul>\s*<li><span>(.+?)</span></li>\s*<li><span>(.+?)</span></li>\s*<li><span>(.+?)</span></li>', re.DOTALL)
        match = pattern.findall(sHtmlContent)
        if match:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in match:

                sTitle =  f'{aEntry[2]} ضد {aEntry[5]}'
                sThumb = aEntry[1]
                siteUrl = aEntry[0]
                sDesc = f'[COLOR orange]الدوري[/COLOR] \n {aEntry[8]} \n \n [COLOR orange]حالة البث[/COLOR] \n {aEntry[3]}'
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addMisc(SITE_IDENTIFIER, 'showLinks3', sTitle, 'foot.png', sThumb, sDesc, oOutputParameterHandler)
        else:
            from datetime import date

            dDate = date.today().isoformat()

            pattern = re.compile(r'API_URL_MATCHES\s*=\s*"([^"]+)"', re.DOTALL)
            match = pattern.findall(sHtmlContent)
            if match:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in match:
                    API_URL_MATCHES = aEntry

                    now = datetime.datetime.now()
                    gmt_offset = datetime.timedelta(hours=3)
                    gmt_time = now - gmt_offset
                    time_str = gmt_time.strftime("%H%M")
                    sUrl = f'{API_URL_MATCHES}{dDate}?t={time_str}'

                    oRequestHandler = cRequestHandler(sUrl)
                    oRequestHandler.enableCache(False)
                    sHtmlContent2 = oRequestHandler.request(jsonDecode=True)

                    for match in sHtmlContent2:
                        if match['active'] == '0':
                            continue
                        pattern = re.compile(r'MAIN_URL\s*=\s*["\']([^"\']+)["\'];', re.DOTALL)
                        aResult = pattern.findall(sHtmlContent)
                        if aResult:
                            oOutputParameterHandler = cOutputParameterHandler()
                            for aEntry in aResult:
                                MAIN_URL = aEntry
                        sCondition = 'لم تبدأ'
                        sTitle =  f"{match['home']} vs {match['away']}"
                        sThumb = f'https://kora-api.top/uploads/team/{match["home_logo"]}'
                        siteUrl = "/"
                        desc = f"{match['home_en']}-vs-{match['away_en']}".lower().replace(" ", "-")
                        if match["has_channels"] == '1' and match["active"] == '1':
                            sCondition = 'مباشر'
                            siteUrl = f"{MAIN_URL}live/{match['id']}/{match['api_matche_id']}/{desc}/"
                        sDesc = f'[COLOR orange]الدوري[/COLOR] \n {match["league"]} \n \n [COLOR orange]الوقت[/COLOR] \n {match["date"]} | {match["time"]}GMT \n \n [COLOR orange]حالة البث[/COLOR] \n {sCondition}'
                        
                        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addMisc(SITE_IDENTIFIER, 'showLinks3', sTitle, 'foot.png', sThumb, sDesc, oOutputParameterHandler)

    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange] تعذر الاتصال بالموقع [/COLOR]', 'none.png')

    oGui.setEndOfDirectory()

def showLinks3():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    try:
        if sUrl.startswith('/'):
            oGui.addText(SITE_IDENTIFIER, '[COLOR orange] تعذر الحصول على روابط [/COLOR]', 'none.png')  
        else:
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()
            
            result = extract_data(sHtmlContent)
            if result:
                if 'channels/' in result["cLinks"][0]:
                    oOutputParameterHandler = cOutputParameterHandler()
                    for link in result["cLinks"]:
                        oRequestHandler = cRequestHandler(link)
                        oRequestHandler.enableCache(False)
                        sHtmlContent = oRequestHandler.request()

                        linkMatch = re.findall(r'source:\s*"([^"]+)"', sHtmlContent)
                        sHosterUrl = linkMatch[0]

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
                else:
                    u_key = result["u_key"][0]
                    #kt = result["kt"][0]
                    #k_url = result["k_url"][0]
                    p = result["p"][0]

                    for ch, server_name, sLink in zip(result['ch'], result['server_name'], result["cLinks"]):

                        oOutputParameterHandler = cOutputParameterHandler()
                        sTitle = f'{sMovieTitle} [COLOR orange] {server_name} [/COLOR]'

                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                        oOutputParameterHandler.addParameter('u_key', u_key)
                        oOutputParameterHandler.addParameter('sLink', sLink)
                        #oOutputParameterHandler.addParameter('kt', kt)
                        #oOutputParameterHandler.addParameter('k_url', k_url)
                        oOutputParameterHandler.addParameter('p', p)
                        oOutputParameterHandler.addParameter('ch', ch)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                        oGui.addMisc(SITE_IDENTIFIER, 'showLinks4', sTitle, 'foot.png', sThumb, sTitle, oOutputParameterHandler)
    except:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange] تعذر الحصول على روابط [/COLOR]', 'none.png')        

    oGui.setEndOfDirectory()  

def showLinks4():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    u_key = oInputParameterHandler.getValue('u_key')
    kt = oInputParameterHandler.getValue('kt')
    k_url = oInputParameterHandler.getValue('k_url')
    p = oInputParameterHandler.getValue('p')
    ch = oInputParameterHandler.getValue('ch')
    sLink = oInputParameterHandler.getValue('sLink')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #querystring = { "kt": kt }

    #kurl = decode_token(k_url)
    #payload = { "kt": encode_token(nowtime()) }
    #headers = {
    #    "user-agent": UA,
    #    "referer": kurl.split('key')[0]
    #}

    #response = requests.post(kurl, json=payload, headers=headers, params=querystring).json()
    #token = response["key"]
    oOutputParameterHandler = cOutputParameterHandler()
    if ch:
        url = decode_token(u_key)

        querystring = {
            "ch": ch,
            "p": p,
            "token": generate_uuid(),
            "kt": kt
        }

        headers = {
            "user-agent": UA,
            "referer": sUrl
        }

        response = requests.get(url, headers=headers, params=querystring).text
        token_pattern = r'var token = "(.*)";'

        token_match = re.search(token_pattern, response)
        if token_match:
            sHosterUrl = token_match.group(1)

            sHosterUrl = f'{decode_token(sHosterUrl)}|Referer={url.split("frame.php")[0]}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)
    else:
        oParser = cParser() 
        sHosterUrl = sLink
        if 'https://href.li/?' in sHosterUrl:
            nUrl = sHosterUrl.split('https://href.li/?', 1)[1] if sHosterUrl.split('https://href.li/?', 1)[1].startswith('http') else sHosterUrl
            oRequestHandler = cRequestHandler(nUrl)
            oRequestHandler.enableCache(False)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe src="([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)	
            if aResult[0]:
                for aEntry in aResult[1]:
                    sHosterUrl = aEntry
                    if sHosterUrl.startswith('//'):
                        sHosterUrl = f'http:{sHosterUrl}|Referer={nUrl}'

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()    

def showLinks2():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.enableCache(False)
    oRequestHandler.addHeaderEntry('content-type', "application/json")
    oRequestHandler.addHeaderEntry('User-Agent', "Dart/3.3 (dart:io)")
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    for item in sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        if '{"' in item["link"]:
            data = json.loads(item["link"])
            for key, value in data.items():
                sHosterUrl = f'{value}|{item["header1"]}={item["header"]}'
                sDisplayTitle = f'{sMovieTitle} ({key})'

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sHosterUrl = sHosterUrl 
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

        else:
            sHosterUrl = f'{item["link"]}|{item["header1"]}={item["header"]}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sHosterUrl = sHosterUrl 
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oOutputParameterHandler)

    oGui.setEndOfDirectory()    

def showLinks():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
   
    sHosterUrl = f'{sUrl}|User-Agent=Android-App@2024'

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sMovieTitle)
    sUrl = sUrl.replace(' ', '%20')
    oGuiElement.setMediaUrl(sHosterUrl)
    oGuiElement.setThumbnail(sThumb)
    oGuiElement.setDescription('')

    from resources.lib.player import cPlayer
    oPlayer = cPlayer()
    oPlayer.clearPlayList()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()

    return False, False

def decode_token(token):
    decoded_bytes = base64.urlsafe_b64decode(token)
    decoded_str = decoded_bytes.decode('latin-1')
    replaced_str = ''.join(f'%{decoded_str[i:i+2]}' for i in range(0, len(decoded_str), 2))
    final_str = urllib.parse.unquote(replaced_str)
    
    return final_str

def encode_token(data):
    encoded_str = urllib.parse.quote(str(data))
    replaced_str = ''.join(f'%{ord(char):02X}' for char in encoded_str)
    base64_bytes = base64.urlsafe_b64encode(replaced_str.replace('%', '').encode('latin-1'))
    base64_str = base64_bytes.decode('utf-8')
    
    return base64_str

def nowtime():
    current_timestamp = int(time.time())
    return current_timestamp

def get_current_minute():
    date = datetime.datetime.utcnow()
    hours = str(date.hour).zfill(2)
    minutes = str(date.minute).zfill(2)

    time = f"{hours}{minutes}"
    return time

def extract_data(html):
    data = {}

    data['u_key'] = re.findall(r'var u_key = "([^"]+)";', html)
    #data['kt'] = re.findall(r'"kt": "([^"]+)"', html)
    #data['k_url'] = re.findall(r'var k_url = "([^"]+)";', html)
    data['p'] = [int(x) for x in re.findall(r'var p = (\d+)', html)]

    apiMatch = re.findall(r'var api_matche = "([^"]+)"', html)
    sUrl = apiMatch[0]
    oRequestHandler = cRequestHandler(f'{sUrl}?t={get_current_minute()}')
    oRequestHandler.enableCache(False)
    oRequestHandler.addHeaderEntry('Host', urlHostName(sUrl))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    channels = sHtmlContent.get("channels", [])
    ch = []
    server = []
    cLinks = []
    for channel in channels:
        ch.append(channel.get("ch"))
        server.append(channel.get("server_name"))
        cLinks.append(channel.get("link"))
    data['ch'] = ch
    data['server_name'] = server
    data['cLinks'] = cLinks

    if not any(data.values()):
        return None

    return data

def decode_token(encoded_token):
    decoded_token = urllib.parse.unquote(base64.b64decode(encoded_token).decode('utf-8'))
    decoded_token = re.sub(r'(.{1,2})', r'%\1', decoded_token)
    return urllib.parse.unquote(decoded_token)

def generate_uuid():
    import random
    timestamp = int(time.time() * 1000)
    template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'

    def replace(match):
        nonlocal timestamp
        random_number = int((timestamp + random.random() * 16) % 16)
        timestamp //= 16
        return hex(random_number if match.group(0) == 'x' else (random_number & 0x3) | 0x8)[2:]

    uuid = re.sub(r'[xy]', replace, template)
    return uuid