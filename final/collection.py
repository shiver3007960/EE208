from math import floor, log
from bitarray import bitarray
from time import time
import numpy as np
import re
import signal
import jieba
from jieba import posseg as pseg
from functools import reduce
from func_timeout import func_set_timeout
import func_timeout
'''
This document implements some general purpose functions
'''

import threading
import time
import inspect
import ctypes
 
# Reference to the network
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def isValidURL(query):
    if not isinstance(query, str) or len(query) < 1:
        return False
    urlPattern = '/;；?#a-zA-Z0-9\._=-'
    searchHTTP = re.search('(?:(?<=https:/)|(?<=http:/)|(?<=ftp:/))[' + urlPattern +\
        ']{6,}(?=([^' + urlPattern + ']|$))', query)
    if searchHTTP is not None:
        return True
    searchWWW = re.search('(?:(?<=www\.)|(?<=wwww\.))[' +  urlPattern +\
        ']{6,}(?=([^' + urlPattern + ']|$))', query)
    if searchWWW is not None:
        return True
    searchCOM = re.search('(?:(?<=[^' + urlPattern + '])|(?<=^))[' +  \
        urlPattern + ']{4,}[(.com)|(.cn)][' + urlPattern + ']*(?=([^' + urlPattern + ']|$))', query)
    if searchCOM is not None:
        return True
    return False

class TimeOutHandler:

   

    def __init__(self):
        pass

    @staticmethod
    def time_out(interval, callback = None):
        def decorator(func):
            @func_set_timeout(interval)
            def _func(*args, **kwargs):
                func(*args, **kwargs)
            def wrapper(*args, **kwargs):
                try:
                    result = _func(*args, **kwargs)
                    print(result)
                    return result
                except func_timeout.exceptions.FunctionTimedOut as error:
                    if callback is not None:
                        callback(*args, **kwargs)
                    else:
                        pass
            return wrapper
        return decorator

class BloomFilter:

    def __init__(self, number = None, false_positive = None ) -> None:
        self.number = number if isinstance(number, int) else 20
        self.false_postive = false_positive
        self.arraylen = floor(- (self.number * log(self.false_postive)) / (log(2) * log(2)))
        self.hash_number = floor(log(10, 2) * self.arraylen / self.number)
        self.bitarray_obj = bitarray(self.arraylen)
        self.bitarray_obj.setall(0)
        self.elements = 0
        self.hashList = [self.RSHash, self.JSHash, self.PJWHash, self.SDBMHash,
                         self.DJBHash, self.DEKHash, self.APHash, self.BKDRHash]

    @property
    def arrayLen(self):
        return self.arraylen
    
    @property
    def counter(self):
        return self.elements
        
    def put(self, target = None) -> None:
        if isinstance(target, str):
            hash_number, index= self.hash_number, 0
            while hash_number > 0:
                while index < len(self.hashList) - 1:
                    self.bitarray_obj[self.hashList[index](target)] = 1
                    index += 1
                seed = '13' * (floor((hash_number + 2) / 2)) + '1' * ((hash_number + 2) & 1)
                self.bitarray_obj[self.hashList[index](target, int(seed))] = 1
                hash_number -= 1
            self.elements += 1
    
    def isExist(self, target = None) -> bool:
        if isinstance(target, str):
            hash_number, index= self.hash_number, 0
            while hash_number > 0:
                while index < len(self.hashList) - 1:
                    if not self.bitarray_obj[self.hashList[index](target)]:
                        return False
                    index += 1
                seed = '13' * (floor((hash_number + 2) / 2)) + '1' * ((hash_number + 2) & 1)
                if not self.bitarray_obj[self.hashList[index](target, int(seed))]:
                    return False
                hash_number -= 1
            return True
        else:
            return False

    # Reference to General Purpose Hash function:
    # http://www.partow.net/programming/hashfunctions/#top
    def RSHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        b, a, hash, i = 378551, 63689, 0, 0
        length = len(string)
        for i in range(0, length):
            hash = hash * a + ord(string[i])
            a *= b
        return hash % self.arraylen
    
    def JSHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        hash, i = 1315423911, 0
        length = len(string)
        for i in range(0, length):
            hash ^= ((hash << 5) + ord(string[i]) + (hash >> 2))
        return hash % self.arraylen
    
    def PJWHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        BitsInUnsignedInt, ThreeQuarters, OneEigth, HighBits = (32, int(32 * 3 / 4), 4, int(0xFFFFFFFF) << 24)
        hash, test, i = 0, 0, 0
        length = len(string)
        for i in range(0, length):
            hash = (hash << OneEigth) + ord(string[i])
            test = hash & HighBits
            if test:
                hash = ((hash ^ (test >> ThreeQuarters)) & (~HighBits))
        return hash % self.arraylen

    def BKDRHash(self, string, seed):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        hash, i = 0, 0
        length = len(string)
        for i in range(0, length):
            hash = (hash * seed) + ord(string[i])
        return hash % self.arraylen
    
    def SDBMHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        hash, i = 0, 0
        length = len(string)
        for i in range(0, length):
            hash = (hash << 6) + ord(string[i]) + (hash << 16) - hash
        return hash % self.arraylen
    
    def DJBHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        hash, i = 5381, 0
        length = len(string)
        for i in range(0, length):
             hash = ((hash << 5) + hash) + ord(string[i])
        return hash % self.arraylen
    
    def DEKHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        length = len(string)
        hash, i = (length, 0)
        for i in range(0, length):
             hash = ((hash << 5) ^ (hash >> 27)) ^ (ord(string[i]))
        return hash % self.arraylen
    
    def APHash(self, string):
        if not isinstance(string, str):
            raise Exception("Unhashable type!")
        hash, i = 0xAAAAAAAA, 0
        length = len(string)
        for i in range(0, length):
            if (i & 1):
                hash ^= (~((hash << 11) + (ord(string[i]) ^ (hash >> 5))))
            else:
                hash =(hash << 7) ^ (ord(string[i])) * (hash >> 3)
        return hash % self.arraylen


