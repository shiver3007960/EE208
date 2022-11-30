import asyncio
import aiohttp
from lxml import etree
from lxml.html.clean import Cleaner
from functools import reduce
import re
import json
from urllib import parse
import os
from sys import exit
from TextProcessor import TextProcessing
from crawler import standard_request
import cloudscraper
class Scrapy:

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
    weiboCookie = {'SUB':'_2AkMVjQcMf8NxqwJRmfkVy23jbopxyw_EieKj0fbXJRMxHRl-yT9jqm0CtRB6Pg0p45zdEiw4EaR9GM3XPR0mxp5bx6mg; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WW7P3WJFnAIxb5vLnDwlfWF; SINAGLOBAL=7515420940606.472.1657899068870; ULV=1665407385061:2:1:1:2226771643602.4453.1665407385049:1657899068872; XSRF-TOKEN=7DncEeATqZcK6aS1ANxpVqzn; WBPSESS=rcUsgxdBPA3YG5ZaoysyzNeY-qzYWf8WUFWSKIKWbevtlbGnr3lOF0Fn0fipX5Uuq-hcmjQ63esGDgXBrM0K5CftNAKwePmZccYq4XnBfPf5_yl7LF-JcFBmphpk-Qw_JpXLOGUmQQaUq4a4pjxxvX1DS2pEK1-wUP1kgIxJH1I='}
        
    def __init__(self) -> None:
        pass

    @staticmethod
    def TokenizeChinese(content):
        pat = re.compile('[\u4e00-\u9fa5，。、？！《》‘’“”：；]+')
        res = reduce(lambda a, b: a + ' ' + b, map(lambda element: element.group(), re.finditer(pat, content)), '')
        return res

    @staticmethod
    def htmlCleaner(topboard):
        clear = Cleaner(style=True, scripts=True, page_structure=False)
        topboard = clear.clean_html(topboard)
        topboard =  etree.HTML(topboard)
        return topboard

    @staticmethod
    async def asynCrawl(url, params = None, semaphore = asyncio.Semaphore(20), timeout = 2, cookie = None, bytesRequired = False):
        try:
            async with semaphore:
                timeout = aiohttp.ClientTimeout(total=timeout)
                conn = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(timeout=timeout, connector=conn, cookies=cookie) as session:
                    async with session.get(url, params=params) as response:
                        if bytesRequired:
                            return await response.read()
                        return await response.text()
        except Exception as error:
            print('error Aiohttp ' + str(error))

    @staticmethod
    async def main(urls, params = None, semaphore = asyncio.Semaphore(20), timeout = 20, cookies=None):
        task = [asyncio.ensure_future(Scrapy.asynCrawl(url, params=params, semaphore=semaphore, timeout=timeout, cookie=cookies)) for url in urls]
        return await asyncio.gather(*task)

    @staticmethod
    def storeImg(url, Referer = None):
        # Given a imgUrl and an optional Referer, store it in the directory and return its directory path
        # Be careful t0 change the relative path when moving this function
        dirpath = os.path.join('app', 'static', 'image', 'imgStore')
        parseRes = parse.urlparse(url).path.rsplit('/')
        urlpath = os.path.join(dirpath, parse.urlparse(url).netloc, *parseRes[0:-1])
        if not os.path.exists(urlpath):
            os.makedirs(urlpath)
        imgpath = os.path.join(urlpath, parseRes[-1])
        if os.path.exists(imgpath):
            imgpath = imgpath.replace('app', '..', 1)
            return imgpath
        try:
            if Referer is not None:
                content = asyncio.run(Scrapy.asynCrawl(url=url, params={'Referer':Referer}, bytesRequired=True))
            else:
                content = asyncio.run(Scrapy.asynCrawl(url=url, bytesRequired=True))
            with open(imgpath, mode='wb') as f:
                f.write(content)
        except Exception as error:
            print('Error encountered when requesting imgURL ' + str(error))
        imgpath = imgpath.replace('app', '..', 1)
        return imgpath

    @staticmethod
    def addBaiduHotspot():
        def addhotspot(element, hotspots):
            imgsrc = element.xpath('./img[starts-with(@class, "line_")]')[0].get('src')
            title = element.xpath('.//div[contains(@class, "single-text")]')[0].text
            content = element.xpath('.//div[contains(@class, "hot-desc")]')[0].text
            num = element.xpath('.//div[contains(@class, "trend_")]/div[contains(@class, "hot-index")]')[0].text
            # imgsrc, titlle, content, and popularity
            hotspots.append((imgsrc, title, content, int(num)))
        hotspots = list()
        content = asyncio.run(Scrapy.asynCrawl('https://top.baidu.com/board?tab=realtime', None, asyncio.Semaphore(5), 10))
        topboard = Scrapy.htmlCleaner(content)
        mapObj = list(map(lambda element: addhotspot(element, hotspots), topboard.cssselect('div[class^="category-wrap"]')))
        return hotspots
    
    @staticmethod
    def formatBaiduHotSpot_forForm():
        Hotspots = Scrapy.addBaiduHotspot()
        hotspots = dict()
        hotspots['Description'] = list()
        hotspots["href"] = list()
        def addformat(element):
            nonlocal hotspots
            hotspots['Description'].append(element[1].strip())
            hotspots["href"].append('https://www.baidu.com/s?wd=%s'%element[1].strip())
        mapObj = list(map(addformat, Hotspots))
        return hotspots

    @staticmethod
    def formatBaiduHotSpot_forNews():
        Hotspots = Scrapy.addBaiduHotspot()

    @staticmethod
    def addBaiduMovie():
        def addhotspot(element, hotspots):
            imgsrc = element.xpath('./img[starts-with(@class, "line_")]')[0].get('src')
            title = element.xpath('.//div[contains(@class, "content_")]/a/div[contains(@class, "single-text")]')[0].text
            info = element.xpath('.//div[contains(@class, "content_")]/div[contains(@class, "single-text")]')[0].text
            intro = element.xpath('.//div[contains(@class, "intro")]')
            if len(intro) > 1:
                intro = reduce(lambda a, b: a.text + ' ' + b.text, intro)
            else:
                intro = intro[0].text
            num = element.xpath('.//div[contains(@class, "trend_")]/div[contains(@class, "hot-index")]')[0].text
            #imgSrc, Name, longdescription, cast, popularity (Movies)
            hotspots.append((imgsrc, title, info, intro, num))
        hotspots = list()
        topboard = Scrapy.htmlCleaner(asyncio.run(Scrapy.asynCrawl('https://top.baidu.com/board?tab=movie', None, asyncio.Semaphore(5), 10)))
        mapObj = list(map(lambda element: addhotspot(element, hotspots), topboard.cssselect('div[class^="category-wrap"]')))
        return hotspots

    @staticmethod
    def addBaiduTvSeries():
        def addhotspot(element, hotspots):
            imgsrc = element.xpath('./img[starts-with(@class, "line_")]')[0].get('src')
            title = element.xpath('.//div[contains(@class, "content_")]/a/div[contains(@class, "single-text")]')[0].text
            info = element.xpath('.//div[contains(@class, "content_")]/div[contains(@class, "single-text")]')[0].text
            intro = element.xpath('.//div[contains(@class, "intro")]')
            if len(intro) > 1:
                intro = reduce(lambda a, b: a.text + ' ' + b.text, intro)
            else:
                intro = intro[0].text
            num = element.xpath('.//div[contains(@class, "trend_")]/div[contains(@class, "hot-index")]')[0].text
            #imgSrc, Name, longdescription, cast, popularity (TVSeries)
            hotspots.append((imgsrc, title, info, intro, num))
        hotspots = list()
        topboard = Scrapy.htmlCleaner(asyncio.run(Scrapy.asynCrawl('https://top.baidu.com/board?tab=teleplay', None, asyncio.Semaphore(5), 10)))
        mapObj = list(map(lambda element: addhotspot(element, hotspots), topboard.cssselect('div[class^="category-wrap"]')))
        return hotspots

    @staticmethod
    def addWeiboHotspot():
        urls = ['https://weibo.com/ajax/statuses/topic_band?sid=v_weibopro&category=all&page=%s&count=10'%number for number in range(1, 4)]
        content = asyncio.run(Scrapy.main(urls=urls, cookies=Scrapy.weiboCookie))
        print(content)

        Hotspot = list()
        def addHotspot(dic):
           
            nonlocal Hotspot
            topic = dic['topic']
            newsSource = dic['claim']
            newsSource = re.search('[\d]+_([\u4e00-\u9FFF]+)$', newsSource).group(1)
            imgSrc = dic['images_url']
            content = dic['mblog']['text']
            content = Scrapy.TokenizeChinese(content)
            popularity = int(dic['mention']) + int(dic['read'])
            category = dic['category']
            category = re.search('^([\u4e00-\u9FFF]+)(?=[｜|])', category).group(1)
            
            Hotspot.append((topic, newsSource, imgSrc, content, popularity, category))
        
        mapObj = list(map(lambda element: list(map(addHotspot, json.loads(element)['data']['statuses'])), content))
        return Hotspot

    @staticmethod
    def formatWeiboHotspot_fornews(newsContent):
        contents = Scrapy.addWeiboHotspot()
        
        def _addhotspot(element, newsContent):
            newsContent['website icon imgsrc'].append('')
            newsContent['website href'].append('')
            newsContent['website URLtitle'].append(element[1])
            newsContent['News Title'].append(element[0])
            newsContent['News Content'].append(element[3])
            newsContent['News Href'].append('https://www.baidu.com/s?wd=%s'%element[0])
            imgPath = Scrapy.storeImg(element[2])
            newsContent['News imgSrc'].append(imgPath)
            newsContent['News Additional information'].append('')
        mapObj = list(map(lambda element: _addhotspot(element, newsContent), contents))
        return newsContent

    @staticmethod
    def drawPic():
        pass
