

from flask import Flask, Request, render_template, Request, redirect, url_for, request
from werkzeug.utils import secure_filename
from os.path import join
from dataStore import Scrapy
from time import sleep
#from Search import Query
app = Flask(__name__)

class Query:
    def __init__(self) -> None:
        self.data = dict()
        self.picdata = dict()
        self.refreshing = 0
        self.precision = 0
        self.loading = 0
        self.shortcut = Query.initshortcut()
        self.startD = None
        self.endD = None
    
    @staticmethod
    def initshortcut():
        shortcut = dict()
        shortcut['Facebook'] = {'title':'Facebook', 'href':'https://www.facebook.com', 'stock':'../static/image/facebookicon.png'}
        shortcut['Yahoo'] = {'title':'Yahoo', 'href':'https://www.yahoo.com', 'stock':'../static/image/yahooicon.png'}
        shortcut['Instagram'] = {'title':'Instagram', 'href':'https://www.instagram.com', 'stock':'../static/image/insicon.png'}
        shortcut['facebook'] = {'title':'facebook', 'href':'https://www.facebook.com', 'stock':'../static/image/facebookicon.png'}
        shortcut['Twitter'] = {'title':'Twitter', 'href':'https://twitter.com', 'stock':'../static/image/twitter.png'}
        shortcut['Youtube'] = {'title':'Youtube', 'href':'https://www.youtube.com', 'stock':'../static/image/youtubeicon.png'}
        shortcut['Amazon'] = {'title':'Amazon', 'href':'https://www.amazon.com', 'stock':'../static/image/amazonicon.png'}
        shortcut['Microsoft'] = {'title':'Microsoft', 'href':'https://www.microsoft.com', 'stock':'../static/image/microsofticon.png'}
        shortcut['linkdein'] = {'title':'linkdein', 'href':'https://www.linkedin.com', 'stock':'../static/image/linkedinicon.png'}
        return shortcut

    def querySearch(self, query):
        if query in self.data.keys():
            return self.data[query]
        else:
            # search the index
            # The main Content
            # Must be precisely more than 5 items, only display first 5 items, null must be in format ('', '', '', '', '', '')
            # If it the really semantic content exceeds number 5, it will only display 5 items
            # The format is ('URLTitle', 'the full URL', 'The scheme plus the the netloc', 'the following path separated by >s', 'theMainDescription', 'imgsrc', 'Additional information'(optional))(length == 7)
            print("query is %s"%query)
            sleep(5)

            mainContent = dict()
            mainContent['URLTitle'] = ['Google - Wikipedia'] * 36
            mainContent['the full URL'] = ["https://en.wikipedia.org/wiki/Google"] * 36
            mainContent['scheme+netloc'] = ['https://en.wikipedia.org'] * 36
            mainContent['path'] = ['› wiki › Google'] * 36
            mainContent['theMainDescription'] = ['<em>Google</em> LLC is an American multinational technology company that focuses on search engine technology, online advertising, cloud computing, computer software,&nbsp;'] * 36
            mainContent['imgsrc'] = ['../static/image/facebookicon.png'] * 36
            mainContent['Additional information'] = [''] * 36

            """ mainContent['URLTitle'] = list()
            mainContent['the full URL'] = list()
            mainContent['scheme+netloc'] = list()
            mainContent['path'] = list() 
            mainContent['theMainDescription'] = list()
            mainContent['imgsrc'] = list()
            mainContent['Additional information'] = list() """

            self.data[query] = mainContent

            return mainContent

    def imgSearch(self, query):
        if query in self.picdata.keys():
            return self.picdata[query]
        sleep(5)
        picPool = dict()
        # In the format of pictureBrief Description, picSrc, the name of the website to which the image belongs to, URlhref
        picPool['Description'] = ['Sam Donald Sucks'] * 2
        picPool['picSrc'] = ['../static/image/pexel/06.jpg'] * 2
        picPool['picWebtitle'] = ['google.com'] * 2
        picPool['picWeblink'] = ['http://www.google.com'] * 2
        self.picdata[query] = picPool
        return picPool

record = Query()
    

@app.route('/user/<username>')
def user(username):
    print(username)
    return render_template('host.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/stastics/search', methods=["GET", "POST"])
def stastics_search():

    if request.method =="GET" or request.method =="POST":
        record.precision =  request.args.get('pre') if request.args.get('pre') is not None else record.precision
        record.refreshing = request.args.get('fresh') if request.args.get('fresh') is not None else record.refreshing
        query = request.args.get('q')
    record.querySearch(query=query)
    return {'status':200}
    
@app.route('/stastics/images', methods=["GET", "POST"])
def stastics_images():
    if request.method =="GET" or request.method =="POST":
        query = request.args.get('q')
    record.imgSearch(query=query)
    print("i am here")
    return {'status':200}