class Weights:
        def __init__(self, tf = 0, tf_idf = 0) -> None:
            self.TF = tf if isinstance(tf, (int, float)) and tf >= 0 else 0
            self.TF_IDF = tf_idf if isinstance(tf_idf, (int, float)) and tf_idf >= 0 else 0

        @property
        def tf(self):
            return self.TF

        @tf.setter
        def tf(self, value) -> None:
            if isinstance(value, (int, float)) and value > 0:
                self.TF = value
            else:
                return

        @property
        def tf_idf(self):
            return self.TF_IDF

        @tf_idf.setter
        def tf_idf(self, value) -> None:
            if isinstance(value, (int, float)) and value > 0:
                self.TF_IDF = value
            else:
                return

        def __repr__(self) -> str:
            return '''(%s, %s)'''%(self.TF, self.TF_IDF)


def Pagerank(graph = None, max_limit = None, friction_rate = 0.15):
    start = time.time()
    if not isinstance(graph, np.ndarray) and not isinstance(max_limit, float):
        return

    # Dead Ends
    size = graph.shape[0]
    for i in np.where(~graph.any(axis=0))[0]:
        aux_vec = np.zeros((1, size))
        aux_vec[0][i] = 1
        graph += np.full((size, 1), 1 / size).dot(aux_vec)

    #Spider-traps
    aux_matrix = np.ones((size, 1)).dot(np.full((1, size), 1 / size))
    graph = friction_rate * graph + (1 - friction_rate) * aux_matrix

    initial = np.full((size, 1), 1 / size)
    while True:
        res = graph.dot(initial)
        if np.max(np.absolute(res - initial), axis = 0)[0] < max_limit:
            print("Running time:"+str(time.time() - start))
            return res
        initial = res
        

