#coding=utf-8
from parsel import Selector
import requests
import json
import urllib.parse
from requests.adapters import HTTPAdapter

class Ting89:
    def search(self,name):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'searchword':name,
            'searchtype':'-1',
            'submit':'搜索'
        }
        data_gb2312 = urllib.parse.urlencode(data, encoding='gb2312')
        try:
            r = requests.post('http://www.ting89.com/search.asp', data=data_gb2312, headers=headers,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return []

        r.encoding = 'gb2312'
        sel = Selector(r.text)

        albumList = []
        for c in sel.xpath("//div[@class='clist']//li"):
            album = {}
            album['title']=c.xpath(".//b/text()").get()
            album['author']=c.xpath(".//p[3]/text()").get()
            album['sound']=c.xpath(".//p[4]/text()").get()
            album['url']=urllib.parse.urljoin(r.url, c.xpath("./a/@href").get())
            albumList.append(album)
        
        return albumList

    def getAlbumData(self,url):
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            r=s.get(url,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'timeout'}
        r.encoding = 'gb2312' # 此网站不规范，只能手写
        
        sel = Selector(r.text)

        albumTitle = sel.xpath("//h1/text()").get()
        sounds = []

        for s in sel.xpath("//div[@class='numlist border'][2]//a"):
            title = s.xpath("./text()").get()
            url = s.xpath("./@href").get()
            data = {
                "title":title,
                "url":urllib.parse.urljoin(r.url, url)
            }
            sounds.append(data)
        data = {
            'title':albumTitle,
            'sounds':sounds,
            'error':''
        }
        return data

    def getUrl(self,url,index):
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        ad = self.getAlbumData(url)
        if ad['error'] != '':
            return {'error':'timeout'}
        sounds = self.getAlbumData(url)['sounds']
        try:
            r = s.get(sounds[index]['url'],timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'timeout'}
        r.encoding = 'gb2312'
        sel = Selector(r.text)
        iframe = sel.xpath("//iframe[contains(@src,'mp3')]/@src").get()
        # print('iframe:',iframe)
        u = (iframe.split('url='))[1]
        s = u.split('9090/')
        # print(s[1])
        url = s[0]+'9090/'+urllib.parse.quote(s[1])
        # print(url)
        data = {
            "url":url,
            'error':''
        }
        return data

if __name__=='__main__':
    t = Ting89()
    # print(t.getUrl("http://www.ting89.com/books/13503.html",0))
    # print(t.getAlbumData("http://www.ting89.com/books/13503.html"))
    print(t.search("阳间巡逻人"))

