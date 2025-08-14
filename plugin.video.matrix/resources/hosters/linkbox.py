#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog, VSlog, siteManager, addon
from resources.hosters.hoster import iHoster
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'linkbox', 'Linkbox')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        addons = addon()

        token = addons.getSetting('LBtoken')

        URL_MAIN = siteManager().getUrlMain('linkbox')
        url = f'{URL_MAIN}api/file/share_out_list/?sortField=utime&sortAsc=0&pageNo=1&pageSize=50&shareToken=' + self._url.rsplit('/', 1)[1]
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        data = sHtmlContent.get("data")
        if data and isinstance(data, dict):
            data = data.get("list", [])
        else:
            data = []

        for aEntry in data:
            item_id = aEntry.get('item_id', '')

        if item_id:
            oRequestHandler = cRequestHandler(f"{URL_MAIN}api/file/repost?isImport=1&pid=0&itemIds={item_id}&shareToken=&token={token}&platform=web&pf=web&lan=en")
            oRequestHandler.addHeaderEntry("connection", "Keep-Alive")
            sHtmlContent = oRequestHandler.request(jsonDecode=True)
            if sHtmlContent.get("msg") == "suc" and sHtmlContent.get("status") == 1:

                oRequestHandler = cRequestHandler(f"{URL_MAIN}api/file/my_file_list/web?sortField=utime&sortAsc=0&pageNo=1&pageSize=50&pid=0&token={token}&platform=web&pf=web&lan=en")
                oRequestHandler.addHeaderEntry("connection", "Keep-Alive")
                file_list_response = oRequestHandler.request(jsonDecode=True)
                for item in file_list_response.get("data", {}).get("list", []):
                    if item.get("item_rid") == item_id:
                        my_item_id = item.get("item_id")

                        oRequestHandler = cRequestHandler(f"{URL_MAIN}api/file/detail?itemId={my_item_id}&needUser=1&needTpInfo=1&token={token}&platform=web&pf=web&lan=en")
                        oRequestHandler.addHeaderEntry("connection", "Keep-Alive")
                        file_detail_response = oRequestHandler.request(jsonDecode=True)

                        data = file_detail_response['data']['itemInfo']['resolutionList']
                        if data:
                            sUrl = []
                            sQual = []
                            for link in data:
                                sUrl.append(link['url'])
                                sQual.append(link['resolution'])

                            api_call = dialog().VSselectqual(sQual, sUrl)

                        oRequestHandler = cRequestHandler(f"{URL_MAIN}api/file/delete?dirIds=&itemIds={my_item_id}&token={token}&platform=web&pf=web&lan=en")
                        oRequestHandler.addHeaderEntry("connection", "Keep-Alive")
                        sHtmlContent = oRequestHandler.request(jsonDecode=True)
                        if sHtmlContent.get("msg") == "suc" and sHtmlContent.get("status") == 1:
                            VSlog(f'File with {my_item_id} was successfully deleted')

                if api_call:
                    return True, api_call + '|User-Agent=' + UA

        return False, False