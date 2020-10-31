#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
import requests,re,time
sgn = requests.Session()
from resources.lib.CloudflareScraper import CloudflareScraper
scraper = CloudflareScraper()
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'egybest'
SITE_NAME = 'egybest'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://tool.egybest.ltd'
host = 'tool.egybest.ltd'


MOVIE_EN = ('https://tool.egybest.ltd/movies/subbed', 'showMovies')
MOVIE_AR = ('https://tool.egybest.ltd/movies/arab', 'showMovies')
MOVIE_HI = ('https://tool.egybest.ltd/movies/hindi', 'showMovies')
MOVIE_ASIAN = ('https://tool.egybest.ltd/movies/japanese-korean-mandarin-chinese-cantonese-thai', 'showMovies')
MOVIE_TURK = ('https://tool.egybest.ltd/movies/turkish', 'showMovies')

MOVIE_POP = ('https://tool.egybest.ltd/trending/', 'showMovies')
KID_MOVIES = ('https://tool.egybest.ltd/movies/animation', 'showMovies')

SERIE_EN = ('https://tool.egybest.ltd/tv/', 'showSeries')

DOC_NEWS = ('https://tool.egybest.ltd/movies/documentary', 'showMovies')
DOC_SERIES = ('https://tool.egybest.ltd/tv/documentary', 'showSeries')
REPLAYTV_PLAY = ('https://tool.egybest.ltd/masrahiyat/', 'showMovies')


