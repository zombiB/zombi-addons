# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.util import Quote
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.Styling import getGenreIcon
from bs4 import BeautifulSoup

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'aflamtop'
SITE_NAME = 'Aflamtop'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/tag/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showMovies')
MOVIE_CLASSIC = (URL_MAIN + '/tag/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%a8%d9%8a%d8%b6-%d9%88%d8%a7%d8%b3%d9%88%d8%af/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a7%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_YEARS = (True, 'showYears')
MOVIE_QUALITY = (True, 'showQuality')

DOC_NEWS = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9/', 'showMovies')


URL_SEARCH = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)
    
    showSiteCats()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1] , "Movies by Genres", icons + "/Genres.png", oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_YEARS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_YEARS[1] , "Movies by Year", icons + "/Calendar.png", oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QUALITY[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QUALITY[1] , "Movies by Quality", icons + "/HD.png", oOutputParameterHandler) 
    # #oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    # #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'أقسام الموقع', icons + '/Icon.png', oOutputParameterHandler)
   
# #    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
# #    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'مسلسلات', icons + '/TVShows.png', oOutputParameterHandler) 
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', icons + '/Movies.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler) 
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)   
    
# #   oOutputParameterHandler = cOutputParameterHandler()
# #   oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
# #   oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج وثائقية', icons + '/Documentary.png', oOutputParameterHandler 
 
    oGui.setEndOfDirectory() 
    
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSiteCats():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN# oInputParameterHandler.getValue('siteUrl')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.find("form",{"action":"https://aflam.top"})
    genres = soup.find("select",{"name":"cat"})

    sPattern = '<option value=\"(\d*)\">(.+?)</option>'
    oParser = cParser()
    aResult = oParser.parse(genres, sPattern)

    ItemLs = []
    if aResult[0]:
        for Entry in aResult[1]:
            if Entry[0] not in [None,""] and Entry[1] not in [None,"","اغاني وكليبات","افلام تعرض قريبا"]:
                item = [Entry[1], URL_MAIN+ '/?cat=[%s]&genre=&Quality=&year=' % (Entry[0])]
                ItemLs.append(item)
 
    for sTitle,sUrl in ItemLs:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, getFunc(sTitle), sTitle, getThumb(sTitle), oOutputParameterHandler)       

    #oGui.setEndOfDirectory()    

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN# oInputParameterHandler.getValue('siteUrl')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.find("form",{"action":"https://aflam.top"})
    genres = soup.find("select",{"name":"genre"})
    VSlog(genres)
    sPattern = '<option value=\"(.*?)\">(.+?)</option>'
    oParser = cParser()
    aResult = oParser.parse(genres, sPattern)
    VSlog(aResult)
    ItemLs = []
    if aResult[0]:
        for Entry in aResult[1]:
            if Entry[0] not in [None,""]:
                item = [Entry[1], URL_MAIN+ '/?cat=&genre=[%s]&Quality=&year=' % (Entry[0])]
                ItemLs.append(item)
 
    for sTitle,sUrl in ItemLs:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, getFunc(sTitle), sTitle, getGenreIcon(sTitle), oOutputParameterHandler)       

    oGui.setEndOfDirectory()  

def showQuality():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN# oInputParameterHandler.getValue('siteUrl')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.find("form",{"action":"https://aflam.top"})
    genres = soup.find("select",{"name":"Quality"})
    VSlog(genres)
    sPattern = '<option value=\"(.*?)\">(.+?)</option>'
    oParser = cParser()
    aResult = oParser.parse(genres, sPattern)
    VSlog(aResult)
    ItemLs = []
    if aResult[0]:
        for Entry in aResult[1]:
            if Entry[0] not in [None,""," ", "coming-soon", "mp3", "hdcam"]:
                item = [str(Entry[1]), URL_MAIN+ '/?cat=&genre=&Quality=[%s]&year=' % (Entry[0])]
                ItemLs.append(item)

    for sTitle,sUrl in ItemLs:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, getFunc(sTitle), sTitle, icons + "/HD.png", oOutputParameterHandler)       

    oGui.setEndOfDirectory() 

def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN# oInputParameterHandler.getValue('siteUrl')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.find("form",{"action":"https://aflam.top"})
    genres = soup.find("select",{"name":"year"})
    VSlog(genres)
    sPattern = '<option value=\"(.*?)\">(.+?)</option>'
    oParser = cParser()
    aResult = oParser.parse(genres, sPattern)
    VSlog(aResult)
    ItemLs = []
    if aResult[0]:
        for Entry in aResult[1]:
            if Entry[0] not in [None,""]:
                item = [Entry[1], URL_MAIN+ '/?cat=&genre=&Quality=&year=[%s]' % (Entry[0])]
                ItemLs.append(item)
 
    for sTitle,sUrl in ItemLs:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, getFunc(sTitle), sTitle, icons + "/Calendar.png", oOutputParameterHandler)       

    oGui.setEndOfDirectory() 
    
