import math
from operator import length_hint
from bitarray import bitarray

'''
This document implements some general purpose function hash functions
and completes class BloomFilter
'''

class BloomFilter:

    def __init__(self, number = None, false_positive = None ) -> None:
        self.number = number if isinstance(number, int) else 20
        self.false_postive = false_positive
        self.arraylen = math.floor(- (self.number * math.log(self.false_postive)) / (math.log(2) * math.log(2)))
        self.hash_number = math.floor(0.7 * self.arraylen / self.number)
        self.bitarray_obj = bitarray(self.arraylen)
        self.bitarray_obj.setall(0)
        self.elements = 0
        self.hashList = self.hashList = [self.RSHash, self.JSHash, self.PJWHash, self.SDBMHash,self.DJBHash,\
             self.DEKHash, self.APHash, self.BKDRHash]

    @property
    def arrayLen(self):
        return self.arraylen
    
    @property
    def counter(self):
        return self.elements
        
    def put(self, target = None | str) -> None:
        if isinstance(target, str):
            hash_number, index= self.hash_number, 0
            while hash_number > 0:
                while index < len(self.hashList) - 1:
                    self.bitarray_obj[self.hashList[index](target)] = 1
                    index += 1
                else:
                    seed = '13' * (math.floor((hash_number + 2) / 2)) + '1' * ((hash_number + 2) & 1)
                    self.bitarray_obj[self.hashList[index](target, int(seed))] = 1
                hash_number -= 1
    
    def isExist(self, target = None) -> bool:
        if isinstance(target, str):
            hash_number, index= self.hash_number, 0
            while hash_number > 0:
                while index < len(self.hashList) - 1:
                    if not self.bitarray_obj[self.hashList[index](target)]:
                        return False
                    index += 1
                seed = '13' * (math.floor((hash_number + 2) / 2)) + '1' * ((hash_number + 2) & 1)
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

if __name__ == "__main__":
    length = 11
    b = BloomFilter(256 * (length + 1), 0.00000001)
    for i in range(0, 256):  # produce all 'xxxx','xxx','xx','x' in ASCII
        for j in range(1, length):
            b.put(chr(i) * j) # total 256 * 2 = 512

    cnt = 0
    new = ' ' * length
    while not b.isExist(new):
        new = chr(cnt % 256) * (length + int(cnt / 256)) # produce 'xxxxx...' by order
        #print(new)
        cnt += 1
    
    print(cnt)