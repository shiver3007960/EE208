# <center>小型搜索引擎</center> #

<center>姓名：刘洺皓 学号：521030910014 班级：F2103001</center>

## 1.项目概述 ## 
&emsp;本项目旨在实现一个小型搜索引擎，其实现的基本原理如下：
* 利用python的urllib库和HTTP Base Handler库来实现网页爬取
* 利用lxml库构建网页树，解析网页内容，提取相关有用信息，使用jieba分词，亮点在于构建了一个具有打分机制的，兼容中英文，基本能够适配大量网站的对于图片的描述信息的提取的函数。
* 利用开源的Lucene引擎进行利用WhitespaceAnanlyzer实现中文分词建立索引和读取索引，以及一些增删改查和不同字符串搜索方式的实现。
*  构建了一个*Web*前端，实现了简单的主页，搜索结果呈现页和图片排版页，并拓展了一些如搜索历史查看，快捷方式增删，日期范围划定，加载页面呈现等功能。
* 接触并自己简略实现了*Simhash*文本查重,*Pagerank*,*Textrank*等算法。
*  再尝试寻找*Pagerank*的优化时，在*Google Scholar*上找到了一篇 *Adaptive methods for the computation of PageRank* 并咀嚼消化，最后也自己进行了实现。


## 2.项目环境 ##
本项目具体使用的工具如下:
* Docker中的ee208镜像(含Pylucene库)
* docker初始环境未安装的库:aiohttp(与asyncio实现异步协程爬虫),lxml,bitarray, func_set_timeout, jieba
* Python(Vscode)

## 3.项目片段 ##

### 3.1.1 中文的分词  ###
&emsp;利用jieba分词，可以利用 *cut_for_serach* 或者 *lcut_for_serach* 方法尽可能地切词，以提高召回率，同时在分析网页时也需要将原来的中文内容按照分词结果切开，中间留有空格，以期 _StandardAnalyzer_ 能够像英文切词一样将中文以空格切开，但是实际证明 _StandardAnalyzer_ 对待中文还是会一个一个字切开，所以这里改用 _WhitespaceAnalyzer_ 进行切词，提高对短语的完整性保留。


### 3.2.1 索引的建立 ### 
1. Indexer问题
    在使用 docker container 时经常会发现会 killed 现象，初步判断是内存溢出进程自动被杀死，第一部我先检查了线程问题，我使用了 *threading.active_count* 发现我的活跃线程数在200以下，且线程名字都能对应上我初始化线程的线程名字，应该不是线程问题，接下来考虑内存使用情况，我对代码进行了内存的部分优化，并且尝试降低线程数以降低内存负载，但是还是会出现 KILLED 现象，之后我又尝试了 docker Desktop 中提升容器的 CPU  CORE， DISK IMAGE SIZE和 Memory 与 Swap 容量， 并且经过命令行 top 指令查看动态内存使用情况，发现 python3 占用的内存并不足以达到使该进程被 killed的程度，反而是几个node进程占用了大量内存，在未运行python3 时尝试 kill PID 但是并没有实效，接下来尝试本机安装 *pylucene* 但是意料之中地受挫而归，最终的解决方法是利用 *OPEN_OR_APPEND* 方法来打开 *SimpleFSDirectory* 进行index多次来达到网页数量要求。
