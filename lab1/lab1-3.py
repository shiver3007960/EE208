# SJTU EE208

import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


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


def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()


def main():
    url = "http://daily.zhihu.com/"
    content = urllib.request.urlopen(url).read()
    zhihus = parseZhihuDaily(content, url)
    write_outputs(zhihus, "res3.txt")


if __name__ == '__main__':
    main()