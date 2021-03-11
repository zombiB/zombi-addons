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
import base64
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
import requests,re,time
sgn = requests.Session()
from resources.lib.CloudflareScraper import CloudflareScraper
scraper = CloudflareScraper()
import urllib2,urllib,re
import unicodedata
import sys
 
SITE_IDENTIFIER = 'egybest'
SITE_NAME = 'egybest'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://tool.egybest.ltd'
host = 'tool.egybest.ltd'


MOVIE_FAM = ('https://tool.egybest.ltd/movies/family-subbed', 'showMovies')
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
 
def showSeriesSearch():
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
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
				sThumb = "https:"+aEntry[1]
            sDesc = ''

            # Filtrer les résultats
            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH_MOVIES[0], ''), sTitle) == 0:
                    continue


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'movie'  in siteUrl: 
			
				oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
			
            if 'series'  in siteUrl: 
			
				oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
				sThumb = "https:"+aEntry[1]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				sYear = str(m.group(0))
				sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
				sThumb = "https:"+aEntry[1]
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
 
            sTitle =  aEntry[2].replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10").replace("الموسم","S")
            siteUrl = str(aEntry[0])
            sThumbnail = aEntry[1]
            sInfo = ""
            if sThumbnail.startswith('//'):
				sThumbnail = "https:"+aEntry[1]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="movie"><span class="r"><i class="i-fav rating"><i>.+?</i></i></span> <img src="([^<]+)"> <span class="title">([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = sMovieTitle+' E'+aEntry[2].replace(" العاشر","10").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace("الموسم","S").split('الحلقة')[-1].replace("ى","").replace("ة","").replace("E ","E")
            sTitle = sTitle.replace("E ","E")
            siteUrl = str(aEntry[0])
            sThumbnail = str(sThumbnail)
            sInfo = aEntry[2]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
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
	
def parseInt(sin):
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else 0
  
def atob(elm):
    try:
        ret = base64.b64decode(elm)
    except:
        try:
            ret = base64.b64decode(elm+'=')
        except:
            try:
                ret = base64.b64decode(elm+'==')
            except:
                ret = 'ERR:base64 decode error'
    return ret

def a0d(main_tab,step2,a):
    a = a - step2
    if a<0:
        c = 'undefined'
    else:
        c = main_tab[a]
    return c

def x(main_tab,step2,a):
    return(a0d(main_tab,step2,a))
    
def decal(tab,step,step2,decal_fnc):
    decal_fnc = decal_fnc.replace('var ','')    
    decal_fnc = decal_fnc.replace('x(','x(tab,step2,') 
    exec(decal_fnc)
    aa=0
    while True:
        aa=aa+1
        tab.append(tab[0])
        del tab[0]
        #print([i for i in tab[0:10]])
        exec(decal_fnc) 
        #print(str(aa)+':'+str(c))
        if ((c == step) or (aa>10000)): break

     
def VidStream(script):
    tmp = re.findall('function.+?{ var(.+?)=', script, re.S)
    if not tmp: return 'ERR:Varconst Not Found'
    varconst = tmp[0].strip()
    print('Varconst     = %s' % varconst)
    tmp = re.findall('}\('+varconst+'?,(0x[0-9a-f]{1,10})\)\);', script)
    if not tmp: return 'ERR:Step1 Not Found'
    step = eval(tmp[0])
    print('Step1        = 0x%s' % '{:02X}'.format(step).lower())
    tmp = re.findall('a=a-(0x[0-9a-f]{1,10});', script)
    if not tmp: return 'ERR:Step2 Not Found'
    step2 = eval(tmp[0])
    print('Step2        = 0x%s' % '{:02X}'.format(step2).lower())    
    tmp = re.findall("try{(var.*?);", script)
    if not tmp: return 'ERR:decal_fnc Not Found'
    decal_fnc = tmp[0]
    print('Decal func   = " %s..."' % decal_fnc[0:135])   
    tmp = re.findall("'data':{'(_[0-9a-zA-Z]{10,20})':'ok'", script)
    if not tmp: return 'ERR:PostKey Not Found'
    PostKey = tmp[0]
    print('PostKey      = %s' % PostKey)
    tmp = re.findall("(var "+varconst+"=\[.*?\];)", script)
    if not tmp: return 'ERR:TabList Not Found'	
    TabList = tmp[0]
    TabList = TabList.replace('var ','')
    exec(TabList) in globals(), locals()
    main_tab = locals()[varconst]
    print(varconst+'          = %.90s...'%str(main_tab))
    decal(main_tab,step,step2,decal_fnc)
    print(varconst+'          = %.90s...'%str(main_tab))
    tmp = re.findall(";"+varconst[0:2]+".\(\);(var .*?)\$\('\*'\)", script, re.S)
    if not tmp: return 'ERR:List_Var Not Found'		
    List_Var = tmp[0]
    print('List_Var     = %.90s...' % List_Var)
    tmp = re.findall("(_[a-zA-z0-9]{4,8})=\[\]" , List_Var)
    if not tmp: return 'ERR:3Vars Not Found'
    _3Vars = tmp
    print('3Vars        = %s'%str(_3Vars))
    big_str_var = _3Vars[1]
    print('big_str_var  = %s'%big_str_var)    
    List_Var = List_Var.replace(',',';').split(';')
    for elm in List_Var:
        elm = elm.strip()
        if 'ismob' in elm: elm=''
        if '=[]'   in elm: elm = elm.replace('=[]','={}')
        elm = re.sub("(a0.\()", "a0d(main_tab,step2,", elm)
        #if 'a0G('  in elm: elm = elm.replace('a0G(','a0G(main_tab,step2,') 
        if elm!='':
            #print('elm = %s' % elm)
            elm = elm.replace('!![]','True');
            elm = elm.replace('![]','False');
            elm = elm.replace('var ','');
            #print('elm = %s' % elm)
            try:
                exec(elm)
            except:
                print('elm = %s' % elm)
                print('v = "%s" exec problem!' % elm, sys.exc_info()[0])            
    bigString = ''
    for i in range(0,len(locals()[_3Vars[2]])):
        if locals()[_3Vars[2]][i] in locals()[_3Vars[1]]:
            bigString = bigString + locals()[_3Vars[1]][locals()[_3Vars[2]][i]]	
    print('bigString    = %.90s...'%bigString) 
    tmp = re.findall('var b=\'/\'\+(.*?)(?:,|;)', script, re.S)
    if not tmp: return 'ERR:GetUrl Not Found'
    GetUrl = str(tmp[0])
    print('GetUrl       = %s' % GetUrl)    
    tmp = re.findall('(_.*?)\[', GetUrl, re.S)
    if not tmp: return 'ERR:GetVar Not Found'
    GetVar = tmp[0]
    print('GetVar       = %s' % GetVar)
    GetVal = locals()[GetVar][0]
    GetVal = atob(GetVal)
    print('GetVal       = %s' % GetVal)
    tmp = re.findall('}var (f=.*?);', script, re.S)        
    if not tmp: return 'ERR:PostUrl Not Found'
    PostUrl = str(tmp[0])
    print('PostUrl      = %s' % PostUrl)
    PostUrl = re.sub("(window\[.*?\])", "atob", PostUrl)        
    PostUrl = re.sub("([A-F]{1,2}\()", "a0d(main_tab,step2,", PostUrl)    
    exec(PostUrl)
    return(['/'+GetVal,f+bigString,{ PostKey : 'ok'}])

 
	

def get_Scripto(data):
    script = ''
    scrtp = re.findall("<script.*?>(.*?)</script>", data.content, re.S)
    for s in scrtp:
        if '(){ var' in s:
            #print s
            return s
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
    url = sUrl
    MLisTe = []
    host = url.split('//')[1].split('/')[0]
    print host
    url = url+"#download"
    rgx = '<iframe class="auto-size" src="(.+?)"'
    tmx = '<td class="tar">.+?dl _open_window" data-url="(.+?)"'
    data = sgn.get(url).content
    link = "https://"+host+re.findall(rgx,data)[0]
    _tar = re.findall(tmx,data)
    for href in _tar:
        href = "https://"+host+href
        MLisTe.append((href))
    print link
    bimbo = MLisTe[0]
    data =  sgn.get(link)
    scrtp  = get_Scripto(data)
    print "scrtp"
    print scrtp
    ln1,ln2,prm = VidStream(str(scrtp))
    ln1 = "https://"+host+ln1
    ln2 = "https://"+host+ln2
    sgn.get(ln1)
    T = sgn.post(ln2,data=prm).content
    print "REPONSE = ",T
    if T == 'ok':
        data = sgn.get(link).content
        sPattern = '<source src="(.+?)" type="application/x-mpegURL">'
        oParser = cParser()
        aResult = oParser.parse(data, sPattern)
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