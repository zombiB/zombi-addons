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
from bs4 import BeautifulSoup

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'arblionz'
SITE_NAME = 'Arblionz'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = ' class="logo"><a href="(.+?)" title'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]

MOVIE_EN = (URL_MAIN + '/category/movies/english-movies/', 'showMovies')
MOVIE_4k = (URL_MAIN + '/Quality/4k/', 'showMovies')
#MOVIE_AR = (URL_MAIN + '/category/movies/arabic-movies/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/movies/indian-movies/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/movies/asian-movies/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/anime-cartoon/cartoon/', 'showMovies')
SERIE_TR = (URL_MAIN + '/category/series/turkish-series-translated-20221/', 'showSeries')

SERIE_TR_AR = (URL_MAIN + '/category/turkish-series-dubbed/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/series/english-series/', 'showSeries')
#SERIE_AR = (URL_MAIN + '/category/series/arabic-series/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/series/asian-series/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/category/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%85%d9%83%d8%b3%d9%8a%d9%83%d9%8a/', 'showSeries')

ANIM_NEWS = (URL_MAIN + '/category/series/anime/', 'showSeries')

REPLAYTV_NEWS = (URL_MAIN + '/category/tv-show/', 'showSeries')
# REPLAYTV_PLAY = (URL_MAIN + '/category/other-shows/theater/', 'showSeries')
# SPORT_FOOT = (URL_MAIN + '/category/other-shows/sport/', 'showMovies')
SPORT_WWE = (URL_MAIN + '/category/other-shows/wrestling/', 'showMovies')
URL_SEARCH = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_4k[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', ' 4k أفلام', icons + '/4k.png', oOutputParameterHandler)

    # #oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    # #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    # oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)
 
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    # #oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    # #oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)
 
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', icons + '/TVShowsTurkish-Dubbed.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكي', icons + '/TVShows.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)
    
    # #oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    # #oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%b9%d8%b1%d8%a8%d9%8a/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج عربي',icons + '/Programs.png', oOutputParameterHandler)
  
    sUrl = URL_MAIN

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class=\"active__link\" href=\"(.+?)\">.*?</i>(.+?)</a>'
    matches = re.findall(sPattern,sHtmlContent)
    aResult = [True,matches]
    
    AcceptedCats = ['افلام','مسلسلات','رياضة','مصارعة','انمي','اطفال','رمضان','كرتون','بث حي','مباشر','مباريات', 'مسرحيات']
    okCats = ' '.join(AcceptedCats)
    
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = aEntry[1]
            #VSlog("Checking if " + sTitle + " is in [" + okCats +"]")
            sSubTitle = sTitle.split(" ")
            for Sub in sSubTitle:
                if Sub in okCats:
                    sThumb = getThumb(sTitle.replace("ة","ه").replace("أ","ا").replace("آ","ا")) 
                                    
                    siteUrl = aEntry[0]+'/page/1'
                    #VSlog(siteUrl)
                    sDesc = ''
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)

                    oGui.addDir(SITE_IDENTIFIER, getFunc(sTitle), sTitle, sThumb, oOutputParameterHandler)
                    break
                else:
                    VSlog("iTS IS NOT")
            
    oGui.setEndOfDirectory()

