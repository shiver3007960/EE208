# <center>Lab1 HTML-parser </center> #

<center>姓名：刘洺皓 学号：521030910014</center>

## 1.实验概述 ## 
&emsp;本实验旨在了解 HTML 的结构，并利用 _BeautifulSoup_ 对 HTML 文本进行分析。通过阅读 _BeautifulSoup_ 的官方文档，接触了 _BeautifulSoup_ 对tag的基本操作和在HTML元素中进行过渡的常用方法。该实验基于 _urllib_ 库对网页发起请求，并在对不同URL的抓取中掌握了不同的tag类型与属性。在实验的第一部分与第二部分，主要通过查找指定类型的tag来获取相应内容，通过修改header中的各种参数来使浏览器模仿用户发起请求。在实验的第三部分，需要利用HTML文档中各个元素之间的联系来对具有确定树状结构的HTML文档，获取各类标签内的内容与属性，如超链接、图片地址等。本实验主要运用正则表达式，利用正则表达式引擎可以更快速，有效地对字符串文本进行匹配，并爬取到目标内容。 


## 2.实验环境 ##
本实验具体使用的工具如下:
* Docker中的ee208镜像 
* HTML解析器 _BeautifulSoup_
* Python(Vscode)（运用到sys,Beautifulsoup,re,urllib库）

## 3.实验练习 ##

### 3.1.1问题描述  ###
> &emsp; 给定任意网页内容，返回网页中所有超链接的URL（不包括图片地址），并将结果打印至文件res1.txt中，每一行为一个链接地址。建议参考example1.py。


### 3.1.2 问题分析 ###

&emsp; 只需要填充代码完成其中的 `parseURL` 函数，通过main函数的工作，网页内容已转换成     _BeautifulSoup_ 对象，并通过调用`.read()`函数转化为bytes object,在parseURL函数中为了处理content, 先要用`.decode("UTF-8")`转化为string对象，再利用正则表达式进行匹配。（注：经查询，对于数据量较大的html文档，使用 _BeautifulSoup_ 解析器（尤其是 _lxml_ 解析器）来查找目标标签将是效率更高的方法，这里使用regex只是为了提供另一种解法。）
 

&emsp; 正则表达式的pattern分析：


```
#使用 raw string literal 来规避需要大量使用转义字符'\'的情况

r'''(?<=     # 零宽正向后行断言
        <a href=
            (["'])   #分组1捕获字符组
                )\b(.+?)   # \b匹配单词边界以避免极端情况，分组2为实现后续使用MatchObject.group(2)函数获取目标地址
        (?=    # 零宽正向先行断言
        \1      # back reference
        .*>.*</a>)'''
```

&emsp; 使用`r''' '''`的raw string literal在正则表达式中大有裨益，在处理 _"\\"_ 时不再将紧随字符视为escape character，使得regex的书写更加方便简洁。



### 3.1.2 代码与运行结果 ###
代码展示如下: 


    def parseURL(content):
        urlset = set()

        s = content.decode("UTF-8")
        pat = re.compile(r'''(?<=<a href=(["']))\b(.+?)(?=\1.*>.*</a>)''', re.DOTALL)

        for match in re.finditer(pat, s):
            urlset.add(match.group(2))

        return urlset

运行结果如图:


```
{'http://news.baidu.com', 'http://image.baidu.com/', 'http://image.baidu.com/i?tn=baiduimage&amp;ps=1&amp;ct=201326592&amp;lm=-1&amp;cl=2&amp;nc=1&amp;ie=utf-8', 'https://map.baidu.com/?newmap=1&amp;ie=utf-8&amp;s=s', 'https://b2b.baidu.com/s?fr=wwwt', 'https://www.baidu.com/s?rtt=1&amp;bsst=1&amp;cl=2&amp;tn=news', 'http://map.baidu.com', 'http://wenku.baidu.com/search?lm=0&amp;od=0&amp;ie=utf-8', 'http://tieba.baidu.com/', 'https://www.hao123.com?src=from_pc', 'javascript:;', 'http://zhidao.baidu.com/q?ct=17&amp;pn=0&amp;tn=ikaslist&amp;rn=10&amp;fr=wwwt', 'https://haokan.baidu.com/?sfrom=baidu-top', 'http://v.baidu.com/v?ct=301989888&amp;rn=20&amp;pn=0&amp;db=0&amp;s=25&amp;ie=utf-8', 'https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F&sms=5', 'http://tieba.baidu.com/f?fr=wwwt', 'https://pan.baidu.com?from=1026962h', 'http://www.baidu.com/more/'}
```


