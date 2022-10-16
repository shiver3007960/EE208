
import re
import jieba
from urllib import request
from lxml import etree
from lxml.html.clean import Cleaner
from lxml import html
from urllib import parse
from functools import reduce
from difflib import Differ
from math import pow, log2
from func_timeout import func_set_timeout
import func_timeout
from crawler import standard_request
from json import loads

class TextProcessing():

    with open(r'stopwords/cn_stopwords.txt', 'r') as file:
        stopwords = set(map(lambda string: string.strip(), file.readlines()))
        stopwords = stopwords

    downloadEndswith = {'\.txt', '\.doc', '\.rtf', '\.pdf', '\.zip', '\.rar', '\.jar', '.exe', '.tar.gz', '.dll'}
    sourceEndswith = {'\.wav', '\.mp3', '\.mp4'}
    # To avoid scenarios like data:image/jpeg;base64,/9j/4AAQSkZJ...
    imgEndswith = {'mpeg', 'gif', 'jpg', 'svg', 'jpeg', 'image', 'webp', 'png', 'base64'}
    downloadPattern = '.+?(' + '|'.join(downloadEndswith) + r'){1,2}'
    sourcePattern = '.+?(' + '|'.join(sourceEndswith) + r'){1,2}'
    imgPattern = '.+?(' + '|'.join(imgEndswith) + r'){1,2}'
    
    def __init__(self) -> None:
        
        self.charset = 'utf-8'
        self.language = None
        jieba.enable_parallel(4)
        
    @staticmethod
    def clean_html(html):
        """
        Copied from NLTK package.
        Remove HTML markup from the given string.

        :param html: the HTML string to be cleaned
        :type html: str
        :rtype: str
        """
        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        cleaned = re.sub(r"  ", " ", cleaned)
        return cleaned.strip()

    #Return a two-element tuple, the first index is the original query, the second index is the URl
    @staticmethod
    def _vaildURL(query):
        urlPattern = '/;；?#a-zA-Z0-9\._=-'
        searchHTTP = re.search('(https:/|http:/|ftp:/)[' + urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', query)
        if searchHTTP is not None:
            query = re.sub('(https:/|http:/|ftp:/)[' + urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', '', query)
            return (query, searchHTTP.group(0))
        searchWWW = re.search('(www\.|wwww\.)[' +  urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', query)
        if searchWWW is not None:
            query = re.sub('(www\.|wwww\.)[' +  urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', '', query)
            return (query, 'https://' + searchWWW.group(0))
        searchCOM = re.search('(?:(?<=[^' + urlPattern + '])|(?<=^))[' +  \
            urlPattern + ']{4,}[(.com)|(.cn)][' + urlPattern + ']*(?=([^' + urlPattern + ']|$))', query)
        if searchCOM is not None:
            query = re.sub('([^' + urlPattern + ']|^)[' +  \
            urlPattern + ']{4,}[(.com)|(.cn)][' + urlPattern + ']*(?=([^' + urlPattern + ']|$))', '', query)
            return (query, 'https://' + searchCOM.group(0))
        return (query, None)

    @staticmethod
    def TokenizeMixedLan(content):
        if not isinstance(content, str) or len(content) < 2:
            return
        pat = re.compile('[\u4e00-\u9fa5，。、？！《》‘’“”：；]+')
        
        last_tokenized = 0
        def _Tokenize(matchObj):

            if matchObj is None:
                return ''
            nonlocal last_tokenized
            filterObj = filter(lambda string: string not in TextProcessing.stopwords, jieba.cut(matchObj.group()))
            
            try:
                if filterObj:
                    tokenized = ' '.join(filterObj)
                else:
                    tokenized = ''
            except AttributeError as e:
                return ' '
            except ValueError as e:
                return ' '
            res = content[last_tokenized:matchObj.span()[0]].strip() + tokenized
            last_tokenized = matchObj.span()[1]
            return res

        res = reduce(lambda a, b: a + ' ' + b, map(_Tokenize, re.finditer(pat, content.strip())), '')

        return res

    @staticmethod
    def TokenizeChinese(content, jiebaRequired = True, cut_for_search = False):
        pat = re.compile('[\u4e00-\u9fa5，。、？！《》‘’“”：；]+')

        if not cut_for_search:
            def _Tokenize(matchObj):
                tokenized = ' '.join(filter(lambda string: string not in TextProcessing.stopwords, jieba.cut(matchObj.group())))
                return tokenized
        else:
            def _Tokenize(matchObj):
                tokenized = ' '.join(filter(lambda string: string not in TextProcessing.stopwords, jieba.cut_for_search(matchObj.group())))
                return tokenized

        if not jiebaRequired:
            res = reduce(lambda a, b: a + ' ' + b, map(lambda element: element.groups(), re.finditer(pat, content)), '')
            return res
        try:
            res = reduce(lambda a, b: a + ' ' + b, map(_Tokenize, re.finditer(pat, content)), '')
        except AttributeError as e:
            return ' '
        except ValueError as e:
            return ' '
        return res

    def Tokenize(self, content):
        if self.language is None:
            return TextProcessing.TokenizeMixedLan(content)
        elif re.match(r'''zh-.*?cn | ZH-.*?CN | zh-.*?CN''', self.language) is not None:
            return TextProcessing.TokenizeChinese(content)
        else:
            return TextProcessing.TokenizeMixedLan(content)


    @staticmethod
    def display(page):  # str->null
        if isinstance(page, str):
            pat = re.compile(r'(.+(\\x[0-9a-zA-Z]{2,}).*)+|(.+(%[0-9a-zA-Z]{2,}).*)+|(.+(\\u[0-9a-zA-Z]{2,}).*)+', re.DOTALL)
            if re.match(pat, page.__repr__()) is not None:
                #print('Contains Chinese!')
                #Deal with '\x4e\x96\xc3\xd5' form
                s = page.encode('unicode_escape').decode('utf-8').replace('\\x', '%')
                #Deal with '%E8%C3%A2%D6' form 
                #The 'raw_unicode_escape' cannot be changed to 'unicode_escape', or the display will collapse
                temp = parse.unquote(s).encode('raw_unicode_escape').decode()
                #Deal with '\u54f4\u675f\uf436\ug623'form
                print(temp.encode('utf-8').decode('unicode_escape'))
            else:
                print(page)
    
    # (stored_directory_path, HTMLDocTitle, URL, Content, Links, Images)
    def parseHTML(self, content = '', baseURL = ''):
        
        if not isinstance(content, str) and not isinstance(content, bytes):
            return None

        tree = etree.HTML(content)
        
        if tree is None:
            return None

        charsetTag = tree.xpath("//head/meta[contains(@content,'charset=')]")
        if charsetTag:
            self.charset = re.search(r'charset=(.+)\b|charset =(.+)\b',\
            charsetTag[0].get('content')).group(1).strip()
        else:
            charsetTag = tree.xpath("//head/meta[@charset]")
            if charsetTag:
                self.charset = charsetTag[0].get('charset')
            else:
                self.charset = 'utf-8'

        languageTag = tree.xpath("/html[@lang]")
        if languageTag:
            self.language = languageTag[0].get('lang')
            
        #Deal with encoding problem
        if self.charset != 'utf-8' and self.charset != 'UTF-8':
            try:
                tree = etree.HTML(content.decode(self.charset))
            except UnicodeDecodeError as error:
                print("******Unicode Decode Error encountered:******")
                print("self.charset is %s"%self.charset, "BaseURL is %s"%baseURL)
                return None
            except Exception as error:
                print("****** Unknown parseHTML Error encountered:******")
                print(str(error))

        if tree.base is not None:
            baseURL = tree.base
        
        info = list()
        # The stored path
        info.append(baseURL)
        # Title of the HTMLDOc
        title = tree.xpath('//title')
        title = "None" if not title else title[0].text
        info.append(title)
        # Title of the URL
        info.append(baseURL)
        # Contents of the URL
        info.append(self.parseContents(tree))
        # Links
        info.append(self.parseLinks(tree, baseURL))
        # Picture
        info.append(self.parseImage(tree)) # return a dict
        return info

    @staticmethod
    def parsePath(url):
        netloc = parse.urlparse(url, allow_fragments=False).netloc
        afterFix = ''.join(parse.urlparse(url)[2:5])
        return(netloc, afterFix)

    def parseContents(self, tree):
        remove_tags = frozenset(['footer'])
        clean = Cleaner(style=True, scripts=True, links = False, remove_tags = remove_tags)
        htmlBody = tree.xpath('//body')
        if not htmlBody:
            return ''
        sanitized = clean.clean_html(etree.tostring(htmlBody[0]).decode(self.charset))
        sanitized = self.Tokenize(TextProcessing.clean_html(sanitized))
        return sanitized

    def parseLinks(self, tree, baseURL):
        # 三种连接形式：资源下载链接，网页元素链接，外部或内部网址链接 
        safe_attrs = frozenset(['href'])
        clean = Cleaner(style=True, scripts=True, links = True, safe_attrs = safe_attrs)
        htmlBody = tree.xpath('//body')
        if not htmlBody:
            return ''
        tree = etree.HTML(clean.clean_html(etree.tostring(htmlBody[0]).decode(self.charset)))
        res = [set(), set(), set()]



        def _sortHref(element):
            href = element.get('href')
            downloadMatch = re.match(TextProcessing.downloadPattern, href)
            sourceMatch = re.match(TextProcessing.sourcePattern, href)
            if downloadMatch is None and sourceMatch is None:
                if not parse.urlparse(href).scheme:
                    href = parse.urljoin(baseURL, href)
                res[0].add(href)
                #网址
            elif downloadMatch is not None:
                #下载链接
                res[1].add(href)
            else:
                #网页元素
                res[2].add(href)
        
        filterObj = filter(lambda element: not element.get('href').startswith('#') or not element.get('href').startswith('/#'),\
                 tree.xpath('//a[@href and @rel != "nofollow"] | //a[@href] | //iframe[@src]'))
        mapObj = list(map(_sortHref, filterObj))
        return res

    # Given the lxml tree Object and an optioanl baseURl, return a dict
    # The dict's key is the ImgHref, the value is Pic Brief information

    def parseImage(self, tree, imgAttr = 'src', rawRequired = False):

        safe_attrs = frozenset(['src','alt','title'])
        remove_tags = frozenset(['footer', 'nav', 'form', 'link', 'style'])
        clean = Cleaner(style=False, scripts=True, links = False, safe_attrs = safe_attrs, remove_tags = remove_tags)
        
        if not rawRequired:
            tree = etree.HTML(clean.clean_html(etree.tostring(tree).decode(self.charset)))

        res = dict()

        filterObj = list(filter(lambda element: self._sortImg(element, self.charset, imgAttr, res), tree.xpath('//img[@%s] | //embed[@%s] |\
            //iframe[@%s] | //div[contains(@style, "background")]'%(imgAttr, imgAttr, imgAttr))))
        
        return res

    def _sortImg(self, element, charset, imgAttr = 'src', res = None):
            
            href = element.get(imgAttr)
            # Be compatible with scenerios like style="background-image: url (https://media.gettyimages.com)"
            if href is None:
                href = re.match(r'''((background-image)|(background)):(\s)?url(\s)?\(([^\s]+?)(\s){0,2}\)''', \
                        element.get('style'))
                if href is None:
                    return 
                href = href.group(6)
            
            downloadMatch = re.search(TextProcessing.imgPattern, href)
            if downloadMatch is None:
                return
            
            imgInfo = self._retrieveImgInfo(element, href, charset)

            if imgInfo is not None:
                res[href] = imgInfo
        

    @staticmethod
    def _getBasicInfo(element):
        classOrID = dict()
        classOrID['class'] = element.get('class') if element.get('class') is not None else None
        classOrID['id'] = element.get('id') if element.get('id') is not None else None
        
        #print(re.search('(?<=(\b|\s))(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))|(?<=^)(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))', ' '.join(element.attrib.keys())))

        identifier = re.search('(?<=(\b|\s))(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))',\
            ' '.join(element.attrib.keys()))
        if identifier is None:
            identifier = re.search('(?<=(^))(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))', \
                ' '.join(element.attrib.keys()))
        classOrID['identifier'] = identifier.group(2) if identifier is not None else None
        return classOrID

    @staticmethod
    def _common(string1, string2):
        
        if not isinstance(string1, str) or not isinstance(string2, str) or \
            len(string1) < 3 or len(string2) < 3:
            return 0
        differ = Differ()
        return reduce(lambda a, b: a + b, map(lambda fragment : 1 if not fragment.startswith('-') \
            and not fragment.startswith('+') else 0, differ.compare(string1, string2)))

    def _filterAttrorText(self, span) -> set:
        if (not isinstance(span, str) or len(span) < 1):
            return set()
        span = span.lower()
        span = re.sub(r'(\d|\s){6,}|([0-9]{1,}[a-zA-Z]{1,}){3,}', '', span)
        #last one to be compatible with Chinese
        span = re.sub(r'[$#@&^%*{}[/\\]|[()=_-]|[。？！]', " ", span)
        
        # When the title is too long, look for overlapping characters
        retrieveCounter = 0
        if len(span) > 125:
            while retrieveCounter < 10:
                matchObj = re.search(r'(\b[\w\d]{4,}?\b).+?\1.+?\1.', span)
                
                if matchObj is None:
                    break
                span = span.replace(matchObj.group(1), '')
                retrieveCounter += 1
            
        # Looking For meaningful segments
            segments = set(filter(lambda segment: re.match('[\w\s]{3,}', segment) is not None, map(lambda matchObj: matchObj.group(2), \
                re.finditer('(?<=("|<|>|,|;|:|，|。|；|：))([\w\s、·\.+]{6,})(?=(,|;|:|，|。|；|：|$|<|>|"))', span))))
        else:
            segments = set((re.sub(r'''[<>,;:，。；：+|"“”‘’']''', ' ', span).split()))
        return segments

    def _filterTags(self, toFilter, scope, info_Weight, classOrID, codec):
        
        if (toFilter.tag == 'em' or toFilter.tag == 'strong' or toFilter.tag == 'p') and scope < 3:
            result = self._filterAttrorText(toFilter.text)
            
            if len(result) > 0 and len(result) < 9:
                info_Weight.append((0.8 * pow(0.8, scope), TextProcessing.TokenizeChinese(' '.join(result))))
                return

        elif (toFilter.tag == 'div' or toFilter.tag == 'span' or toFilter.tag == 'a'):
            
            identifier = re.search('(?<=(\b|\s))(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))',\
            ' '.join(toFilter.attrib.keys()))
            if identifier is None:
                identifier = re.search('(?<=(^))(data.{0,5}?([0-9]*[a-zA-Z]*[0-9]+)+?(?=(\b|$|\s)))', \
                    ' '.join(toFilter.attrib.keys()))
            # If there is not a match, then the credentaility should descend
            if not ((toFilter.get('class') is not None and TextProcessing._common(toFilter.get('class'), classOrID['class']) > 5) or\
                (toFilter.get('id') is not None and TextProcessing._common(toFilter.get('id'), classOrID['id']) > 5) or \
                    (classOrID['identifier'] is not None and identifier is not None and \
                    TextProcessing._common(identifier.group(2), classOrID['identifier']) > 5)):
                scope *= 1.15

        if (toFilter.tag == 'div' or toFilter.tag == 'span' or (toFilter.tag == 'a' and scope != 1)) and scope < 3:
            content = toFilter.text if toFilter.text is not None else ''
            content += toFilter.tail if toFilter.tail is not None else ''
            text = (content) if isinstance(content, str) else ''
            
            if toFilter.get('title') is not None:
                result = self._filterAttrorText(text)
                if result and re.search(r'[\u4e00-\u9fff]', ' '.join(result)) is not None:
                    info_Weight.append((0.75 * pow(0.55, scope), TextProcessing.TokenizeChinese(' '.join(result))))

            filterObj = list(filter(lambda fragment: len(fragment) > 6, \
                map(lambda item: self._filterAttrorText(item), map(lambda x: x[1], toFilter.items()))))
            
            if len(filterObj) > 0:
                list(map(lambda res: info_Weight.append((0.8 * pow(0.55, scope), res)), filterObj))

            result = self._filterAttrorText(text)

            if len(result) > 0 and len(result) < 20:
                info_Weight.append((0.75 * pow(0.6, scope), TextProcessing.TokenizeChinese(' '.join(result))))
                return
            
            mapObj = list(map(lambda htmlTag: self._filterTags(htmlTag, scope - 0.05, info_Weight, classOrID, codec), toFilter.iterchildren()))

        elif toFilter.tag == 'a' and scope == 1:
            
            content = toFilter.text if toFilter.text is not None else ''
            content += toFilter.tail if toFilter.tail is not None else ''
            result = self._filterAttrorText(content)
            if len(result) > 0 and len(result) < 9:
                info_Weight.append((0.75, TextProcessing.TokenizeChinese(' '.join(element))))
                return

    @staticmethod
    def _processInfo(info_Weight):

        if len(info_Weight) == 0:
            return

        imgInfo = dict()
        def _process(segment):
            matchObj = len(list(re.finditer('[\u4e00-\u9fff]', ''.join(segment[1]))))
            if matchObj > 0:
                segment = (segment[0] * 3 + log2(matchObj) / 15, segment[1])
            imgInfo[segment[0]] = segment[1]

        filterObj = list(filter(_process, info_Weight))

        if len(imgInfo.keys()) == 1:
            return [imgInfo[list(imgInfo.keys())[0]]]
        
        #print([imgInfo[sorted(imgInfo.keys(), reverse = True)[0]], \
            #imgInfo[sorted(imgInfo.keys(), reverse = True)[1]]])
        return[imgInfo[sorted(imgInfo.keys(), reverse = True)[0]], \
            imgInfo[sorted(imgInfo.keys(), reverse = True)[1]]]

    def _retrieveImgInfo(self, element, src, codec = 'utf-8'):

        info_Weight = list()
        #Local Scope: From the origin src
        path = parse.urlparse(src)[2]
        path = re.sub('[_+&~=-]{1,3}', ' ', path)
        def _filterSubElement(matchObj):

            string = matchObj.group(1)
            numFreq = len(list(re.finditer(r'[\d]+', string)))
            segments = list(map(lambda subElement: re.sub(r'(\w*?[\d]{5,}\w*?)+', '', subElement), string.split(' ')))
            # To see if this is like a5d46sf3b3 kind...
            if numFreq / len(segments) > 0.6:
                return
            # To compose a reasonable sentence
            if len(segments) < 3 or len(segments) > 15:
                return 
            info_Weight.append((0.9, ' '.join(segments)))

        filterObj = list(filter(_filterSubElement, re.finditer(r'''(?<=/)([\w\s]+)(?=(/|$|.))|\
                                                            (?<=^)([\w\s]+)(?=(/|$|.))''', path)))
    
        # The Alt and title Tag
        altOption = element.get('alt')
        titleOption = element.get('title')
        if altOption is not None and len(altOption) > 2:
            info = re.sub('[_+&~=/#@!-]{1,3}', ' ', altOption)
            info_Weight.append((1, TextProcessing.TokenizeChinese(info)))
        if titleOption is not None and len(titleOption) > 2:
            info = re.sub('[_+&~=/#@!-]{1,3}', ' ', titleOption)
            info_Weight.append((1, TextProcessing.TokenizeChinese(info)))
        if len(info_Weight) > 0:
            return TextProcessing._processInfo(info_Weight)
        #Outer Text: Rated by the range
        #1.Get the basic information
        classOrID = TextProcessing._getBasicInfo(element)
        #2.filtertags
        filterObj = list(filter(lambda sibling: self._filterTags(sibling, 1, info_Weight, classOrID, codec), list(element.itersiblings(preceding=True, tag=('p', 'span', 'a', 'em', 'strong','div'))) + \
            list(element.itersiblings(preceding=False, tag=('p', 'span', 'a', 'em', 'strong', 'div')))))
        #print('fiter Tags', info_Weight)
        #3.Retrieve and repeat
        scope = 2
        parent = element
        while(scope < 4):
            parent = parent.xpath('..')[0]
            #Find Chinese
            res = TextProcessing.TokenizeChinese(etree.tostring(parent).decode(codec), jiebaRequired=False)
            if len(res) > 0:
                if (not isinstance(res.split(' '), list) and len(res.split(' ')) > 3):
                    print("*********************************")
                    print(res.split(' '))
                    print(type(res.split(' ')))
                    raise Exception("Fuck you")
                info_Weight.append(res.split(' '))
            #If it is the div, load the information and only find the neighbours
            classOrID = TextProcessing._getBasicInfo(parent)
            if parent.tag == 'div':
                index = parent.xpath('..')[0].index(parent)
                right_sibling = parent.xpath('..')[0].xpath('./*[position()=%s]'%(index+2))
                
                left_sibling = parent.xpath('..')[0].xpath('./*[position()=%s]'%(index))
                
                if right_sibling:
                    self._filterTags(right_sibling[0], scope, info_Weight, classOrID, codec)
                if left_sibling:
                    self._filterTags(left_sibling[0], scope, info_Weight, classOrID, codec)
                break
            #If it's the figure or picture tag, we have ascertained the scope
            elif parent.tag == 'figure' or parent.tag == 'picture':
                mapObj = list(map(lambda x: info_Weight.append((0.4 * pow(0.8, scope), TextProcessing.TokenizeChinese(' '.join(x)))), \
                    map(lambda x : self._filterAttrorText(x), parent.itertext())))
                break
            #Other situations
            else:
                filterObj = list(filter(lambda sibling: self._filterTags(parent, scope, info_Weight, classOrID, codec), list(parent.itersiblings(preceding=True, tag=('p', 'span', 'a', 'em', 'strong','div'))) + \
                    list(parent.itersiblings(preceding=False, tag=('p', 'span', 'a', 'em', 'strong', 'div')))))
            scope += 1
        
        return TextProcessing._processInfo(info_Weight)
        
content = '''<span class="title">
新华全媒+丨牺牲77年，“无名烈士”被找回姓名
</span>
<span class="btn-audio"></span>
</h1>
<audio class="hide" id="audioDom" src="" loop></audio>
<div class="pageShare">
<div class="setFont">字体：
<span id="fontSmall">小</span>
<span id="fontNormal" class="active">中</span>
<span id="fontBig">大</span>
</div>
<div class="share">
分享到：<a href="javascript:void(0)" class="wx"></a><a href="javascript:void(0)" class="wb"></a><a href="javascript:void(0)" class="xcx"></a><a href="javascript:void(0)" class="khd"></a>
<div class="wx-ewm"><img /></div>
<div class="xcx-ewm"><img /></div>
<div class="khd-ewm"><img src="http://www.xinhuanet.com/politics/newpage2020/images/qrcode-app.png" /></div>
</div>
</div>
</div>
</div>
</div>
<div class="mheader domMobile">
<h1>
<span class="title">
新华全媒+丨牺牲77年，“无名烈士”被找回姓名
</span>
</h1>
<div class="info">
2022-09-29 16:09:32
<span>
来源：
新华网
</span>
</div>
</div>
<div class="main clearfix">
<div class="main-left">
<div id="detail">
<p>　　新华社杭州9月29日电（记者王俊禄、林光耀）刚获评全国“人民满意的公务员”不久的浙江基层民警柯伟力，日前又通过DNA比对，为77年前牺牲的无名烈士确认身份、找回姓名。</p>
<p>　　故事要从今年夏天说起。6月30日，浙江省台州市路桥区退役军人事务局接到一份协助函，来函单位是南京市高淳区退役军人事务局。</p>
<p>　　函中称，1945年8月，两名新四军战士在东坝战役的游子山战斗期间牺牲，后葬于高淳，请求台州市路桥区退役军人事务局协调台州市公安局路桥分局“团圆工作室”提供技术支持，帮助查找两名先烈的姓名、籍贯及后人信息等。</p>
<p>　　“团圆工作室”负责人柯伟力，是名法医，同时也担任台州市公安局路桥分局刑事科学技术室副主任。2021年以来，柯伟力领衔的“团圆工作室”，利用DNA比对等技术手段，已经为两百多名全国各地的寻亲者找到了家人。</p>
<p style="TEXT-ALIGN: center"><img id="{55B7CBB2-7ACF-41F9-936A-2B21F33F77DA}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878651n.jpg" /></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为柯伟力。（受访者供图）</font></span></p>
<p>　　“烈士牺牲已经有77年，我们也是第一次碰到年代如此久远的物证，这是一个很大挑战。”任务很艰巨，但也很光荣，柯伟力决定接下这个工作。</p>
<p>　　关于烈士的有效信息很少。“我们只有烈士遗骸，在南京市高淳区寻访时了解到，村里有老人还记得，早年间，其中一个烈士墓上有毛竹片做的简单墓碑，碑上用红漆写了‘山东人刘金山’六个字，除此再无其他信息。”柯伟力说。<br /></p>
<p>　　有限的信息给寻找工作带来了很大的困难。为了帮烈士找到家人，柯伟力和团队拼尽全力。“台州市公安局DNA实验室成立了专门检验团队，负责烈士遗骸的检验鉴定和比对工作，采用多种技术手段，最大限度保证了提取质量，最终检验出烈士完整的DNA分型。”柯伟力说。</p>
<p>　　根据烈士DNA数据在数据库中的比对和后期研判，这位烈士极有可能来自山东枣庄刘氏家族。山东、刘氏——仅有的线索和DNA检验结果指向了同一个地方，这是个好消息。但能否找到烈士的家人，一切还是未知。</p>
<p style="TEXT-ALIGN: center"><img id="{0C668735-D306-4829-BE08-1AB95A2EF957}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878661n.jpg" /></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为柯伟力在实验室开展鉴定工作。（受访者供图）</font></span></p>
<p>　　9月7日上午，台州市公安局路桥分局门口，柯伟力脚步匆匆，怀揣着一份“带英雄回家”的任务赶赴山东枣庄，为1945年牺牲在南京的新四军烈士寻找家人。</p>
<p>　　顺着前期的DNA比对结果，柯伟力找到了DNA数据库中比对结果最为接近的刘继军、刘继宝堂兄弟二人，并找到了刘继军已是耄耋之年的父亲刘金山（与烈士刘金山同名），和刘继军年届古稀的叔叔刘金岭。</p>
<p style="TEXT-ALIGN: center"><img id="{0664F9BD-06E3-42F4-A7B9-4C87CAF2F97C}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878621n.jpg" /></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为柯伟力在给刘金山采集血样，用于比对DNA。（受访者供图）</font></span></p>
<p>　　谈话中，两位老人都还记得：1956年前后，他们定居南京的二伯刘毓喜曾返回山东探亲，提到过自己的两个儿子，其中大儿子在南京做生意，二儿子在抗战中加入了共产党的队伍。刘毓喜曾到部队探望过二儿子，之后与二儿子失去了联系。</p>
<p style="TEXT-ALIGN: center"><img id="{DC543F84-41A4-487F-9B52-FCB54FC237EF}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878631n.jpg" /></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为刘金山（前排右）在给柯伟力讲述家族史。（受访者供图）</font></span></p>
<p>　　后来刘毓喜回到了南京，也逐渐和大家族断了联系。2000年前后修族谱的时候，刘氏后人曾到访南京，希望警方帮忙查找这一支后人，无奈时过境迁、物是人非，查找未果。</p>
<p>　　同时，在刘氏族谱中，柯伟力也发现了烈士刘金山的名字，就写在刘毓喜之下。</p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><img id="{7F0E9944-F3DE-4768-AD2B-FD2DA45877A0}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878641n.jpg" /></span></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为刘氏族谱，其中红框部分为1945年牺牲的烈士刘金山，由于该支长期失联，且族中老人记忆模糊，在修族谱时，以刘金岭之名入谱。（受访者供图）</font></span></p>
<p>　　DNA是不会说话的证人。比对结果显示，“烈士刘金山”遗骸检出的基因型与刘金山、刘金岭兄弟二人全部匹配。</p>
<p>　　结合现场走访收获的信息，柯伟力和同事经过综合分析，得出最后的结论：“烈士刘金山”遗骸与刘金山、刘金岭同属一个家族，无名烈士“山东人刘金山”，就是籍贯山东省枣庄市市中区永安镇寨子村刘氏家族的刘毓喜之子刘金山。</p>
<p style="TEXT-ALIGN: center"><img id="{680FED23-BEBB-446F-B1A8-11295D8D5869}" style="MAX-WIDTH: 100%; MARGIN-LEFT: auto; DISPLAY: block; MARGIN-RIGHT: auto" src="1129041895_16644386878671n.jpg" /></p>
<p style="TEXT-ALIGN: center"><span style="COLOR: rgb(51,127,229)"><font color="navy" face="楷体">图为柯伟力在抄录刘氏族谱。（受访者供图）</font></span></p>
<p>　　“这么多年了，我们一直没有放弃寻找这一支脉的亲人，柯警官带来的消息让我们激动又欣慰，这场跨越3个省份的联合寻找也圆了家族的寻亲夙愿。”曾主持重修族谱的刘凯万分感慨、万分感谢。</p>
<p>　　心里的一块石头落地，柯伟力也觉得对烈士有了交代。“既然烈士留下了身世的线索，我们就不能让他继续无名下去，要把无名烈士墓变成有名有姓的墓，供后人祭奠。”柯伟力说。</p>
<p>　　寻找还在继续。另一名据称来自四川的烈士，由于时间久远，其遗骸在烈士墓中受到了损坏，需要花费更多的精力去破解其中的“身世秘密”，柯伟力的团队也一直在努力。</p>
<p>　　“留在数据库里的DNA，就像一颗种子，终有一天会开花结果。”柯伟力说，他将带领“团圆工作室”，让更多失散、破碎的家庭实现“圆满”。</p>
<p>　　为刘金山烈士寻亲的故事，是全国烈士寻亲工作的一个缩影。对于这项工作，全国各地、各部门一直念兹在兹。2021年起，退役军人事务部将烈士寻亲工作列入“我为群众办实事”实践活动清单，探索建立烈士寻亲合作机制。</p>
<div id="articleEdit">
<span class="tiyi1 domPC">
<a href="javascript:void(0);" class="advise">【纠错】</a>
<div class="tiyi01" id="advisebox01" style="display:none">
<div>
<iframe id="jc_link1" style="width:600px;height:350px; float:left;" border="0" marginwidth="0" framespacing="0" marginheight="0" frameborder="0" noresize="" scrolling="no" vspale="0"></iframe>
</div>
<div class="tiyi03">
<div id="jc_close1" style="cursor:pointer"><img src="http://www.xinhuanet.com/images/syicon/space.gif" width="24" height="24" border="0" />
</div>
</div>
</div>
</span>
'''


if __name__ == '__main__':
    
    content = standard_request('http://migu.cn/')
    
    html = TextProcessing()
    
    res = html.parseHTML(content)[5]
    res = loads(str(res))
    print(res['https://www.migu.cn/assets/pc/images/icon_wx.png'])
    