URL_SEARCH = ('https://tool.egybest.ltd/explore/?q=', 'showMoviesSearch')
URL_SEARCH_MOVIES = ('https://tool.egybest.ltd/explore/?q=', 'showMoviesSearch')
URL_SEARCH_SERIES = ('https://tool.egybest.ltd/explore/?q=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showMoviesSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://tool.egybest.ltd/explore/?q='+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return

	
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" class="movie">.+?src="([^<]+)" alt=.+?class="title">([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = "https:"+aEntry[1]
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'movie'  in siteUrl: 
			
				oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
			
            if 'series'  in siteUrl: 
			
				oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" class="movie">.+?src="([^<]+)" alt=.+?class="title">([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = "https:"+aEntry[1]
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" args="&output_mode=movies_list" rel="#movies" class="auto load btn b">المزيد</a></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            page =   aEntry.split('=')[1]
            pUrl =  sUrl.split('?page=')[0]
            sTitle =  'page='+str(page)
            siteUrl = page
            siteUrl = pUrl+"?page="+str(siteUrl)
            sThumbnail = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
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
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" class="movie">.+?src="([^<]+)" alt=.+?class="title">([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = "https:"+aEntry[1]
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" args="&output_mode=movies_list" rel="#movies" class="auto load btn b">المزيد</a></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            page =   aEntry.split('=')[1]
            pUrl =  sUrl.split('?page=')[0]
            sTitle =  'page='+str(page)
            siteUrl = page
            siteUrl = pUrl+"?page="+str(siteUrl)
            sThumbnail = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="movie">.+?src="([^<]+)" alt=".+?"> <span class="title">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = '[COLOR aqua]'+sTitle+'[/COLOR]'
            siteUrl = str(aEntry[0])
            sThumbnail = "https:"+aEntry[1]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="movie">.+?src="([^<]+)"> <span class="title">([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle
            siteUrl = str(aEntry[0])
            sThumbnail = str(sThumbnail)
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

 
 
def __checkForNextPage(sHtmlContent):
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sPattern = '<a href="([^<]+)" args='
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return sUrl + aResult[1][0]

    return False
	
def showHosters():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    call = ''
    auth = ''
    mpo = {}
    cv_url = ''
    postData = {}
    fonctiono = ''

            
    sPattern =  '<iframe class="auto-size" src="(.+?)" allowfullscreen></iframe>' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        url = aResult[1][0] 
        if 'watch/' in url:
			url = "https://"+host+url
			vs = url.split('v=')[1].split('&h=')[0]
			hs = url.split('&h=')[1]
			mpo = {'v':vs,'h':hs}
			fonctiono = 'function'
        else:
			url = "https://"+host+url
			call = url.split('call=')[1].split('&auth=')[0]
			auth = url.split('auth=')[1].split('&v=')[0]
			mpo = {'call':call,'auth':auth,'v':'1'}
			fonctiono = ' function'
        step = '' 
        script = '' 
        post_key = '' 
        post_key_1 = '' 
        hdrst ={'Host': host,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Upgrade-Insecure-Requests': '1'} 
        r = scraper.get(url,headers=hdrst,data=mpo,verify=False)
        print "cdxss"
        
        tmp_script = re.findall("<script.*?>(.*?)</script>", r.content, re.S)
        for s in tmp_script: 
			if s.startswith(fonctiono):
				script = s
				break
        if script:
			tmpStep = re.findall("}\(a0a ?,(0x[0-9a-f]{1,3})\)\);", script)
			if tmpStep: 
				step = eval(tmpStep[0])
			else: 
				step = 128
			post_key = re.findall("'data':{'(_[0-9a-zA-Z]{10,20})':'ok'", script)
			if post_key:
				post_key = post_key[0] 
				post_key_1 = post_key
			tmpVar = re.findall("(var a0a=\[.*?\];)", script)
			if tmpVar: 
				wordList=[]
				var_list = tmpVar[0].replace('var a0a=','wordList=').replace("];","]").replace(";","|") 
				exec(var_list) 
				tmpVar2 = re.findall(";a0c\(\);(var .*?)\$\('\*'\)", script, re.S) 
				if tmpVar2: 
					threeListNames = re.findall("var (_[a-zA-z0-9]{4,8})=\[\];" , tmpVar2[0])
					for n in range(0, len(threeListNames)): 
						tmpVar2[0] = tmpVar2[0].replace(threeListNames[n],"charList%s" % n) 
					for i in range(0,len(wordList)):  
						r = "a0b('0x{:x}')".format(i) 
						j = i + step 
						while j >= len(wordList): 
							j = j - len(wordList) 
						tmpVar2[0] = tmpVar2[0].replace(r, "'%s'" % wordList[j]) 
					var2_list=tmpVar2[0].split(';') 
					charList0={}
					charList1={}
					charList2={} 
					for v in var2_list:  
						if v.startswith('charList'):
							exec(v)  
					bigString='' 
					for i in range(0,len(charList2)): 
						if charList2[i] in charList1:  
							bigString = bigString + charList1[charList2[i]]
					if 'watch/' in url: 
						cv_url = "https://"+host+"/cv.php?verify=" + bigString  
						postData={post_key_1:'ok'} 
					else: 
						cv_url = "https://"+host+"/api?call=" + bigString 
						postData={post_key_1:'1'}  
					T5 = scraper.get(cv_url,data=postData,verify=False) 
					T9 = scraper.get("https://"+host+"/cv.php",verify=False)
					hdr1 = {'Host': host,
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'keep-alive',
                       'Referer': 'https://beal.egybest.xyz/movie/romeo-juliet-2013/?ref=movies-p1',
                       'Upgrade-Insecure-Requests': '1'}
					hdr = {'Host': host,
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
                       'Accept': '*/*',
                       'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Content-Length': '23',
                       'Origin': 'https://'+host,
                       'Connection': 'keep-alive',
                       'Referer': url,
                       'TE': 'Trailers'} 
					TY = scraper.get(url,headers=hdr,data=mpo,verify=False)
					
					if 'watch/' in url: 
						sPattern = '<source src="(.+?)" type="application/x-mpegURL">'
						oParser = cParser()
						aResult = oParser.parse(TY.content, sPattern)
						if (aResult[0] == True):
								total = len(aResult[1])
								progress_ = progress().VScreate(SITE_NAME)
								for aEntry in aResult[1]:
									progress_.VSupdate(progress_, total)
									if progress_.iscanceled():
										break
									kurl = "https://tool.egybest.ltd"+str(aEntry)
									print kurl
									sTitle =  sMovieTitle
									sHosterUrl = kurl 
									oHoster = cHosterGui().checkHoster(sHosterUrl)
									if (oHoster != False):
										sDisplayTitle = sTitle
										oHoster.setDisplayName(sDisplayTitle)
										oHoster.setFileName(sMovieTitle)
										cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
								progress_.VSclose(progress_)

                
    oGui.setEndOfDirectory()