#### 分析与反思： #### 
<span name="footnote1"></span>

在运行时发现了问题，作出如下分析与反思:

1. 若将代码中的 `re.finditer(pat, s)` 替换为 `re.findall(pat, s)`, 将不能达到预期效果。经网上查询后，得知 `re.findall(pat, s)` 在遇到regex文本中有分组时将会只输出匹配文本的分组部分，例如当代码如下时：

```
pat = re.compile(r'''(?<=<a href=(["']))[^"']+?(?=\1.*>)''', re.DOTALL)
for match in re.findall(pat, '<a href="http://www.wandoujia.com/apps/com.zhihu.daily.android"></a>'):
    print(match)
```
输出结果将为：
```
"
```
这将无益于目标URL匹配。而当使用`re.search(pat, s)`时效果将大为不同：
```
pat = re.compile(r'''(?<=<a href=(["']))[^"']+?(?=\1.*>)''', re.DOTALL)
print(re.search(pat, '<a href="http://www.wandoujia.com/apps/com.zhihu.daily.android"></a>'))
```
输出结果将为：
```
<re.Match object; span=(9, 62), match='http://www.wandoujia.com/apps/com.zhihu.daily.and>
```

所以为了实现迭代器查找，推荐使用`re.finditer(pat, s)`方法。

2. 为了使代码更为简洁，利用分组2来捕获目标文本，并通过调用`Match.object.group()`方法来输出字符串类型的所需答案，注意这里因为零宽断言不捕获文本，所以在字符串匹配时也不自动为其分配组号，所以regex文本中的`(.+?)`即是分组2。

3. 在`re.compile(pat, s, flag)`的flag中设置`re.DOTALL`是为了将regex文本中的 ++.++ 的意义从除换行符外的任意字符改为任意字符，这样可以避免爬取到的html文档中在形如 `<a href = "...">...</a>`中出现换行符导致匹配失败。


4.  若regex文本从`r'''(?<=<a href=(["']))\b(.+?)(?=\1.*>.*</a>)'''`改为`r'''(?<=<a href=(["']))\b(.+)(?=\1.*>.*</a>)'''`, 则输出结果将为
```
<re.Match object; span=(1973, 66788), match='https://www.baidu.com/" data-path="s?wd=">网页</a><>
```


可以看见匹配文本的长度将是极其之大的，这是因为正则表达式匹配时都默认使用贪婪模式，再带有限定符处将尽可能多的匹配文本，这将导致很多不合法的答案，
解决方法[^1]
<span name="footnote1"></span>
就是改为懒惰模式匹配，这将匹配尽可能少的文本，懒惰模式只需在原有的限定符后再加一个？即可。

[^1]:<https://blog.csdn.net/qq_42667613/article/details/115859383> 
***

[跳转到注释1]（#footnote1）

### 3.2.1 问题描述 ### 
> &emsp; 给定任意网页内容，返回网页中所有图片地址，并将结果打印至文件res2.txt中，每一行为一个图片地址。

### 3.2.1 问题分析 ### 


&emsp; 只需要填充代码完成其中的 `parseIMG` 函数，与`parseURL` 函数大同小异，这里不再赘述。
 
### 3.2.3 代码与运行结果 ###  
代码展示如下: 


    def parseIMG(content):

        urlset = set()

        s = content.decode("UTF-8")
        pat = re.compile(r'''(?<=<img src=(["']))([^"']+?)(?=\1.*>)''', re.DOTALL)

        for match in re.finditer(pat, s):
            urlset.add(match.group(2))

        return urlset
运行结果如下：


