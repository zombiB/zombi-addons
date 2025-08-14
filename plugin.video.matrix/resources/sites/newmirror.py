# -*- coding: utf-8 -*-

import re, requests, base64
import xbmcgui
import six
import time
import json
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, siteManager, addon, dialog

UA = "Mozilla/5.0 (Linux; Android 11; Mi 5s Build/RQ3A.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.200 Mobile Safari/537.36 /OS.Gatu v3.0"
addons = addon()

SITE_IDENTIFIER = 'newmirror'
SITE_NAME = 'NewMirror'
SITE_DESC = 'multi audio vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_MAIN = base64.b64decode(URL_MAIN).decode("utf-8")[::-1]
IMG_MAIN = base64.b64decode('cG90Lm5kY3JvcnJpbWZuLmdtaQ==').decode("utf-8")[::-1]
VRF_MAIN = base64.b64decode('cHBhLnJvcnJpbXRlbi55ZmlyZXZyZXN1').decode("utf-8")[::-1]

MOVIE_EN = (f'{URL_MAIN}movies?app=1', 'showPack')
MOVIE_NETFLIX = (f'{URL_MAIN}movies?app=1', 'showPack')
SERIE_EN = (f'{URL_MAIN}series?app=1', 'showSeriesPack')

URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'أفلام نتفلكس', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesPack', 'مسلسلات أجنبية', '1/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def set_setting(id, value):
    if not isinstance(value, six.string_types):
        value = str(value)
    addons.setSetting(id, value)