def getThumb(sTitle):
    sTitle = sTitle.replace("أ","ا").replace("آ","ا").replace("ة","ه")
    sThumb = None
    if 'افلام' in sTitle: 
        sThumb = icons + '/Movies.png'
    if 'مسلسلات' in sTitle: 
        sThumb = icons + '/TVShows.png'
    if 'أنمي' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'اجنبي' in sTitle: 
        sThumb = icons + '/Movies.png'
    if 'عربي' in sTitle: 
        sThumb = icons + '/Arabic.png'
    if 'عربيه' in sTitle: 
        sThumb = icons + '/Arabic.png'
    if 'تركيه' in sTitle: 
        sThumb = icons + '/Turkish.png'
    if 'تركي' in sTitle: 
        sThumb = icons + '/Turkish.png'
    if 'اسيوي' in sTitle: 
        sThumb = icons + '/Asian.png'
    if 'اسيويه' in sTitle: 
        sThumb = icons + '/Asian.png'
    if 'كوري' in sTitle: 
        sThumb = icons + '/Korean.png'
    if 'كوريه' in sTitle: 
        sThumb = icons + '/Korean.png'
    if 'هندي' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'هنديه' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'مسلسلات اجنبيه' in sTitle: 
        sThumb = icons + '/TVShows.png'
    if 'برامج' in sTitle: 
        sThumb = icons + '/Programs.png'
    if 'وثائقي' in sTitle: 
        sThumb = icons + '/Documentary.png'
    if 'وثائقيه' in sTitle: 
        sThumb = icons + '/Documentary.png'
    if '4k' in sTitle: 
        sThumb = icons + '/4k.png'
    if 'اسلامي' in sTitle: 
        sThumb = icons + '/Islamic.png'
    if 'إسلامي' in sTitle: 
        sThumb = icons + '/Islamic.png'
    if 'رمضان' in sTitle: 
        sThumb = icons + '/Ramadan.png'
    if 'قرآن' in sTitle: 
        sThumb = icons + '/Quran.png'
    if 'اناشيد' in sTitle: 
        sThumb = icons + '/Anasheed.png'
    if 'كوميدي' in sTitle: 
        sThumb = icons + '/Comedy.png'
    if 'باكستاني' in sTitle: 
        sThumb = icons + '/Pakistani.png'
    if 'باكستانيه' in sTitle: 
        sThumb = icons + '/Pakistani.png'
    if 'رياضه' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'فاتبول' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'مباريات' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'مسرح' in sTitle: 
        sThumb = icons + '/Theater.png'
    if 'كلاسيكي' in sTitle: 
        sThumb = icons + '/MoviesClassic.png'
    if 'مصارعه' in sTitle: 
        sThumb = icons + '/WWE.png'
    if 'أخرى' in sTitle: 
        sThumb = icons + '/Misc.png'
    if 'هندي' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'كرتون' in sTitle: 
        sThumb = icons + '/Cartoon.png'
    if 'انمي' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'انيميشن' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'الانيميشن' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'اطفال' in sTitle: 
        sThumb = icons + '/Kids.png'
    if 'عائلي' in sTitle: 
        sThumb = icons + '/Family.png'
    if 'مدبلج' in sTitle: 
        sThumb = icons + '/Dubbed.png'
    if 'مترجم' in sTitle: 
        sThumb = icons + '/Subtitled.png'
    if 'تركيه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsTurkish-Dubbed.png'
    if 'كوريه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsKoean-Dubbed.png'
    if 'باسكتانيه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsPakistani-Dubbed.png'
    if 'هنديه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsHindi-Dubbed.png'
    if 'اسيويه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsAsian-Dubbed.png'
    if 'مباشر' in sTitle: 
        sThumb = icons + '/Live.png'

    if sThumb is None:
        sThumb = icons + '/None.png'
    return sThumb

