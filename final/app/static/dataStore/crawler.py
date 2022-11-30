# SJTU EE208
'''
This documents is only for registration
'''
from curses import reset_prog_mode
from inspect import ArgSpec
import json
from multiprocessing import Semaphore
from re import compile, match
import socket
import sys
from unittest import result
from urllib import request,parse,error
from http import cookiejar
import ssl
from random import randint
import asyncio
from aiohttp import ClientResponse
import aiohttp


user_agent= [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",

    # 各种移动端

    # IPhone
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPod
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPAD
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # Android
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # QQ浏览器 Android版本
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # Android Opera Mobile
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # Android Pad Moto Xoom
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # BlackBerry
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # WebOS HP Touchpad
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # Nokia N97
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # Windows Phone Mango
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC浏览器
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # UCOpenwave
    "Openwave/ UCWEB7.0.2.37/28/999",
    # UC Opera
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def standard_request(url, opener=None, timeout = 2):
    if opener == None:
        cookie = cookiejar.CookieJar()
        cookie_handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(cookie_handler)

    header = user_agent[randint(0,len(user_agent)-1)]

    #防止服务器对请求头中不重要的信息进行检查来鉴别人还是虫
    # 但是还有诸如 refereer, authority, host和最重要的 cookie不具有普适性
    headers = {
            "User Agent": header,
            "Accept": "text/html, application/xhtml+xml, */*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "Keep-Alive"
            }

    open_Request = request.Request(url, headers = headers)
    
    try:
        return opener.open(open_Request, timeout = timeout).read()
    except error.HTTPError as e:
        if (e.code == 418 or e.code == 400):
            host = parse.urlparse(url=url).scheme + "://" + parse.urlparse(url=url).netloc
            headers["host"] = host
            try:
                open_Request = request.Request(url, headers = headers)
            except error.HTTPError as e:
                print('HTTPError' + '\t' + str(e.code) + '\t' + str(e.reason))
        print('HTTPError' + '\t' + str(e.code) + '\t' + str(e.reason))
    except error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('TimeOut Error')
        else:
            print('URLError' + '\t' + str(type(e.reason)))
    except TimeoutError as e:
        print("TimeOut Error")
        print(e)
    except Exception as e:
        print("Unknown Error", e)



def login_request(referer, args = {}, timeout = 2, destination = ''):
    cookie = cookiejar.CookieJar()
    cookie_handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_handler)

    header = user_agent[randint(0,len(user_agent)-1)]

    #防止服务器对请求头中不重要的信息进行检查来鉴别人还是虫
    # 但是还有诸如 refereer, authority, host和最重要的 cookie不具有普适性
    headers = {
            "User Agent": header,
            "Accept": "text/html, application/xhtml+xml, */*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "Keep-Alive"
            }
    opener.addheaders = headers

    postdata = parse.urlencode(args).encode('utf-8')

    def _assign(key):
        nonlocal headers, args
        headers[key] = args[key]

    filterObj = list(map(_assign, args.keys()))
    if not destination:
        open_Request = request.Request(referer, data = postdata)
    else:
        open_Request = request.Request(referer, data = postdata, headers = dict(Referer = referer))
    
    try:
        print(opener.open(open_Request, timeout = timeout).read())
        return opener.open(open_Request, timeout = timeout).read()
    except error.HTTPError as e:
        print('HTTPError' + '\t' + str(e.code) + '\t' + str(e.reason))
    except error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('TimeOut Error')
        else:
            print('URLError' + '\t' + str(type(e.reason)))
    except TimeoutError as e:
        print("TimeOut Error")
        print(e)


async def asynCrawl(url, params=None, semaphore=asyncio.Semaphore(5), timeout = 2, cookie = None):
    async with semaphore:
        timeout = aiohttp.ClientTimeout(total=timeout)
        conn = aiohttp.TCPConnector(ssl=False)
        params = {'username':'13818842238', 'password':"11111111a"}
        async with aiohttp.ClientSession(timeout=timeout, connector=conn, trust_env=True) as session:
            async with session.get(url, ssl=False) as resp:
                print(resp.headers)
                print(resp.status)
                return await resp.read()

urls = ['http://www.baidu.com']


