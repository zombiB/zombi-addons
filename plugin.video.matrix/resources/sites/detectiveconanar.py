# -*- coding: utf-8 -*-

import re, requests
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager, VSlog, addon
from resources.lib.parser import cParser
 
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"

SITE_IDENTIFIER = 'detectiveconanar'
SITE_NAME = 'Detectiveconanar'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
ANIM_NEWS = (f'{URL_MAIN}episodes/', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}movies/', 'showMovies')
 
def load():
    addons = addon()
    oGui = cGui()

    if (addons.getSetting('hoster_connan_username') == '') and (addons.getSetting('hoster_connan_password') == ''):
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', 'الموقع يطلب حساب لاظهار الروابط'))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        oOutputParameterHandler = cOutputParameterHandler()   
        oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)
        
        oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)
        
        oGui.setEndOfDirectory()
   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    cook = account_login()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('cookie', cook)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="film-poster">\s*<img data-src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]       
            sDesc = '' 
            siteUrl = aEntry[2]
            sThumb = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('cook', cook)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showSeries(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    cook = account_login()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('cookie', cook)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="film-poster">.+?data-src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[2]
            sThumb = aEntry[0]
            sDesc = ''
            sTitle = aEntry[1].replace('الموسم ','S').replace('الحلقة ','E').replace('للعربية','').replace('مدبلجة','مدبلج').replace('مترجمة','مترجم').replace('عربي','').replace('أنمي','')

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a title="التالي" class="page-link" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    
    else:
        sPattern = '<span class="current">.+?href=(.+?) class='
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return aResult[1][0].replace("'","")

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    cook = account_login()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('cookie', cook)
    oRequestHandler.addHeaderEntry('accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    oRequestHandler.addHeaderEntry('content-type', "application/x-www-form-urlencoded")
    oRequestHandler.addHeaderEntry('user-agent', UA)
    oRequestHandler.addHeaderEntry('referer', f"{URL_MAIN}wp-login.php")
    sHtmlContent = oRequestHandler.request()      

    sPattern = 'data-embed="([^"]+)".+?class="btn">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'Blog' in aEntry[1]:
                continue

            sLink = aEntry[0]
            if sLink.startswith('//'):
               sLink = f'http:{sLink}'
            
            try:
                sQual = re.search(r"\(([^)]+)\)", aEntry[1]).group(1)
            except:
                sQual = aEntry[1]

            sDisplayTitle = f'{sMovieTitle} [{sQual}]'
            sHosterUrl = f'{sLink}|Referer={URL_MAIN}'
            oHoster = cHosterGui().getHoster('jimmy') 
            if oHoster:
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               
    oGui.setEndOfDirectory()

def account_login():
    # tempfix
    return 'wordpress_test_cookie=WP%20Cookie%20check; wordpress_logged_in_e619744f790045bf4afa8104daabef09=MatrixUser%7C1780678987%7CfEG9xgO5kDNVykijFYXCfn3MQ27osuZTyJQ36qPMfCe%7Ce2e16640ab54155a87546f2b5d6738186b1226c5e7124a462467c0cef42dbdab; _lscache_vary=0308e1d837a92b2e6e615784e2c2cbed'
    import time
    addons = addon()
    aUser = addons.getSetting('hoster_connan_username')
    aPass = addons.getSetting('hoster_connan_password')

    try:
        last_gen = int(addons.getSetting('last_connan_cookie_create'))
    except Exception:
        last_gen = 0
    if not addons.getSetting('last_connan_cookie') or last_gen < (time.time() - (1 * 20 * 60 * 60)):

        sess = requests.session()

        url = f"{URL_MAIN}"

        headers = {
            "user-agent": UA,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        }

        response = sess.get(url, headers=headers)

        headers=response.headers

        url = f"{URL_MAIN}wp-login.php"

        response = sess.get(url)

        headers=response.headers

        url = f"{URL_MAIN}wp-login.php"

        payload = {
            "log": "lMatrixUserl@gmail.com",
            "pwd": "Matrix123",
            "wp-submit": "دخول",
            "redirect_to": f"{URL_MAIN}wp-admin/",
            "testcookie": "1"
        }

        response = sess.post(url, data=payload)

        headers=response.headers

        set_cookie_header = headers.get('set-cookie', '')
        cookies = set_cookie_header.split(', ')
        cookie_dict = {}
        for cookie in cookies:
            parts = cookie.split(';')
            if '=' in parts[0]:
                name_value = parts[0].split('=')
                cookie_dict[name_value[0]] = name_value[1]
        cookie_string3 = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])

        url = f"{URL_MAIN}wp-login.php"

        payload = {
            "log": aUser,
            "pwd": aPass,
            "wp-submit": "دخول",
            "redirect_to": f"{URL_MAIN}wp-admin/",
            "testcookie": "1"
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": UA,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "referer": f"{URL_MAIN}wp-login.php",
        }

        response = requests.post(url, data=payload, headers=headers)
        cookies_string = "; ".join(f"{key}={value}" for key, value in response.cookies.items())
        merged_cookies_string = f"{cookies_string}; {cookie_string3}"

        addons.setSetting('last_connan_cookie', merged_cookies_string)
        addons.setSetting('last_connan_cookie_create', str(int(time.time())))

        return merged_cookies_string
    else:
        return addons.getSetting('last_connan_cookie')

def opensetting():
    addon().openSettings()