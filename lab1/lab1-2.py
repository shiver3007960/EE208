import re
import urllib.request
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def parseIMG(content):

    urlset = set()

    s = content.decode("UTF-8")
    pat = re.compile(r'''(?<=<img src=(["']))([^"']+?)(?=\1.*>)''', re.DOTALL)

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
    url = "https://image.baidu.com"
    content = urllib.request.urlopen(url).read()
    urlSet = parseIMG(content)
    write_outputs(urlSet, "res2.txt")

if __name__ == '__main__':
    main()