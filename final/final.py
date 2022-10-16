
import lucene


if __name__ == '__main__':
    VM = lucene.initVM(vmargs=['-Djava.awt.headless=true'])#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    VM.attachCurrentThread()


from collection import BloomFilter, isValidURL
from crawler import standard_request
from IndexFiles import Indexer
from TextProcessor import TextProcessing


from queue import Queue
from threading import Thread, Lock
from time import sleep
from math import ceil, log2
from functools import reduce
from os import makedirs
from func_timeout import func_set_timeout
import func_timeout
from sys import exit


def _parse(IndexingPool, URLPool, content):
        
    htmlParser = TextProcessing()
    
    parseResult = htmlParser.parseHTML(content[1], content[0]) #content[1] is rawContent, content[0] is baseURL
    #print("parseRes %s "%str(parseResult)[0:100])
    # To avoid misformatting in the parseResult 
    if isinstance(parseResult, list) and len(parseResult[4]) > 1 and isinstance(parseResult[4][0], set):
        processLinks = list(map(lambda element: URLPool.put(element) if isValidURL(element) else None, parseResult[4][0]))
        IndexingPool.put(parseResult)
        with open('data.txt', 'a+') as file:
            if parseResult is not None:
                try:
                    file.write(str(parseResult))
                except Exception as error:
                    pass
        print("Consuming website is  %s "%(content[0]))


def crawl(URLPool, ContentsPool, crawled, IndexingPool, timeout = 3600 * 10):

    @func_set_timeout(timeout)
    def _crawl():
        nonlocal ContentsPool, URLPool
        while True:
            page = URLPool.get()
        
            if not crawled.isExist(page):
                #TextProcessing.display(page)
                if isinstance(page, str) and len(page) > 3:
                    query, urlContains = TextProcessing._vaildURL(page)
                    if urlContains is None:
                        continue
                    content = standard_request(page)
                    if content is not None:
                        _parse(IndexingPool, URLPool, (page, content))
                crawled.put(page)
    try:
        _crawl()
    except func_timeout.exceptions.FunctionTimedOut as error:
        pass

def indexHTML(IndexingPool, IndexingPoolLock, VM = None, indexWriter = None, timeout = 3600 * 10):

    @func_set_timeout(timeout)
    def _index():
        nonlocal IndexingPool, IndexingPoolLock, indexWriter, VM
        while True:
            with IndexingPoolLock:
                parseResult = IndexingPool.get()
            Indexer.indexURL(parseResult, indexWriter, VM = VM)
            with open('data.txt', 'a+') as file:
                if parseResult is not None:
                    try:
                        file.writelines(str(parseResult))
                        file.write('\n')
                    except Exception as error:
                        print("The fucking I/O error occurs %s"%str(error))
            print("*****Indexing website****** is  %s "%(parseResult[0]))
    try:
        _index()
    except func_timeout.exceptions.FunctionTimedOut as error:
        pass


def _init(seedList = None, VM = None, indexwriter = None, STORE_DIR = "URLinfo", crawlThreads = 8):

    URLPool = Queue()

    IndexingPool = Queue()
    IndexingPoolLock = Lock()

    ContentsPool = Queue()
    crawled = BloomFilter(1000, 0.001)
    VM.attachCurrentThread()

    if indexwriter is None:
        indexWriter = Indexer.getIndexWriter(STORE_DIR)
    else:
        indexWriter = indexwriter

    filterObj1 = list(map(lambda element: URLPool.put_nowait(element), seedList))

    crawlThreadPool = list()
    for i in range(0, crawlThreads):
        crawlThread = Thread(name = 'crawl%s'%seedList[0], target = crawl, args = [URLPool, ContentsPool, crawled, IndexingPool])
        crawlThreadPool.append(crawlThread)
        crawlThread.start()
    
    indexThread = Thread(name = "index", target = indexHTML, args = [IndexingPool, IndexingPoolLock, VM, indexWriter])
    
    indexThread.start()

    crawlJoin = list(map(lambda thread: thread.join(), crawlThreadPool))

    indexThread.join()

    if indexwriter is None:
        Indexer.closeWriter(indexWriter)

def readSeedList(filename = 'seedList.txt'):

    def _read(element):
        line = TextProcessing._vaildURL(element)
        return None if line[1] is None else line[1]

    with open('seedList.txt') as file:
        line = list(filter(lambda element: element is not None and element.startswith('http'), map(_read, file.readlines())))
        return line


seedList = readSeedList(filename = "seedList.txt")

initThread = list()
indexWriter = Indexer.getIndexWriter(storeDir="URLinfo")
for index in range(ceil(len(seedList) / 2)):

    thread = Thread(name = "main_scrapy", target=_init, args=[seedList[2*index:2*index+2], VM, indexWriter, None])
    initThread.append(thread)
    #thread.setDaemon(True)
    thread.start()

for thread in initThread:
    thread.join()

Indexer.closeWriter(indexWriter)