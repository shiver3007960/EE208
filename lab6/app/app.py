
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join
from dataStore import Scrapy

app = Flask(__name__)

@app.route('/user/<username>')
def user(username):
    print(username)
    return render_template('host.html')

@app.route('/search', methods=["GET", "POST"])
def querySearch():

    if request.method =="GET" or request.method =="POST":
        query = request.args.get('q')
        fn = int(request.args.get('fn'))

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

    # The main Content
    # Must be precisely more than 5 items, only display first 5 items, null must be in format ('', '', '', '', '', '')
    # If it the really semantic content exceeds number 5, it will only display 5 items
    # The format is ('URLTitle', 'the full URL', 'The scheme plus the the netloc', 'the following path separated by >s', 'theMainDescription', 'imgsrc', 'Additional information'(optional))(length == 7)
    mainContent = dict()
    mainContent['URLTitle'] = ['Google - Wikipedia'] * 36
    mainContent['the full URL'] = ["https://en.wikipedia.org/wiki/Google"] * 36
    mainContent['scheme+netloc'] = ['https://en.wikipedia.org'] * 36
    mainContent['path'] = ['› wiki › Google'] * 36
    mainContent['theMainDescription'] = ['<em>Google</em> LLC is an American multinational technology company that focuses on search engine technology, online advertising, cloud computing, computer software,&nbsp;'] * 36
    mainContent['imgsrc'] = ['../static/image/facebookicon.png'] * 36
    mainContent['Additional information'] = [''] * 36

    return render_template('form.html', hotspots = hotspots, lenhotspots = lenhotspots, relatedSearch = relatedSearch, lenrelatedSearch = 6, URLtitle = URLtitle, searchGeneral = searchGeneral, recommendPic = recommendPic, lenrecommendPic = 6, mainContent=mainContent, lenmainContent = [(fn-1)*5, fn*5], lenpagechangetable=len(mainContent['path'])//5+1)



@app.route('/news')
def news():
    if request.method =="GET" or request.method =="POST":
        fn = request.args.get('fn')
    if not fn:
        fn = 1
    else:
        fn = int(fn)

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

    return render_template('news.html', newsContent=newsContent, lennewsContent =[(fn-1)*6, fn*6], lenpagechangetable = len(newsContent['News Href']) // 6 + 1)

@app.route('/images')
def images():
    if request.method =="GET" or request.method =="POST":
        fn = request.args.get('fn')
    if not fn:
        fn = 1
    else:
        fn = int(fn)
    
    picPool = dict()
    # In the format of pictureBrief Description, picSrc, the name of the website to which the image belongs to, URlhref
    picPool['Description'] = ['Sam Donald Sucks'] * 2
    picPool['picSrc'] = ['../static/image/pexel/06.jpg'] * 2
    picPool['picWebtitle'] = ['google.com'] * 2
    picPool['picWeblink'] = ['http://www.google.com'] * 2
    return render_template('images.html', lenPicPool = 2, picPool = picPool, lenpagechangetable=20//5)

@app.route('/')
def host():
    return render_template('host.html')

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
