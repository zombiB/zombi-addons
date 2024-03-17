# Adopted from Resolveurl, 
# Added PC and Mobile modern versions

import random
import time
import six
from kodi_six import xbmcaddon

addon = xbmcaddon.Addon()

get_setting = addon.getSetting

def set_setting(id, value):
    if not isinstance(value, six.string_types):
        value = str(value)
    addon.setSetting(id, value)

def get_random_ua():
    first_num = random.randint(90, 122)
    third_num = random.randint(3221, 4235)
    fourth_num = random.randint(0, 95)
    os_type = [
        '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '(X11; Linux x86_64) AppleWebKit/537.36',
        '(X11; Linux i686) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 
        '(iPhone; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15s',
        '(iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/604.1.34', 
        '(Windows NT 11.0; Win64; x64) AppleWebKit/537.36',  
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type),
                           '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return random_ua

def get_pc_ua():
    first_num = random.randint(90, 122) 
    third_num = random.randint(3221, 4235)
    fourth_num = random.randint(0, 95)
    os_type = [
        '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '(Windows NT 11.0; Win64; x64) AppleWebKit/537.36', 
        '(X11; Linux x86_64) AppleWebKit/537.36',
        '(X11; Linux i686) AppleWebKit/537.36',
        '(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type),
                           '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                      )
    return random_ua

def get_phone_ua():
  first_num = random.randint(90, 122) 
  third_num = random.randint(0, 4000) 
  fourth_num = random.randint(0, 140)
  os_type = [
      '(iPhone; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15s',
      '(iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/604.1.34',
      '(Linux; U; Android 13; en-us; Pixel 6 Pro Build/TPP1.220621.005)', 
      '(Linux; U; Android 12; en-us; SM-G998B Build/SP1A.210812.016)', 
  ]
  chrome_version = 'Chrome/{}.0.{}.{}'.format(
      first_num, third_num, fourth_num)

  random_ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', chrome_version, 'Mobile Safari/537.36']
                  )
  return random_ua

def get_ua():
    try:
        last_gen = int(get_setting('last_ua_create'))
    except Exception:
        last_gen = 0
    if not get_setting('current_ua') or last_gen < (time.time() - (7 * 24 * 60 * 60)):
        user_agent = get_random_ua()
        set_setting('current_ua', user_agent)
        set_setting('last_ua_create', str(int(time.time())))
    else:
        user_agent = get_setting('current_ua')
    return user_agent

def force_ua():
    return get_random_ua()

def set_ua(ua):
    set_setting('current_ua', ua)
    set_setting('last_ua_create', str(int(time.time())))