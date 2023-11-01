# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
import base64
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'witanime'
SITE_NAME = 'WitAnime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_MOVIES = (URL_MAIN + '/anime-type/movie/', 'showMovies')
ANIM_NEWS = (URL_MAIN+'/episode/' , 'showSeries')
ANIM_LIST = (True, 'showAnimesList')

URL_SEARCH = (URL_MAIN + '/?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + '/?search_param=animes&s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/anime-status/%d9%8a%d8%b9%d8%b1%d8%b6-%d8%a7%d9%84%d8%a7%d9%86/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'يعرض الان', icons + '/Anime.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/anime-season/%D8%B4%D8%AA%D8%A7%D8%A1-2023/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أنميات الموسم', icons + '/Anime.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'قائمة الأنمي', icons + '/All.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesList():
    oGui = cGui()

    liste = []
    liste.append( ['#', URL_MAIN + '/en-anime-letter/228'] )
    liste.append( ['أ', URL_MAIN + '/ar-anime-letter/أ'] )
    liste.append( ['ب', URL_MAIN + '/ar-anime-letter/ب'] )
    liste.append( ['ت', URL_MAIN + '/ar-anime-letter/ت'] )
    liste.append( ['ث', URL_MAIN + '/ar-anime-letter/ث'] )
    liste.append( ['ج', URL_MAIN + '/ar-anime-letter/ج'] )
    liste.append( ['د', URL_MAIN + '/ar-anime-letter/د'] )
    liste.append( ['ر', URL_MAIN + '/ar-anime-letter/ر'] )
    liste.append( ['ز', URL_MAIN + '/ar-anime-letter/ز'] )
    liste.append( ['س', URL_MAIN + '/ar-anime-letter/س'] )
    liste.append( ['ش', URL_MAIN + '/ar-anime-letter/ش'] )
    liste.append( ['ط', URL_MAIN + '/ar-anime-letter/ط'] )
    liste.append( ['غ', URL_MAIN + '/ar-anime-letter/غ'] )
    liste.append( ['ف', URL_MAIN + '/ar-anime-letter/ف'] )
    liste.append( ['ك', URL_MAIN + '/ar-anime-letter/ك'] )
    liste.append( ['ل', URL_MAIN + '/ar-anime-letter/ل'] )
    liste.append( ['م', URL_MAIN + '/ar-anime-letter/م'] )
    liste.append( ['ن', URL_MAIN + '/ar-anime-letter/ن'] )
    liste.append( ['هـ', URL_MAIN + '/ar-anime-letter/ه'] )
    liste.append( ['و', URL_MAIN + '/ar-anime-letter/و'] )
    liste.append( ['ي', URL_MAIN + '/ar-anime-letter/ي'] )
    liste.append( ['A', URL_MAIN + '/en-anime-letter/A'] )
    liste.append( ['B', URL_MAIN + '/en-anime-letter/B'] )
    liste.append( ['C', URL_MAIN + '/en-anime-letter/C'] )
    liste.append( ['D', URL_MAIN + '/en-anime-letter/D'] )
    liste.append( ['E', URL_MAIN + '/en-anime-letter/E'] )
    liste.append( ['F', URL_MAIN + '/en-anime-letter/F'] )
    liste.append( ['G', URL_MAIN + '/en-anime-letter/G'] )
    liste.append( ['H', URL_MAIN + '/en-anime-letter/H'] )
    liste.append( ['I', URL_MAIN + '/en-anime-letter/I'] )
    liste.append( ['J', URL_MAIN + '/en-anime-letter/J'] )
    liste.append( ['K', URL_MAIN + '/en-anime-letter/K'] )
    liste.append( ['L', URL_MAIN + '/en-anime-letter/L'] )
    liste.append( ['M', URL_MAIN + '/en-anime-letter/M'] )
    liste.append( ['N', URL_MAIN + '/en-anime-letter/N'] )
    liste.append( ['O', URL_MAIN + '/en-anime-letter/O'] )
    liste.append( ['P', URL_MAIN + '/en-anime-letter/P'] )
    liste.append( ['Q', URL_MAIN + '/en-anime-letter/Q'] )
    liste.append( ['R', URL_MAIN + '/en-anime-letter/R'] )
    liste.append( ['S', URL_MAIN + '/en-anime-letter/S'] )
    liste.append( ['T', URL_MAIN + '/en-anime-letter/T'] )
    liste.append( ['U', URL_MAIN + '/en-anime-letter/U'] )
    liste.append( ['V', URL_MAIN + '/en-anime-letter/V'] )
    liste.append( ['W', URL_MAIN + '/en-anime-letter/W'] )
    liste.append( ['X', URL_MAIN + '/en-anime-letter/X'] )
    liste.append( ['Y', URL_MAIN + '/en-anime-letter/Y'] )
    liste.append( ['Z', URL_MAIN + '/en-anime-letter/Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Letter [COLOR coral]' + sTitle + '[/COLOR]', icons + '/All.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?search_param=animes&s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?data-content="([^<]+)".+?<h3><a href="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("بلوراي","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[3]
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="img-responsive" src="([^"]+)" alt="([^"]+)".+?data-content="([^"]+)".+?redirectTo.+?["\']([^"\']+)["\']'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = base64.b64decode(aEntry[3]).decode('utf8',errors='ignore')
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[0])  
            sDesc = aEntry[2]
            sYear = ''
            sTitle = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sTitle = sTitle.replace("Season ","S")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def ShowEps():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    oParser = cParser()

    sStart = '<div class="episodes-list-content">'
    sEnd = '<div class="space"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<h3><a href=.+?onclick="(.+?)">([^<]+)</a></h3>.+?src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace("الحلقة ","").replace("الفلم ","").replace("الخاصة ","")
            sTitle = " E"+sEp
            sTitle = sMovieTitle+sTitle
            EnCodedUrl = aEntry[0].replace("openEpisode('","").replace("')","")
            siteUrl = base64.b64decode(EnCodedUrl).decode('utf8',errors='ignore')
            sDesc = ''
            sYear = ''
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
       
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
      # (.+?) ([^<]+) .+?

    sPattern = 'data-url="([^<]+)" onclick='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in reversed(aResult[1]):

            url = base64.b64decode(aEntry).decode('utf8',errors='ignore')
            VSlog(url)
            sTitle = aEntry
            if url.startswith('//'):
               url = 'http:' + url
            if 'yona' in url:
                    oRequestHandler = cRequestHandler(url)
                    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
                    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                    sData = oRequestHandler.request()
                    sPattern = 'go_to_player(.+?)".+?<p>([^<]+)'
                    oParser = cParser()
                    aResult = oParser.parse(sData, sPattern)
                    
                    if aResult[0]:
                       for aEntry in reversed(aResult[1]):  
                            if 'mega' in aEntry[0]:
                               continue      
                            url = aEntry[0].replace(')','').replace('(','').replace("'","").replace('"','')
                            sQual = aEntry[1].replace('-','').replace(' ','')

                            sHosterUrl = url
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = ('[COLOR coral] Yonaplay (%s)[/COLOR]') % (sQual)
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)                 

            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = ('[COLOR coral](%s)[/COLOR]') % (sTitle)
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = 'data-url="([^<]+)" target='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] :       
        for aEntry in reversed(aResult[1]):
            sQual = aEntry[0].replace("الخارقة ","").replace(" العالية","").replace("المتوسطة","").replace("الجودة","").replace('-','').replace(' ','')
            sHtmlContent1 = aEntry[1]

            sPattern = 'href="([^"]+)'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent1, sPattern)
		
            if aResult[0] :
                for aEntry in aResult[1]:            
                    url = base64.b64decode(aEntry).decode('utf8',errors='ignore')
                    sTitle = " "
                    if url.startswith('//'):
                        url = 'http:' + url		         
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = ('[COLOR coral](%s)[/COLOR]') % (sQual)
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)	
	       
    oGui.setEndOfDirectory()