2. *IndexFiles*
* 自定义field可以利用fixed好的 *TextField*, *StringField*, *NumericField*但是这样的话当调用`indexReader.getTermVectors`的话会无法获得相应的权词向量，只有当是自定义field类型且`setStoreTermVectors(True)`时才会正常获得*Termvectors*
* 同时发现当设置STORED为TRUE时，内存空间会被大量消耗，导致top命令观察到的剩余空闲内存急剧减少以致进程被快速kill，所以在container中进行实验时要*SetStored(False)*,但这样就需要在展示结果时重新获取，无论是读取本地已存储文件还是重新发起网页请求，复刻parse结果都会延长程序运行时间，这是又一个时间与空间的权衡，在本次试验中因为考虑到container的运行效果不及裸机，所以index时不存储内容，需要在查询时重新获取内容，会造成一定的时间浪费。
3. *SearchFiles*
* 为了节省建立索引空间，在每次返回一个查询成功的结果时，都会重新进行网页请求。所以构建了一个工具函数presentQuery函数，作用是每次接收一个目标网址发起请求，进行搜索结果的查重，建立文档并存储网页内容。然后返回本地文件存储地址。
presentQuery函数需要注意以下几点:
1. 为了实现在文档当中快速定位查询成功的结果所在的offset,这里运用了lucene的API,使用了*SimpleHTMLFormatter*,*QueryScorer*类来实例化*Highlighter*,并且为了文本切割定位使用了setTextFragmenter,最终调用getBestFragment来获得相对应的文本片段
2. 为了实现搜索结果的查重(因为即使网址大相径庭，搜索仍能获得相似结果），在整个循环过程当中维护一个已查重的。*contentPool*,并且利用字符串的*Differ*库解析两个字符串的比较返回结果，这里调用了TextProcessor中所写的*common*工具函数，利用*differlib*所产生的字符串的-+号数量之差来判断两个字符串的文本差异
3. 在获得目标网页响应内容之后，按照网页网址的域名*netloc,path,params,query*来逐级创建目录存储内容，并在且返回创建路径
4. 为了保证能够准确获取网页，屏蔽网址环境变更所带来的不确定性。在调用*crawler.py*的`standard_request`函数获取网页内容不符合要求时将会再使用asyncio异步爬虫进行爬取，因为协程异步爬虫充分调用cpu资源，所以带来的时间耗费可以忽略不计


### 3.3.1 网页解析 ### 
1. 清除 HTML 标签
   &emsp;显示 _nlkt_ 库已经 deprecate *clean_html* 方法，这里从 nlkt package 中沿用了原来的方法、
2. 为了提高匹配精确度，这里对 *jieba* 使用了停用词，以过滤常见词汇，停用词文件名称为 cnstopwords.txt, 在 instantiating *Textprocessing* 类时将会自动读取停用词并且将停用词作为类的静态变量给不同的实例化对象共享以节省空间。
3. 网页分析中考虑语言问题，这里使用 lxml 库来解析， 并运用 xpath 或 cssselect(需要 pip另外安装) 选择 <meta> 标签中的 lang属性， 若lang为en-US,则在分词时会不使用jieba而是将英文单词作为 raw material 传入 _WhitespaceAnalyzer_ , 若lang为 zh-CN ,则在分词时会使用jieba预留空格， 调用 *TextProcessor* 中的 `TokenizeChinese` 方法， 若lang中没有表明文件语言类型，那么将调用 *TextProcessor* 中的 `TokenizeMixedLan` 方法。
   * 查询 <meta> 中 lang，可用`"//head/meta[contains(@content,'charset=')]"`作为xpath.
   * *TextProcessor* 中的 `TokenizeChinese`方法：可利用正则表达式 '[\u4e00-\u9fa5，。、？！《》‘’“”：；]+' 匹配，然后对中文的meaningful segment进行切分，为作扩展，`TokenizeChinese` 方法提供了是否使用jieba分词及是否利用 *jieba* 的搜索引擎匹配模式的接口
   * *TextProcessor* 中的 `TokenizeMixedLan` 方法目的在于保留除中文字符与标点符号外的内容，但将中文替换为分词后的结果，为了节省空间，`TokenizeMixedLan` 方法比 `TokenizeChinese` 方法 多做的工作在循环中记录了上一次的分词终止的位置，然后将 last_tokenized 到当前分词开始处的内容保留，重复更新结果变量。
4.  *TextProcessing* 中的 `parseContents` 方法
    为加强文本与网页的相关性，这里使用了 *lxml.html.clean.Cleaner* 类，利用 `Cleaner(style=True, scripts=True, links = False, remove_tags = remove_tags)` 方法来定位到我们想要的内容，我清除掉了 footer, css样式，脚本文件（虽然无法排除有少数网页的HTML内容就放在script中进行动态渲染，或者以 Ajax 请求交换 JSON 数据来得到脚本渲染网页时的原材料）,同时我也只保留了body部分的网页内容。
5. parse 网页中的外链
   xpath中的写法为 `'//a[@href and @rel != "nofollow"] | //a[@href] | //iframe[@src]'` 这里不处理网页的 nofollow 标签，因为做的假设是这些 nofollow links对网页的贡献度不大，这里也就爬取时滤过，网页中的链接分好多种，这里只针对转向其他有效网页的外链，所以首先去除 `href:"javascript:void(...)`形式，其次判断是否是锚点，即是否startswith('#'),最后判断该链接是否是资源下载链接，作为另一种连接形式保存，这里使用正则表达式匹配后缀名实现。
6. 如果网页中有 `<base>` 标签，那么可以将其作为基准网页定位相对地址。
7. 编码问题：有些网站的 charset 与实际网页内容使用的编码方式不符，常见在某些 gbk 与 gb2312 为主的网站,所以要对 *UnicodeError* 进行异常捕获。
8. `TokenizeMixedLan` 函数中为了提高效率，`jieba.enable_parallel(4)` 开启了多线程的并行分词模式，其底层工作原理是将待分词内容分割为几小块，对每一块进行分词，这种方法对待长篇幅文本效率会显著提升，但是对待短篇幅文本例如一个网站的内容来说，其并行分词的效率提升还不足以弥补启动多线程并关闭线程所耗费的时间，这里可以选择把`jieba.disable_parallel()`放在所有分词行为的末端，而在 *TextProcessing* 类初始化时就调用`jieba.enable_parallel(4)`这样可以减少开关线程造成的时间浪费。在实际运行jieba分词过程中又出现了一个新问题，就是当jieba模块被调用好之后，相当于给jieba的分词器上了锁，在多线程共同请求分词时，只有一个线程会获得锁，所以在任意时刻真正只有一个线程是在进行切词工作，这无疑是降低了程序的效率，退化成了单线程工作，所以如何考虑将*jieba*的分词行为在并行线程中展开是必要的问题。同时,多线程运用*jieba*分词而非使用*jieba*所提供的*native API*`enable_parallel` `disable_parallel()` 也会使得线程工作变得混乱，在实际运行过程中就经常遇*ZeroDivisionError*, *ValueError*,并且报错信息显示在 *jieba/__init__.py* 中的 `lcut(pool, map)` 的一行，并且trigger了*multiprocessing*库中的错误，说明*jieba*并非thread-safe,或者对于多线程调用的兼容性不好，这里的处理方法目前只能是异常捕获，可以在以后尝试阅读源码并修改。

程序的健壮性维护：
&emsp;网页返回的内容以及处理文本返回的内容经常无法保证是期望的数据类型，为了维护程序运行的健壮性，经常会进行数据类型的实例检查以及不符合条件的提前退出。
* 在*TextProcessing*的健壮性handling中，首先检查请求网页输入的内容是*string instance* 或*bytes instance*，然后检查lxml库是否能正常产生etreeObject,并且对于网页分析的URL,网页标题和网页内容都要考虑可能是*NoneObject*,在这些过程当中，一旦没有获得期望的instance，就应该提前退出，防止继续运行产生异常。
* 在*searchFiles*的文件当中，要判断得到的url是否是string对象以及调用工具函数_validURl判断是否是合法url网址。如果开头并非startswith HTTP, urllib没法识别，所以要在字符串头加上*scheme*,最重要的是在调用getBestFragment函数之后，要检查返回的是*Noneobject*还是*string instance*
* 在*IndexFiles*的indexURL函数中进行了异常捕获，是为了防止*Field*输入的对象并非是str instance
* 

### 3.4.1 图片相关信息提取 ### 

&emsp; 这里构建了一个具有打分机制的，兼容中英文，基本能够适配大量网站的对于图片的描述信息的提取的函数。
想法综述：
1. 过滤掉不必要内容，保留关键内容
2. 鉴别链接，判断链接合法性，并回溯寻找图片相关文本
3. 在不同的scope下对不同标签属性进行文本过滤与打分
4. 排序，返回最高分的两个结果作为图片的相关文本
   

代码过长可以略过，接下来是基本的较为详细的思路，注意这里打分机制的*coefficient,base,exponential*还需要经过大量网站图片的相关信息经验来做动态修正。

* `parseImg`
1. 先是利用 *lxml.html.Cleaner* 清除掉与图片无关HTML标签,和标签中的属性,这里保留了安全属性为*src alt title*,并清除掉了无关标签为 *footer nav form link style*,该函数的主要任务是寻找网页响应内容当中的图片链接,并且检查其合法性，这里的安全图片链接定义为*div style*中的*backgroundImage,background*和*img,embed，iframe*中的图片属性，并且调用`_retrieveimgInfo`来获得该图片周围所对应的该图片信息，并存储在与图片链接地址作为键值的字典中
* `retrieveImgInfo`
0. 在整个过程当中可以评价一个相关信息的crendential,通过其所在标签在树中的*scope*,与*img*标签本身的距离和该标签当中*semantic segment*的长度来综合打分，因为scope和distance占较为重要的比例，所以打分机制以*scope*和*distance*为指数衰减，最终衡量一个图片相关信息就可以不断地将加入其信息向量的分数进行优先级插入
1. 寻找图片周围所在相关信息的函数分为三个部分
   * 第一部分是*local scope*. 从*original src*的链接地址本身所含信息来查询信息,这对大型专业图片素材网站成功率较高，如*pexels,pixabay,unsplash,freePhotos(CC0)*,为了从图片链接地址本身过滤出有用信息，先要排除掉图片链接地址的scheme,netloc,锚点等信息，这里所做的假设是图片的信息如果隐藏在链接地址当中，大概率是出现在url的*path*和*params*字段，所以可以调用`parse.urlparse()`函数获取
   * 第2部分是*src*所在标签的*alt*与*title*属性，这两个属性经常用来表示这个图像所代表的信息，以及当图片加载失败时显示出的alternative信息。这两个标签是网页开发者在插入图片时经常会使用的，公认的隐含图片信息的属性，所以这两个图片的credibility较大，*credential*设为1。在处理这两个标签时，也要将标点符号去除。来过滤掉信息，以方便最后信息向量的排序组合。
   * 第三部分也是最重要的*scope*是outer text，并且是严重dependent on *rated by range*机制，作为图片，一个与图片相关的信息经常会与该图片HTML标签具有相同的*data-vid,id,class*或者网页开发者自定义的attribute,所以先要获取到该图片HTML标签本身的一种身份证明，用`getBasicInfo`函数实现
      * 获得一个图片可能的身份证明之后，首先检查该图片HTML标签的兄弟们，这里利用*lxml*的`itersiblings`函数并且只保留*p,span,em,strong,div*这种能够contain文本的标签形式,并且对符合要求的每一个兄弟调用`filterTags`函数
      * 在`retrieveImgInfo`的while循环中，当scope小于4时停止循环，因为过远的距离，文本与图片相关度将锐减，对于一个新的scope,首先去寻找中文，因为当在符合要求的scope中`itertext`中寻找到中文时，其大概率可以作为一个可信的图片相关信息，接下来根据标签形式分类讨论，首先获得当前scope下标签的*basicInfo*,即一个以*Class ID identifier*作为键值的字典，这样为了方便之后的与图片相关度的匹配打分，如果该标签是div,找其上下邻居，这里做的假设是一个图片标签所在的*div*标签的上下邻居更有潜力隐藏这个图片的描述性文本，如果该标签是*figure*或*picture*类型，那么就确信已经到达了跟这个图片相关的*HTMLTag*的顶部，接下来只需要itertext并且`filterAttrorText`过滤即可。
   * 在其他情况下，还是迭代去寻找当前标签的所有兄弟，调用`filterTags`来获取基本信息，与最初在*img HTML*标签本地信息获取`itersibling`的过程相似，最终该scope下的循环结束，scope自增1并进入下一轮循环。

2. 其次为了过滤掉乱码，观察大多数图片链接地址的乱码形式，特征多为无规律的数字与英文字母的组合重复不断地相join，所以利用正则表达式匹配该类型，如果匹配到的字符串数目与该图片链接，地址的path长度的比例大于0.6,就认为这些匹配的字符串属于地址乱码，在过滤掉乱码之后，尝试去识别链接地址中的*semantic segment*,这经常体现为一些短语的组合，所以如果匹配到的*semantic segment*的长度是大于3小于15的，就认为这是一个可以连接成句子的代表图片相关信息的短语组合。


* `getBasicInfo`函数
  * 首先默认将*class*与*ID*属性作为最有可能作为一个图片的身份证明的attribute,然后去找一个能够代表这个图片的attribute的*identifier*,一个semantic的符合要求的*identifier*在这里被定义为一串数字与字母的随机组合，其长度经常在3~10之间，这样的表征图片身份的*identifier*经常出现在电商，网购，和娱乐网站平台上.是一种为了方便规划不同item并识别item相关*div*与*span*的网页组合方式,该函数返回一个字典,其键值分别为*class ID identifier*


   
* `Filter tags`函数关键在于对于不同HTML标签类型的分类讨论。
  * 首先，该函数判断是否是*em,strong,p*标签，因为这些函数最有可能获得一个图片相关的文本，所以他们的优先级最高，在经过`filterAttrOttext`函数的过滤后获得*semantic segment*的数量，如果数量大于0小于9就被认为是一个潜在可能与图片相关的信息元素，其打分的*base*是0.8，以*scope*为指数，以0.8为*coefficient*,这里做的假设是这些文本的潜力值较大。
  * 如果接收的函数参数标签类型是*div span a*，那么这些标签如果与图片相关联，极有可能会拥有一个与那个图片身份证明相同的*identifier*，所以对这些标签先寻找identifier，如果找到，那么自然该标签的*credential*大幅提升，如果没有corresponding identifier,其*credential*会打折扣，这里体现在scope会自乘1.15使得*credential* descend。
  * 在确认好目标tag的打分的基数后，接下来进入主要的标签文本的查找与过滤,这里因为标签所含内容可能大相径庭，鱼龙混杂，需要进行较多的isinstance检查，这里仍旧将目标tag的title属性作为优先级最高的attribute对待，值得注意的是，如果title中含中文，其*credential*也会提升，其打分机制为*coefficient*为0.75，基数为0.55。
  * 接下来去遍历这个标签的孩子们，即调用*lxml*的`items(）`方法，并调用`_filterAttrorText`函数来过滤文本寻找semantic *segment*,如果其数量大于0小于20，就认为这是一个潜在的与图片相关的信息元素，但是其*credential*会稍有下降，其打分机制为*coefficient*为0.8,基数为0.55.
  * 最终检查这个标签的plain text,因为在该scope中的文本出现图片相关信息的可能性比`items()`的概率相对提升,其打分机制为*coefficient*为0.75,基数为0.6.
    * 如果该标签类型为超链接，并且其scope为1，可以直接认为这个超链接作为图片标签的父亲，是这一个图片item的总领，可以直接调用*lxml*的itertext函数。
    * 但在目标tag是*div,span,a*且scope不为1时，在`filterTags`函数中递归调用`filterTags`，对象为该函数tag下的`iterchildren`的迭代器，而其每一个child的scope都会自动下降0.05,这基于一个图片与其文本是分列在不同的div标签中的假设，这种图片与文本分列并居于同一个大div分组的网页排版，这经常运用在tmall,taobao,migu等国内网站中，这也是除专业图片素材网站外许多大型网站的图片典型排版方式。
   
* `filterAttrOrText`函数
  * 主要完成对于一个标签内所含的plain text中的有效semantic *segment*的查询
  * 首先将输入字符串转为全部小写，然后将乱码*segment*与半角全角标点符号清除，接下来当输入字符串长度过长之后，这里假设标签当中所含的属性plain text中有overlapping内容，根据*tf-idf*的启发，这种几个文档共同重复出现的内容一般价值较小，可以去除，这在kugou音乐的官网中可以找到example,但为了避免出现Overlapping内容的循环重叠，设置去除循环内容的循环次数上限为10，最后寻找*semantic segments*,同时兼容了中文与英文以及半角全角标点符号，并且将*semantic* *segments*作为set返回.


### 3.5.1 网页前端 ### 
* 这里在设计网页时，发现较好地能够适应不同浏览工具的网页布局方式是css在2014年推出的盒子布局，简称*flex*布局，它可以通过设置`align-items`,`align-contents`,`justify-contents`这几个属性在主轴与交叉轴上实现每一个div小标签的自动排版，而有了主轴与交叉轴，那么一个canvas上就有了灵巧绘制的工具，剩下来的就只需一个个将小元素填充进去
* 在*javascript*的运用中，尤其是在图片网页的排版上，发现*javascipt*根本没有起作用，甚至在console中调用时也无法`getElementById`,后来经上网查询发现自己将脚本的链接位置放在了head中，这时候正文部分还没有加载完毕，所以这时候运行javascript脚本是没有作用的，要将*javascript*的链接放在正文的末端才能正常地与元素交互来时网页动态化
* 同时我还实现了一个用户上传文件的窗口，使用了几个Flask提供的接口，具体的实现可以看代码。
* 为了能够使图片正常展示，这里原本采用了在html文件中直接通过`<img src=''>`标签来插入图片，但是发现图片的超链接地址当呈现在网页上时，一般都显示不出来，但是自己手动在浏览器上打开时就可以显现，这里就只能使用朴素地将每一个图片的超链接地址作为URL发送请求，获取图片，然后以二进制格式写入图片内容储存在服务器端的方法，这里还要注意到在储存图片的时候应该注意不能够重复储存在同一个路径上，但是某些图片的URL是以乱码实现呈现的，这里为了不让本地存储的文件太过杂乱，就将*netloc, path, parameters*作为一个图片存储网址的唯一identifier，将锚点抛弃，如果处在同一个*identifier*的串联路径中，那么就以1, 2, 3, 4, 5....来标识图片。
* 这里可能会涉及到大量网址的采集，所以相比于*requests*和*urllib*库所使用的传统申请方法，这里使用了协程异步爬虫，利用了*asyncio*与*aiohttp*库，可以提升采集的速度，因为在网页浏览的语境下，用户经常追求的是准确与快速，所以不仅是在建立索引文件时我将大部分的field都设置为stored,而且在处理其他业务时除非不必要的情况下都会直接将数据存储到服务器端
* 为了美化丰富网页内容，我这里设计了一个*Scrapy*类，该类的函数有:
    * `htmlCleaner(topboard)`:工具函数，清除不必要的html标签，使网页展示的内容清晰整洁
    * `asynCrawl(url, params = None, semaphore = asyncio.Semaphore(20), timeout = 2, cookie = None, bytesRequired = False)`:协程异步爬虫，提升爬取网页的效率，提升用户体验
    * `storeImg(url, Referer = None)`:存储图片函数，前面已提到过
    * `addBaiduHotspot()`:添加百度热点
    * `formatBaiduHotSpot_forNews()`: 为了方便展示结果在新闻页面，将百度热点的内容格式化适应输出
    * `formatBaiduHotSpot_forForm()`: 为了方便展示结果在搜索页面，将百度热点的内容格式化适应输出
    * `addBaiduMovie()`:添加百度热点
    * `addBaiduTvSeries()`:添加百度热点
    * `addWeiboHotspot()`:添加微博热点，这里花了挺多功夫，为了获取到微博热点，发现微博有较为完善的反爬机制，不能够使用传统的URL申请获取数据，经一番折腾后在Network中抓包之后发现服务器会传递过来一个JSOn文件，里面有展示完整的新闻更新日期，新闻内容，新闻网址，相关图片
    * `formatWeiboHotspot_fornews(newsContent)`:为了方便展示结果在新闻页面，将微博热点的内容格式化适应输出
* 我这里还实现了对于其实页面的background-image的切换，这里在js文件中调用了`timer = setInterval(changeBackground, 1000*300, bgim, 9)`;来实现间隔一定时间切换壁纸
* 这里展示一下app文件的树结构，为了方便日后维护，不易混淆，也给自己做个备忘录：
```
-| static
    -| css # Cascading Style Sheet
        -| form.css
        -| host.css
        -| images.css
        -| news.css
        -| style.css
        -| test.css
    -| image
        -| imgStore
        -| news     #新闻网站的图片获取
        -| pexel    
        -| pexels-wallpaper #pexel网站的壁纸来作为起始页面的backgound-image
    -| js
        -| form.js
        -| host.js
        -| iamges.js
        -| new.js
    -| shortcut icon #用来存储小型图片，常用在favorite-icon和小图标的展示
-| stopwords    #停用次，TextProcessing文件需要
-| templates
    -| base.html    # html文件的基类，实现了对于header, nav, aside, article, footer的接口的预留
    -| form.html    # 搜索页面的展示，继承了header, nav, aside, article, footer几个区块
    -| host.html    # 起始页面
    -| images.html  #图片网站
    -| index.html
    -| news.html    #新闻网站
-| app.py   # 主文件
-| crawler.py   # 请求网页数据
-| dataStore.py     #实现对于零散网页业务的处理，存储图片，获取热点消息等等
-| TextProcessor.py     #实现HTML文本处理和特征获取
```

* 发现每次获取的速度都很慢，代码的另一个缺点是即使是同样的query，都会在更换页码时重新search index一下，所以接下来的优化方向就是使得服务器具有缓存功能，使得访问更快速。
* 实现了一些小插件与功能拓展，比如快捷方式的增删改，网页检索结果的动态变化，搜索历史的呈现，搜索结果的日期范围的界定。
  
## 4.效果展示 ## 

* 主页
![11.30.2](https://cdn.jsdelivr.net/gh/Learner209/snakegame@master/img/11.30.2.png)

* 搜索结果页
![11.30.1](https://cdn.jsdelivr.net/gh/Learner209/snakegame@master/img/11.30.1.png)

* 加载页
![11.30.3](https://cdn.jsdelivr.net/gh/Learner209/snakegame@master/img/11.30.3.png)

* 图片排版页
![11.30.5](https://cdn.jsdelivr.net/gh/Learner209/snakegame@master/img/11.30.5.png)
  