def Adaptive_Pagerank(graph = None, max_limit = None, friction_rate = 0.15):
    start = time.time()
    
    if not isinstance(graph, np.ndarray) and not isinstance(max_limit, float):
        return

    # Dead Ends
    size = graph.shape[0]

    for i in np.where(~graph.any(axis=0))[0]:
        
        aux_vec = np.zeros((1, size))
        aux_vec[0][i] = 1
        graph += np.full((size, 1), 1 / size).dot(aux_vec)
    

    #Spider-traps
    aux_matrix = np.ones((size, 1)).dot(np.full((1, size), 1 / size))
    graph = friction_rate * graph + (1 - friction_rate) * aux_matrix

    prev = np.full((size, 1), 1 / size)
    NN_matrix, CN_matrix = np.copy(graph), np.copy(graph)
    CN_const, CN_vector, C_vector = np.zeros((size,1)), np.zeros((size,1), dtype=np.int32), np.zeros((size, 1))
    prev_CN_vector, prev_NN_vector = np.zeros((size,1)), np.ones((size,1))
    N_vector = np.copy(prev)

    while True:
        
        after = NN_matrix.dot(N_vector) + C_vector + CN_const

        prev_CN_vector = CN_vector

        CN_vector = np.array([np.all(np.absolute(after - prev) < max_limit, axis = 1)], dtype=np.bool8)
        # Judge whether changes should be made
        if np.any(np.array(prev_CN_vector ^ CN_vector), axis=1)[0]:
            #modify the Ann matrix
            NN_matrix[CN_vector[0]] = 0
            NN_matrix.transpose()[CN_vector[0]] = 0
            #modify the Acn matrix
            CN_matrix[CN_vector[0]] = 0
            CN_matrix.transpose()[~CN_vector[0]] = 0
            #Construct the Xn and Xc vector
            C_vector = after * CN_vector.transpose()
            N_vector = after * ~CN_vector.transpose()
            
            CN_const = CN_matrix.dot(prev)

        if np.max(np.absolute(after - prev), axis = 0)[0] < max_limit:
            print("Running time: ", time.time() - start)
            return after
        
        prev = after


