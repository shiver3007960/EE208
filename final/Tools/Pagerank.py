import numpy as np
import time
import re
import jieba
from jieba import posseg as pseg
import math
from functools import reduce

        
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


a = np.array([[0, 0, 1/2, 1], [1/2, 0, 0, 0], [1/2, 1, 0, 0], [0, 0, 1/2, 0]])


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
                self.dictionary[word]['idf'] = math.log(len(documents) / (document_frequency + 1), 10)
            else:
                self.dictionary[word]['idf'] = math.log(len(documents) / document_frequency, 10)
        
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
        
        return len(_words & words) / math.log(len(_words), 10) + math.log(len(words), 10)

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