async def _(urls, params = None, semaphore = asyncio.Semaphore(100), timeout = 2):
    tasks = [asyncio.ensure_future(asynCrawl(url, params=params, semaphore=semaphore,timeout=timeout)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == '__main__':
    semaphore = asyncio.Semaphore(100)
   
    cookie = {'_zap':'30a2e973-a14c-41c5-a1e5-39936f7a4d25; d_c0="ACCSyEixPBWPTrTJenLNUU0cgoen3g5dJrU=|1657630258"; _9755xjdesxxd_=32; YD00517437729195:WM_TID=n5jaY4JavsNFBBEAQALEGFVJau24Fdk7; _ga=GA1.2.102165221.1663504464; __snaker__id=nlUfy3BWzU2aRZkM; q_c1=adbf1a7f356c4080b4c2ed3700f21380|1663751223000|1663751223000; YD00517437729195:WM_NI=3q+5Z63gj8t/5tyAkVHawYcnEHk2s6UPF8/JedMBFIPcevqqxyymjl6S9WydlBTsSC7GSxCdQgbLaIbYINAS20Br4Kknz/mrkE5gbrUqtr6FV/Qf1gMRJHQi8dNUhWjlNU4=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6ee8fdc61f79ca7b8b57d8e9e8aa2d55f979b9badc854f2abfd8ec470baad8f8fd72af0fea7c3b92af1afe5d6d93ef1b9a6d9f725f7acb7a2ea5e8cbfb9bae2668798a5d3f23e97908ad9ae42a7bc83a3c54394bdab97f47bbca7b78ee968f68df7b8fc70b09e9c94d249f5999d99c27093b9aeade443a28787afc459f2f08e93b741a9b2b6d0f07aa99bfb88e17a97afbc93b54e96f19f87b46d8f8e86a9d463fcbc82b6eb5daab482b6b737e2a3; gdxidpyhxdE=yLwuK8AuESELlZ7boQ40jGx8HY5HzTXRuwjkHTCQT+9fptfUsUtau+lbPRRqXeTjlDrAtkyAMMfEau+qZWWhRXebsStxio6Khri74qwxbD+LGU/6BZ\QbvsUoPAdM0qRHVaVYaSRlCX+jZA8dIEHMJV8acBAjrwT8siALGIszCEhjga9:1664260970830; captcha_session_v2=2|1:0|10:1664260071|18:captcha_session_v2|88:QTNrdUx4elNpaElBbVN3c3ZyQjAvancyVjB6VEZjTDE4RW5VTmFpOFBKVmxHMEw4ZDZMazRBNUZQakIyNlhrSw==|791ec050dfbd7f65c1b12cb8fdc0053deb1c1f49eec51daad7cc62d373a6e88a; captcha_ticket_v2=2|1:0|10:1664260086|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfUkpKanpFV3otMkg0OEltSEFTVEt6ODI4LU56aDhQY2tPVENLX1k2OHJxMi4wQU04T21yTTFfNVVobml0RWVHYmJsOWlfR2FkRncwOHJEVXJBcmpvOWRqbm5lMWJkVVJiZlpUZ0R6UVpKRTlfVnNXSVBoTkk3RmRxR0FsTGFpQjRiU2prMnkyWENHbjU0ZEhFV2ZiX2RZeFhWWUxIdFZaTWtCOXk5WXg4cXk5bVJZTWlNWEpqWTIwYXYuTmlFaUJGQVZ4TVJNTEpLdEVwa3pfaFZvLXFDbVo3bUVYbEcxT0twcGpNWU4uRVBFWEE4dmM3R1JTbTJBZGdJMkdYVTFHb1Zrb3E3QmF1c1g4YkNuaURGdHVVRlc3MHBGNFpjY1RYWmtKN0VGbWRueFFBdWNYQzAyT3FFSVlzdXRFbEpVR1lKV2N5alhHLm5yT3BNdW9WWExqc1F5WWhSSEZ0Uzl0QkdBaEJKaDhCalhaaHJGVTlnMWZoY2NxTG1kWEdIY1pDc3VreFhSb0IyeDlHVFhBdVVVVjRJNjFJU0Q4a09BV0xIZnJRRC5rUmRPRjBUNHZTTGZsaldDS0o4QkVQc2Z3OXJ4NWRIblRkelBGdjdYR0RPR21uejloYlBKWkNHN25FbEdaV0lCcGZyN3g5YlQ0UzF2X2V5UVN1SFdyMyJ9|c648a4530f1b83304e312e00d4e0cf58bacadb26f2a619b2b577e7679277570e; z_c0=2|1:0|10:1664260087|4:z_c0|92:Mi4xNFFUU0N3QUFBQUFBSUpMSVNMRThGU1lBQUFCZ0FsVk45dVVmWkFBNDR5bzk3Z21XemtHSVZ5eExZa3F0Q1VJXzJ3|cd9e24ef6e177d0259392edba21c0e132f6774ea889e383c2a6e7c62eece61be; _xsrf=d5cacfd0-3e4a-4aa9-a848-228497ce2dfc; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1664667624,1665244636,1665326725,1665413391; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1665413391; tst=r; NOT_UNREGISTER_WAITING=1; SESSIONID=C8RJDMflxnUL9QHsseQf5BNHlxc2XXRHYLa2Hig2w4R; JOID=UFkRA08HBuLQVSmveAXDdNE2mOprRzu0nhdnzBB5a7KYaH7kDg42prFQL654mvtiVoj7bS8Aq0FHJ1cIib4BECc=; osd=V1EXA0oADuTQUC6nfgXGc9kwmO9sTz20mxBvyhB8bLqeaHvjBgg2o7ZYKa59nfNkVo38ZSkArkZPIVcNjrYHECI=; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1665414502|1665413389'}
    data = asyncio.run(asynCrawl('https://www.facebook.com/', timeout=120, cookie=cookie))
    print(data.decode('utf-8'))