def fetch_html_content(sUrl, ott='nf'):
    def bypass(main_url):
        oRequestHandler = cRequestHandler(f"{URL_MAIN}home")
        response = oRequestHandler.request()

        match2 = re.search(r'data-time="([^"]+)"', response)
        if match2:
            time_data = match2.group(1)
        else:
            VSlog("addhash not found")

        #pattern = r"(?<!//)window\.open\('([^\,]+)\""
        #match = re.search(pattern, response.text)
        #if match:
        #    verify_url = match.group(1)
        #    verify_url = verify_url.replace('+','').replace(' ','').replace('addhash2',addhash).replace('"','').replace("'","")

        match = re.search(r'data-addhash="([^"]+)"', response)
        if match:
            addhash = match.group(1)

            # url = f"https://raw.githubusercontent.com/SaurabhKaperwan/Utils/refs/heads/main/urls.json"
            # response = requests.get(f'{url}').json()
            # verify_url = response["nfverifyurl"].replace("###", addhash)

        #hash_digits = "".join(char for char in addhash if char.isdigit())
        #first_16_digits = hash_digits[:16]  
        #verify_url = (f"{verify_url}0.{first_16_digits}")

            #requests.get(f"{verify_url}&t={time_data}")
        
        verify_check = ""
        timeout = 60
        
        if 'search.php' in sUrl:
            dialog().VSinfo(f' الموقع يطلب الانتظار جرب الدخول على احد اقسام موق NewMirror اولا...')
            return ''

        dialog().VSinfo(f'الموقع يطلب الانتظار ...')

        start_time = time.time()
        while '"r":"n"' not in verify_check:
            if time.time() - start_time > timeout:
                break
            time.sleep(2)

            oRequestHandler = cRequestHandler(f"{main_url}tv/p.php")
            oRequestHandler.setRequestType(1)
            verify_check = oRequestHandler.request()
            
            VSlog(f"Verification Check: {verify_check}")
            sCook = oRequestHandler.GetCookies()

            parts = sCook.split(';t_hash_t=')
            if len(parts) < 2:
                raise Exception("Expected cookie t_hash_t not found")
            t_hash_t = parts[1].split(';')[0]

        set_setting('t_hash_t', t_hash_t)
        set_setting('t_hash_t_create', str(int(time.time())))
        
        return t_hash_t

    try:
        last_gen = int(addons.getSetting('t_hash_t_create'))
    except Exception:
        last_gen = 0

    if not addons.getSetting('t_hash_t') or last_gen < (time.time() - (1 * 15 * 60 * 60)):
        t_hash_t = bypass(URL_MAIN.replace('mobile/',''))
    else:
        t_hash_t = addons.getSetting('t_hash_t')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'app.netmirror.netmirrornew')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Cookie', f"t_hash_t={t_hash_t}; ott={ott}; hd=on")
    sHtmlContent = oRequestHandler.request()
    return sHtmlContent

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search.php?s={sSearchText}'
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    oOutputParameterHandler = cOutputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Netflix Section', 'neflix.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}home?app=1' + '?ott=dp')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Disney Section', '1/Movies.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', sUrl + '?ott=pv')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'PrimeVideo Section', '1/Movies.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showSeriesPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', oInputParameterHandler.getValue('siteUrl'))
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Netflix Section', 'neflix.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}home?app=1' + '?ott=dp')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Disney Section', '1/Movies.png', oOutputParameterHandler)
    oOutputParameterHandler.addParameter('siteUrl', oInputParameterHandler.getValue('siteUrl') + '?ott=pv')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'PrimeVideo Section', '1/Movies.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        oOutputParameterHandler = cOutputParameterHandler()
        for ott in ['hs', '', 'pv']:
            sUrl = sSearch.replace('/search.php', f'/{ott}/search.php')
            data = fetch_html_content(sUrl, ott)
            data = json.loads(data)
            if 'searchResult' in data and data['searchResult']:
                for key in data['searchResult']:
                    if '/hs/' in sUrl or '/pv/' in sUrl:
                        siteUrl = f"{URL_MAIN}{ott}/playlist.php?id={key['id']}".replace('/dp/','/hs/')
                    else:
                        siteUrl = f"{URL_MAIN}playlist.php?id={key['id']}"
                    sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
                    if ott == 'pv':
                        sThumb = f"https://{IMG_MAIN}/pv/480/{key['id']}.jpg"
                    if ott == 'hs':
                        sThumb = f"https://{IMG_MAIN}/hs/v/166/{key['id']}.jpg"    
                    sTitle = key['t']
                    sDesc = ''
                    sCode = key['id']

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oInputParameterHandler = cInputParameterHandler()
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if '?ott=' in sUrl:
            sUrl2 = sUrl.split('?ott=')[0]
            ott = sUrl.split('?ott=')[1]
            sHtmlContent = fetch_html_content(sUrl2, ott)
        else:
            sHtmlContent = fetch_html_content(sUrl)

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                if 'serie' in sCat.lower():
                    continue
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().select("Select Category", listitems)
        if index != -1:
            selected_category = listitems[index]

        oParser = cParser()
        sStart = f'>{selected_category}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&tm={sTime}'
                sThumb = aEntry[1]
                if '?ott=' in sUrl:
                    sMovie = f'{URL_MAIN}{ott}/post.php?id={aEntry[0]}'.replace('/dp/','/hs/')
                else:
                    sMovie = f'{URL_MAIN}post.php?id={aEntry[0]}'
                data = fetch_html_content(sMovie)
                data = json.loads(data)
                if data['type'] == 't':
                    continue
                sTitle = data['title']
                siteUrl = f'{URL_MAIN}playlist.php?id={aEntry[0]}&t={sTitle}&tm={sTime}'
                sDesc = ''
                sCode = aEntry[0]
                if '?ott=' in sUrl:
                    siteUrl = siteUrl.replace('/playlist.php',f'/{ott}/playlist.php').replace('/dp/','/hs/')

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oOutputParameterHandler.addParameter('sType', 'Movie')

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        oOutputParameterHandler = cOutputParameterHandler()
        for ott in ['hs', '', 'pv']:
            sUrl = sSearch.replace('/search.php', f'/{ott}/search.php')
            data = fetch_html_content(sUrl, ott)
            data = json.loads(data)
            if 'searchResult' in data and data['searchResult']:
                for key in data['searchResult']:
                    if '/hs/' in sUrl or '/pv/' in sUrl:
                        siteUrl = f"{URL_MAIN}{ott}/post.php?id={key['id']}".replace('/dp/','/hs/')
                    else:
                        siteUrl = f"{URL_MAIN}post.php?id={key['id']}"
                    sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
                    if ott == 'pv':
                        sThumb = f"https://{IMG_MAIN}/pv/480/{key['id']}.jpg"
                    if ott == 'hs':
                        sThumb = f"https://{IMG_MAIN}/hs/v/166/{key['id']}.jpg"    
                    sTitle = key['t']
                    sDesc = ''
                    sCode = key['id']

                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sCode', sCode)
                    oOutputParameterHandler.addParameter('ott', ott)
                    if ott == '':
                        oOutputParameterHandler.addParameter('ott', 'nf')
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
      
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if '?ott=' in sUrl:
            sUrl2 = sUrl.split('?ott=')[0]
            ott = sUrl.split('?ott=')[1]
            sHtmlContent = fetch_html_content(sUrl2, ott)
        else:
            ott = 'nf'
            sHtmlContent = fetch_html_content(sUrl)

        sPattern =  'data-time="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sTime = aResult[1][0] 

        listitems =[]
        sPattern =  'class="tray-link">(.+?)</a>' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sCat = aEntry
                if 'movie' in sCat.lower():
                    continue
                listitems.append(sCat)
      
        index = xbmcgui.Dialog().select("Select Category", listitems)
        if index != -1:
            selected_category = listitems[index]

        oParser = cParser()
        sStart = f'>{selected_category}</a>'
        sEnd = '<div class="tray-container">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = 'data-post="([^"]+)".+?data-src="([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent1, sPattern)	
        if aResult[0] :
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                sThumb = aEntry[1]
                if '?ott=' in sUrl:
                    siteUrl = f'{URL_MAIN}{ott}/post.php?id={aEntry[0]}'.replace('/dp/','/hs/')
                else:
                    siteUrl = f'{URL_MAIN}post.php?id={aEntry[0]}'
                data = fetch_html_content(siteUrl)
                data = json.loads(data)
                if data['type'] == 'm':
                    continue
                sTitle = data['title']
                sDesc = ''
                sCode = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sCode', sCode)
                oOutputParameterHandler.addParameter('sTime', sTime)
                oOutputParameterHandler.addParameter('ott', ott)
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()  

def showSeasons():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCode = oInputParameterHandler.getValue('sCode')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTime = oInputParameterHandler.getValue('sTime')
    ott = oInputParameterHandler.getValue('ott')
    
    data = fetch_html_content(sUrl)
    data = json.loads(data)
    if 'season' in data and data['season']:
        for key in data['season']:
            sSeason = ' S'+ key['s']
            if ott == 'nf':
                siteUrl = f"{URL_MAIN}episodes.php?s={key['id']}&series={sCode}"
                sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
            else:
                siteUrl = f"{URL_MAIN}{ott}/episodes.php?s={key['id']}&series={sCode}".replace('/dp/','/hs/')
                if ott == 'pv':
                    sThumb = f"https://{IMG_MAIN}/pv/480/{key['id']}.jpg"
                if ott == 'dp':
                    sThumb = f"https://{IMG_MAIN}/hs/v/166/{key['id']}.jpg"            
            sTitle = data['title']
            sTitle = sTitle + sSeason
            sDesc = data['desc']
                
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sCode', sCode)
            oOutputParameterHandler.addParameter('sTime', sTime)
            oOutputParameterHandler.addParameter('ott', ott)

            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR orange]تعذر الحصول على موسم - جرب البحث في الأفلام[/COLOR]')

    oGui.setEndOfDirectory() 
        