def getFunc(sCat):
    if 'افلام' or 'الانيميشن' or 'ملتيميديا' in sCat:
        return 'showMovies'
    else:
        return 'showSeries'
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?

    sPattern = '<article aria-label="post"><a href="(.+?)">.+?<li aria-label="episode"><em>.+?</em>(.+?)</li><li aria-label="year">(.+?)</li>.+?<li>الموسم(.+?)</li>.+?</em>(.+?)<em>.+?data-src="(.+?)" width'
		
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[4]+'S'+aEntry[3]+' E'+aEntry[1]
            sTitle = sTitle.replace("S ","S")
            siteUrl = aEntry[0] + "watching/"
            sThumb = aEntry[5]
            sYear = ""
            sDesc = ""

            if sTitle not in itemList:
                itemList.append(sTitle)


                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                
                oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)


 
    if not sSearch:
          # ([^<]+) .+?
        sStart = '</section>'
        sEnd = '</ul>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<li><a href="([^<]+)">([^<]+)</a>'
        oParser = cParser()
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
                
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""


                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', sTitle, '', oOutputParameterHandler)

            progress_.VSclose(progress_)
        oGui.setEndOfDirectory() 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search?s='+sSearchText
        showSeries(sUrl)
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
 # ([^<]+) .+? (.+?)
    sPattern = '<a class="block.+?" href="(.+?)">.+?<img src="(.+?)" alt="(.+?)" title='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[arabic]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1].replace("background-image:url(","").replace(");","").replace(")","").replace("(","")
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<a class="block.+?" href="(.+?)">.+?<img src="(.+?)" alt="(.+?)" title='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").split('الموسم')[0].split('الحلقة')[0].strip()
            
            siteUrl = URL_MAIN+aEntry[0].replace("/film/","/watch/").replace("/episode/","/watch/")
            sThumb = URL_MAIN+aEntry[1]
            sDesc = ''
            sYear = ''

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sSeason = ''
    
    #Recuperation infos

    sPattern = '<h1 class="section-title">(.+?)</h1>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sSeason = aResult[1][0].replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("كاملة","").replace("برنامج","").replace("كامل","").replace("مترجم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")

    #print sHtmlContent
   
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = '<h2 class="entry-title">([^<]+)</h2.+?src="([^<]+)" class=.+?<a href="([^<]+)" class="lnk-blk">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 


            sTitle = aEntry[0].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
            siteUrl = URL_MAIN+aEntry[2]
            sThumb = URL_MAIN+aEntry[1]
            sDesc = ""
            sYear = ""
            if '/episode/' in aEntry[2]:
                sTitle = sSeason+' E'+aEntry[2].split('/episode/')[1]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if '/episode/'  in aEntry[2] :
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else: 
	            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
       
    oGui.setEndOfDirectory() 
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sHtmlContent
   
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = '<h2 class="entry-title">([^<]+)</h2.+?src="([^<]+)" class=.+?<a href="([^<]+)" class="lnk-blk">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 

            sTitle = sMovieTitle
            siteUrl = URL_MAIN+aEntry[2]
            sThumb = URL_MAIN+aEntry[1]
            sDesc = ""
            if '/episode/' in aEntry[2]:
                sTitle = sMovieTitle+'E'+aEntry[2].split('/episode/')[1]
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)
               
       
    oGui.setEndOfDirectory() 
 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('origin', 'www.arblionz.org')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', 'https://www.arblionz.org/download/%D9%81%D9%8A%D9%84%D9%85-beyond-the-woods-2020-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?        

    sPattern = 'data-src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) .+?
    #print sHtmlContent           

    sPattern = 'href="([^<]+)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            url = url.replace("moshahda","ffsff")
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
				
                
    oGui.setEndOfDirectory() 
			
def showServer():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
    data = {'wtchBtn':''}
    s = requests.Session()
    r = s.post(sUrl,data = data)
    sHtmlContent = r.content.decode('utf8') 
				     
    # (.+?) ([^<]+) .+?
    sPattern = '<a href="([^<]+)" target="_blank">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    # (.+?) ([^<]+) .+?
    sPattern = '<iframe width="100%" height="100%" src="([^<]+)" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
            
            sHosterUrl = url
            if 'userload' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'streamtape' in sHosterUrl:
               sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


       
    oGui.setEndOfDirectory()  
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    
    # (.+?) ([^<]+) .+?

    sPattern = 'data-q="([^<]+)"  data-num=(.+?)'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:


            sId = URL_MAIN + '/wp-content/themes/Shahid%2B/Ajax/server-single.php?q='+aEntry[0]+'i='+aEntry[1]+'&out=0'
            siteUrl = sId+'&serverid='+aEntry[0]
			
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()
   
            sPattern = '([^<]+)'
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry
                   sTitle = " "
                   sThumb = sThumb
                   if 'govid' in url:
                      url = url.replace("play","down").replace("embed-","")
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      sDisplayTitle = sMovieTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       	
    sPattern = 'rel="nofollow" href="(.+?)" class'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               sDisplayTitle = sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]----------------------------[/COLOR]')
 
     # (.+?) ([^<]+) .+?
    sPattern = '<li><a class="Hoverable" href="([^<]+)" title="([^<]+)"><em>(.+?)</em>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مسلسل","").replace("مشاهده","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").split('الحلقة')[0]  
            if "E" not in sTitle:
                sTitle=sTitle+" E"+aEntry[2]
            siteUrl = aEntry[0].replace("/episode/","/watch/").replace("/post/","/watch/")
            sThumb = ""
            sDesc = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

     
    oGui.setEndOfDirectory()	
 
# (.+?) .+? 
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="(.+?)" />'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False
