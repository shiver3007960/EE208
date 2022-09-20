# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()

    s = content.decode("UTF-8")
    pat = re.compile(r'''(?<=<a href=(["']))\b(.+?)(?=\1.*>.*</a>)''', re.DOTALL)

    for match in re.finditer(pat, s):
        urlset.add(match.group(2))

    return urlset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "http://www.baidu.com"
    content = urllib.request.urlopen(url).read()
    urlSet = parseURL(content)
    write_outputs(urlSet, "res1.txt")


if __name__ == '__main__':
    main()