def showEpisodes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sCode = oInputParameterHandler.getValue('sCode')
    sTime = oInputParameterHandler.getValue('sTime')
    ott = oInputParameterHandler.getValue('ott')

    data = fetch_html_content(sUrl)
    data = json.loads(data)
    for key in data['episodes']:
        sEpisode = key['ep']
        if ott == 'nf':
            siteUrl = f'{URL_MAIN}playlist.php?id={key["id"]}&tm={sTime}'
            sThumb = f"https://{IMG_MAIN}/poster/v/{key['id']}.jpg"
        else:
            siteUrl = f'{URL_MAIN}{ott}/playlist.php?id={key["id"]}&tm={sTime}'.replace('/dp/','/hs/')
            if ott == 'pv':
                sThumb = f"https://{IMG_MAIN}/pvepimg/150/{key['id']}.jpg"
            if ott == 'dp':
                sThumb = f"https://{IMG_MAIN}/hsepimg/{key['id']}.jpg"
        sTitle = sMovieTitle + sEpisode
        sDesc = sDesc

        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sType', 'Serie')

        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    sPage = int(data['nextPageShow'])
    if sPage > 0: 
            if ott == 'nf':
                siteUrl = f'{URL_MAIN}episodes.php?s={data["nextPageSeason"]}&series={sCode}&page={data["nextPage"]}'
            else:
                siteUrl = f'{URL_MAIN}{ott}/episodes.php?s={data["nextPageSeason"]}&series={sCode}&page={data["nextPage"]}'.replace('/dp/','/hs/')
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('ott', ott)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
 
def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCode = oInputParameterHandler.getValue('sCode')
    sType = oInputParameterHandler.getValue('sType')

    sSub = False
    data = fetch_html_content(sUrl)
    data = json.loads(data)
    for key in data:
        if sType == 'Movie':
            if '/pv/' in sUrl:
                sMovie = f'{URL_MAIN}/pv/post.php?id={sCode}'  
            elif '/hs/' in sUrl:
                sMovie = f'{URL_MAIN}/hs/post.php?id={sCode}'  
            else: 
                sMovie = f'{URL_MAIN}post.php?id={sCode}'

            data = fetch_html_content(sMovie)
            data = json.loads(data)

            sMovieTitle = data['title']
        try:
            for data in key['tracks']:
                if data['kind'] == 'thumbnails':
                    continue

                if data["label"] == "ar":
                    sSub = 'https:' + data["file"]
                elif data["label"] == "en":
                    sSub = 'https:' + data["file"]
        except:
            VSlog('no subs')

        for data in key['sources']:
            sQual = data['label']
            if 'Full' in sQual:
                sQual = '1080p'
            if 'Mid' in sQual:
                sQual = '720p Default'
            if 'Low' in sQual:
                sQual = '480p'

            sUrl = f'{URL_MAIN[:-1]}{data["file"]}'
            sThumb = ''
            sTitle = ('%s  [COLOR coral](%s)[/COLOR]') % (sMovieTitle, sQual)  

            sHosterUrl = f'{sUrl.replace("mobile/mobile/","mobile/")}|Referer={URL_MAIN}&cookie={addons.getSetting("t_hash_t")};hd=on'
            if sSub:
                sHosterUrl += f'?sub.info={sSub}'
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def identify_streaming_platform(content_id):
    if content_id.isdigit(): 
        if len(content_id) == 10:
            return "dp"
        elif len(content_id) in [6, 8]:  
            return "nf"
    elif len(content_id) == 26 and not content_id.isdigit():
        return "pv"

    return "nf"