@app.route('/search', methods=["GET", "POST"])
def querySearch():

    if request.method =="GET" or request.method =="POST":
        if 'q' not in request.args or 'fn' not in request.args:
            return {'status':404}
        
        record.precision =  request.args.get('pre') if request.args.get('pre') is not None else record.precision
        if 'start' in request.args and 'end' in request.args:
            record.refreshing = [request.args.get('start'), request.args.get('end')]
        else:
            record.refreshing = int(request.args.get('fresh')) if request.args.get('fresh') is not None else record.refreshing
        query = request.args.get('q')
        fn = int(request.args.get('fn'))
    
    if query not in record.data.keys():
        return render_template('null.html', mainContent = None, lenmainContent = 1, lensearchHistory = min(5, len(record.data.keys())), searchContent = query, searchH = list(record.data.keys()))

    # in the scope of form .html
    # Must be precisely more than 15 items, only display first 15 items, null must be in format ('', '')
    hotspots = Scrapy.formatBaiduHotSpot_forForm()
    lenhotspots = min(len(hotspots['Description']), 19)
    # Must be precisely more than 5 items, only display first 5 items,null must be in format ('', '')
    relatedSearch = dict()
    relatedSearch['href'] = ['http://www.baidu.com'] * 6
    relatedSearch['content'] = ['Hello from outside'] * 6
    # URLtitle
    URLtitle = "Google google search"
    # quantity of results and searchConsumed time
    searchGeneral = [20202020, 0.56]
    # recommended pic banner
    # Must be precisely more than 6 items, only display first 6 items, null must be in format ('', '', '', '')
    # The format is ('URLtitle', "URLbrieDescrition", "URLhref", "URLimgSrc")
    recommendPic = dict()
    recommendPic['URLTitle'] = ['天猫'] * 6
    recommendPic['URLBrief'] = ['综合性购物'] * 6
    recommendPic['URLhref'] = ["https://www.baidu.com"] * 6
    recommendPic['URLimgSrc'] = ['../static/image/facebookicon.png'] * 6

    mainContent = record.data[query]
    lensearchHistory = min(5, len(record.data.keys()))
    searchH = list(record.data.keys())

    #Query.runForWeb(indexDir = 'app/URLinfo', query = query, field = "Contents", mainContent = mainContent, VM = VM)
    if not len(mainContent['URLTitle']):
        print(query)
        return render_template('index.html', mainContent=mainContent, lenmainContent = [(fn-1)*5, fn*5], lensearchHistory = lensearchHistory, searchContent = query, searchH = searchH)
    
    daterange =  None if not isinstance(record.refreshing, list) else '从_%s_到_%s'%(record.refreshing[0], record.refreshing[1])
    return render_template('form.html', hotspots = hotspots, lenhotspots = lenhotspots, relatedSearch = relatedSearch, lenrelatedSearch = 6, \
        URLtitle = URLtitle, searchGeneral = searchGeneral, recommendPic = recommendPic, lenrecommendPic = 6, \
            mainContent=mainContent, lenmainContent = [(fn-1)*5, fn*5], lenpagechangetable=len(mainContent['path'])//5+1, \
                lensearchHistory = lensearchHistory, searchH = searchH, \
                    fresh = record.refreshing if isinstance(record.refreshing, int) else 6, pre = record.precision, daterange = daterange)


@app.route('/news')
def news():
    sleep(5)
    return "hello"
    if request.method =="GET" or request.method =="POST":
        fn = request.args.get('fn')
    if not fn:
        fn = 1
    else:
        fn = int(fn)


    lensearchHistory = 3
    #return render_template('null.html')
    return render_template('index.html', lensearchHistory = lensearchHistory)
    
    # The format is [('website icon imgsrc', 'website href', 'website URLtitle'), ('News Title', 'News Content', 'News Href', 'News imgSrc', 'News Additional information'(optional))] length is [(3), (5)]
    newsContent = dict()
    newsContent['website icon imgsrc'] = list()
    newsContent['website href'] = list()
    newsContent['website URLtitle'] = list()
    newsContent['News Title'] = list()
    newsContent['News Content'] = list()
    newsContent['News Href'] = list()
    newsContent['News imgSrc'] = list()
    newsContent['News Additional information'] = list()
    newsContent = Scrapy.formatWeiboHotspot_fornews(newsContent)
    print(newsContent)
    
    return render_template('news.html', newsContent=newsContent, lennewsContent =[(fn-1)*6, fn*6], lenpagechangetable = len(newsContent['News Href']) // 6 + 1)

@app.route('/images')
def images():
    if request.method =="GET" or request.method =="POST":
        query = request.args.get('q')
        fn = request.args.get('fn')
    if not fn:
        fn = 1
    else:
        fn = int(fn)
    
    if query is None:
        return render_template('window.html')
    if query not in record.picdata.keys():
        return render_template('null.html', mainContent = None, lenmainContent = 1, lensearchHistory = min(5, len(record.data.keys())), searchContent = query, searchH = list(record.data.keys()))

    picPool = record.picdata[query]
    lensearchHistory = min(5, len(record.picdata.keys()))
    searchH = list(record.picdata.keys())

    if not picPool['Description']:
        print(query)
        return render_template('index.html',  mainContent=None, lenmainContent = 0, lensearchHistory = lensearchHistory, searchContent = query, searchH = searchH)
    
    return render_template('images.html', lenPicPool = 2, picPool = picPool, lenpagechangetable=20//5, lensearchHistory = lensearchHistory, searchH = searchH)

@app.route('/')
def host():
    lensearchHistory = min(5, len(record.data.keys()))
    searchH = list(record.data.keys())
    shortcut = record.shortcut
    return render_template('host.html', lensearchHistory = lensearchHistory, searchH = searchH, shortcut = shortcut)

@app.route('/test')
def test():
    return '''
    <img src="app/static/image/yahooicon.png" alt="fucker">
    
    '''
@app.route('/upload')
def upload():
    def isValidFilename(string):
        if not isinstance(string, str):
            return
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config['PERMITTED_EXTENSIONS']
    #文件上传目录
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    #支持文件格式
    app.config['PERMITTED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    uploadFile = request.files['image']
    if uploadFile and isValidFilename(uploadFile.filename):
        filename = secure_filename(uploadFile.filename)
        uploadFile.save(join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    else:
        return 'The file is not valid'


if __name__ == "__main__":
    app.run(debug=True, port=8080)
