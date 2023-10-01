# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re

from resources.lib.gui.hoster import cHosterGui	
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'awaan'
SITE_NAME = 'Awaan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
 
URL_SERIE = URL_MAIN+'/show/allprograms/30348/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA'

MOVIE_AR = (URL_MAIN+'/movies?page=1', 'showMovies')
SERIE_AR = (URL_MAIN+'/series', 'showSeries')

REPLAYTV_PLAY = (URL_MAIN+'/show/205952/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA-%D8%B2%D9%85%D8%A7%D9%86', 'showEps')
ISLAM_SHOWS = (URL_MAIN+'/programs/30349/إسلاميات', 'showSeries')

ISLAM_QURAN = (URL_MAIN+'/programs/208779/القرآن-الكريم', 'showSeries')
URL_SEARCH = (URL_MAIN+'/search_result?term=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN+'/search_result?term=', 'showMoviesSearch')
URL_SEARCH_SERIES= (URL_MAIN+'/search_result?term=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    addons = addon()

    if (addons.getSetting('hoster_awaan_username') == '') and (addons.getSetting('hoster_awaan_password') == ''):
        oGui = cGui()
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', 'الموقع يطلب حساب لاظهار الروابط'))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:

        oGui = cGui()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', ISLAM_QURAN[0])
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'القرآن الكريم', icons + '/Quran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', ISLAM_SHOWS[0])
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'إسلاميات', icons + '/Quran.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام ', icons + '/Arabic.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)
    
        oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
        oGui.addDir(SITE_IDENTIFIER, 'showEps', 'مسرحيات', icons +'/Theater.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN+'search_result?term='+sSearchText+'&page=1'
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN+'search_result?term='+sSearchText+'&page=1'
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
		
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&page=1'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")

    sPattern = '<li class="show-item filter newcategory">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'               
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
    if not sSearch:
        oGui.setEndOfDirectory()
    
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&page=1'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")

    sPattern = '<div class="item info">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'
              
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]+'?page=1'
            sThumb = aEntry[1]
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
    if not sSearch:
        oGui.setEndOfDirectory()  
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")


    sPattern = '<a class="img-wrappper no_effect" href="([^"]+)".+?data-src="([^"]+)".+?<h3>(.+?)</h3>'                
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sUrl = sUrl.replace("&page=","?page=")
    page = sUrl.split('?page=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?page=')[0]
    siteUrl = siteUrl +'?page='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle,'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
    
    if sPage is False:
        sPage = '1'
    else:
        sPage = sPage
    if '208779' in sUrl:
        sUrl = f'{sUrl}?page={sPage}&category_id=208779'
    elif '30349' in sUrl:
        sUrl = f'{sUrl}?page={sPage}&category_id=30349'
    else:
        sUrl = f'{sUrl}?page={sPage}'


    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")

    sPattern = '<div class="item info">.+?href="([^"]+)".+?data-src="([^"]+)".+?<h3>(.+?)</h3>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            sPage = int(sPage) +1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sPage', sPage)
            oOutputParameterHandler.addParameter('siteUrl', sUrl.split('?')[0])
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]More >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def showEps():
    oGui = cGui()
    addons = addon()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPage = oInputParameterHandler.getValue('sPage')

    aUser = addons.getSetting('hoster_awaan_username')
    aPass = addons.getSetting('hoster_awaan_password')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    if sPage is False:
        sPage = '1'
    else:
        sPage = sPage

    oParser = cParser()

    import requests
    St=requests.Session()

    sPattern =  'var selected_season = ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sSeason = aResult[1][0]

    sPattern =  '_token: ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        _token = aResult[1][0]

        data = {'_token':_token,
                'back_rel':f'{sUrl}',
                'username':aUser,
                'password':aPass}
        url = URL_MAIN+'auth/login'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': URL_MAIN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie':cook}
        r = St.post(url,data=data,headers=headers)
        r = St.get(f'{URL_MAIN}auth/manage-profiles?back_rel={URL_MAIN}')
        sHtmlContent = r.text
        sPattern =  'data-profile-id="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sprofile = aResult[1][0]
        data = {'_token':_token,
                'profile_id':sprofile,
                'back_rel':URL_MAIN}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
        r = St.post(f'{URL_MAIN}auth/select-profile?back_rel={URL_MAIN}', data=data,headers=headers)
        r = St.get(f'{sUrl}?page={sPage}&season={sSeason}')
        sHtmlContent = r.text


    sPattern = '<div class="item info">.+?<a href="([^"]+)".+?data-src="([^"]+)".+?<h3>(.+?)</h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:

            sTitle = aEntry[2].replace("الحلقة "," E").replace("حلقة "," E").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            if sMovieTitle is False:
                sMovieTitle = sTitle
            if ':' in aEntry[2]:
                sTitle = sTitle.split(':')[1]+' '+sMovieTitle
            else:
                sTitle = sTitle+' '+sMovieTitle
            

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            sPage = int(sPage) +1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sPage', sPage)
            oOutputParameterHandler.addParameter('siteUrl', sUrl.split('?')[0])
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]More >>>[/COLOR]', 'next.png', oOutputParameterHandler)


    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('white', ' الموقع لم يرفع حلقات هذا المسلسل'), 'none.png')

    oGui.setEndOfDirectory() 

def __checkForNextPage(sHtmlContent):
    sPattern = '"has_more":(.+?)'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return aResult[1][0]

    sPattern = 'data-page="([^"]+)'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    addons = addon()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    aUser = addons.getSetting('hoster_awaan_username')
    aPass = addons.getSetting('hoster_awaan_password')

    oParser = cParser()

    import requests
    St=requests.Session()

    sPattern =  '<div class="show_bottom_row">.+?<a href="([^"]+)" class="btn watch-now play">'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sLink = aResult[1][0]
    else:
        sLink = sUrl

    sPattern =  '_token: ["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        _token = aResult[1][0]

        data = {'_token':_token,
                'back_rel':f'{sUrl}',
                'username':aUser,
                'password':aPass}
        url = URL_MAIN+'auth/login'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': URL_MAIN,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie':cook}
        r = St.post(url,data=data,headers=headers)
        r = St.get(f'{URL_MAIN}auth/manage-profiles?back_rel={URL_MAIN}')
        sHtmlContent = r.text
        sPattern =  'data-profile-id="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            sprofile = aResult[1][0]
        data = {'_token':_token,
                'profile_id':sprofile,
                'back_rel':URL_MAIN}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
        r = St.post(f'{URL_MAIN}auth/select-profile?back_rel={URL_MAIN}', data=data,headers=headers)
        r = St.get(sLink)
        sHtmlContent = r.text


    oParser = cParser()
            
    sPattern =  'id="iframe-tv".+?data-src="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]: 
            m3url = aEntry
            if m3url.startswith('//'):
                m3url = 'http:' + m3url 	
            if 'player' not in m3url:
                continue
    headers = {'Referer': URL_MAIN}
    r = St.get(m3url, headers=headers)
    sHtmlContent = r.text

    oParser = cParser()
       
    sPattern = 'var source =.+?src: "([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:       
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url

            sTitle = '[COLOR gold] Direct Link رابط مباشر [/COLOR]'

            oOutputParameterHandler.addParameter('siteUrl', url)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, '', oOutputParameterHandler, oInputParameterHandler)


    oGui.setEndOfDirectory()	

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    sHosterUrl = sUrl

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb, oInputParameterHandler=oInputParameterHandler)

    oGui.setEndOfDirectory()