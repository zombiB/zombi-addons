# -*- coding: utf-8 -*-
from resources.lib.comaddon import VSlog, dialog, VSPath
import xbmc, xbmcgui, xbmcaddon, os, sys, json
monitor = xbmc.Monitor()

def pvrstalkerinstall():
    try:
        try:
            stalkeraddonpath = VSPath('special://home/addons/pvr.stalker/addon.xml')
            if xbmc.getCondVisibility('System.HasAddon(pvr.stalker)') == False and os.path.exists(stalkeraddonpath) == False:
                while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                    if monitor.waitForAbort(0.1):
                        sys.exit()
                yes = xbmcgui.Dialog().yesno("[B]matrix[/B]", "يتوفر خيار (تجريبي) لتفعيل الإعداد المسبق لمشاهدة بث القنوات المباشرة!!![CR]إذا كنت مهتمًا، فعليك تثبيت مشغل الـ PVR الآن. وإلا، فاختر [B]إلغاء[/B].[CR]هل تريد تثبيت [B][COLOR skyblue]PVR Stalker client[/COLOR][/B] الآن؟", nolabel='[B]إلغاء[/B]', yeslabel='[B]تثبيت[/B]')
                if yes == False:
                    return False
                else:
                    dialog().VSinfo('بدء تثبيت PVR Stalker', 'matrix', 4)
                    xbmc.executebuiltin('InstallAddon(pvr.stalker)')
                    xbmc.executebuiltin('SendClick(11)')
                    x = 0
                    while xbmc.getCondVisibility('System.HasAddon(pvr.stalker)') == False and x < 60:
                        x += 1
                        if monitor.waitForAbort(1):
                            sys.exit()
                    if xbmc.getCondVisibility('System.HasAddon(pvr.stalker)'):
                        dialog().VSinfo('تم تثبيت PVR Stalker', 'matrix', 4)
                        return True
                    else:
                        return False
            else:
                return True
        except BaseException:
            return False

    except BaseException:
        return False

def setpvrstalker():
    if pvrstalkerinstall():
        enablestalker()
        try:
            setaddon = xbmcaddon.Addon('pvr.stalker')
            set_prev = setaddon.getSetting('set')
            set_new = '1.0'
            if set_prev == '' or set_prev is None:
                set_prev = '0'
            changes = []
            if str(set_new) > str(set_prev):
                dialog().VSinfo('بدء إعداد PVR Stalker', 'matrix', 4)
                setlist = [['mac_0', '00:1A:79:CC:51:09'], ['server_0', 'http://mutant.arrox.top/c/'], 
                           ['mac_1', '00:1A:79:76:3F:CC'], ['server_1', 'http://tv.greatstar.me/c/'], 
                           ['mac_2', '00:1A:79:D9:85:3C'], ['server_2', 'http://d.tvdark.eu//c/'], 
                           ['mac_3', '00:1A:79:C7:01:32'], ['server_3', 'http://mag.premiumplus.tv/c//c/'], 
                           ['mac_4', '00:1A:79:90:60:0C'], ['server_4', 'http://cooltv4u.xyz/stalker_portal/c//c/'], 
                           ['mac_5', '00:1A:79:51:37:A2'], ['server_5', 'http://iptv.darktv.eu:80/c/'], 
                           ['mac_6', '00:1a:79:a9:da:9d'], ['server_6', 'http://danatv.tv.streamtv.to:8080/c/'], 
                           ['mac_7', '00:1a:79:ad:0a:60'], ['server_7', 'http://danatv.tv.streamtv.to:8080/c/'], 
                           ['mac_8', '00:1A:79:56:55:EC'], ['server_8', 'http://danatv.tv.streamtv.to:8080/c/'], 
                           ['mac_9', '00:1A:79:d3:60:af'], ['server_9', 'http://qqwawa.xyz:80/c/'], 
                           ['mac_10', '00:1A:79:48:18:45'], ['server_10', 'http://ggddnss2.com:8080/c/'], 
                           ['mac_11', '00:1A:79:3a:4e:91'], ['server_11', 'http://chaotic-streams.cc/c/'], 
                           ['mac_12', '00:1A:79:0C:F9:0F'], ['server_12', 'http://dhoom4u.me/c/'], 
                           ['mac_13', '00:1A:79:84:F8:62'], ['server_13', 'http://main2.cwdn.cx/c/'], 
                           ['mac_14', '00:1A:79:10:de:ec'], ['server_14', 'http://chaotic-streams.cc/c/'], 
                           ['mac_15', '00:1A:79:03:78:5E'], ['server_15', 'http://wowtv.cc/c/'], 
                           ['set', set_new]]
                
                if dissablestalker():
                    dialog().VSinfo('تطبيق إعدادات PVR Stalker...', 'matrix', 4)
                    for setitem in setlist:
                        if monitor.waitForAbort(0.1):
                            sys.exit()
                        setid = setitem[0]
                        setvalue = setitem[1]
                        prevsetvalue = setaddon.getSetting(setid)
                        if setvalue != prevsetvalue:
                            setaddon.setSetting(setid, setvalue)
                            changes.append(setitem)
                else:
                    dialog().VSinfo('غير قادر على تكوين Gateway-MAC في Stalker...', 'matrix', 4)

            if len(changes) > 0:
                enablestalker()
                xbmcgui.Dialog().ok("[B]matrix[/B]", "تم تحديث إعدادات سيرفرات PVR %s." % str(len(changes)))
                restartstalker()
                return True
            else:
                enablestalker()
                return 
        except BaseException:
            dialog().VSinfo('غير قادر على تطبيق إعدادات Stalker...', 'matrix', 4)
            return
    else:
        return True