if __name__ == "__main__":

    #Pexel
    pexel = '{"_gaexp":"GAX1.2.QPVeTCo4QqGdu--TWlKpuw.19336.4", "_fbp":"fb.1.1664628803073.1152147209", "_hjSessionUser_171201":"eyJpZCI6IjNkMjgzNjE1LTA3NTEtNTk2Yi1iOTU5LTA5MWQ2ZTVmNjM1MyIsImNyZWF0ZWQiOjE2NjM1ODcxNzc5NzYsImV4aXN0aW5nIjp0cnVlfQ== locale=en-US","NEXT_LOCALE":"en-US","_gid":"GA1.2.1435658365.1665488097"} '#ab.storage.deviceId.5791d6db-4410-4ace-8814-12c903a548ba=%7B%22g%22%3A%22d7529444-9843-8ce8-a1ed-c9dd1a77d447%22%2C%22c%22%3A1665244719102%2C%22l%22%3A1665549192184%7D; _hjIncludedInSessionSample=0; _hjSession_171201=eyJpZCI6IjUzNTVhM2JlLTI2ZmEtNGM2OS04ZDJkLWM2N2Q4MDRiZmIwNyIsImNyZWF0ZWQiOjE2NjU1NDkyNzAyOTEsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; ab.storage.sessionId.5791d6db-4410-4ace-8814-12c903a548ba=%7B%22g%22%3A%22b57c65cd-499b-c533-1c97-47c00cdb1eb3%22%2C%22e%22%3A1665551713782%2C%22c%22%3A1665549192183%2C%22l%22%3A1665549913782%7D; __cf_bm=VmrraiaNbwljYyXmItcdT0i4awK0q3t5ZQIlhJsMNJs-1665550374-0-AZqi9NFz8ZhESqZdBJzhIpHK/7Ja/yi5hgxlgh+1n+vsdAm0pR7SG39WKYt+gqjMtylH/R8ACVk3ti1Vik0jooQiS+8hWK6zHYfH68IJkKBuDJVjv4GfpGHLxXF2nVgT9dLZPe3KD+V481MQUFfywcux2XLJm63Pbm5OAegFtzmZ; _ga_8JE65Q40S6=GS1.1.1665549158.8.1.1665550439.0.0.0; _ga=GA1.1.376656959.1663587177; _pexels_session=gEWzE7%2FqwPyKu4tXAtCJIslwQUqMxfhgevJ1%2FJlsinvl7zvsgi%2F2VYNaMRk%2F0jq2WJ9SQwzqjfr3ZuolVwCAQcSW04VBWri5qs1Dn12O9L7F1AmTe%2Btn6hZzsuevrUBb2UemRSoMPnwOFaKpsNvTgL19DZkDVjxXIWAz%2FZX3x%2BS6cP3g%2Fjsjhi28u4ZuteUFcz2fHdOpnMuxHO6O0Qbt5fmwVaI0o0av1FDN0op5o%2B86pyyj%2BfxqnmMosc8Tz2GhF1qyrr3NmQpLRuEojV2eaf5Mwh492TY%3D--GEHRVd3iRai0EkZb--%2FrOhT0bI1kixoT07kKb4jQ%3D%3D}'
    #Pixabay
    pixabay = {"is_human":"1", "_ga":"GA1.2.1181954266.1665550125","_gid":"GA1.2.261480469.1665550125", "_hjSessionUser_920442":"eyJpZCI6Ijk5ZDhmYjUzLWNlODQtNTE4NC05ZTg0LWZkYmZkMzZmNTVhZCIsImNyZWF0ZWQiOjE2NjU1NTAxMjYzMzMsImV4aXN0aW5nIjp0cnVlfQ==","__cf_bm":"TUodNE.Z7.uFKKSyaMAiyKPrjXoqPc0TmpTwzOAEEa8-1665558587-0-AbJItMJqEngAcrTkXuqUZYBeA0Wd35jDO36BPB/M1+yqNSydiDg7tVGz//WlhMo6LAZaEK1Wwpt1a0mV45gelHo=", "_hjIncludedInSessionSample":"0","_hjSession_920442":"eyJpZCI6IjA1NzY2OWZiLTY3YzItNDQ1MC1iMTQxLWY1NjI5NjJiYjAxNCIsImNyZWF0ZWQiOjE2NjU1NTg1ODg3OTMsImluU2FtcGxlIjpmYWxzZX0=" ,"_hjAbsoluteSessionInProgress":"1","anonymous_user_id":"e741ca9654f044b39a80ecb9f6ed2298","csrftoken":"w8TfMSIcu4achzW7nj7pgJpDwMjlISS7TwHEHzv2D6R4vIqFas5mkINue91qhfVm","OptanonConsent":"isGpcEnabled=0&datestamp=Wed+Oct+12+2022+15%3A09%3A49+GMT%2B0800+(China+Standard+Time)&version=6.31.0&isIABGlobal=false&hosts=&consentId=5f2bf2fd-15ac-44a5-a285-af4607d84e3d&interactionCount=1&landingPath=https%3A%2F%2Fpixabay.com%2Fzh%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1","client_width":"603"}
    #cookie = json.loads(pixabay)
   
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',\
             'referer':'https://pixabay.com/'}
    #print(Scrapy.addWeiboHotspot())
    #content = asyncio.run(Scrapy.asynCrawl(url='https://nytimes.com', timeout=10, params=headers, cookie=pixabay))
  
    a = TextProcessing()