def getThumb(sTitle):
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
    if 'افلام' in sCat:
        return 'showMovies'
    else:
        return 'showSeries'

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/'+sSearchText
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
    sPattern = '<div class="Posts--Single--Box"> <a href="([^<]+)" title="([^<]+)">.+?data-image="([^<]+)" alt='
 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            if "فيلم" not in aEntry[1] and "عرض" not in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("عرض","").replace("الرو","").replace("بالتعليق العربي","[COLOR gold]- تعليق عربي -[/COLOR]")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        
  # # ([^<]+) .+? (.+?)

    # sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    # if aResult[0]:
        # total = len(aResult[1])
        # progress_ = progress().VScreate(SITE_NAME)
        # oOutputParameterHandler = cOutputParameterHandler() 
        # for aEntry in aResult[1]:
            # progress_.VSupdate(progress_, total)
            # if progress_.iscanceled():
                # break
 
            # sTitle = aEntry[1]           
            # sTitle =  "PAGE " + sTitle
            # sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            # siteUrl = aEntry[0]
            # sThumb = ''


            # oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            # oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            # oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            # oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

        # progress_.VSclose(progress_)
 
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="Posts--Single--Box"> <a href="([^<]+)" title="([^<]+)">.+?data-image="([^<]+)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    item = {}
    itemList = []
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            sDesc = ''
            sYear = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").split('الموسم')[0].split('الحلقة')[0].strip()
            #VSlog(sDisplayTitle)

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        #VSlog(itemList)
        
        
  # ([^<]+) .+? (.+?)

    # sPattern = '\"next\" href=\"(.+?)\">'

    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    # if aResult[0]:
        # total = len(aResult[1])
        # progress_ = progress().VScreate(SITE_NAME)
        # oOutputParameterHandler = cOutputParameterHandler() 
        # for aEntry in aResult[1]:
            # progress_.VSupdate(progress_, total)
            # if progress_.iscanceled():
                # break
 
            # sTitle = "Next" #aEntry[1]           
            # #sTitle =  "PAGE " + sTitle
            # #sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            # siteUrl = aEntry
            # sThumb = icons + '/Next.png'


            # oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            # oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            # oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            # oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, sThumb, oOutputParameterHandler)

        # progress_.VSclose(progress_)
			
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
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
    sPattern = 'href="([^<]+)"><span>([^<]+)</span><em'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:
    # (.+?) .+? ([^<]+)
        sPattern = '<a href="(.+?)"><span>حلقة </span>(.+?)</a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                sTitle =  sMovieTitle+' E'+ aEntry[1]
                siteUrl = aEntry[0]
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
   
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    sHtmlContent = str(soup.find("div",{"class":"paginate"}))
    current = '<li class=\"active\"><a href=\".+?\">(.+?)</a></li>'
    oParser = cParser()
    currentpage = oParser.parse(sHtmlContent, current)
    #VSlog('currentpage : ' + str(currentpage))
    sPattern = '<li><a href=\"(.+?)\">(.+?)</a></li>'
	
    
    aResult = [True,re.findall(sPattern,sHtmlContent)]
    
    if aResult[0]:
        for res in aResult[1]:
            if res[1] == '»':
                #VSlog(res[0])
                return res[0]

    return False
		
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieUrl = oInputParameterHandler.getValue('sMovieUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')


    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('origin', URL_MAIN)
    sHtmlContent = oRequestHandler.request()


   
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = '<a href="(.+?)">.+?</span>(.+?)</a></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 

            sTitle = sMovieTitle+' E'+ aEntry[1]
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
         
       
    oGui.setEndOfDirectory() 
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = ',"homeUrl":"(.+?)"}'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        URL_MAIN = aResult[1][0]
        VSlog(URL_MAIN)
    
    #Recuperation infos
    sNote = ''

    sPattern = 'data-id="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId = aResult[1][0]
    siteUrl = URL_MAIN + '/PostServersWatch/'+sId


    from resources.lib.util import Quote

    oRequestHandler = cRequestHandler(siteUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
    oRequestHandler.addHeaderEntry('origin', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li data-i="([^<]+)" data-id="([^<]+)" class'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        for aEntry in aResult[1]:
            link = URL_MAIN + '/Embedder/'+aEntry[1]+'/'+aEntry[0]
            oRequestHandler = cRequestHandler(link)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('origin', URL_MAIN)
            oRequestHandler.addHeaderEntry('Cookie', cook)
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
            sHtmlContent = oRequestHandler.request()
    
    # (.+?) .+? ([^<]+)        

            sPattern = '<iframe src="(.+?)" frameborder='
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

	
            if aResult[0]:
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sTitle = sMovieTitle
            
                   sHosterUrl = url.strip()
                   if 'moshahda' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
					   
    siteUrl = URL_MAIN + '/PostServersDownload/'+sId

    oRequestHandler = cRequestHandler(siteUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', Quote(sUrl))
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li><a href="([^<]+)" rel="nofollow".+?</span>([^<]+)</a></li>' 
    aResult1 = re.findall(sPattern, sHtmlContent)
    sPattern = '<li><a href="([^<]+)" target="_blank"><i class="fas fa-arrow-circle-down"></i>(.+?)</a></li>' 
    aResult2 = re.findall(sPattern, sHtmlContent)
    aResult = aResult1 + aResult2
    
    # (.+?) .+?  ([^<]+)       
	
    if aResult:
        for aEntry in aResult:
            
            url = aEntry[0]
            sTitle = sMovieTitle+'('+aEntry[1]+')'
            
            sHosterUrl = url
            if '?download_' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
				
                
    oGui.setEndOfDirectory()  
# (.+?) .+? 
# def __checkForNextPage(sHtmlContent):
    # sPattern = '<a class="page-link current".+?</a><a class="page-link" href="(.+?)">'
	
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
 
    # if aResult[0]:
        # return URL_MAIN+aResult[1][0]

    # return False
