# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################
# Thanks to TSIPlayer Creators

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress,VSlog, siteManager, dialog, addon

import json
import requests


SITE_IDENTIFIER = 'linkbox'
SITE_NAME = 'Telebox [COLOR orange]- Linkbox -[/COLOR]'
SITE_DESC = 'A Box Linking The World'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = ('https://www.zain3.com/api/search?kw=', 'GetSearch')
FUNCTION_SEARCH = 'GetSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)

    sList = [
            ('AflamHQ','bNA04cJ','sites/aflaam.png'),
            ('مكتبة المسلسلات والأفلام Movies and Series Library with 4k','_ig_gOEnWNM_2543983_3648','sites/linkbox.png'),
            ('Anime Box','app01e2f1adf1aca0a1a1a4a7a2a0adf2aca0a1a1a4a7a2a0','sites/linkbox.png'),
            ('Htm.Animes','app01e2f1adf2acaeafa1a3a1a0a0adf1acaeafa1a3a1a0a0','sites/linkbox.png'),
            ('Bein Movies','app01e2f1adf1aca5a4a7aea7a0a4adf2aca5a4a7aea7a0a4','sites/linkbox.png'),
            ('Cinema Baghdad','UiLE7sU','sites/linkbox.png'),
            ('Cinema-Club (أفلام)','app01e2f1adf1aca4a3a2a1a7aea4adf2aca4a3a2a1a7aea4','sites/cimaclub.png'),
            ('Cinema-Club (مسلسلات)','app01e2f1adf1aca4a1afaea4a5a1adf2aca4a1afaea4a5a1','sites/cimaclub.png'),
            ('Cinema-Club (أفلام و مسلسلات الأنمي)','app01e2f1adf1aca4a3a5aea3aea0adf2aca4a3a5aea3aea0','sites/cimaclub.png'),
            ('Cinema Crown','app01e2f1adf1aca7a4a5a3a1a3aeadf2aca7a4a5a3a1a3ae','sites/linkbox.png'),
            ('Cinema Dose','_ig_app01e2f1adf0f2acf0e6a5e7e5e1a6a6a4a1eefe_10100689_6184','sites/linkbox.png'),
            ('Cinema mix','app01e2f1adf1aca5aea7afa0a6a5adf2aca5aea7afa0a6a5','sites/linkbox.png'),
            ('Cinema sold','app01e2f1adf1aca0a3a1a1a0a0adf2aca0a3a1a1a0a0','sites/linkbox.png'),
            ('cimaabdo','_ig_esEuECt_609855_299a','sites/linkbox.png'),
            ('CiMA Now TV','app01e2f1adf1aca5a3a3a5a3a7adf2aca5a3a3a5a3a7','sites/cimanow.png'),
            ('Dopanime Movies','_ig_app01e2f1adf0f2acf0e6a5e6faf9a6a6a7afa5e2_9389145_6e86','sites/linkbox.png'),
            ('Egybest','xgLMOew','sites/egybest.png'),
            ('EGY-BEST','app01e2f1adf2aca7a3a6a0a1a1a5adf1aca7a3a6a0a1a1a5','sites/egybest.png'),
            ('ايجي بست EgyBest','_ig_app01e2f1adf0f2acf0e6a5fbf9e5a6a6a6eefdf8_3589656_8ed8','sites/egybest.png'),
            ('|| For You','ho3FrEE','sites/linkbox.png'),
            ('Kowaya Cinema','_ig_app01e2f1adf0f2acf0e6a5f9e4f1a6a6a5fcfba2_4250624_a55c','sites/linkbox.png'),
            ('MARVEL MOROCCO','SD9p5bO','sites/linkbox.png'),
            ('Movies Plus - أفلام','app01e2f1adf1aca0a2a3a1a0a6adf2aca0a2a3a1a0a6','sites/linkbox.png'),
            ('Movies Time','U9eySIc','sites/moviztime.png'),
            ('Netflix','_ig_app01e2f1adf0f2acf0e6a5fda0aea6a6a6f3afe0_2674587_0ddd','sites/netflix.png'),
            ('Netflix','46Qaojv','sites/netflix.png'),
            ('افلام و مسلسلات netflix','_ig_2z1IFpK_4702801_f98c','sites/netflix.png'),
            ('Netfilx (2022) أفلام ومسلسلات متنوعة','app01e2f1adf2acaea1aea1afa0adf1acaea1aea1afa0','sites/netflix.png'),
            ('New Q','_ig_app01e2f1adf0f2acf0e6a5fafae5a6a6f4f2aff4_4606358_e7ba','sites/linkbox.png'),
            ('ONE Cima TV','app01e2f1adf1aca7a5a2a5a5a4a2adf2aca7a5a2a5a5a4a2','sites/linkbox.png'),
            ('Star Cinema','app01e2f1adf1aca1afaea6a7adf2aca1afaea6a7','sites/linkbox.png'),
            ('Showtime Movies','app01e2f1adf1aca2a4a7afa5afa7adf2aca2a4a7afa5afa7','sites/linkbox.png'),
            ('The Movie Night','app01e2f1adf2acaeafa3a3afa3adf1acaeafa3a3afa3','sites/linkbox.png'),
            ('English Films - افلام اجنبي','_ig_app01e2f1adf0f2acf0e6a5f1e2a6a6a6a5a6efe3_752951_b7af','sites/linkbox.png'),
            ('The Movies','app01e2f1adf2aca5a5a2a3a3a4aeadf1aca5a5a2a3a3a4ae','sites/linkbox.png'),
            ('THROW LOB (رياضة)','NZKr9gl','sites/linkbox.png'),
            ('The Movie Muse','ZmM9DaP','sites/linkbox.png'),
            ('Yalla Anime','app01e2f1adf2aca4afa3a5a1a5aeadf1aca4afa3a5a1a5ae','sites/linkbox.png'),
            ('World1Movies','app01e2f1adf2aca0a6a7a5aea3adf1aca0a6a7a5aea3','sites/linkbox.png'),
            ('افلام ومسلسلات عربيه واجنبيه مترجمه Various Movies','app01e2f1adf2aca7a2aea3a1a6aeadf1aca7a2aea3a1a6ae','sites/linkbox.png'),
            ('مجتمع الأفلام والمسلسلات | Documentary Films','app01e2f1adf2acaea7a5a2a3a5a4adf1acaea7a5a2a3a5a4','sites/linkbox.png'),
            ('فرجني شكرا - Faragny','_ig_app01e2f1adf0f2acf0e6a5fcaff5a6a6a6afa7fe_2609502_fdae','sites/linkbox.png'),
            ('Marvel Movies أفلام و مسلسلات','_ig_app01e2f1adf0f2acf0e6a5fbf1fda6a6a2f7a6fa_935938_2c28','sites/linkbox.png'),
            ('Shof_Ha افلام','app01e2f1adf2aca4afa5a5a6a2aeadf1aca4afa5a5a6a2ae','sites/linkbox.png'),
            ('يلا Movies','app01e2f1adf2aca3a5afa1aea4a4adf1aca3a5afa1aea4a4','sites/linkbox.png'),
            ('سيما هاوس & Cima House','app01e2f1adf1aca7a2a0a2a3a0a2adf2aca7a2a0a2a3a0a2','sites/linkbox.png'),
            ('موطن المفيز Movies المدبلج','app01e2f1adf2aca0aea6a2a5a3adf1aca0aea6a2a5a3','sites/linkbox.png'),
            ('سينما موفيز | Cinema Movies','app01e2f1adf1aca7a6a2a6a0a0a3adf2aca7a6a2a6a0a0a3','sites/linkbox.png'),
            ('سينما أونلاين','app01e2f1adf1aca5a2aea1a2a6a3adf2aca5a2aea1a2a6a3','sites/linkbox.png'),
            ('عشاق الافلام','app01e2f1adf2acafafa4a2a3a2adf1acafafa4a2a3a2','sites/linkbox.png'),
            ('إجي بيست','DERRaVk','sites/egybest.png'),
            ('اجي بيست','_ig_app01e2f1adf0f2acf0e6a5f9faa2a6a6a2e6f4e2_2751140_2b6c','sites/egybest.png'),
            ('مسلسلات: دراما نيوز','_ig_app01e2f1adf0f2acf0e6a5fde3aea6a6a6aff7f2_3576258_c91a','sites/linkbox.png'),
            ('⏎مــــــسلســــــلات ⇍ كل المسلــسلات والافـلام','app01e2f1adf1aca3a7afa4a0a0a0adf2aca3a7afa4a0a0a0','sites/linkbox.png'),
            ('أفلام ومسلسلات أجنبية','_ig_app01e2f1adf0f2acf0e6a5fae2fda6a6a6f1a3ae_1077534_cc7b','sites/linkbox.png'),
            ('مسلسلات أجنبية أكشن إثارة','_ig_app01e2f1adf0f2acf0e6a5fbe6fda6a6a6eef4ff_6032611_496c','sites/linkbox.png'),
            ('تلفازك المتنقل','_ig_app01e2f1adf0f2acf0e6a5fdf3aea6a6a5e6f8af_3519730_d7ac','sites/linkbox.png'),
            ('جميع الاقسام دراماتك','_ig_app01e2f1adf0f2acf0e6a5faf1a6a6a6a5a3ecf8_4462318_8a7c','sites/linkbox.png'),
            ('الربيعي موفيز','app01e2f1adf2aca3a5a5a4a1a0a1adf1aca3a5a5a4a1a0a1','sites/linkbox.png'),
            ('أفلام مجان نت','app01e2f1adf2aca4a7a5a7a0aeafadf1aca4a7a5a7a0aeaf','sites/linkbox.png'),
            ('مسلسلات وأفلام (2023)','app01e2f1adf2aca5aea1a5aea0a2adf1aca5aea1a5aea0a2','sites/linkbox.png'),
            ('أفلام ومسلسلات نتفليكس','vhOWCrx','sites/netflix.png'),
            ('كيدراما (الأسيوية)','app01e2f1adf1aca4a3a6afa0a6adf2aca4a3a6afa0a6','sites/linkbox.png'),
            ('مسلسلات وأفلام أسيوية','app01e2f1adf2aca0a0a0afa0aeadf1aca0a0a0afa0ae','sites/linkbox.png'),
            ('إستراحة المنوعات','app01e2f1adf2aca5a4afa7a7aea6adf1aca5a4afa7a7aea6','sites/linkbox.png'),
            ('عرب سينما','app01e2f1adf2aca5a5a3a4aea0adf1aca5a5a3a4aea0','sites/linkbox.png'),
            ('سلاسل أفلام','_ig_app01e2f1adf0f2acf0e6a5fbefe1a6a6fca0fff2_728149_b0d7','sites/linkbox.png'),
            ('تسس موفيز','app01e2f1adf2aca5a2a6afafa7adf1aca5a2a6afafa7','sites/linkbox.png'),
            ('موفيز لاند | SA','app01e2f1adf1aca1afafa4a7a7adf2aca1afafa4a7a7','sites/linkbox.png'),
            ('اكوام افلام ومسلسلات','app01e2f1adf2acafa3a4a6a3adf1acafa3a4a6a3','sites/akwam.png'),
            ('جميع المسلسلات والافلام','app01e2f1adf2aca5a0a3a3a2a6aeadf1aca5a0a3a3a2a6ae','sites/linkbox.png'),
            ('مسلسلات اجنبية وافلام اجنبية','ypev9W9','sites/linkbox.png'),
            ('أنميات','app01e2f1adf2acaeaea5a2aea4afadf1acaeaea5a2aea4af','sites/linkbox.png'),
            ('شانكس ساما ( إنمي)','app01e2f1adf2aca0aeaeafa2a1adf1aca0aeaeafa2a1','sites/linkbox.png'),
            ('تارو ساما ( إنمي)','app01e2f1adf2aca0a5a5a3a0adf1aca0a5a5a3a0','sites/linkbox.png'),
            ('؏عـ()ـالم اݪانــٓـــٓـمــــٴ͜ـــي','app01e2f1adf2aca4aea5a4a6a1a3adf1aca4aea5a4a6a1a3','sites/linkbox.png'),
            ('لوفي ساما ( (إنمي','lUprnhl','sites/linkbox.png')]
    
    for sServer in sList:
            icon = sServer[2]
            if icon != '':
                icon = sServer[2]
            else:
                icon = 'host.png'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sServer[1])
            oGui.addDir(SITE_IDENTIFIER, 'showContent', sServer[0], icon, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = 'https://www.zain3.com/api/search?kw='+sSearchText+'&pageSize=50&pageNo=1'
        GetSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showContent(sSearch = ''):
    import requests
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')
    
    
    nb_elm = 50
    shareToken = sUrl

    page = 1
    pid = spid


    if spage > 1:
        page = spage
    else:
        page = 1

    sUrl = URL_MAIN + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(nb_elm)+'&'+'shareToken='+shareToken+'&pid='+str(pid)+'&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'

    data = requests.get(sUrl).json()
    data = data.get('data',{})
    data = data.get('list',[])
    if not data: data = []
    elm_count = 0

    oOutputParameterHandler.addParameter('siteUrl',shareToken)
    oGui.addDir(SITE_IDENTIFIER, 'showGroupSearch', '[COLOR yellow] Search Files within Group [/COLOR]', 'search.png', oOutputParameterHandler) 

    for elm in data:
                sTitle = elm.get('name','')
                type_ = elm.get('type','')

                pid   = elm.get('id','')
                spid = elm.get('pid','')

                desc  = ''
                elm_count = elm_count + 1
                
                icon  = 'host.png'

                link  = elm.get('url','')
                size = elm.get('size','')
                size = size/1024 
                size = size/1024
                size = int(size)

                oOutputParameterHandler.addParameter('spid', pid) 
                oOutputParameterHandler.addParameter('sTitle', sTitle)            
                oOutputParameterHandler.addParameter('sThumb', '') 
                oOutputParameterHandler.addParameter('siteUrl',shareToken)
               
                if type_=='dir':
                    oGui.addDir(SITE_IDENTIFIER, 'showContent', sTitle, icon, oOutputParameterHandler)
                    
                if elm_count + 1 > nb_elm:
                    page = page + 1
                    oOutputParameterHandler.addParameter('page',page)
                    oOutputParameterHandler.addParameter('siteUrl',shareToken)
                    oOutputParameterHandler.addParameter('spid', spid) 
                    oGui.addDir(SITE_IDENTIFIER, 'showContent', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

                elif (type_=='video') or (type_=='audio'):
                    icon  = elm.get('cover','')
                    if '&x-image-process' in icon: 
                         icon = icon.split('&x-image-process',1)[0]
                    sHosterUrl = link
                    sDisplayTitle = sTitle + '  [COLOR yellow]('+str(size) + 'MB)[/COLOR]'
                    oHoster = cHosterGui().getHoster('lien_direct')        
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icon)                

    oGui.setEndOfDirectory()


def GetSearch(sSearch = ''):
    import requests
    oGui = cGui()
    sUrl = sSearch

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler()
    spage = int(oInputParameterHandler.getValue('page'))     
    nb_elm = 50
    shareToken = sUrl

    if spage > 1:
        page = spage
    else:
        page = 1

    data = requests.get(sUrl).json()
    data = data.get('data',{})
    data = data.get('list',[])
    if not data: data = []
    elm_count = 0
    for elm in data:
                sTitle = 'Search Result for: ' + elm.get('name','').replace('<em>','').replace('</em>','')
                type_ = elm.get('type','')

                pid   = elm.get('id','')
                elm_count = elm_count + 1
                
                icon  = 'host.png'

                url  = elm.get('url','')
                if '/f/' in url: url = url.replace('/f/','/s/')
                if ('/s/' in url):
                    shareToken = url.split('/s/')[1]
                    if '?pid=' in shareToken:
                        shareToken,pid = shareToken.split('?pid=')
                    else:
                        pid = ''
                if elm_count + 1 > nb_elm:
                    page = page + 1
                    oOutputParameterHandler.addParameter('page',page)
                oOutputParameterHandler.addParameter('spid', pid) 
                oOutputParameterHandler.addParameter('sTitle', sTitle)            
                oOutputParameterHandler.addParameter('sThumb', '') 
                oOutputParameterHandler.addParameter('siteUrl',shareToken)
                oGui.addDir(SITE_IDENTIFIER, 'showContent', sTitle, icon, oOutputParameterHandler)            
 
    oGui.setEndOfDirectory()

def showGroupSearch(sSearchText = ''):
    import requests
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')

    nb_elm = 50
    shareToken = sUrl

    page = 1
    pid = spid


    if spage > 1:
        page = spage
    else:
        page = 1

    sUrl = URL_MAIN + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(nb_elm)+'&'+'shareToken='+shareToken+'&pid='+str(pid)+'&needTpInfo=1&scene=singleGroup&name='+sSearchText+'&platform=web&pf=web&lan=en'

    data = requests.get(sUrl).json()
    data = data.get('data',{})
    data = data.get('list',[])
    if not data: data = []
    elm_count = 0
    for elm in data:
                sTitle = elm.get('name','')
                type_ = elm.get('type','')

                pid   = elm.get('id','')
                spid = 0

                desc  = ''
                elm_count = elm_count + 1
                
                icon  = 'host.png'

                url  = elm.get('url','')
                size = elm.get('size','')
                size = size/1024 
                size = size/1024
                size = int(size)

                shareToken = shareToken


                oOutputParameterHandler.addParameter('spid', pid) 
                oOutputParameterHandler.addParameter('sTitle', sTitle)            
                oOutputParameterHandler.addParameter('sThumb', '') 
                oOutputParameterHandler.addParameter('siteUrl',shareToken)
                    
                if elm_count + 1 > nb_elm:
                    page = page + 1
                    oOutputParameterHandler.addParameter('page',page)
                    oOutputParameterHandler.addParameter('siteUrl',shareToken)
                    oOutputParameterHandler.addParameter('spid', spid) 
                    oOutputParameterHandler.addParameter('sSearchText', sSearchText) 
                    oGui.addDir(SITE_IDENTIFIER, 'showGroupSearchNext', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

                elif (type_=='video') or (type_=='audio'):
                    icon  = elm.get('cover','')
                    if '&x-image-process' in icon: 
                         icon = icon.split('&x-image-process',1)[0]

                    sHosterUrl = url
                    sDisplayTitle = sTitle + '  [COLOR yellow]('+str(size) + 'MB)[/COLOR]'
                    oHoster = cHosterGui().getHoster('lien_direct')        
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icon)          
 
    oGui.setEndOfDirectory()

def showGroupSearchNext(sSearchText = ''):
    import requests
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()  
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oInputParameterHandler.getValue('sSearchText')
    spage = int(oInputParameterHandler.getValue('page'))   
    spid = oInputParameterHandler.getValue('spid')

    nb_elm = 50
    shareToken = sUrl

    page = 1
    pid = spid


    if spage > 1:
        page = spage
    else:
        page = 1
    VSlog(page)

    sUrl = URL_MAIN + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(nb_elm)+'&'+'shareToken='+shareToken+'&pid=0&needTpInfo=1&scene=singleGroup&name='+sSearchText+'&platform=web&pf=web&lan=en'

    data = requests.get(sUrl).json()
    data = data.get('data',{})
    data = data.get('list',[])
    if not data: data = []
    elm_count = 0
    for elm in data:
                sTitle = elm.get('name','')
                type_ = elm.get('type','')

                spid = 0

                elm_count = elm_count + 1
                
                icon  = 'host.png'

                url  = elm.get('url','')
                size = elm.get('size','')
                size = size/1024 
                size = size/1024
                size = int(size)
                shareToken = shareToken

                   
                if elm_count + 1 > nb_elm:
                    page = page + 1
                    oOutputParameterHandler.addParameter('page',page)
                    oOutputParameterHandler.addParameter('siteUrl',shareToken)
                    oOutputParameterHandler.addParameter('spid', spid) 
                    oOutputParameterHandler.addParameter('sSearchText', sSearchText) 
                    oGui.addDir(SITE_IDENTIFIER, 'showGroupSearchNext', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

                elif (type_=='video') or (type_=='audio'):
                    icon  = elm.get('cover','')
                    if '&x-image-process' in icon: 
                         icon = icon.split('&x-image-process',1)[0]

                    sHosterUrl = url
                    sDisplayTitle = sTitle + '  [COLOR yellow]('+str(size) + 'MB)[/COLOR]'
                    oHoster = cHosterGui().getHoster('lien_direct')        
                    if oHoster:
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icon)          
 
    oGui.setEndOfDirectory()