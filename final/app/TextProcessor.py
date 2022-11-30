from email import charset
from email.errors import CharsetError
import re
import jieba
from urllib import request
from lxml import etree
from lxml.html.clean import Cleaner
from lxml import html
from urllib import parse
from functools import reduce
from difflib import Differ
from threading import Thread, Lock
from math import pow, log2
from func_timeout import func_set_timeout
import func_timeout

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

    @staticmethod
    def TokenizeMixedLan(content):
        pat = re.compile('[\u4e00-\u9fa5，。、？！《》‘’“”：；]+')

        last_tokenized = 0
        def _Tokenize(matchObj):
            nonlocal last_tokenized
            filterObj = filter(lambda string: string not in TextProcessing.stopwords, jieba.cut(matchObj.group()))
            tokenized = '' if filterObj is None else ' '.join(list(filterObj))
            """ try:
                tokenized = '' if filterObj is None else ' '.join(filterObj)
            except AttributeError as e:
                print("****************************")
                print(list(filterObj))
                print(type(filterObj))
                print(tokenized)
                print("****************************") """
            res = content[last_tokenized:matchObj.span()[0]].strip() + tokenized
            last_tokenized = matchObj.span()[1]
            return res

        jieba.enable_parallel(4)
        res = reduce(lambda a, b: a + ' ' + b, map(_Tokenize, re.finditer(pat, content.strip())), '')
        jieba.disable_parallel()

        return res

    @staticmethod
    def TokenizeChinese(content, jiebaRequired = True):
        pat = re.compile('[\u4e00-\u9fa5，。、？！《》‘’“”：；]+')

        def _Tokenize(matchObj):
            tokenized = ' '.join(filter(lambda string: string not in TextProcessing.stopwords, jieba.cut(matchObj.group())))
            return tokenized

        if not jiebaRequired:
            res = reduce(lambda a, b: a + ' ' + b, map(lambda element: element.groups(), re.finditer(pat, content)), '')
            return res
        jieba.enable_parallel(4)
        res = reduce(lambda a, b: a + ' ' + b, map(_Tokenize, re.finditer(pat, content)), '')
        jieba.disable_parallel()

        return res

    def Tokenize(self, content):
        if self.language == None:
            return TextProcessing.TokenizeMixedLan(content)
        elif re.match(r'''zh-.*?cn | ZH-.*?CN | zh-.*?CN''', self.language):
            return TextProcessing.TokenizeChinese(content)
        else:
            return content

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
    def parseHTML(self, content = '', baseURL = '', timeout = 2.5, callback = None):
        # (stored_directory_path, HTMLDocTitle, URL, Content, Links, Images)
        @func_set_timeout(timeout)
        def _parseHTML(self, content = '', baseURL = ''):
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
                tree = etree.HTML(content.decode(self.charset))

            if tree.base is not None:
                baseURL = tree.base
            
            info = list()
            # The stored path
            info.append(baseURL)
            # Title of the HTMLDOc
            title = tree.xpath('//title')
            title = 'None' if not title else title[0].text
            info.append(title)
            # Title of the URL
            info.append(baseURL)
            # Contents of the URL
            info.append(self.parseContents(tree))
            # Links
            info.append(self.parseLinks(tree, baseURL))
            # Picture
            info.append(self.parseImage(tree, baseURL)) # return a dict
            return info
        try:
            result = _parseHTML(self, content, baseURL)
            return result
        except func_timeout.exceptions.FunctionTimedOut as error:
            if callback is not None:
                callback()
            else:
                pass

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
    def parseImage(self, tree, baseURL = None, imgAttr = 'src', rawRequired = False):

        safe_attrs = frozenset(['src','alt','title'])
        remove_tags = frozenset(['footer', 'nav', 'form', 'link', 'style'])
        clean = Cleaner(style=False, scripts=False, links = False, safe_attrs = safe_attrs, remove_tags = remove_tags)
        
        if not rawRequired:
            tree = etree.HTML(clean.clean_html(etree.tostring(tree).decode(self.charset)))

        
        res = dict()
        imgInfoLock = Lock()
        imgThreadPool = list()

        def _sortImg(element, charset, imgAttr = 'src'):
            
            href = element.get(imgAttr)
            
            nonlocal res, imgInfoLock
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
                imgInfoLock.acquire()
                res[href] = imgInfo
                imgInfoLock.release()
        
        def _produceThread(element, codec):
            
            nonlocal imgThreadPool, imgAttr
            imgThread = Thread(target=_sortImg, args=(element, codec, imgAttr))
            imgThreadPool.append(imgThread)
            imgThread.setDaemon(True)
            imgThread.start()
            
        filterObj = list(filter(lambda x: _produceThread(x, self.charset), tree.xpath('//img[@%s] | //embed[@%s] |\
            //iframe[@%s] | //div[contains(@style, "background")]'%(imgAttr, imgAttr, imgAttr))))
        
        filterTar = list(filter(lambda imgThread: imgThread.join(), imgThreadPool))
        
        return res
    
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

    def _filterAttrorText(self, span, codec) -> set:
        if (not isinstance(span, str) or len(span) < 1):
            return set()
        span = span.lower()
        span = re.sub(r'(\d|\s){6,}|([0-9]{1,}[a-zA-Z]{1,}){3,}', '', span)
        #last one to be compatible with Chinese
        span = re.sub(r'[$#@&^%*{}[/\\]|[()=_-]|[。？！]', " ", span)
        raw_length = len(span)
        
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
            result = self._filterAttrorText(toFilter.text, codec)
            if len(result) > 0 and len(result) < 9:
                info_Weight.append((0.8 * pow(0.8, scope), result))
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
                result = self._filterAttrorText(text, codec)
                if result and re.search(r'[\u4e00-\u9fff]', ' '.join(result)) is not None:
                    info_Weight.append((0.75 * pow(0.55, scope), result))

            filterObj = list(filter(lambda fragment: len(fragment) > 6, \
                map(lambda item: self._filterAttrorText(item, 'utf-8'), map(lambda x: x[1], toFilter.items()))))
            #print(list(map(lambda item: _filterAttrorText(item, 'utf-8'), map(lambda x: x[1], tree.items()))))
            
            if len(filterObj) > 0:
                list(map(lambda res: info_Weight.append((0.8 * pow(0.55, scope), res)), filterObj))

            result = self._filterAttrorText(text, codec)

            if len(result) > 0 and len(result) < 20:
                info_Weight.append((0.75 * pow(0.6, scope), result))
                return
            
            mapObj = list(map(lambda htmlTag: self._filterTags(htmlTag, scope - 0.05, info_Weight, classOrID, codec), toFilter.iterchildren()))

        elif toFilter.tag == 'a' and scope == 1:
            
            content = toFilter.text if toFilter.text is not None else ''
            content += toFilter.tail if toFilter.tail is not None else ''
            result = self._filterAttrorText(content, codec)
            if len(result) > 0 and len(result) < 9:
                info_Weight.append((0.75, result))
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
        print(element)
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
            info_Weight.append((1, info))
        if titleOption is not None and len(titleOption) > 2:
            info = re.sub('[_+&~=/#@!-]{1,3}', ' ', titleOption)
            info_Weight.append((1, info))
        #print(info_Weight)
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
                mapObj = list(map(lambda x: info_Weight.append((0.4 * pow(0.8, scope), x)), \
                    map(lambda x : self._filterAttrorText(x, codec), parent.itertext())))
                break
            #Other situations
            else:
                filterObj = list(filter(lambda sibling: self._filterTags(parent, scope, info_Weight, classOrID, codec), list(parent.itersiblings(preceding=True, tag=('p', 'span', 'a', 'em', 'strong','div'))) + \
                    list(parent.itersiblings(preceding=False, tag=('p', 'span', 'a', 'em', 'strong', 'div')))))
            scope += 1
            
        return TextProcessing._processInfo(info_Weight)


if __name__ == '__main__':
    content = request.urlopen('http://migu.cn').read()
    htmlDoc = TextProcessing()
    res = htmlDoc.parseHTML(content, 'https://www.migu.cn/', 50)
    print(res)
