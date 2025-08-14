# -*- coding: utf-8 -*-
# Adopted from ResolveURL

import re, requests, json
from six.moves import urllib_parse
from resources.lib.comaddon import dialog, VSlog 
from resources.lib.util import urlHostName
from resources.hosters.hoster import iHoster
from resources.lib import helpers
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vk', 'Vk')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        host = urlHostName(self._url)
        ref = f'https://{host}/'
        headers = {'User-Agent': UA,
                   'Referer': ref,
                   'Origin': ref[:-1]}

        media_id = self._url.rsplit('/', 1)[1]
        if 'video_ext.php?' in media_id:
            media_id = media_id.split('video_ext.php?')[1]

        video_list = ''
        try:
            query = urllib_parse.parse_qs(media_id)
            oid, video_id = query['oid'][0], query['id'][0]
        except:
            if '_' in self._url:
                media_id = self._url.split(f'{host}/')[1]
                oid, video_id = re.findall('(.*)_(.*)', media_id)[0]
                if 'list=' in self._url:
                    video_list = re.findall('list=(.*)', media_id)[0]
            else:
                pass

        if 'doc/' not in self._url and not media_id.startswith('doc'):
            oid = oid.replace('video', '')
            sources = self.__get_sources(host, oid, video_id, headers, video_list)
            if sources:
                sources.sort(key=lambda x: int(x[0]), reverse=True)
                source = helpers.pick_source(sources)
                if source:
                    headers.pop('X-Requested-With')
                    return True, source + helpers.append_headers(headers)

        html = requests.get(self.get_url(host, urllib_parse.urlparse(self._url).path.lstrip('/')), headers=headers).text
        if 'doc/' in self._url or self._url.startswith('doc'):
            jd = re.search(r'Docs\.initDoc\(({.+?})\)', html)
        else:
            jd = re.search(r'var\s*playerParams\s*=\s*(.+?});', html)
        if jd:
            jd = json.loads(jd.group(1))
            if 'doc/' in self._url or self._url.startswith('doc'):
                source = jd.get('docUrl')
            else:
                params = jd.get('params')[0]
                source = params.get('hls') or params.get('hls_ondemand')
            if source:
                return True, source + helpers.append_headers(headers)

        return False, False

    def __get_sources(self, host, oid, video_id, headers={}, video_list=''):
        sources_url = 'https://{0}/al_video.php?act=show'.format(host)
        data = {
            'act': 'show',
            'al': 1,
            'video': '{0}_{1}'.format(oid, video_id)
        }
        if video_list:
            data.update({
                'list': video_list,
                'load_playlist': 1,
                'module': 'direct',
                'show_next': 1,
                'playlist_id': '{0}_-2'.format(oid)
            })
        headers.update({'X-Requested-With': 'XMLHttpRequest'})
        html = requests.post(sources_url, data=data, headers=headers).text

        if html.startswith('<!--'):
            html = html[4:]
        js_data = json.loads(html)
        payload = []
        sources = []
        for item in js_data.get('payload'):
            if isinstance(item, list):
                payload = item
        if payload:
            for item in payload:
                if isinstance(item, dict):
                    js_data = item.get('player').get('params')[0]
            for item in list(js_data.keys()):
                if item.startswith('url'):
                    sources.append((item[3:], js_data.get(item)))
            if not sources:
                str_url = js_data.get('hls') or js_data.get('hls_live')
                if str_url:
                    sources = [('360', str_url)]
        return sources

    def get_url(self, host, media_id):
        if 'doc/' in media_id or media_id.startswith('doc'):
            url = 'https://{0}/{1}'.format(host, media_id)
        else:
            media_id = media_id.replace('video', '')
            url = 'https://{0}/video_ext.php?{1}'.format(host, media_id)
        return url