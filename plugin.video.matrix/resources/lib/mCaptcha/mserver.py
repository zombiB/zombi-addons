# -*- encoding: utf-8 -*-
# Thanks to E2iPlayer project for their MyE2i browser extension
# Adopted to be used in this addon - Tesing Functionality . . .

from urllib.parse import urlparse, parse_qs
from http.server import SimpleHTTPRequestHandler
import base64
import json
import socketserver
import os
import socket
import time
import xbmcgui
from resources.lib.comaddon import VSPath, VSlog, addon
from resources.lib.util import urlHostName

addons = addon()

class CaptchaServer:
    def __init__(self, captcha_data):
        self.IP = self.get_ip()
        self.PORT = 9001
        self.site_url = captcha_data['siteUrl']
        self.site_key = captcha_data['siteKey']
        self.captcha_type = captcha_data['captchaType']
        self.httpd = None
        self.url = self.get_url()
        self.write_html_page()
    
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('8.8.8.8', 80))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def get_url(self):
        if self.captcha_type == 'CF':
            return f"{self.site_url}#e2itcf_sep_c={self.site_key}"
        else:
            return f"{self.site_url}/#e2it?k={self.site_key}&st={self.captcha_type}"

    def write_html_page(self):
        job_type = 'cloudflare' if 'e2itcf' in self.url else 'captcha'
        html_content = f'''
<!doctype html>
<html>
    <body style="background-color: #c8dee1">
        <center>
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAACXBIWXMAAAsTAAALEwEAmpwYAAA9xElEQVR4nO2deZxkVXn3v885996q3qanZ2PYmRm2AcKiJi74jgZZ1Gg0hkXfGOOSoJlEI0REjbu44RI1EQVN8hKjSSTuGkEgRtxQQVkEBRmGZWBmmKWnp6e76i7nPO8f51R1z0IDzsAMNffXn/up6ltVt+65dX732Z8jqkqNGjV2DLO7T6BGjT0ZNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBNUFq1JgBye4+gd0BVQfdfnkKBoQWSoVnBOm84jfgJzZQVXfOrqoVhzu9f6k6NdYNtzwOkzSLNB1abczC2+k7ZkPSHMQyF8XgPahMIPQjXsE4kHEMs9hLL/vjErJXdlb04aEyJYogmiAerAVwlK2bKSZ//H908trnmdaGpU7zJxiZ2F9MjqjHqKIISoJoghNZ224M/kjskluS5rIvNgeeeXPWty8OcAC0SNRiPGBSEHmQE6uxp2HvJAgVAIUPd/JMwAuM59eTj33+7HTsptfMarsTaBSUzQqjDQRDYJaG52pBLQpY2hgdpXIpbT+L0sy7PBk68l8bIy/696xxOMoQeBAciKkJ8jjCXksQVcFhSUTJ/W0U6755ZjV2+ZtSs/6EphnASwMHJPShCohHzRZUPOgg4hOMgqGFisXpEBkbEduiBFrlJKoDP2XorHc15r3sv5vJ3N085hq/DXqeIBUF1qWICj6pAMVRItpPIpBPXJ211/7zZ7L8rpc1MwHpw2HJsxZGCxpVhicBEhQBKhCPaIaoINJCxVHIIMYnKBNIw9EYGIBGBabCJ4s/Z8yL3wwn3ecxCCAlIEBS4EkRL4iCGijEkSDY2oey29HzBClok1YpooYiDRaB1QQjMDH65cXtB/7pa7PNA8ckyQCFZIgGDUh8UIVUHOCj4S6oBCULTeP/BYKiakhsiVnYgHyI0VsbPHD3KK0ta6EqSEfmbJx/+Al/t+CIsz9N40gA2kDTl3gBowk4AQOlqbBiMDVBdjt6niAexWiOitDSBpkEH9L42s8fUa694AfDdmBelc4C8VifAIpEG8GLoGLiPgMIiEOlAhLQcNd3kmOGDNnIodx15Ur+57P3suInJa0HxtFyBMs8TCOnb/4Y+x06+/MLT33uJ4598Ut/umjRYfEcSzyKaIJVA6pgaztlT0DvE0RBZJISi9MGfQKtBy5bsmXlJ66dl7h5Uh1EmZb4bBTrJKg9CILisXRUomBYB4JgSlAQDOpS7CyDnb2Ar75rFd/+2I2kZMxpzibrn02alhg8rhyilQ+yub0RdWMMDMz53rF/+cILnvO2P79q1qwhADZrTioZmQaXQG3L737sFQQxUlJqQirCxObv0rrxLXcM274lPpmFsaMkxTBOLC6ZQNTGTwaSCD48j5NVo5olWiKkSMNi9jmAL735Wr76zzdyZPM4mrMSSiz4ISSZRJMC0RSvgyjzGfCWyc2buX1yNQuOOubSU8/5o7c/68+ffw8E/1ow/oGaILsdPU8QvCc3E1iGSNobWHf933xqqH3baxqNfWmbHEnXkRUjqJuFMzmCYEyHDT5sQCCJida1R63B+Umyg4/kx5/6DZ+94AccNnIwSWJxtomXPqzzYAbxOgRYjPGIGAprUdtPxgBb7h/j/mL9xOKTjn//H73hTy9c+pxjS4CCCusMFgmixHg8imLCOYbBxXOrbZVHCz1PEHWOCduin0HGb7r4BLvi0z8fGNqH0pQYtUADlSIE1jUFccFIFw3uXQRQgtgQLB5ByJOKxpyE8Tvn854/+RZ97WEG5w7gfAKSIiSoNhFjgiomKUZSlAyRBEOGYiDNyHyT++9Zy3imvzruFU992/Pf8KIv7XfogQBUroWVBHEplS1RIyQkUbho3GqCPFro+StbWc8Ag1Sb1jBx95c+3rAZ1aSFlsW3BfISaQuSWyiBQtBC8DlormihaAFaKlI6XNEkLwYxeYnovlx16S8ZG3cMze1H6bjADIhBRDBiwSQgCSpJVNoELwZvEsDQkoKFh+zPonmLlv784p/810ef9r4rv/6+r/9ukZcktg8xSiUlgmDVT2leKuwFP+FuRc9LkAJHhmX9tZ9+enPFh78/2HcwTgdBCtBoT0x333buyhKSSTqGgDEGQXGklLakbzBncs0wH3jt95At82nOMigJqhnGNEASjDYRY/FYlBQRixBegwSVsK+VWCxNmm6AVAaZGJ1gzdgYC05YcNFJb1l2wYmnP2U1hAgOFXjxGJMgHarUtsqjhp6//WRYJjavp7zvS+cNthdQTC6gcgUmt0hhkFziZqD7HCQHUxpMKZhSIFc0B8kdyUQLGgu5+QdjbFyXMzCc4jRIDjFJsBMkBTE4QMUiYmNcxQSJYiwqghpD5vqwmuGMp6CgMWeAIxctwt1aLv/cGV++5eMv+sxr7/zpnQgWSSxGBJEQsER6+wa3u9HzBHFAeefV+zfWrnkuOgstCrQQyAXNwbdBC0Fzh89LfO6gVDT3uLYLalZ3Ay0qEm9g3QC3X7+ehgzjFAwJpislbLA7Oua0xn2agSaIGsDGzyQ0vKVRCYk3iAnSa8yOMXTgMEfvf+zIqm9t+MTHn/O5n3z23C++YP29o4hJgBSnJV5jYrIrwAdbys90QWo8IvQ8QUogu/PaF/aNzU5KKWm4UZLJJlWh+AIoBV8IUkJWKGmh2ByS3GBywbUV347kaAuUFWIt7Xs2s3bVAwz1D2CcxUojZgUnCGkghYARGyLiahEyhJDkKJpgJEVIcQacIWYHN8CnJG4Yp5bWwAT7LFnI/P6Df++Gv1/51Q8+8zNf+fonr1jqcVhpYERRPGBQbwm+rmo3X/XeQc8TxOdjtNbed1KaZOhEAz/ZjxZgSkVKkEKh8Ji2IG2LtA3SEqQtmLZBShNUscIgpUDLgBvgvvvXs3FTi6TZD0ZQETC2a6Bv/9yiRkAsIgYRG7xY8TmSdDN91UjXwDea4ipgwHPY4sOYu37/F37rdT++9W3P+PCHf/iN64YhpKSUNqGdhFwxW8uQXYaeJ0ix/l5k3QOLkjLD5Bm0DbTAtATbNpi2IWkJLjcUlaWsEsrKUFYWXybYdorJU6RlkZbBtBKoBlh33yQTkxaRBojBq6DasUHC5FdN0E6ioxhUAyFULE4MHoNiYzKkDfsxEFMViaqYqsW6jA2NMdr7Cocf/LtsuW7W3376/15x64f+9AuvvuPmlaRAHznqBK2y3XrNewk9T5By44YRNm1aTCtBcwNFG3KHtoG2Qhu0rdAWtG0gN2ieoEUCucV0DPfCIoXF5Am0MsY2tPDSj5gGXhSx6RQ5JEgMxAAGiRIkBBotXlLCpbfRoJdIHAOSRDsm2CfeQUz7RdRQmTZbks3M329fDp23dL9b/mPs0+8+6bKffO78rz1rfGNOYtPgJKuxS9DzBPEbR/cz7WzYq4fCo0UaHxVfKFoqWoLkSjqpJJOedFJJJzzSUlwOPhrp5OArhUnP+GZDKg1EIHNpMMajJDHRUA8p8gk+SgIk7BOVQACTxPcmYevYK2LAGFzXyyx4cQy2m8xqNRHJyc0mfDrOYYv35WC79Pe+c+Gqq970zEsv/eY/ff/I6eN3+JBv4x3BItOp+GLtAHtI9DxBsoktDdMaoKSFaTl8ayi4dAsgn7aVHq0cWnq0dGhZoYVD24q2I0na4F0JLU8xNkAmhjypQAdJKoPzwW0rGKyzQBMkRTVIFRWDeIPpEMIniKYElSqL+wVUcUBlwRtCyr1WtNOcVlqhPsH6FCGjzTjMGmfJofuj9w+97LNnf/fmNzzrn957/ZUrmgAWTyU5pU7jQ3B7QW3MPyR6niDeIb5wUX0SKEooQQoLhYFCoJCuIU5B8FjloAXhplsqUgCVkJQWxivW3b8acYJJMvJMsGqxWIxJcNZSGBAj3fhHMMxjRD0a8N2buNiuUa9qgv0iMi1dUoJBH3J88d2a+BCRLwy0xTE8dzaLj1iUrP1J6y0ff8E3b/7IK7760nt+OUYiTVJrcaRUQGUKvOShOrLGjOh5gpgKNZMG086QdoLJBdMWaBukbbB5is3Da9IywZOVWyRPMUWCLSw2T0I6Sktg3IEm7LfsqT9a59r3tu9ey6wqwSfBsLYkoVbdBvVKSYIHi2ifGAsYBItKgsfSsUXAIiZFSQNJYixFNdamIKEWXgKBvBKcAxicCJUX0mqAgw5YwMJ99j/0mv+36XPnnXrZ1V94z+VPLccno7ugpKKFVws+3b0/zuMAvU+QEqQNtG2QIu0qlPK1LbQN2jZoSyCSJhAnkCS4fj2SK5ILtD2MOkbXjK560cUfOPF1V/zHUdkJSz/28wdu86ObxkmSBsYbrApGAyHAYCR6sYyJxnoao+lJdO/GKDudvC2Laki091GCEKWKGsKxxKAGjE+wPkHF4WwQeblm5I2MI5Y2GUnkpC+849Yfve7E/7z4O//64/0hockwiTRiLleNmdDzBHFO0dwFUkR1SXPFF4Lmgm8HY51C0MqgpYmRdcEXimsrLvdoCeoESku5OR9d09rCsac+dctbrv/yOS/88DuPzwfst3517234iYp++jDO4g04aylN8Ehl3naN+ZD3ZRFJYuQ9GPHeyzT7WcKTjvSIW+d1D4gKRkPHFBVPZTwqk6Q6gS8z+vr246CjlrB+dXr2R1/+s1vOfcG/vOWma1eEo1vwtKnU40M6M9EgI9gnwUbZm235nidIpYjkkE2GlBJfpUhhsXm0KwrQ0uALxbcrfNtB6ZEyuIKDhDHQFmTShp4NpaTNzaG+PRP4w7/9s5vfdON/Pe/pf/OKZ9+9ZfQXK1bdR0Yfg4BRi6Mf1SbGpaG/kBeMTxFNo5Ee7QsVPIoXDcWLBO+ToKAueKJ8oIfH44HSVpRShL5ePgGf4H1ChVBapZASqoL5CxosOnLJ8K+ubLz3b57z5Vve/1efe/Hau9diaJKIUlKEC6YVqEc1tDgKcfq9lyI9TxB1Mi1tXaP3SsNWgs892nZoAVIZpJKY8g6UgsQtGPPR1ZuLmDhnKg/Oe+but4A/+9gbrnjtdz/xhH2f9zuvvXX1LQ+MrRpnpMiYk4do+ea+FIzBiA3qFjGK3gksds45SgrvNb6vIzlMN/uYbq1K2O+79blR2oiNiYw+vK6GSiY4cMks9p+36Khvf2bdvy///a9949ILv/97vsxpSAYIFQN4GqAZxG4wtuMe3gvR8wSRyirtmLXbNphJwbSBNsikBjsjl2CgtyzSsuikoJMm7MvDpi3FtxQmDaadqPdhQjoJ5nVe5RQ4jnz6sZz/jQ//48v//S1Ht4+b/4kf3n8zmyc2MOQNg0WCmBQnIYLeyfwNafKRKEaCdFANhrjYriEeDHPBKbGZhODVTHsuOJGt3kcklfcZzjep/CR9acXRS5aSTR7yvE+df/NPXvmMz3zyO/913XyAREBkDO/bdLUub9lbc+p7nyCFaHDvBi+UtARygxSCFIIpDCYnEiiZMtCLtPuaycHmBlsQoustIxKUdrxUiAoNl5KpUPoKD5x41qnr3/7jj/zNsz/00t+9d96Wr916z+0kLU8ifdGbFbxUaPAthVSTOJnF4ySkyUPMzpUoKZDo0TK4ac8VG8hBZ9Ng6Hdel84rBieOXEbpm9PmqKVHsfaWBcvf/bJrbznnrEtfe+NPb0MYxiYNkAmQKnra9k70PEHUaYx/2KBelYTHQqCUrasIQ8Y4Wk5VFfq2hpT4UtAyxFK0DT6GEEQVtULeCGpOAjjNyclpZil/8oaXXvfO7370hcf/+UnPvmXT/Tfed/dqGtpHw/UDCVU0S4JlEaJ5xicY7fw0odS3YxF0IuvbYiqiMWXMI8FFrFhESozZAprgdRYlQ+QCbVnP/H37OPTA35n/ky/ZT/zlaVfccOG533p2PpkjZgCVyZhpPP2bQgO+vQE9TxCcFz/pYFLQPMWXBpf7qYnfUmgppq2Y3GHaHpsrpu2Q3Ae7o1AkbuTgSuudhEtnsYgqoY2cICYhlQYNsjChcSw8cD5/8ZlXXvGXV//l8QtO2+f1t911+/qJ+1r0+1mUBiqjOONwJserw/gUo4ZptMBJSBvx4lHxeK0QdRg8Ki6kuIsn9O3yOKNT+7UIsRRtxBoVh1El8WC84Iwnt5s45Mh5LJh9+HGf//iqb5+17GOf+sWPf9UQZmG1nLoj4AguwZogPQFfKb5kSnLkBHWrlFB1W4BEA7xrzE/LvQqvET1aQK74wqG+64gFOjHu6RBEg0u21BagnHDi7/DGb5778T/+3POPGjvmgU/+euXNDK0ZpOkHYqBQcLak3dhMZasYFAzlwEG4yLRviYZ8LBWe/tqUG1imnVmMs0w7SxWNToIknmebdKDgmKOXsObXR77mVc/+3o8v/8pN+xtJEdMhSAo6GDONex89P0pXGfVtgt3RAiYVaZtQ19EymHYSIuft7TdyC3mC5AnaNvh2cPdq7qRDEODBb6adknEJLVALXwJw8p88a907v/+mv37me554/Ormr7+2csVvSIoGfeUssmKApEpQD45gaHvtyJKYd0go3fUSbRLoRtxDqkow1DUStNtIIpIsyJ14nK1SV0JnyaIaZ9FBBzJn1tITznnFl2/6z0t/eEIg0STeR3cwFXtD7WLPE0ScVS1ivXlbprxSbRMqBONzYjq7FCHCThGLp9oSHw2mbUPEPffdO6g+CDuCchVeS0ixJCH7vQqdRfv7+zn9rX9442uu+pMXHvmyBWfevvGGW+9dez+J9pG6gZCuYjRM4thySGVr6aBMdxGHiLvrEIgponhCZrCTaNh3Ehd1imC+815N8CIU2UqG93uAhfsfMedtr7/hqqv/+/Z5Qj+e8SiQaoL0BLwLE8QXxDhIiIVIGaoF6QQLc40pKEG1oh0j7nmMnZQCpYFS0EKl20+uG9PeFlOlsLgE61KspqgtAEepkDvP4qMW89f/7xWX/fVXzjp69lOab/jFXbeUa7eMY5O+sMQCoTGDJwkeL7Woxr7AXbnSUa1i61SZEl2KwXlwXqMaRnx/8GwFCk9LhBSLN/046afwDQZmD7LggP3n/O2rL7/6179cRWLmhvFqg71g+vT+CJ06DBYz0USdQ0oXJEjZ8UyBlsTgoQvSodSwdbxdRbBXpPCQZ7gisap56A6qobfVthDC8gWCdOefEbqFU6lAZk2MUuec8KzjeMd3zv7ISz/5+8e5OVs+f9vtt5NPKKn2Y7TCa5BIQao0YvOHFkIO0VAHjzcej0M1xsDFY4yGbvEaZAsSovVOPJUp8Z1SYBVEHc6WOCN4SVBV5iwQaAwf+/Y3XfvRsmoBntITJFuPo+cJolVQIGg5NO/Ud4T/aTmkrUg7RNa70fZ8apO2hiTFtkLLd58bH2ZHJTJ1x94GW/Wt6j6dMpTDfVyoyGjj8cbx3L982q8u+N7LXnrKm5Y8467yjh//cuUmvB+iXzaD2UyRtnHpJoqkzYQdpJImoi5m/HZsCbrNIIO7t8tOQLo5il01LFyh8HnrwXjEOMRWYJSqEvZdvJCf//Kecy7+9LVPggQrk1Pj62H0PEGM78wGQSuLlkmwQ9qy1RaSEzvxj6Ba+TbdbiaaC1pY8IJVRVw4rhfFi9upc0xUSNTQpqBFi+EFs/mz951+zbuvfOnTjntJ4+W3r/vZ3ffeW5C5Q8mKOTRKS6oVlqBuTdkcJhjmYkLsQg1o2BeM+7iInEo0/DUS1uBVgwvZghpBjU57TChEWXDIAi795zWfvm/VKMYEg77X0fMEwQguZs4qCU5TPFOb0wSnIcHPuwQ3bfPe4pylckJVGZzr6OpTTt3t3bu/BbQk8Y5+30ef74uTueCw4w/iLZ97yaXn/tvzjxk6fvCCm+64w01symn42TTKfjLfAi1CpFs6hjrduhFVwakQlK+OF2xaSooK4mO9SeBSJITiLUFds6DGYSRncHiEdVuqJ37hP2/6P9AIcZceR88TJBSWmpiaYamwlFgKmb4lVNiQArLVlkzbTKwtN4R819DS0Co73dywMp6qE60Wh2ELeEdVVSiep/3hk7d8/IdnvO1lnzj42Mm5v77sF3fewnjRoMoGcSYoOgrBtSumG1PRmJcVu3GH/TJFIiMhxQWiOhhLfLESNTMNnzMFieb4ChYeolz9vXvPWT/a7n62l9HzBDHOaI6wxYBXgxNDiaXCUCGx6kHjo6GctlUytTkJPXaLuKiOjXGQxO28sWrIYpNr4mROMdIgsQmqBq8VSMaZrz3l1o9c/VdnLnv9whfd1b7h56tuHwc3AGmC9RlGW3jbwkXXsEoVOtd78GGdN7w6FAcxIl8hOFFIKtQoGMEbFyVJKMryklGafsRO0Dc0h9/cv/l53//RzQt3+sd5HKDnCYKGkFaBoZQQJKswQfXQEBcIU0YokUiasJWdTQmkESFH4qpTU6TYWUUjtHmYrrSFXltIsK1N7OOjWjF3vxHe+NE//cqHvn3WE4/6g4nX/WrVD0fvXTOO2GFEB0L6iPrYMNsS3M0hZhE8Wzq1vAMde4OpGhQjHe9BiLsYARvq7DEeL03KNEt/cP0dz9/JYT8u0PME8d6oJ8FF1SrHUIgE1cpIV8UqjKU0ZusNE4llKcRQROlTYKdiCkJUaR4DqOJ0Eqdtlj7pUN7z5Vf9w5sufc5Rw0s2XfyLO69nbNLRqBZi3SBePHRUReNR42KAUEKHFR9aFGE0VBZKsEG8UbRTv2UIDJUKbIGS4UQZWjiXX9yV/5/xdu93Rel9gmC0IqUUQ44ll4S2JORiybEUZmrLTbLV1jaWtlhym9A2hpYY2qSUpOLVdxOfHitfjkiK0I+XBlWUW6edceKaz3zvz1/zyvctPWGs+csrb1rxS0rvEVuGFBK1MU3eTJGDuD5JTK33VpEkkkNiLMWEMhAVxRvFWQXJMOJoDllWr/dH33nPxsdo5LsPPU8QjNUCpVJwYilje8+qa7B31Kjtt6CfR5Wsa7cYPLa7Eq48aLLJowGPaKdnfPjpvCtoNPt45d8++4ZPX/HyU09+zdCZqzbcdOuae0ZDqyGTodqMdSdBkQv7Ow3qiH2FZUpqxOYQ0vFsWagSQciwFGTSgnZ52JrVq+c8ZkPfTeh5gngqqUgo6KNUj/rg5qzwOAh2iEbP1jQDvSDsV2/w3uBdmCmKMIFSRQ0rty7mwj4GiDG/6bF7MSmqOY5xDlx8EG/75Msvu/CrLzhuydPd235922/GR1enWCOoHUNNSIX3OJQCY8pABLutemWmYiDWIza0tqvSEk09Vgxtw9DqsXyfx2bguw+9TxANBAmbD7XZGCrxlBIi4ZUIzhi8Mbi4eWNicl+UHBKI4zEUqPhopTsU85gtYrPDpHpEsqB6RaI+4RmHVRf99ysueN8XTll6zLLi4s3tlno/L6xHqklIXrSCJho8tUajnRK9WDa6iAmd5jFhNROfuNg1xVImwnjR+421ep8gkmhQlSA3lrYRCmMoJaGUIDlKLKU3U5uGrcCQG9M10AuJkgXjFOMgLD6wWxc0j1m1opaQvtjGsRlIOfmsY+47+Bnj/3jn2K98yzVI0yyoU1i8Tcit6Xqx1GpQqUJgPZImqlhCJA8dtxqIIuJ6PlLY833AvTUUCHmMZ6gRrMauH9PuxobpAb+Oh2p7yRDcv6h0X7TEViO7BcGFW6KaUTpoJE2gydXfuzH70IX//aZf/GjtGxfu4+16vk6RH8Osgdkk0iSnwlvBGEWtBhJYmSJFVK/USDTaAzHUCN6GlBRrTU2QxzuqsJofJUppwtLOqZ+q2YbghUriDTIkj8fmbKbzagdCt0/U1Iqfu7nhRxN86BTfMHDHHffy4b+/6iX/9aVr35U7d9iiQw6izxmKagurq1tpb96HOYMH0uwbJjehaoUOSUxMauwUIhoJl6iTQm8MYh0iDjVSDgz2j+3OkT8W6HmCCFCQUJom4j1KShVTvkNNRZj2pYnrd2gIpIWUVw/q4jumkJNJpVMZuV5jsuwuRMeeCByNZVKxjY+LX2a8C6WwJqWV53z4k9986mcu/s771tzffuaSxYeTpilSllQOjGQ00zatLWtYs2EzI/MOJRtZyCQe61ISDy7JcUmJ0ghpJzZE1b2FMlUyk+MlpSUpWbL57gPm9a/etaPe89D7BFHVHKGQlKZLUWMpcXQ4EgPIcZmBGNGOioONDtXpCOkmWTd6LihOZZcTZGvJFbKnnAR/mdUS9YrYDLB8/rLvHvihi7/99htvHv/zA+cfwpHHNCmLNupLEq1C9NxbjM+wjTaumGDN2l8zq5pkeL/9KMWSiyBJ9FyJgjXd+Ie3YT9UOGmSKwwPJ79Zst/8WsV6vMOLxSNU6skl5B15YkfDaEkYQjkqsfZbJOzfquVmrK3w0T3cscs9nuRR8HVMHTGW1io44wgWVT9i4YfX32w/8I//c943L//Nm/uHR2YdtvQwTF7iXAsxHnVBExTR0CfYCLYS0kTp05zJNbeTFWP0H34EW2yCektTmxgbFhUlGuZihFQVjMVbYXJ8HccvTn960ILZu3zcexp6nyAxKFjGeuyKoEuHCRh0bKMxYhz2YLYqTZ1W9EQ3oTF4QSFmcj16l1EVnAf1QmZCk7lVq9fxvou+dvqnvnH7O8n7jj5o6VKsgCvGEVPGD9nQAsiELN5uo7tYxZh5T6Ph2bzuLvIBYXjJkYzlSmkTrA2JjGo0ZPba4AZ2JsGlhlZrPU85fOnlvV8utTcQRJGQkGjwopQmNDewGtyzJqpYaKj97kgOQ1BsnIROCZ0WDZ6Qj6U61Yzn0TPSw3cnNqSiu6rkI/965XEf/bcfvWPtPf6P5h+wlP6sQsstmMqT4RB1od2PhIKo0OhBsOqw3lFiY+MGh7OQDGVsXrmSvqSf2YuWsMFVSCfc0vVceYqsQiWjQJjVlDue9YTDrn20Rr0noecJkhu0jVIhWB9Wl5U4SSAuISBKty5CQFW7Hq3QUERi+89OSatHTUeCJISSpJ2ojagIqeimAASjGfgyLGtoGgB87aqfjrzrku+9/Re/3PD6bMH+HLB0Ds3WOFQllSQgFeo7nU7CWrnBle265x2sKkVUYmtTSNQw3FA2r/g1c+cM01gwl6ooY3Q9FkwJJD6jbE4yumETJx566GeedNSSeOK9PYV6e3RAYaVb2xFKS8NqsT56ebVjpce7NdOeGo2t1sSgqngNTmBHSOADwopSFOwMQdpSIZKQ+ASjClKCDcT42e138J5LrnjNN/73/nfSmLfPfkccialyrBujZZXEGEzl8SJUNni7EgXRThWlR1GctUFhjMspqAlEsZXBpQp5m7F7VjK4YC7jVsD4GA/xQSX1GdYI+diq1h+d9OSLg/Oi97N5e54geJGQlGhwNtghEtPVRUKVdkg3NNNUpY50CVlL3bgIQWKUJOJDeWFopiM7V1mX25IMh60spOEnWTc2zgX/8u3nfeIbN72byeETssVPYEQnkGIiSD+JlYS6dbJk1AiDahVd1l7ARlexdocnePHkiQe1NJr9jK9dT9/6jaT7zqWsCjr9JbytKBoNNt6XcOJRB7739GcsGcN5kKznczF6niBeDTmGSWsxPlToJZjQ0b9rhHei4Z0GDzH+Z0y42ypBF8ejklJqYqINglOHZeci6bOKPiTZAmmGx/P3l/3wyE/85y/edc897TPtAb/LrH1ShraswZuC0lhMJEVoDyzRDPJ0xaKJzeaUkJkrMcAZh9tZyk1i4FO9IbGWpJpkcv0aGgcuCE0cOukm1lC4HGk/cO95L/2DC1NsVAF7nB3sBQQhJhhO2rDIsvGCqo19azWSotN8LUbW42QPsQ3fVa20uwSBUQmGS5QsO2elSwYwyNd/9MuRt33hh+ff9POx81iwwAwddSC2VZKWExRJ6NMY2olOSYKOtOg+h67U6GiOREVL4r7OZ0UV62PZrRcyI+QT44j6mHZShS4nto977lzJG8445KynH31AiTpcmuyahhV7OHqfICq0sAy6BEcaVmLqrvkH6k3MuZJuZL2rgmiHOJ20LNOVSB0YMd3ajK2/l65NE4RTicdRkpGpIs5BkgHws7vW8/5/u/rVX/mf+9+Jnbewefh+pLIFU21GrFKI0LYD9FUFWZlHEgiqnWi7dMcVCBADlyHAg4oNpR8utieK3rrgEEgxeEQUYwR1LaQaJ02b5GSYxHL3vas59bj5573xpaf+OLSdTKOqWhPk8Q8P4yTsXzaYtArig+EZpYan48aVqaTcOPFUBDRERURBvKJYJsNRBIKUsTvKdhfw6iBW8hliI4XKI2kBST8bJyd4/+d/+sx/+MbN78vH/VPTAw+hYYWkHCPxKc4MUJkKcRWDzmFVQrEWfupchZAj5WzkuO/0NAket5jlG4hTBlNLO5IopPV7jbaYxA6/4iglAZtx/713cNT+5h8+e95zPtxPhqva2MTFrpG9j54niJPghM2NRtemIDolNTSqIKJT06ibxDjNtOjICEXiin0xH6qTI7XNbPEouali0yBBNMNKgk0BEj55+e0Hf+A/f/yOVSvHX9Hcdw6zFwyQuwR8hRGLN4KX4HEyYkLQTn1IIPRBenSbWXdiNx2JxZRDTkXDIj+E2vmuTQU4W+JNgbpA/LISNB2kHJrHFp9wzz2385RF7v3/9LYXv2XO0CyqKicRz14wbbro+ZFWIrQI6e6FMSihB6FuU8MxVTor3XLa+C9TnmClEkupU14reZCWP0aFhssQmUSl6MYzLr9pRXrh568977vXlW9meO7gnCPmUlSOwocOJIGipjvJPYKY4GL2GtI+UInu6fDo43Mf1aTOhzU+145hYizqwuq4CcQlFDQQzhpaAoML51L4Ce6+847itBMPeuWnzn3B5+c0MvBtEjvVNG9vkB6wFxAktOpR8ti2BwnFRdtWkj9YzVMnhNhRKLxYctWuJS/ePKgibpxCYwBhgF+tfoAP/vsNL770fze8E1se0b90CFMp0mpgJceaKqSDKHgaaLdbVzC4p1Lxowt32nd296M40WBPTHstWOexRaoIJrYmNVVC4kMSYoUjH2ow6nKGNtx29Xv/9Imv/auznvUrgMrnGEm67uyOq6LnfbzsBQTx4sSR4WOJrZKGKMg2d/6tCBL9Uzr933A0DAmefumIIDV5tDGgIkMUrK8CqxoJm53yD1/66e9+6Fsr3jW2ceA56QHzaCZpWGbatyga4ySVRPvG0+mxK9O+u/tcpCsVIE5P6UiT4DAQD1PtqCM3xCGaYHyG0kKlQrTCqpL6DKSfFff+BrPf0B3PO+3ot73q9OP/40lL9gXaqFO89DHdkx1Cjm6bs+tN9DxBMAXKLBwlpVY4hsl0MiZdTMMOVCWJy8v4abPDWyh8o5vu7gQUR2edNOvK6J2q+I/v37DwXV+99a2/Xjn4V8xfxJwlbbxzeFdixIXmbT6UwTrCeoJGPEKJVYvToF6JkdCFxIdcMNOJ0wihrxWKUcFKiMSLerypuvaRSqibN1JRGY/zjrQyNEzCxtEN3LPhPnfCsYs+9tYPv+zvnnXKsfnUFWgiFrIdXtjebzsKewFBKhJyhMJYnFSI87EfVCf9cJpl23ke3bymE0TswiJakDMmpQ1REkOKKUIqeEi2Tfn+ilWc//W7Xv/jn294B9mC2bMWzSYr22hRoja088R3vq3jmJ0uqeLag7q1wd09Q5l67OwL8RCl80f4ilhwleCTccpkHC3nkDLCRL6FW++6hUMOanzx3ef98buXn3PGLUmWomxCGA52Drq1PbYXoucJ4tRqTkaL0B0xBRwW10nc667GNC0rVzvJJ1PpHJ2ExQxDH/0YjTXpugGyPmCQO8Y2c+E3b37Opf+z9n1FedDxyUFLGSrGaRSTlAotOwvDJIYqeNNiIEE0aGydvy4DZCoo6E0w/INECN43p3H5TplaSjokX8YoeVS/xDi868PIXMQbVt55K2my7ud/8bpnvPXc88769gEHLAA86idBB8FK9ODt3eSAvYAgxkswdyUlTyoqNSQa3L9CSETsplzQWYEpTFKvIF6CZ4jQhbCSJm2G1FZhQU4jc2jj+PgVPz/mwu+ue9fG9YMvyuYcw3BqsG4j4kNMoTAQ14jCu1DE1DG2dxiRnhYl90rssjslOWxHwmh3ZZBuZrLtMAYP4qMaNsz9d2+iNX7zuuc9d8kF55z76k885anHA1BpAWJITH+30XBNjYCeJ0i/nU3GIIV15FKSmj5EU6aWTg5uUqMu2hudbiehRTXGUHWEhYYExxYb/T7zkgrgyz+/b9YHLr/rzT+7N30jw0eYOQcKRbmJSVEybeBsWO88cRM0/ESoJZHOGujbYmpadpWuqSB/N21kKnESiBWTIhWCxxgT8qRwOGmQpAljGzex9u7reMIxQ58853V/9q6XvPjZ68J4KkQNIllcXKfAmArofzR+isclep4gDd1f9mELE9UKTGIQL0xIQupLVPtCzYMUJOIQEkppogiZC6VFakL9uo0RdQpHQ1jwk5Wblly+8tfHXHTlxD+SzTtg4OBhTNmiKtsYEfo8iDosRZi4Amr6EHWIehDTpWio+xXUdZy5wUZSDVm4puOpip4jG1UvRBFCAiaEtQgNIJVgTD+TpWHl7bdywFx/+fveevKbX/+659+QNYfid+SIJCAmrpULkLIXTIlHhJ6/GjZX5rOITcUgG8vfoP1jTNqUZjkQ0khEEJ9SmH68CKoGER9Ka20LpWKgyqgcjFUFm+YuxD35xOG3XLH5pl+mpr+58HhSuxmp1oXotkkQH1WbOKFDMC8G+Jhm6nQeOxZ6NxGs4zKbNhBVQkJVqE8XLF4MDS1IXIn3BkhQESo7wH13309/teJXrznryLe+8W/P+vKigw8EoKpKrBVEGmyvSO0N2VWPDD1PEPEl/cxhMDkYV1o2tK6jGFSMVZASnI8rwAqhDVoZ1J8YYXa5ZUPp2DJ7iPLQwyiOWcK6A4bZUE70DzaGMLoZq5upJEHFE5bjieatMai3MbjnQ7REQmKhiExFxTtJkWaKRPhgJIekRB+5E4KSqi54zfCU3uISCz4jMYY1a9fRfuCXrWc8Zb/3XPDav37/0088Pl6JHNUUOy0aXuOh0fMEoc/7kkmG8yEW9x/NIJY78hW0y3FM4sBWIc6ghkwNXktypxSkGNtPMmsIPXA+fvG+tPaZy6bGJJOTD9BIh0A3IdpCFSpJQapIEodgguozrTuj7+R/TT+/jifLhFWgumqXdpInOwn1EuozPJiYgSw4StMA26AaG2PTihs57IjZ/3TuuS+44DUvftZdU5JIgSz00Oq6rXXaCdR4MPQ8QZI5ZnNBS62rRNoJ+w0dizYXMp6vZqJcR4txSq3IMUwkhiS1aHMIOzgfO2cY2aef1px+NiQVZV5gKqHZHKYiwycVuRnAkSFmC/iwtADGB40IpqTJjtSXabu2SXzBGxf7doVEF8UjvrPueoHzCraJlsqGlbczt5l/723Ln/nWc19z6g9mz5oNwGRZYtKUhpFg98T2QeErOjZNz/ef3in0PEGGDk5W5di7G0weMioZRdFgHguY07eA1mDFuN1MK2vjsbSaDcp+IW1muEHLeOrIKck3F9jMoQ1AlcpVVFlFUoIzSmlyjJpggKOhfp0KY+OSZ+pDKokBdcGDJdG96ztuZRUsofxVvMfZFp4EWw4g6nAySarBKHdJA1HlgXvWweT9d57+7EPe+3eveu4/H39EsDPUO0Qs/Wk6zbTpxHs6V6ZWsx4Oep4g+yztd/207/LMOsR6JVUHladoJ9A0pOks1A4iViH1OBziPEWrovIea5XMGJyGzFqvBJew2tD0QH3oq0VMbIw9bI23MRLuowwJXbe0Kzamq1rR3dx5Jp6+Ygi8x5sxvKlAodVsYcxsWqsy9L7b8t87IXvv+X9x+ode9PQntsNxWnjtA7Hb82GHZKgJ8lDofYIsGWTuEfdfN37bPs9MK4OxjtKUiCbgwFdxuee0gMRhog1rKoNNCCu+qoZ4gQMjglGL8R39vhP1NohJ8C7kb3VL+tQGF61R1PvuMs3BuRqCeJ3ajs6KzYFYBmcrykRxvkHKHPLxCr3nVuYvdP9x/vlPfvu5f/KM30g8jlYtxNjQBa+e+LsMPU8QkZSDn+G/8dPb1rxhH/ZDXLi7W0JJrXiPwSAqGG9DI7lKEauBBGrDaiBeEOe7FXnSiWI7wAuahSZ0oZ7P0BErXTvdCapVjHmY2A/FBjVLqm4wMKSgGNrZREjPN7MwbWX8ztvpt9kPXvnHx739ja884bsHzp0H+Nh5xyAyEBxhFOH7e/+nfUywV1zF33n2wmt+ccn4PZ7yIBdjBUaD4SoaUkZQCQ2e8XRK9YSq23kxkCLMYqMm1mdotD2YShKUkHkb2vG4bjC8G/0WE6WGj5+bippPSRAFm2Gkj/Z962Hzb9ad8vQF73jfy0761JOOPjScbl4GiZW2cDiMDgT1TlPiydfYBdgLCFKy+A+GmbMk/1dZoW91RmnhSJ2lTKFRJogVWkmFuIK0MrQbYX4lzlOKw9rQ29aoBmnhg1QRwPkK8RLigl5jAwXFq49Vex6V0BUY8VNzd1p9hSBYKTDe4Hw/vq9kYkzg3ns49oj8w297/bMvPP3Up64L73bgLZKm8RgplmRajXod7NuV6PmSMFWHzTKedN7Yp1axmqHK0FekOBOCb9YbTFxnzHiiZAkmtNGpAKLxIbvXqAR724fOIOF1D06jdAhZVtrJeSRmxRoz5dbtFGRFkjR8cMG2syG2aMKWlSsYqW76ynv+4tATfnTJ8vMCOcqgomFhWqxPSDCkdebto4SeJwhVA6XgaWfvc/+sA9ofGfMw7EKNt/UgquB9SHrFYGKWiKiJ6pWJeeSCuCApxIUsYfEa32dIXOxcEqqYMNi4NrlBsSBxmxb8sJFBbTubLclsWqtW4dfecNPLT134gp//45+96K0vO+mGAWPxVQtcxbZrldR49NHzV1wAh8PKPF74ifnn38etqwpXkFQ2TPC4mRihNj6WrTpBvIlEEEx8jziJzqewXxwk3oZl3aL3yYjFYgJZOn24YpsdCCnpRG8VScbEps24lTdsPOmo6vXfu/AFx/3Luad//ZAF+xBFFSR9lLavW+RV47FD71/xtI0hwwHH/tGIe8qfTr7kNiboc1OpHMEIN2EjZPziNEoSiYa4xNZAJhZSmWisB6liHBhJUGtADCZOZicSFvGJHRwl6l5iU8ZaFWN3rmPx7I0f++y5T1569ftf8fFlxywC7/C+Ag1rtAfHrd82SaXGY4DeJ0joSoWnBISzLln6gwOPvv8d97QfYChPsFpRSVjSDB8M9QRPCqRVkBgeSF0w2p04UCWrQtNrb5TEx55U6kIduASvVqoeiw1rUKmS0MY3DbkbZvPKNk23+utvfsm8J133sTPPedWzfu8BANSjxmJM8J8YE1Lek9oxtVsgnfaVPQsNnqSSAnGW1KZsuXeMdz31rotb9x1+9qKhPsb6Jxjvq3B2CJdWtJsVVSOUubYa0OoDpKRoKuN9oNbjM5hsOlqNsCRymSntTCkzQX3IEvZe6CvGSNwEbdvPGAPomntg84ZbTn/avm99y5lHfvWE/eZOP9UuajLsGdirCFKpp0EDK5a1K9bx979/3yc33Xvo8kNmD7JpQJnMBJdA3iwpGm3ECpPNhFbTgXXkDaXVgCpVXKa0Go4ic1SJUGVKK4MiC/EP4wq885SkYAzt9etgw9pNTz5MPviOFxz+oeccvyg0ym2VaJaEGtppqAmyZ6D3CULIcvJxHRABCpQ+Elr3jfGh00f/9uZr+z980PxZJMNNJhTyhlI2JiEVWlnCZLNCrAaC9ClVAlXqaTccZTP8X6bQypR2IyQlptUkqW5hbTkX1m5g/1mr/vktp+7/9uWnHHtfOKtRoIFW/d11OKajJsiegZ4nSOxqFfrxxjQlzzhOm6QmBTbyuTff9YTLP5B8MmHRU2YvGqLdB1WjhVpPu5ky3qywxtNuwmRT8dZRpEq74ckbQd0qrdJuCK1+wAoTObi1D9BnVn31b06c/d5znnvUdQuGBgGHFhWVtZQ2oakVBruDVqg19gT0PEG0U5Gx1TArFEspQsYWYJA7vjvBv3/ojlfd+N2+cz37HDV88CzsSE7bQCuBvKkUzYIyVcqoUuUNaDcUb8E3YP1gk00A61djZPXVLzomveCc5xz+v087YHY4F1+FNqKahHXZgYQY/KspsUei5wny8OGBCX7ytQ3mfy/bdOZ119rTH9g05zkm7etvzunHz0lgMCdvKBONFG8r2o2CdlqwpfRsyh1F4777911Qfufkowb+9f8+dd53n334AYSYfDu4d7UR3FI1HjeoCRJRqMNKgaUBOO79zXp+9v3Wvr++sXzayvvyJ60ZtXPGJ/oObNv0kIlGZSXLnRlqF8mQXzF7n1m3HLLI/fDph+n3Tzpm/uRB8zueqS1omSJkocrQVuF5LS0eN6gJElFQhM6JmsWl1yo6SlCeT3L/6s2s39Cm1U7wVWpMw/u+QWXW3AYLFgwxYlO6yyKrweMxkofWQhp6+DqBHfUSqbHnoiZIjRozoFaIa9SYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYAbt9Ec9lI8tPBkavGb3o+t15jL0NxcrTngic/DDffme26IrL4ucWd3Zmi66489E4tz0Ju7Uv1rKR5SuAzgW//prRi570CD+/GLgOGIm7rrpm9KJTduEpPmpYNrJ85JrRi0Yf6+8tVp52NnDxI/zYVdmiK04pVp52MnDltP1ndoizg+8ZyRZd8ZiPb1djt6lYy0aWn80UOQCeuGxk+SP94S5mihwAJy8bWf7EnT65RxnLRpZfCWxcNrJc43V4LPGBXXisHUqgYuVpVwIbi5WnaSTk4xZ7mg1ydlSXHhJxYu3ovSM72PdbYdnI8pOXjSw/P0qqXXXMM9j6vM/fVcd+KBQrTzuD3+76PGxJEL9jt4zv0cBut0F2gIuBJTO9IU7YXXkn3NF3TNc9FwOv3kWH3p1qx7bk+CBwyUN96BHaGo97tWo69kSCLF42svzia0YvmmlCbqtaPW5wzehFVy0bWX4ZcEbc9cHdeDp37mpDO1t0xVXFytP2lPHtNPZEgkBQtS67ZvSiq7Z9YdnI8vN5+N6XPRLXjF505u4+h0cT2aIremZ8exJBrmLrib+dqvUgqtW2n3tQTLclrhm9qOddlDV2HnsSQT5IUJs6XqjFy0aWf3Gbu+0Xt/nMZcxAkOjR6kickW1eg6Avf/Ca0YseSg04extv0yXbqoDLRpaPxO86gynv3GjcrgLe1HHrbmPfvKnz/Q/XbR29YNPHvGRPInyx8rStxpctuuKDcf9248sWXbHd+KIXbKvx7a6Yy57mxTqTrY28M6LXp6NaTXfh3vkwVJWzCRP2weyVEeADccL91oietxUEgkz3eI3E/88mTIwdoTsR4iSfPv6Tl40s30pi7kDFvHMnyHFxdMXuaNupazIN3XONk3yr8RUrT9tqfMXK07Yb3+4MSO5RBIk/9Ju22X1xlATbqla7yqsEYSI+Endk90eOkuOLPLTT4OF6d07Z5r3nd1zf8fHRvA6PBbYbXwxAEh/3qPHtUQQBuGb0oksIKkkHI2x/971kRwb8DnAV4ce4nqDCnUmwa04hqGfTMZMdc2c81lXxu6eT+Hy2J8f1097fmQwP53wf7Cbxxah+bativvphXoc9BlEabDe+qH5tN75s0RW7dXx7kg3SxTWjF52ybGT5RnZ8V77zIVzA049zGdsTAeKEXzay/Dqm2TwzHOqqGb5z23N80s7mhF0zetElUWp27J4Rggo3HZfFm8nO4Hp2LNlGeRTds9miKy6JuWAzji9bdMXOjm+nsUcSJOLVbH9HgSAFHhGiHXMGgQwjPIoxlF2VMHnN6EWvjirVjoj7cOyvh4NLdtckzBZd8eqoUu1wfHuKq3iPU7E6iHf/bX+8Vz+SCRhTRTYSiNbxLj2eAowPlnj5uEjIfBjY48e3xxIEwl2UIDE+CJzySFSKR2A878l4MMfB4zq/aRr2+PHtySoWMKMd8VDY1njuxCK6EmgH8YQ9BlG9erBM2LOXjSy/Kl6bxyWievWg4ytWnnbVg6XSP5bYoyXITmI6Oa6/ZvSiUx4vBVXTpN90bDtZLt6VWcaPJYqVpz2s8U0vztpd6GWCTMfiOOl+W5y8bGT54rid/HBT8h8mFu+gJmRb1fCyaJRPVzFHeOSFTzuLbT1eI8XK00Y6cYwHweId1IRsN75olO/u8W2HXibItrGUjctGll+3bGT5lXG7joeOfXSwmOCGXEGoqNvZKPP0ibaYIA3OhgeNlJ8JXZts+nltF2l/NJEtumJbCXwGsBG4MtaBdLDd+DokeZBI+Znx+NuNb9tI+2ONniVI1M+3/UE7ddgns3Xayo6wbTBrV2KHqt7DzBjY9v/zd7FEeyg8mJr6xId6T4x9POLxPYSEelSxpxCkE+3epceJNe4PJxJ7Gdu4FiPBts0N6+DBjvlwc4ZezY7Hu11B07aR8vj/riLvb3PNz2TH45y+72GPb9tIefz/0bw5PSLs1qYNjxWi/dEJFC5mikhXPRzDPX5+BOo0+Q6ioT0Cvd3dZK8gSI0avy32FBWrRo09EjVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYATVBatSYAf8fs6hyVD7z4YkAAAAASUVORK5CYII="/>
        <br><br><br><br>
        </center>
        <center>
            <a href="{self.url}" target="_blank"><button type="Button" style="color: white; font-weight: bold; font-size: x-large; text-align: center; padding: 4ex; border-radius: 20px; background-color:#448844">Get {job_type} job</button></a>
        </center>
    </body>
</html>
'''
        file_path = VSPath('special://home/addons/plugin.video.matrix/resources/lib/mCaptcha/htdocs/e2it.html')
        with open(file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        VSlog(f"HTML page written to {file_path}")

    def start_server(self):
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        self.httpd = socketserver.ThreadingTCPServer((self.IP, self.PORT), lambda *args, **kwargs: CaptchaHandler(self, *args, **kwargs))
        self.httpd.daemon_threads = True

        VSlog(f"Http Server Serving at ip: {self.IP} and port: {self.PORT}")

        Yes = xbmcgui.Dialog().yesno(
            'الموقع محمي',
            f"انتقل إلى المتصفح على نفس الشبكة وادخل الموقع: \n   http://{self.IP}:{self.PORT} \n\n يرجى الضغط على نعم قبل فتح الموقع",
            'إلغاء'
        )

        if Yes:
            self.httpd.serve_forever()
            VSlog("Server stopped, returning to Kodi...")
        else:
            VSlog("Server was not started, exiting...")
            return

    def shutdown_server(self):
        try:
            if self.httpd:
                VSlog("Shutting down HTTP server...")

                self.httpd.shutdown()
                
                for thread in self.httpd._threads:
                    thread.join(timeout=2)
                    
                self.httpd.server_close()
                self.httpd.socket.close()

                VSlog("HTTP server shut down successfully.")
            else:
                VSlog("Error: httpd instance is None!")

        except Exception as e:
            VSlog(f"Warning: Server shutdown encountered an issue - {e}")

class CaptchaHandler(SimpleHTTPRequestHandler):
    def __init__(self, server_instance, *args, **kwargs):
        self.server_instance = server_instance
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(script_dir, "htdocs"))
        super().__init__(*args, **kwargs)

    def do_GET(self):
        VSlog(self.path)
        if self.path == '/':
            self.path = '/index.html'
        elif 'response' in self.path:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.path.encode())
            parsed_path = urlparse(self.path)
            query = parse_qs(parsed_path.query)
            token = query.get('token', [None])[0]

            if self.server_instance.captcha_type == 'CF':
                decoded_result = base64.b64decode(token).decode('utf-8')
                data = json.loads(decoded_result)
                expiry_timestamp = str(int(time.time() + (24 * 60 * 60)))
                for cookie in data['cookie']:
                    if cookie['name'] == 'cf_clearance':
                        expiry_timestamp = cookie['expirationDate']
                addons.setSetting(f"{urlHostName(self.server_instance.url.split('#e2it')[0])}_cloudCaptcha", token)
                addons.setSetting(f"{urlHostName(self.server_instance.url.split('#e2it')[0])}_create", str(int(expiry_timestamp)))
            else:
                addons.setSetting(f"{urlHostName(self.server_instance.url.split('#e2it')[0])}_mcaptcha", token)
                addons.setSetting(f"{urlHostName(self.server_instance.url.split('#e2it')[0])}_mcreate", str(int(time.time())))

            if token:
                VSlog("Token received. Shutting down server...")
                self.server_instance.shutdown_server()

        super().do_GET()