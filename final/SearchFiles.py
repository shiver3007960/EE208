# SJTU EE208

INDEX_DIR = "index"

import sys, os, lucene, re
import operator
from java.io import File
from TextProcessor import TextProcessing
from crawler import standard_request, asynCrawl
import asyncio
from urllib import parse
from os import makedirs, path
from TextProcessor import TextProcessing
from queue import LifoQueue

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.charfilter import HTMLStripCharFilter
from org.apache.lucene.index import DirectoryReader, Term, IndexReader, IndexWriter, IndexWriterConfig, PostingsEnum, MultiFields
from org.apache.lucene.util.automaton import RegExp 
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery, WildcardQuery, FuzzyQuery, MultiPhraseQuery, PhraseQuery, BooleanQuery, RegexpQuery
from org.apache.lucene.search import Query as luceneQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import DocIdSetIterator
from org.apache.lucene.search.highlight import SimpleHTMLFormatter, QueryScorer, Highlighter, SimpleFragmenter
from org.apache.lucene.util import Version
from org.apache.lucene.util import BytesRef, BytesRefIterator

if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)


class Query:

    def __init__(self) -> None:
        pass

    # Recieve a URL and store the content of the URL and return contentsGeneral to filter overlapping content
    @staticmethod
    def presentQuery(URL = None, storeDir = "URLdir", field = None, contentsGeneral = '', highlighter = None, analyzer = None, doc = None):
        
        # Get highlighter fragment
        res = highlighter.getBestFragment(analyzer, field, doc.get(field))
        if isinstance(res, str):
            res = ''.join(map(lambda matchObj: matchObj.group(), re.finditer(formatter, res)))

            # Avoiding common segments
            matchmaxLen = TextProcessing._common(contentsGeneral, res)
            if matchmaxLen / len(res) > 0.95:
                return None
            contentsGeneral += res

            urlpath = '/' .join(filter(lambda netloc: netloc and re.match('[a-zA-Z0-9]', netloc) is not None, \
                            [parse.urlparse(URL).netloc.strip('/'), parse.urlparse(URL).path.strip('/'), parse.urlparse(URL).params.strip('/'),  parse.urlparse(URL).query.strip('/')]))

            if not path.exists("%s/"%storeDir + urlpath):
                makedirs("%s/"%storeDir + urlpath)
                with open("%s/%s/content.txt"%(storeDir, urlpath), 'w+') as file:
                    file.write(doc.get(field))
            return (res, "%s/%s/content.txt"%(storeDir, urlpath), contentsGeneral)

       
    @staticmethod
    def phraseQuery(queries, positions) -> PhraseQuery:
        phraseQueryBuilder = PhraseQuery.Builder()
        mapObj = (map(lambda query, position: phraseQueryBuilder.add(query, position), zip(queries, positions)))
        query = phraseQueryBuilder.build()
        return query

    @staticmethod
    def multiPhraseQuery(queries, positions) -> MultiPhraseQuery: # The first query must be a certain prefix
        prev = positions[0]
        sameQueries = list()
        multiPhraseQueryBuilder = MultiPhraseQuery.Builder()

        def _addBuilder(query, position):
            nonlocal multiPhraseQueryBuilder, prev, sameQueries
            sameQueries.append(query)
            if (position != prev):
                multiPhraseQueryBuilder.add(query, sameQueries)
                sameQueries = list()
                prev = position

        mapObj = (map(lambda query, position: _addBuilder(query, position), zip(queries, positions)))
        query = multiPhraseQueryBuilder.build()
        return query

    @staticmethod
    def _vaildURL(query):
        urlPattern = '/;；?#a-zA-Z0-9\._=-'
        searchHTTP = re.search('(?:(?<=https:/)|(?<=http:/)|(?<=ftp:/))[' + urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', query)
        if searchHTTP is not None:
            query = re.sub('(https:/|http:/|ftp:/)[' + urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', '', query)
            return (query, searchHTTP.group(0))
        searchWWW = re.search('(?:(?<=www\.)|(?<=wwww\.))[' +  urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', query)
        if searchWWW is not None:
            query = re.sub('(www\.|wwww\.)[' +  urlPattern +\
            ']{6,}(?=([^' + urlPattern + ']|$))', '', query)
            return (query, searchWWW.group(0))
        searchCOM = re.search('(?:(?<=[^' + urlPattern + '])|(?<=^))[' +  \
            urlPattern + ']{4,}[(.com)|(.cn)][' + urlPattern + ']*(?=([^' + urlPattern + ']|$))', query)
        if searchCOM is not None:
            query = re.sub('([^' + urlPattern + ']|^)[' +  \
            urlPattern + ']{4,}[(.com)|(.cn)][' + urlPattern + ']*(?=([^' + urlPattern + ']|$))', '', query)
            return (query, searchCOM.group(0))
        return (query, None)

    @staticmethod
    def parseQuery(query, analyzer = WhitespaceAnalyzer()):
        # Create a new Boolean Query
        booleanQuery = BooleanQuery.Builder()
    
        photoRequired = False

        # See if it contains a url
        leftQuery, url = Query._vaildURL(query)

        # Text or picture first
        matchObj = re.search('(图[\w\s]?片|照[\w\s]?片|相[\w\s]?册|[pP]icture[s]*|[Pp]hoto[s]*|[Ii]m[a]*g)', query)
        if matchObj is not None:
            photoRequired = True
            leftQuery = query.replace(matchObj.group(1), '')

        if url is not None:
            regexPattern = '.*%s.*%s.*'%(parse.urlparse(url).netloc, parse.urlparse(url).path)
            term = Term("URL", regexPattern)
            regexQuery = RegexpQuery(term, RegExp.ALL)
            booleanQuery.add(regexQuery, BooleanClause.Occur.MUST)

            leftQuery = QueryParser("Contents", analyzer).parse(leftQuery)
            booleanQuery.add(leftQuery, BooleanClause.Occur.MUST)
            query = booleanQuery.build()
        else:
            query = QueryParser("Contents", analyzer).parse(leftQuery)
        if photoRequired:
            query = MultiFieldQueryParser(["Contents", "Images"], analyzer).parse(leftQuery)
        
        return query
        
    @staticmethod
    def _parseQuery(query, field, analyzer = None):

        # Create a new Boolean Query
        booleanQuery = BooleanQuery.Builder()

        operator = LifoQueue()
        operator.put(-1)
        operation = LifoQueue()
        notFlag = False
        isWordFlag = False

        def _parse(segment, field, analyzer = None):
            nonlocal operator, operation, notFlag, booleanQuery, isWordFlag
            
            conjunction = Query._isConjunction(segment.strip())
            if conjunction != -1:
                # To avoid the operators are together, like "AND AND AND"style, But the NOT style is permitted
                if not isWordFlag and conjunction != 2:
                    return
                # WHy the conjunction can't be NOT? Because it can be "Shanghai AND NOT You"
                if not operation.empty() and conjunction != 2:
                    # Pull out the consecutive content in the content stack
                    content = operation.get_nowait().strip()
                
                    if re.search('[\u4e00-\u9fff]', content) is not None:
                        
                        print("Ready to tokenize %s"%content)
                        listObj = list(map(lambda element: TermQuery(Term(field, element)), list(TextProcessing.TokenizeChinese(finalQuote, jiebaRequired = True, cut_for_serach = True).split())))
                        
                        if len(listObj) < 2:
                            phraseQuery = TermQuery(Term(field, content))
                            print(type(phraseQuery))
                        else:
                            phraseQuery = Query.multiPhraseQuery(listObj, [0] + (len(listObj) - 1) * [10])
                            print("PhraseQuery is %s"%phraseQuery)
                    else:
                        phraseQuery = QueryParser(field, analyzer).parse(content) # All English
                    if notFlag:
                        tmp = BooleanQuery.Builder()
                        tmp.add(phraseQuery, BooleanClause.Occur.MUST_NOT)
                        phraseQuery = tmp.build()
                        notFlag = False
                    # Put in the phraseQuery between two operators
                    operation.put_nowait(phraseQuery)
                    print("PhraseQuery is %s"%phraseQuery)

                isWordFlag = False
                lastOp = operator.get_nowait()
                if conjunction > lastOp and conjunction != 2:
                    print("put %s %s due to precedence obscurity"%(lastOp, conjunction))
                    operator.put_nowait(lastOp)
                    operator.put_nowait(conjunction)
                elif conjunction < 2:
                    # Pull the top two elements from stack and compute acoording to the just pulled operator
                    op1 = operation.get_nowait()
                    op2 = operation.get_nowait()
                    # Put the current operator in the stack Beacause its precedence order is obscure
                    operator.put_nowait(conjunction)
                    print("Ready to put because the precendence order is clear op1 %s op2 %s"%(op1, op2))
                    # Ready to put because the precendence order is clear
                    if lastOp == 0:
                        tmp = BooleanQuery.Builder()
                        tmp.add(op1, BooleanClause.Occur.SHOULD)
                        tmp.add(op2, BooleanClause.Occur.SHOULD)
                        tmp = tmp.build()
                        operation.put_nowait(tmp)
                    else:
                        tmp = BooleanQuery.Builder()
                        tmp.add(op1, BooleanClause.Occur.MUST)
                        tmp.add(op2, BooleanClause.Occur.MUST)
                        tmp = tmp.build()
                        operation.put_nowait(tmp)
                else:
                    operator.put_nowait(lastOp)
                    print("Set the reach final %s"%notFlag)
                    notFlag = True
            else:
                print("The word is %s"%segment)
                if not isWordFlag:
                    operation.put_nowait(segment)
                else:
                    content = operation.get_nowait()
                    content += ' ' + segment 
                    operation.put_nowait(content)
                isWordFlag = True
            

        filterObj = list(filter(lambda element: _parse(element, field, analyzer = analyzer), query.split()))
        #Process the final query
        finalQuote = operation.get_nowait()
        print("Final quote is %s"%finalQuote)
        print("Not flag is %s before reach Final"%notFlag)
        if isinstance(finalQuote, str):
            if re.search('[\u4e00-\u9fff]', finalQuote) is not None:
                print("Ready to tokenize %s"%finalQuote)
                listObj = list(map(lambda element: TermQuery(Term(field, element)), list(TextProcessing.TokenizeChinese(finalQuote, jiebaRequired = True, cut_for_serach = True).split())))
                
                if len(listObj) < 2:
                    phraseQuery = TermQuery(Term(field, finalQuote))
                    print(type(phraseQuery))
                else:
                    phraseQuery = Query.multiPhraseQuery(listObj, [0] + (len(listObj) - 1) * [10])
                    print("PhraseQuery is %s"%phraseQuery)

            else:
                phraseQuery = QueryParser(field, analyzer).parse(finalQuote) # All English
        elif isinstance(finalQuote, luceneQuery):
            phraseQuery = finalQuote
        if notFlag:
            tmp = BooleanQuery.Builder()
            tmp.add(phraseQuery, BooleanClause.Occur.MUST_NOT)
            phraseQuery = tmp.build()
        # Put in the FINAL phraseQuery between two operators
        operation.put_nowait(phraseQuery)
        print(operation.qsize())
        # Deal with the left operation in these two stacks
        while True:
            oper = operator.get_nowait()
            print("Get oper %s"%oper)
            if oper == -1:
                break
            op1 = operation.get_nowait()
            print("op1 is %s"%op1)
            op2 = operation.get_nowait()
            print("op2 is %s"%op2)
            if oper == 0:
                tmp = BooleanQuery.Builder()
                tmp.add(BooleanClause(op1, BooleanClause.Occur.SHOULD))
                tmp.add(BooleanClause(op2, BooleanClause.Occur.SHOULD))
                tmp = tmp.build()
                operation.put_nowait(tmp)
            elif oper == 1:
                tmp = BooleanQuery.Builder()
                tmp.add(BooleanClause(op1, BooleanClause.Occur.MUST))
                tmp.add(BooleanClause(op2, BooleanClause.Occur.MUST))
                tmp = tmp.build()
                operation.put_nowait(tmp)
        print("The final operation size is %s"%operation.qsize())
        if operation.qsize() == 1:
            res = operation.get_nowait()
            print(res.clauses())
            return res
        else:
            ans = BooleanQuery.Builder()
            while not operation.empty():
                res = operation.get_nowait()
                print("THe final pulled out elemrnt is %s"%res)
                
                # Still tokenize the popped out element
                if isinstance(res, str):
                    if re.search('[\u4e00-\u9fff]', res) is not None:
                        print("Ready to tokenize %s"%res)
                        listObj = list(map(lambda element: TermQuery(Term(field, element)), list(TextProcessing.TokenizeChinese(res, jiebaRequired = True, cut_for_serach = True).split())))
                        
                        if len(listObj) < 2:
                            phraseQuery = TermQuery(Term(field, res))
                            print(type(phraseQuery))
                        else:
                            phraseQuery = Query.multiPhraseQuery(listObj, [0] + (len(listObj) - 1) * [10])
                            print("PhraseQuery is %s"%phraseQuery)
                    else:
                        phraseQuery = QueryParser(field, analyzer).parse(res) # All English
                elif isinstance(res, luceneQuery):
                    print("your motherfuckign win %s"%res)
                    phraseQuery = res
                ans.add(BooleanClause(phraseQuery, BooleanClause.Occur.MUST))
            ans = ans.build()
            print(ans.clauses())
            return ans

    @staticmethod
    def _isConjunction(segement):
        isOR = '(^或者$|^或$|^[Oo][Rr]$|^Orr$)'
        isAnd = '(^和$|^以及$|^与$|^[Aa][Nn][Dd]$)'
        isNot = '(^[Nn][Oo][Tt]$|^非$|^否$)'
        if re.match(isOR, segement) is not None:
            return 0
        if re.match(isAnd, segement) is not None:
            return 1
        if re.match(isNot, segement) is not None:
            return 2
        return -1

    @staticmethod
    def run(indexDir, query, field, analyzer = WhitespaceAnalyzer()):
        
        if query == '':
            return
        # 索引目录
        directory = SimpleFSDirectory(File(indexDir).toPath())
        # 索引搜索工具
        indexReader = DirectoryReader.open(directory)
        searcher = IndexSearcher(DirectoryReader.open(directory))
        # 索引搜索
        scoreDocs = searcher.search(query, 75).scoreDocs
        #分词器

        #高亮显示
        htmlFormatter = SimpleHTMLFormatter("", "")
        queryScorer = QueryScorer(query)
        highlighter = Highlighter(htmlFormatter, queryScorer)
        fragmenter = SimpleFragmenter(120)
        highlighter.setTextFragmenter(fragmenter)

        contentsGeneral = ''
        #匹配输出
        hit = 0
        formatter = '[\s(&lt)(&gt)]'
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)

            URL = doc.get("URL")
            print(URL)
            res = Query.presentQuery(URL, field=field, contentsGeneral = contentsGeneral, highlighter = highlighter, analyzer=analyzer, doc = doc)
            if res is not None:
                title = doc.get("htmlTitle")
                title = re.sub(formatter, '', title)
                content, filepath, contentsGeneral = res[0], res[1], res[2]
                print("Title:%s \n path :%s \ncontent :%s \n url:%s\n"%(title, filepath, content, URL))
                hit += 1
                #print ('Contents:', doc.get("Contents"), 'score:', scoreDoc.score)
        print ("%s total matching documents." %hit)
        del searcher



class luceneUtils:
    STOER_DIR = ''
    def __init__(self, STORE_DIR) -> None:
        # 索引目录
        directory = SimpleFSDirectory(File(STORE_DIR).toPath())
        # 索引搜索工具
        self.indexReader = DirectoryReader.open(directory)
        luceneUtils.STOER_DIR = STORE_DIR

    def updateDocument(field, value, document):
        IndexWriter = Indexer.getIndexWriter(storeDir='')
        try:
            IndexWriter.updateDocument(Term(field, value), document)
            Indexer.closeWriter(IndexWriter)
        except Exception as error:
            print("Error encountered when updating the document", error)

    def delDocument(field, value, doc):
        IndexWriter = Indexer.getIndexWriter(storeDir='')
        try:
            IndexWriter.deleteDocuments(Term(field, value))
            Indexer.closeWriter(IndexWriter)
        except Exception as error:
            print("Error encountered when deleting the document", error)

    # get all the terms in a given docID and field
    def getTerms(self, docID, field):
        fields = self.indexReader.getTermVectors(docID)
        # Access to the terms in a specific field.
        terms = fields.terms(field)
        # Returns an iterator that will step through all terms
        if terms is None:
            return None
        termsEnum = terms.iterator()
        # Iterate the terms
        mapObj = map(operator.methodcaller('utf8ToString'), BytesRefIterator.cast_(termsEnum))
        print(list(mapObj))
        return (mapObj, termsEnum.docFreq())

    # Get the posting Eunm for every term
    def getPostingEnum(self, term):
        # Whats the difference between a leafreader and a composite reader?
        leafReader = self.indexReader.leaves().get(0).reader()
        postingsEnum = leafReader.postings(term, PostingsEnum.ALL)

        termDict = dict()

        while(postingsEnum.nextDoc() != DocIdSetIterator.NO_MORE_DOCS):
        
            counter = postingsEnum.freq()
            print(counter)
            termDict[postingsEnum.docID] = [counter, []]
            while counter > 0:
                postingsEnum.nextPosition()
                termDict[postingsEnum.docID][1].append(postingsEnum.startOffset())
                counter -= 1


if __name__ == "__main__":

    
    INDEX_DIR = "URLinfo"
    """ query = TermQuery(Term("Images", "三角恋"))
    htmlFormatter = SimpleHTMLFormatter("<em>", "<em>")
    queryScorer = QueryScorer(query)
    highlighter = Highlighter(htmlFormatter, queryScorer)
    fragmenter = SimpleFragmenter(120)
    highlighter.setTextFragmenter(fragmenter) """
    
    
    luceneutils = luceneUtils("URLinfo")
    luceneutils.getTerms(5, "Images")
    exit()
    #analyzer = StandardAnalyzer()
    analyzer = WhitespaceAnalyzer()
    #res = QueryParser("Contents", analyzer).parse("上海")
    query = "鞠婧祎"
    field = "Contents"

    """ query = TextProcessing.TokenizeChinese(query) """

    res = QueryParser(field, analyzer).parse("漕河泾")
    res = TermQuery(Term("Contents", "中共中央"))
    print(res)
    #res = Query.parseQuery(query, analyzer = WhitespaceAnalyzer())
    #print(res.clauses())
    Query.run(INDEX_DIR, res, field)
'''

postingsEnum.nextDoc()
postingsEnum.nextDoc()
postingsEnum.nextDoc()
print(postingsEnum.docID())

while True:
    print(postingsEnum.endOffset())
    print(postingsEnum.freq())
    if postingsEnum.nextPosition() == -1:
        break
'''