def OKdialogClick():
    x = 0
    while not xbmc.getCondVisibility("Window.isActive(okdialog)") and x < 100:
        x += 1
        xbmc.sleep(100)
    
    if xbmc.getCondVisibility("Window.isActive(okdialog)"):
        xbmc.executebuiltin('SendClick(11)')

def dissablestalker():
    if isenabled('pvr.stalker') == True:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid": "pvr.stalker","enabled":false}}')
        x = 0
        xbmc.sleep(1000)
        while isenabled('pvr.stalker') == True and x < 10:
            x += 1
            if monitor.waitForAbort(1):
                sys.exit()
        if isenabled('pvr.stalker') == False:
            return True
        else:
            return False
    else:
        return True

def enablestalker():
    if isenabled('pvr.stalker') == False:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid": "pvr.stalker","enabled":true}}')
        x = 0
        xbmc.sleep(1000)
        while isenabled('pvr.stalker') == False and x < 10:
            x += 1
            if monitor.waitForAbort(1):
                sys.exit()
        if isenabled('pvr.stalker') == True:
            return True
        else:
            return False
    else:
        return True

def restartstalker():
    try:
        dialog().VSinfo('أعد تشغيل PVR Stalker...', 'matrix', 4)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "pvr.stalker","enabled":false}}')
        xbmc.sleep(1000)
        x = 0
        while isenabled('pvr.stalker') == True and x < 10:
            x += 1
            xbmc.sleep(1000)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":6,"params":{"addonid": "pvr.stalker","enabled":true}}')
        xbmc.sleep(1000)
        x = 0
        while isenabled('pvr.stalker') == False and x < 10:
            x += 1
            xbmc.sleep(1000)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "pvr.stalker","enabled":false}}')
        xbmc.sleep(1000)
        x = 0
        while isenabled('pvr.stalker') == True and x < 10:
            x += 1
            xbmc.sleep(1000)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":6,"params":{"addonid": "pvr.stalker","enabled":true}}')
        xbmc.sleep(1000)
        x = 0
        while isenabled('pvr.stalker') == False and x < 10:
            x += 1
            xbmc.sleep(1000)
        dialog().VSinfo('تم إعادة تشغيل PVR Stalker', 'matrix', 4)

    except:
        dialog().VSinfo('غير قادر على إعادة التشغيل...', 'matrix', 4)

def isenabled(addonid):
    query = '{ "jsonrpc": "2.0", "id": 1, "method": "Addons.GetAddonDetails", "params": { "addonid": "%s", "properties" : ["name", "thumbnail", "fanart", "enabled", "installed", "path", "dependencies"] } }' % addonid
    addonDetails = xbmc.executeJSONRPC(query)
    details_result = json.loads(addonDetails)
    if "error" in details_result:
        return False
    elif details_result['result']['addon']['enabled'] == True:
        return True
    else:
        return False

if __name__ == '__main__':
    setpvrstalker()