class TextRank():

    def __init__(self, content= '', document=dict(), parallel:int = 1) -> None:
        self.content = content if isinstance(content, str) else ''
        self.queries = dict()

        self.sentences_num = 0
        self.sentence_matrix = None
        self.text_rank = None

        self.dictionary = dict()

        self._parallel = parallel
        self._search_scope = ()

        self.documents = dict()
        self.docContainer = dict()

        if isinstance(document, dict) and document:
            for key in document.keys():
                self.docContainer[key] = set()
                self.documents[key] = document[key]

    @property
    def parallel(self):
        return self._parallel

    @parallel.setter
    def parallel(self, num:int) -> None:
        self._parallel = num
        
    def __segSentence(self) -> None:
        index = 0

        if not self.content:
            return 

        for context in re.split(r'\。|\!|\！|\？|\?', self.content):
            if re.search(r'\b[^u4E00-\u9FA5]+\b', context) is not None:
                self.queries[index] = [re.sub(r'[^u4E00-\u9FA5]', '', context), 0]
                index += 1

        self.sentences_num = len(self.queries)
        
        self.sentence_matrix = np.zeros((self.sentences_num, self.sentences_num))
        for vertice in range(0, self.sentences_num):
            for adjacent_vertice in range(vertice + 1, self.sentences_num):
                similarity = self.sentenceSimilarity(self.queries[vertice][0], self.queries[adjacent_vertice][0])
                if similarity:
                        self.sentence_matrix[vertice][adjacent_vertice] = similarity

    def textRank(self, max_limit = 0.001, friction_rate = 0.15):
        
        start = time.time()
        
        if not self.content:
            return

        if not self.sentences_num:
            self.__segSentence()

        self.text_rank = np.full((self.sentences_num, 1), 1 / self.sentences_num)
       
        for vertice in range(0, self.sentences_num):
            for adjacent_vertice in range(vertice + 1, self.sentences_num):
                self.sentence_matrix[vertice][adjacent_vertice] /= (np.sum(self.sentence_matrix[vertice]) + \
                        np.sum(self.sentence_matrix.transpose()[adjacent_vertice]))
        
        res = self.__textRank(max_limit, friction_rate)
        print("Running time:", time.time() - start)

        for sentence in range(0, self.sentences_num):
            self.queries[sentence][1] = self.text_rank[sentence][0]

        return res

    def __textRank(self, max_limit = 0.001, friction_rate = 0.15):

        while True:
            prev = self.text_rank
            self.text_rank = 1 - friction_rate + friction_rate * self.sentence_matrix.dot(self.text_rank)
            #Pause Condition
            if (np.max(np.absolute(self.text_rank - prev), axis = 0))[0] < max_limit:
                return self.text_rank

    def TF(self, name:str = '', attributes:tuple = ('r', 'a', 'v')):
        if not isinstance(name, str) or not name or not name in self.documents.keys():
            return
        
        if self.docContainer[name]:
            return

        for word, attr in pseg.cut(self.documents[name]):
            if not attributes or attr in attributes:
                self.docContainer[name].add(word)
                if word not in self.dictionary.keys():
                    self.dictionary[word] = {name: Weights(1, 0)}
                else:
                    if name not in self.dictionary[word].keys():
                        self.dictionary[word][name] = Weights(1, 0)
                    else:
                        self.dictionary[word][name].tf += 1
    
    def IDF(self, scope = ()):

        documents = self.documents

        for document in self.documents:
            if not self.docContainer[document]:
                self.TF(name = document)

        for word in self.dictionary.keys():
            document_frequency = 0
            for document in documents:
                if document in self.dictionary[word].keys():
                    document_frequency += 1
            
            if document_frequency == 0:
                self.dictionary[word]['idf'] = log(len(documents) / (document_frequency + 1), 10)
            else:
                self.dictionary[word]['idf'] = log(len(documents) / document_frequency, 10)
        
        for word in self.dictionary.keys():
            for document in self.dictionary[word].keys():
                if document != 'idf':
                    self.dictionary[word][document].tf_idf = self.dictionary[word]['idf'] \
                        * self.dictionary[word][document].tf
        
    def sentenceSimilarity(self, sen1, sen2, attributes = ()):
        if not isinstance(sen1, str) or not isinstance(sen2, str) or not sen1 or not sen2:
            return 0
        #jieba.enable_parallel(processnum = self._parallel)
        
        _words = set(list(word for word, attr in pseg.cut(sen1) if not attributes or attr in attributes))
        words = set(list(word for word, attr in pseg.cut(sen2) if not attributes or attr in attributes))
        
        return len(_words & words) / log(len(_words), 10) + log(len(words), 10)

    def __getSignature(self, document):
        if not isinstance(document, str) and not document:
            return
        
        if not self.docContainer[document]:
            self.IDF(document)

        # Assign Weights and get eigen vector
        eigenVec1 = np.array([self.dictionary[word][document].tf_idf for word in self.docContainer[document]])
        #print(self.dictionary)
        #Compute Hash
        hash_vec = np.array([hash(word) for word in self.docContainer[document]])
        # Compute
        def add_hash(hash_value, tf_idf):
            raw_hash = re.sub('-0b|0b', '', str(bin(hash_value)))
            hash_string = (63 - len(raw_hash)) * '0' + raw_hash
            
            temp = np.all(np.array([list(hash_string)]) == '1', axis = 0)
            temp = np.where(np.array(temp), 1, -1)
            #print(temp * tf_idf)
            return np.array(temp * tf_idf)

        res = reduce(lambda a, b: a + b, list(map(add_hash, hash_vec, eigenVec1)), np.zeros((63, )))
        signature = np.where(res > 0, 1, 0)
        return signature

    def simHash(self, document1, document2):
        if not isinstance(document1, str) and not document1 and\
                not isinstance(document2, str) and not document2:
            return
        _signature = self.__getSignature(document1)
        signature = self.__getSignature(document2)
        return np.sum(_signature ^ signature)
