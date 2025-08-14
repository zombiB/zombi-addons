# -*- coding: utf-8 -*-

import re
import string
import xbmcvfs
import json
import unicodedata
import threading

from resources.lib.comaddon import addon, dialog, VSlog, VSPath, isMatrix, xbmc
from resources.lib.util import QuotePlus
from resources.lib.handler.requestHandler import cRequestHandler
try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine for omdb')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine for omdb')

lock = threading.Semaphore()


class cOMDb:

    URL = 'http://www.omdbapi.com/'
    CACHE = 'special://home/userdata/addon_data/plugin.video.matrix/video_cache_omdb.db'

    if not isMatrix():
        REALCACHE = VSPath(CACHE).decode('utf-8')
    else:
        REALCACHE = VSPath(CACHE)

    def __init__(self, api_key='', debug=False):

        self.ADDON = addon()

        self.api_key = self.ADDON.getSetting('api_omdb') 
        self.debug = debug
        self.lang = self.ADDON.getSetting('omdb_lang') 
        if not self.lang:
            self.lang = 'short' 

        try:
            if not xbmcvfs.exists(self.CACHE):
                self.db = sqlite.connect(self.REALCACHE, isolation_level=None)
                self.db.row_factory = sqlite.Row
                self.dbcur = self.db.cursor()
                self.dbcur.execute('pragma journal_mode=wal')
                self.__createdb()
                return
        except Exception as e:
            VSlog('Error: Unable to write on %s - %s' % (self.REALCACHE, e))
            pass

        try:
            self.db = sqlite.connect(self.REALCACHE, isolation_level=None)
            self.db.row_factory = sqlite.Row
            self.dbcur = self.db.cursor()
            self.dbcur.execute('pragma journal_mode=wal')
        except Exception as e:
            VSlog('Error: Unable to connect to %s - %s' % (self.REALCACHE, e))
            pass

    def __createdb(self, dropTable=''):
        try:
            if dropTable != '':
                self.dbcur.execute("DROP TABLE " + dropTable)
        except Exception as e:
            VSlog('Error: Unable to drop table %s - %s' % (dropTable, e))
            pass

        sql_create = "CREATE TABLE IF NOT EXISTS movie ("\
                     "imdb_id TEXT UNIQUE, "\
                     "title TEXT, "\
                     "year INTEGER, "\
                     "director TEXT, "\
                     "writer TEXT, "\
                     "plot TEXT, "\
                     "mpaa TEXT, "\
                     "premiered TEXT, "\
                     "genre TEXT, "\
                     "studio TEXT, "\
                     "poster_path TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "duration INTEGER, "\
                     "cast TEXT"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table movie created')
        except Exception as e:
            VSlog('Error: Cannot create table movie - %s' % e)

        sql_create = "CREATE TABLE IF NOT EXISTS tvshow ("\
                     "imdb_id TEXT UNIQUE, "\
                     "title TEXT, "\
                     "year INTEGER, "\
                     "director TEXT, "\
                     "writer TEXT, "\
                     "plot TEXT, "\
                     "mpaa TEXT, "\
                     "premiered TEXT, "\
                     "genre TEXT, "\
                     "studio TEXT, "\
                     "poster_path TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "nbseasons INTEGER, "\
                     "cast TEXT"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table tvshow created')
        except Exception as e:
            VSlog('Error: Cannot create table tvshow - %s' % e)

        sql_create = "CREATE TABLE IF NOT EXISTS season ("\
                     "imdb_id TEXT, " \
                     "season INTEGER, "\
                     "premiered TEXT, "\
                     "poster_path TEXT, "\
                     "plot TEXT, "\
                     "episode_count INTEGER, "\
                     "UNIQUE(imdb_id, season)"\
                     ");"
        try:
            self.dbcur.execute(sql_create)
            VSlog('table season created')
        except Exception as e:
            VSlog('Error: Cannot create table season - %s' % e)

        sql_create = "CREATE TABLE IF NOT EXISTS episode ("\
                     "imdb_id TEXT, "\
                     "season INTEGER, "\
                     "episode INTEGER, "\
                     "title TEXT, "\
                     "premiered TEXT, "\
                     "plot TEXT, "\
                     "rating FLOAT, "\
                     "votes TEXT, "\
                     "poster_path TEXT, "\
                     "UNIQUE(imdb_id, season, episode)"\
                     ");"

        try:
            self.dbcur.execute(sql_create)
            VSlog('table episode created')
        except Exception as e:
            VSlog('Error: Cannot create table episode - %s' % e)

    def __del__(self):
        """ Cleanup db when object destroyed """
        try:
            self.dbcur.close()
            self.db.close()
        except Exception as e:
            VSlog('Unable to close database: %s' % e)
            pass

    def _call(self, params):
        url = '%s?apikey=%s&%s' % (self.URL, self.api_key, params)
        if self.debug:
            VSlog('OMDb API Call: %s' % url)

        rh = cRequestHandler(url)
        data = rh.request()

        try:
            result = json.loads(data)
            if 'Error' in result and result['Error'] == 'Movie not found!':
                return {'Response': 'False'} 
            return result
        except Exception as e:
            VSlog('Error parsing OMDb JSON response: %s - Data: %s' % (e, data))
            return {'Response': 'False'}

    def get_idbyname(self, name, year='', mediaType='movie'):

        omdb_type = 'movie' if mediaType == 'movie' else 'series' if mediaType == 'tvshow' else 'episode'

        params = 's=%s&type=%s' % (QuotePlus(name), omdb_type)
        if year:
            params += '&y=%s' % year

        meta = self._call(params)

        if meta and meta.get('Response') == 'True' and 'Search' in meta:
            if meta['Search']:
                for item in meta['Search']:
                    if self._clean_title(item.get('Title', '')) == self._clean_title(name):
                        return item.get('imdbID')

                return meta['Search'][0].get('imdbID')
        return False

    def search_movie_name(self, name, year=''):
        params = 't=%s&type=movie' % QuotePlus(name)
        if year:
            params += '&y=%s' % year
        params += '&plot=full'

        meta = self._call(params)

        if meta and meta.get('Response') == 'True':
            return self._format(meta, name, media_type='movie')
        else:
            search_params = 's=%s&type=movie' % QuotePlus(name)
            if year:
                search_params += '&y=%s' % year
            search_results = self._call(search_params)

            if search_results and search_results.get('Response') == 'True' and 'Search' in search_results:
                best_match_id = None
                for item in search_results['Search']:
                    if self._clean_title(item.get('Title', '')) == self._clean_title(name):
                        best_match_id = item.get('imdbID')
                        break
                if not best_match_id:
                    best_match_id = search_results['Search'][0].get('imdbID')

                if best_match_id:
                    return self.search_movie_id(best_match_id)
        return {}

    def search_tvshow_name(self, name, year=''):
        params = 't=%s&type=series' % QuotePlus(name)
        if year:
            params += '&y=%s' % year
        params += '&plot=full'

        meta = self._call(params)

        if meta and meta.get('Response') == 'True':
            return self._format(meta, name, media_type='tvshow')
        else:
            search_params = 's=%s&type=series' % QuotePlus(name)
            if year:
                search_params += '&y=%s' % year
            search_results = self._call(search_params)

            if search_results and search_results.get('Response') == 'True' and 'Search' in search_results:
                best_match_id = None
                for item in search_results['Search']:
                    if self._clean_title(item.get('Title', '')) == self._clean_title(name):
                        best_match_id = item.get('imdbID')
                        break
                if not best_match_id:
                    best_match_id = search_results['Search'][0].get('imdbID')

                if best_match_id:
                    return self.search_tvshow_id(best_match_id)
        return {}

    def search_movie_id(self, imdb_id):
        result = self._call('i=%s&plot=full&type=movie' % imdb_id)
        if result and result.get('Response') == 'True':
            return self._format(result, media_type='movie')
        return {}

    def search_tvshow_id(self, imdb_id):
        result = self._call('i=%s&plot=full&type=series' % imdb_id)
        if result and result.get('Response') == 'True':
            return self._format(result, media_type='tvshow')
        return {}

    def search_season_id(self, imdb_id, season_number):
        result = self._call('i=%s&Season=%s&plot=full' % (imdb_id, season_number))
        if result and result.get('Response') == 'True':
            formatted_meta = self._format(result, media_type='season')
            if 'Episodes' in result:
                formatted_meta['episode_count'] = len(result['Episodes'])
            return formatted_meta
        return {}

    def search_episode_id(self, imdb_id, season_number, episode_number):
        result = self._call('i=%s&Season=%s&Episode=%s&plot=full' % (imdb_id, season_number, episode_number))
        if result and result.get('Response') == 'True':
            return self._format(result, media_type='episode')
        return {}

    def _format(self, meta, name="", media_type=""):
        _meta = {
            'imdb_id': meta.get('imdbID', ""),
            'title': meta.get('Title', ""),
            'year': int(re.search(r'\d{4}', meta.get('Year', '0')).group(0)) if re.search(r'\d{4}', meta.get('Year', '0')) else 0,
            'director': meta.get('Director', ""),
            'writer': meta.get('Writer', ""),
            'plot': meta.get('Plot', ""),
            'mpaa': meta.get('Rated', ""),
            'premiered': meta.get('Released', ""),
            'genre': meta.get('Genre', ""),
            'studio': meta.get('Production', ""),
            'poster_path': meta.get('Poster', ""),
            'rating': float(meta.get('imdbRating', '0.0')),
            'votes': meta.get('imdbVotes', '0').replace(',', ''),
            'duration': 0, 
            'cast': meta.get('Actors', ""),
            'media_type': media_type,
            'tagline': "", 
            'status': meta.get('Status', ""), 
            'nbseasons': int(meta.get('totalSeasons', '0')) if media_type == 'tvshow' else 0,
            'episode': int(meta.get('Episode', '0')) if media_type == 'episode' else 0,
            'season': int(meta.get('Season', '0')) if media_type == 'episode' or media_type == 'season' else 0,
        }

        runtime_str = meta.get('Runtime', '0 min')
        duration_match = re.search(r'(\d+)\s*min', runtime_str)
        if duration_match:
            _meta['duration'] = int(duration_match.group(1)) * 60

        return _meta

    def _clean_title(self, title):
        try:
            bMatrix = isMatrix()
            if not bMatrix:
                title = unicode(title, 'utf-8')
            title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('unicode_escape')
            if not bMatrix:
                title = title.encode('utf-8')
        except Exception as e:
            VSlog('Error cleaning title: %s' % e)
            pass

        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), '', title.lower())
        return title

    def _cache_search(self, media_type, name='', imdb_id='', year='', season='', episode=''):
        sql_select = None
        if media_type == 'movie':
            sql_select = 'SELECT * FROM movie'
            if imdb_id:
                sql_select += ' WHERE imdb_id = \'%s\'' % imdb_id
            elif name:
                sql_select += ' WHERE title = \'%s\'' % name
                if year:
                    sql_select += ' AND year = %s' % year

        elif media_type == 'tvshow' or media_type == 'anime':
            sql_select = 'SELECT * FROM tvshow'
            if imdb_id:
                sql_select += ' WHERE imdb_id = \'%s\'' % imdb_id
            elif name:
                sql_select += ' WHERE title = \'%s\'' % name
                if year:
                    sql_select += ' AND year = %s' % year

        elif media_type == 'season' and season and imdb_id:
            sql_select = 'SELECT * FROM season'
            sql_select += ' WHERE imdb_id = \'%s\' AND season = \'%s\'' % (imdb_id, season)

        elif media_type == 'episode' and season and episode and imdb_id:
            sql_select = 'SELECT * FROM episode'
            sql_select += ' WHERE imdb_id = \'%s\' AND season = \'%s\' AND episode = \'%s\'' % (imdb_id, season, episode)

        if not sql_select:
            return None

        matchedrow = None
        try:
            lock.acquire()
            self.dbcur.execute(sql_select)
            matchedrow = self.dbcur.fetchone()
        except Exception as e:
            VSlog('************* Error selecting from cache db: %s' % e, 4)
            if 'no such column' in str(e) or 'no column named' in str(e):
                self.__createdb(media_type)
                VSlog('Table recreated: %s' % media_type)
                try:
                    self.dbcur.execute(sql_select)
                    matchedrow = self.dbcur.fetchone()
                    VSlog('************* Error fixed')
                except Exception as e_retry:
                    VSlog('************* Error 2 after recreate: %s' % e_retry, 4)
            pass
        finally:
            lock.release()

        if matchedrow:
            VSlog('Found meta information in cache table for %s' % media_type)
            return dict(matchedrow)
        else:
            VSlog('No match in local DB for %s' % media_type)
            return None

    def _insert_cache(self, media_type, meta):
        if not meta or not meta.get('imdb_id'):
            VSlog('Cannot cache, missing imdb_id or meta data.')
            return

        imdb_id = meta['imdb_id']
        try:
            lock.acquire()
            if media_type == 'movie':
                sql_insert = "INSERT OR REPLACE INTO movie (imdb_id, title, year, director, writer, plot, mpaa, premiered, genre, studio, poster_path, rating, votes, duration, cast) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self.dbcur.execute(sql_insert, (
                    imdb_id,
                    meta.get('title'),
                    meta.get('year'),
                    meta.get('director'),
                    meta.get('writer'),
                    meta.get('plot'),
                    meta.get('mpaa'),
                    meta.get('premiered'),
                    meta.get('genre'),
                    meta.get('studio'),
                    meta.get('poster_path'),
                    meta.get('rating'),
                    meta.get('votes'),
                    meta.get('duration'),
                    meta.get('cast')
                ))
            elif media_type == 'tvshow':
                sql_insert = "INSERT OR REPLACE INTO tvshow (imdb_id, title, year, director, writer, plot, mpaa, premiered, genre, studio, poster_path, rating, votes, nbseasons, cast) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self.dbcur.execute(sql_insert, (
                    imdb_id,
                    meta.get('title'),
                    meta.get('year'),
                    meta.get('director'),
                    meta.get('writer'),
                    meta.get('plot'),
                    meta.get('mpaa'),
                    meta.get('premiered'),
                    meta.get('genre'),
                    meta.get('studio'),
                    meta.get('poster_path'),
                    meta.get('rating'),
                    meta.get('votes'),
                    meta.get('nbseasons'),
                    meta.get('cast')
                ))
            elif media_type == 'season':
                sql_insert = "INSERT OR REPLACE INTO season (imdb_id, season, premiered, poster_path, plot, episode_count) VALUES (?, ?, ?, ?, ?, ?)"
                self.dbcur.execute(sql_insert, (
                    imdb_id,
                    meta.get('season'),
                    meta.get('premiered'),
                    meta.get('poster_path'),
                    meta.get('plot'),
                    meta.get('episode_count')
                ))
            elif media_type == 'episode':
                sql_insert = "INSERT OR REPLACE INTO episode (imdb_id, season, episode, title, premiered, plot, rating, votes, poster_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self.dbcur.execute(sql_insert, (
                    imdb_id,
                    meta.get('season'),
                    meta.get('episode'),
                    meta.get('title'),
                    meta.get('premiered'),
                    meta.get('plot'),
                    meta.get('rating'),
                    meta.get('votes'),
                    meta.get('poster_path')
                ))
            self.db.commit()
            VSlog('Cached %s with IMDb ID: %s' % (media_type, imdb_id))
        except Exception as e:
            VSlog('Error caching %s data: %s' % (media_type, e), 4)
        finally:
            lock.release()