<code>
{'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/tupian@2x-482fc011fc.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/baiduyun@2x-e0be79e69e.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/baike@2x-1fe3db7fa6.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/jingyan@2x-e53eac48cb.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/wenku@2x-f3aba893c1.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/yinyue@2x-c18adacacb.png', 'https://dss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/topnav/baobaozhidao@2x-af409f9dbe.png'}
</code>

#### 分析与思考: ####

1. 出现报错：
> ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)

在爬取某些网站时发现会出现ssl库的证书验证报错，经参考后发现是爬取时需要对目标网页的SSL证书进行验证。

解决方法[^2]大致是在全局下修改ssl库属性：

[^2]:https://blog.csdn.net/tt75281920/article/details/104122012&gt;
```
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
```

1. 在爬取网站 _http://pexels.com_ 时出现报错：
> urllib.error.HTTPError: HTTP Error 403: Forbidden
 
经查询[^3]，发现 HTTP Error 403 Forbidden 报错的两个主要原因为：

[^3]:(https://blog.csdn.net/tangjinhu/article/details/99688599)

* 网站所有者编辑了设置，使您无法访问资源，或者他们没有设置正确的权限。
* .htaccess文件中的设置损坏或不正确。在您对文件进行更改后，可能会发生这种情况。您只需创建一个新的 .htaccess 文件即可轻松解决该问题。

这里做出推测，有可能是网站的反爬机制在起作用，也有可能是爬虫爬取到了某些无价值网站，此网站由于本身的配置问题而报错：HTTP Error 403。
 ***

### 3.3.1 问题描述 ### 
>  &emsp;给定知乎日报的url，返回网页中的图片和相应文本，以及每个图片对应的超链接网址。并将图片地址，相应文本，超链接网址以下述格式打印至res3.txt中，每一行对应一个图片地址，相应文本和超链接网址，格式为：图片地址 \t 相应文本 \t 超链接网址。参考example3.py



### 3.3.2 问题分析 ### 
知乎日报的主要部分的树状结构展示如下:
```
<div class="main-content-wrap">
    <div class="row">
        <div class="col-lg-4">
            <div class="wrap">
                <div class="box">
                    <a class="link-button" href="/story/9753144">
                        <img class="preview-image" src="https://picx.zhimg.com/v2-ee8737b97d93e8edd32356494c03cc45.jpg?source=8673f162"/>
                            <span class="title">有哪些普通人很少听说，但在生活中很重要的化学元素？
                            </span>
                    </a>
                </div>
            </div>
            <div class="wrap">
                <div class="box">
                    <a class="link-button" href="/story/9753140">
                        <img class="preview-image" src="https://pic1.zhimg.com/v2-3dd8c5fa5bca0a5a018e058f649c28e2.jpg?source=8673f162"/>
                        <span class="title">青梅煮酒为什么要配青梅，并且要煮酒？</span>
                    </a>
                </div>
            </div>
            <div class="wrap">
                <div class="box">
                    <a class="link-button" href="/story/9753136">
                        <img class="preview-image" src="https://pic1.zhimg.com/v2-5924cbf979d91d60e2de20a64523b0a9.jpg?source=8673f162"/>
                        <span class="title">如果宇宙中真的存在修真文明，我们有胜算吗？</span>
                    </a>
                </div>
            </div>
            <div class="wrap">
                <div class="box">
                    <a class="link-button" href="/story/9753132">
                        <img class="preview-image" src="https://pica.zhimg.com/v2-f9645f66ad9f440b3cd4cc9176ede7e0.jpg?source=8673f162"/>
                        <span class="title">南朝还有荆扬之争吗，荆扬之争什么时候退出历史的？</span>
                    </a>
                </div>
            </div>
```

&emsp;根据HTML元素的嵌套结构，可知目标的图片链接，内容描述（互为兄弟节点）都是网页链接所在tag的儿子，而网页链接所属tag的class属性均是 *"link button"*,可以通过 _BeautifulSoup_ 的 `find_all( name , attrs , recursive , text , **kwargs )` 方法来查找，而且tag对象的属性是以字典形式存储，可以通过以键取值的方法获取超链接，(即 `tag.["href"]`),可以利用 `tag.contents` 方法获取以列表形式存储的子节点，并通过 `tag.string` 方法获取 _NavigableString_ 对象。（注： 也可利用 `tag.children` 或者 `tag.sibling` 获取相应节点）


### 3.3.3 代码与运行结果 ### 


 代码展示如下: 

```
def parseZhihuDaily(content, url):
    zhihulist = list()

    #Add header
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    data = BeautifulSoup(urllib.request.urlopen(req), "lxml")

    for main_data in data.find(class_ = "main-content-wrap").find_all(class_ = "link-button"):
        zhihu = [url+main_data["href"][1:], main_data.contents[1].string, main_data.contents[0]["src"]]
        zhihulist.append(zhihu)

    return zhihulist
```

运行结果如下：

```
[['http://daily.zhihu.com/story/9753144', '有哪些普通人很少听说，但在生活中很重要的化学元素？', 'https://picx.zhimg.com/v2-ee8737b97d93e8edd32356494c03cc45.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753140', '青梅煮酒为什么要配青梅，并且要煮酒？', 'https://pic1.zhimg.com/v2-3dd8c5fa5bca0a5a018e058f649c28e2.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753136', '如果宇宙中真的存在修真文明，我们有胜算吗？', 'https://pic1.zhimg.com/v2-5924cbf979d91d60e2de20a64523b0a9.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753132', '南朝还有荆扬之争吗，荆扬之争什么时候退出历史的？', 'https://pica.zhimg.com/v2-f9645f66ad9f440b3cd4cc9176ede7e0.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753124', '人脑能承载多少知识?', 'https://pic1.zhimg.com/v2-2cb9fd3e51d4536fe5118095ad328dbb.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753145', '瞎扯 · 如何正确地吐槽', 'https://pica.zhimg.com/v2-3dd8c5fa5bca0a5a018e058f649c28e2.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753068', '小事 · 这个陌生的城市是不是喜欢我啊？', 'https://pica.zhimg.com/v2-b781a2a3dbf10fa278ae37a622d9bb4b.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753108', '《水浒传》中林冲真的窝囊吗？', 'https://pic2.zhimg.com/v2-3e7382fb6f54ddcf8513a3c8d4e9d5eb.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753099', '人们为什么对负面信息更感兴趣？', 'https://pic2.zhimg.com/v2-970810aee896e2595878d61b64acefe5.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753089', '电脑的发展以后会脱掉硬件哪个部位?', 'https://pic3.zhimg.com/v2-57b6e4cca2ac81b4f74dc6701e37e417.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753080', '教练是怎么指导比自己强的运动员的？', 'https://picx.zhimg.com/v2-cfb2b4fb04bdf8f151990815cdc41b9c.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753073', '把汉语言文学学到极致会有怎样意想不到的收获？', 'https://pic1.zhimg.com/v2-f9d0f1a4653225aeb0cd2a5c6b640429.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753059', '小事 · 「钱不够打电话，千万不要省吃的」', 'https://pic2.zhimg.com/v2-fab9c8b85e6e77d52fb656527d61d451.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753051', '蚊子最喜欢什么血型（ABO血型）？', 'https://picx.zhimg.com/v2-ee412acafe753be5491179ec8d624910.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753044', '临床医学五年制学生如何能成为法医？', 'https://pic1.zhimg.com/v2-6cf9062dd4667b5d5982bebec4170c8f.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753043', '为什么乒乓球运动员都长得很好看？', 'https://pic1.zhimg.com/v2-6f663448b113e619a263420357781025.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753041', '人类向太空中发射过哪些意想不到的东西？', 'https://pic1.zhimg.com/v2-5a67c9847466d4808b2b6ec92786b3f6.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753038', '从生物学上来看，人类有哪些设定不适合永生?', 'https://picx.zhimg.com/v2-172ec4c0e9c27917500f6bdda5f8bcea.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753006', '为什么《数码宝贝》只有第一部那么火？', 'https://pic2.zhimg.com/v2-9c3f5d01087cf5470e76acaee7d076dc.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753029', '如果给你一百万，你会用来做什么？怎么用才有意义？', 'https://picx.zhimg.com/v2-e24853e7ec6df9a863339a8285b1afd9.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753026', '炫富真的很爽吗？', 'https://pica.zhimg.com/v2-cb6022f2caa63b567287820990ceecaf.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753022', '无线鼠标安全吗？', 'https://picx.zhimg.com/v2-51e1e4f301af4151d9116afdc3eb531f.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753016', '为什么其他生物就不能进化成「人」呢？', 'https://pic1.zhimg.com/v2-71a47b50d48262da0763a390da65da79.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753036', '瞎扯 · 如何正确地吐槽', 'https://pic2.zhimg.com/v2-47932c99a3060179d9c547e107ec17f7.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9752951', '很多动物都能通过气味识别幼崽，人类可以吗？', 'https://pic1.zhimg.com/v2-3d385ec1f253c0ef228937a3ccbab34f.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753003', '有哪些隐含暗喻或细节、情节的名画？', 'https://pic1.zhimg.com/v2-a34281d348e94e5307d5ae03375a70d6.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9753000', '骨头是生的硬还是熟的硬？', 'https://pic2.zhimg.com/v2-23abec2296e70acf6ca2e1211f3654a4.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9752984', '为什么有人说开车时，最能看出一个人的情商和潜力？', 'https://pic1.zhimg.com/v2-1f3d3b17ec70cd6471ed23238be6ae3e.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9752968', '欧洲中世纪的饮食，平民饮食状况是怎样的？', 'https://pica.zhimg.com/v2-768140debb9582aa54bf9b852c57fa33.jpg?source=8673f162'], ['http://daily.zhihu.com/story/9752976', '瞎扯 · 如何正确地吐槽', 'https://pic1.zhimg.com/v2-01abbf13dd9cc4d0b8817326580fd524.jpg?source=8673f162']]
```

#### 分析与反思： ####

1. 添加header的意义

当执行代码
```
url = "https://www.douban.com/"
content = urllib.request.urlopen(url).read()
```
时会报错如下：
```
File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/urllib/request.py", line 643, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 418: 
```
经过查询[^4],`HTTP Error 418' 是网站的反爬程序所返回的错误，需要调整报头信息来解决。

[^4]:(https://blog.csdn.net/shenyuan12/article/details/107849794)


代码如下：
```
url= 'http://www.baidu.com'
req = urllib.request.Request(url)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
```
常见的http请求头，响应头和基本信息都可以在inspect中的network窗口对文件进行审览查询到。


![img1](https://cdn.jsdelivr.net/gh/Learner209/snakegame@master/img/9.20.1.png "Network")  


 > General：

    Request URL: https://blog.csdn.net/weixin_48964486/article/details/122394270
    Request Method: GET
    Status Code: 200 
    Remote Address: 114.116.236.
    Referrer Policy: strict-origin-when-cross-origin

> Reponse-Headers

    content-encoding: gzip
    content-language: en-US
    content-type: text/html;charset=utf-8
    date: Mon, 19 Sep 2022 15:14:54 GMT
    server: openresty
    strict-transport-security: max-age= 31536000
    vary: Accept-Encoding

>Request Headers

    :authority: blog.csdn.net
    :method: GET
    :path: /weixin_48964486/article/details/122394270
    :scheme: https
    accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    accept-encoding: gzip, deflate, br
    accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
    cache-control: max-age=0
    cookie: uuid_tt_dd=10_9949723620-1657898088130-112441; __gads=ID=66481612eb251d19-22782ac135d50056:T=1658018890:RT=1658018890:S=ALNI_Mb_nmyR0wsuZQZCszwHzSZ1lL9sMQ; UserName=yufeiyang553; UserInfo=0dad55a0139944eb8ea2c6fe8e722f42; UserToken=0dad55a0139944eb8ea2c6fe8e722f42; UserNick=yufeiyang553; AU=AD9; UN=yufeiyang553; BT=1663233375666; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22yufeiyang553%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_9949723620-1657898088130-112441!5744*1*yufeiyang553; firstDie=1; csdn_highschool_close=close; ssxmod_itna=eq0xnD9DcDgDRDUx4lRQIqe4Qw4xGgG7GrERxqGXxTGRDCqAPGfDI839GBkRgurrYYE4Uxwxqsb2BwRxqlp4hmWDLFDueD=xYQDwxYEHDALPD9Ii74GGDBeGwD0eG+DD4DWFqDtZIkxGpS9LXFfTLx4eGvnqKgfuDDCODDbopyDB6dxBQVfTQXGeXxZkRo9iETvG55WTha9ADKb8qeQA5q90hbmpqQ975PRBqdR+5wxD3+gODxD=; ssxmod_itna2=eq0xnD9DcDgDRDUx4lRQIqe4Qw4xGgG7GrERxA=WAND/W9iDFOdbI617iFHFEpDN5lYnSwjwqW70AQD6Dh5+ItaY6phvtKtDRLvqRIo5wvK+9pj9=eu29gGmVC7cOg4fNU=HWnU4uq8zPpqMmIhumKCl7p+A2cW0cYHzxHWoKgFRm7p1ruatEE7PPfzGFKp675Nxffaif8FoagiufSt9U7A6UkaQzMTArSth97meXriE1mToCaOa2Kzmlm569rcKy+qQT5wAD07UD08DY954D===; c_segment=9; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1663463484,1663488567,1663546592,1663586435; dc_sid=f4ad8d95ce71090e8e969cbcee06bb92; dc_session_id=10_1663590761206.746808; __gpi=UID=000007c6e633a01f:T=1658018890:RT=1663596027:S=ALNI_MZRv8GYsEh9Bk5-nyy5JD6EDYz3vg; csrfToken=AyZCzYqA5rEsGmRamve8_qDK; c_ref=https%3A//www.baidu.com/link; c_first_ref=www.baidu.com; c_pref=https%3A//www.baidu.com/link; log_Id_click=30; c_first_page=https%3A//blog.csdn.net/weixin_48964486/article/details/122394270; c_dsid=11_1663600473432.842505; c_page_id=default; dc_tos=rigqc9; log_Id_pv=71; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1663600474; log_Id_view=310
    sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "macOS"
    sec-fetch-dest: document
    sec-fetch-mode: navigate
    sec-fetch-site: none
    sec-fetch-user: ?1
    upgrade-insecure-requests: 1
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36

请求头，响应头中对应不同的http属性，请求报文中的信息应该是爬虫需要关注的。

参考：&lt;https://blog.51cto.com/u_13372349/5324814&gt;

| 报头属性 | 实例 | 说明 |
| ---- | ---- | ---- |
|Accept|text/html|浏览器可以接受服务器回发的类型为 text/html|
|Accept|\ |代表浏览器可以处理所有类型|
|Accept-Encoding| gzip, deflate|浏览器申明自己接收的编码方法，通常指定支持什么压缩方法|
|Accept-Language|zh-CN|浏览器申明自己接收的语言|
|Connection|keep-alive|当一个网页打开完成后，客户端和服务器之间用于传输HTTP数据的TCP连接不会关闭，如果客户端再次访问这个服务器上的网页，会继续使用这一条已经建立的连接|
|Connection|close|代表一个Request完成后，客户端和服务器之间用于传输HTTP数据的TCP连接会关闭， 当客户端再次发送Request，需要重新建立TCP连接|
|Host|https://www.baidu.com|(发送请求时，该报头域是必需的)www.baidu.com 请求报头域主要用于指定被请求资源的Internet主机和端口号，它通常从HTTP URL中提取出来的。
|Referer|​https://www.baidu.com/?start=1|当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器我是从哪个页面链接过来的，服务器籍此可以获得一些信息用于处理。​​
|User-Agent|Mozilla/...|告诉HTTP服务器， 客户端使用的操作系统和浏览器的名称和版本。
|Cache-Control|private|默认为private.响应只能够作为私有的缓存，不能再用户间共享|
|Cache-Control|public|响应会被缓存，并且在多用户间共享。正常情况, 如果要求HTTP认证,响应会自动设置为 private|
|Cache-Control|must-reval（按照 RFC 7231 中定义的“超文本传输协议日期”格式来表示)|
|Connection|keep-alive|这个字段作为回应客户端的Connection：keep-alive，告诉客户端服务器的tcp连接也是一个长连接，客户端可以继续使用这个tcp连接发送http请求|
|ETag| "637060cd8c284d8af7ad3082f209582d" |就是一个对象（比如URL）的标志值，就一个对象而言，比如一个html文件，如果被修改了，其Etag也会别修改，所以，ETag的作用跟Last-Modified的作用差不多，主要供WEB服务器判断一个对象是否改变了。比如前一次请求某个html文件时，获得了其 ETag，当这次又请求这个文件时，浏览器就会把先前获得ETag值发送给WEB服务器，然后WEB服务器会把这个ETag跟该文件的当前ETag进行对比，然后就知道这个文件有没有改变了|
|Refresh| 5; url=http://baidu.com |用于重定向，或者当一个新的资源被创建时。默认会在5秒后刷新重定向|
|Access-Control-Allow-Origin|* |代表所有网站可以跨域资源共享，如果当前字段为那么Access-Control-Allow-Credentials就不能为true|
|Access-Control-Allow-Origin|www.baidu.com| 指定哪些网站可以跨域资源共享
|Access-Control-Allow-Methods|GET,POST,PUT,DELETE |允许哪些方法来访问|
|Access-Control-Allow-Credentials|true  是否允许发送cookie。默认情况下，Cookie不包括在CORS请求之中。设为true，即表示服务器明确许可，Cookie可以包含在请求中，一起发给服务器。这个值也只能设为true，如果服务器不要浏览器发送Cookie，删除该字段即可。如果access-control-allow-origin为*，当前字段就不能为true|
|Content-Range|bytes 0-5/7877|指定整个实体中的一部分的插入位置，它也指示了整个实体的长度。在服务器向客户返回一个部分响应，它必须描述响应覆盖的范围和整个实体长度|



在urllib.request中添加headers,就是把请求头的常用信息以字典形式加入`urllib.request.urlopen(url, headers)`函数中,来模仿浏览器访问而非pythonrequest,从而一定程度的克服反爬机制。


## 4.拓展思考 ###

在爬取不同网站重复实验时， 可得href 的链接形式主要有如下 5 种: 

1. `match='javascript:;"> onclick="..."`javascript:;不执行任何代码。
2. `match='javascript: void 0;'>`/`match="javascript:setLocale('zh'）“`javaScript里的void是一个操作符, 如果void 0即是一个不执行跳转页面的链接，可以通过`onclick="..."`来设置鼠标悬停在超链接上时执行的js:method。
3. `match='https://www.douban.com/doubanapp/redirect?channel>`爬取到的是绝对URL路径，执行的是https协议，安全性和隐秘性更好。
> HTTPS协议是由SSL/TLS+HTTP协议构建的可进行加密传输、身份认证的网络协议，要比http协议安全. HTTPS协议的主要作用可以分为两种：一种是建立一个信息安全通道，来保证数据传输的安全；另一种就是确认网站的真实性。
5. `match='http://beian.miit.gov.cn/'>`爬取到的是绝对URL路径，执行的是http协议。
> HTTP是超文本传输协议，全称“Hyper Text Transfer Protocol”，是一个基于请求与响应，无状态的，应用层的协议，常基于TCP/IP协议传输数据，互联网上应用最为广泛的一种网络协议,所有的WWW文件都必须遵守这个标准。设计HTTP的初衷是为了提供一种发布和接收HTML页面的方法。
6. `match='mailto:service@sjtu.edu.cn'`/`match='gatsbyjs/gatsby'`爬取到的是相对URL路径，可以利用`urlib.parse.urljoin()`方法拼接。
7. `match='#label'` 可以在同一个文档中设置锚点，锚点的命名规则为 `<a name='label'>`,然后通过指向该点的href链接来设置锚，实现页面跳转。

