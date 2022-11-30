# SJTU EE208

INDEX_DIR = "test"

import os, lucene, re
from functools import reduce
from func_timeout import func_set_timeout
import func_timeout
from org.apache.lucene.index import IndexWriter

if __name__ == "__main__":
    VM = lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import MMapDirectory


class Indexer(object):
    """Usage: python IndexFiles <doc_directory>"""


    URLfield = FieldType()
    URLfield.setStored(True)
    URLfield.setTokenized(False)
    URLfield.setIndexOptions(IndexOptions.DOCS)  # Not Indexed
    
    datafield = FieldType()
    datafield.setStored(True)
    datafield.setTokenized(True)
    datafield.setStoreTermVectors(False)
    datafield.setStoreTermVectorPositions(False)
    datafield.setStoreTermVectorOffsets(False)
    datafield.setIndexOptions(IndexOptions.DOCS)
    #datafield.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)  # Indexes documents, frequencies and positions.

    htmlField = FieldType()
    htmlField.setStored(True)
    htmlField.setTokenized(True)
    htmlField.setIndexOptions(IndexOptions.DOCS)  # Not Indexed
    
    indexWriters = dict()

    __slots__ = ['storeDir', 'VM']

    def __init__(self, storeDir, VM = None):
        VM.attachCurrentThread()
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        self.storeDir = storeDir
        self.VM = None if VM is None else VM
        # store = SimpleFSDirectory(File(storeDir).toPath())

    @staticmethod
    def getIndexWriter(storeDir, VM) -> IndexWriter:
        print(storeDir)
        VM.attachCurrentThread()
        store = MMapDirectory(Paths.get(storeDir))
    
        analyzer = WhitespaceAnalyzer()
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
        try:
            writer = IndexWriter(store, config)
            while not isinstance(writer, IndexWriter):
                writer = IndexWriter(store, config)
            return writer
        except Exception as error:
            print("Index Writer Error", error)
        
    @staticmethod
    def closeWriter(indexWriter = None)-> None:
        #try:
        if isinstance(indexWriter, IndexWriter) and indexWriter.isOpen():
            indexWriter.commit()
            directory = indexWriter.getDirectory()
            if directory in Indexer.indexWriters.keys():
                del Indexer.indexWriters[directory]
            #Optimize by combining segments
            indexWriter.forceMerge(1)
            indexWriter.close()
        
    @staticmethod
    def terminateIndexWriters() -> None:
        print("********terminating all indexWriters********")
        mapObj = list(map(lambda key: Indexer.closeWriter(Indexer.indexWriters[key]), Indexer.indexWriters.keys()))

    @staticmethod
    def indexDocs(indexWriter = None, root = None, content = None):
            
        def _index(info):
            
            root = info[0]
            dirname = info[1]
            filenames = info[2]

            def _indexFile(filename):
                if not filename.lower().endswith('.txt'):
                    return
                path = os.path.join(root, dirname if dirname else '', filename)
                file = open(path, encoding='utf-8')
                contents = file.read()
                print(path)
                Indexer._indexDocs(indexWriter, contents, path)
                file.close()
                return filename

            filterObj = list(filter(_indexFile, filenames))
            return filterObj

        
        fileObj = reduce(lambda a, b: a + b, map(_index, os.walk(root)), [])
        print(fileObj)
        Indexer.closeWriter(indexWriter)
        return
     
    @staticmethod
    def _indexDocs(indexWriter, content, path):
        doc = Document()
        doc.add(Field("path", path, Indexer.URLfield))
        doc.add(Field("contents", content, Indexer.datafield))
        indexWriter.addDocument(doc)

    @staticmethod
    def indexURL(urlInfo, indexWriter, timeout = 1000, VM = None):

        @func_set_timeout(timeout)
        def _indexURL(urlInfo, indexWriter) -> None:

            VM.attachCurrentThread()
            doc = Document()

            #1.Index HTMlDoctitle ('None' respresents none)
            HTMLDoctitle = "None" if not isinstance(urlInfo[1], str) or len(urlInfo[1]) < 2 else urlInfo[1]
            doc.add(Field("htmlTitle",HTMLDoctitle, Indexer.htmlField))
            #2.Index URL
            URL = "None" if not isinstance(urlInfo[2], str) or len(urlInfo[2]) < 2 else urlInfo[2]
            doc.add(Field("URL",URL, Indexer.URLfield))
            #3.Index Content
            content = 'None' if not isinstance(urlInfo[3], str) or len(urlInfo[3]) < 2 else urlInfo[3]
            content = re.sub('[^\u4e00-\u9fff\w\d]', ' ', content)
            doc.add(Field("Contents", content, Indexer.datafield))
            #4.Index URlLinks
            if isinstance(urlInfo[4], list) and len(urlInfo[4]) == 3:
                linksInfo = urlInfo[4]
                doc.add(Field("Links", '内链或外链 %s 资源下载 %s 网页元素 %s '%(' '.join(linksInfo[0]), ' '.join(linksInfo[1]), ' '.join(linksInfo[2])), Indexer.datafield))
            #5.Index Images
            if isinstance(urlInfo[5], dict) and len(urlInfo[5].keys()) > 0:
                res = ' '.join(map(lambda key: ' %s %s '%(key, ' '.join(urlInfo[5][key])) if isinstance(urlInfo[5][key][0], str) and len(urlInfo[5][key][0]) > 1 else '', urlInfo[5].keys()))
                doc.add(Field("Images", res, Indexer.datafield))
            indexWriter.addDocument(doc)
            indexWriter.commit()
        try:
            _indexURL(urlInfo, indexWriter)
        except func_timeout.exceptions.FunctionTimedOut as error:
            print("Indexing Operation timed out: %s"%(urlInfo[2]))
        except Exception as error:
            with open("ParseLog.txt", "a+") as file:
                file.writelines(' %s '%str(error))
                file.writelines('\n')
