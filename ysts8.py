#coding=utf-8
from parsel import Selector
import requests
import json
import urllib.parse
from requests.adapters import HTTPAdapter
from getUrlFromDatas import getUrlFromDatas
import urllib.parse
# from selenium import webdriver

class Ysts8:
    def search(self,name):        
        name_gb2312 = urllib.parse.quote(name, encoding='gb2312')
        url = 'https://www.ysts8.net/Ys_so.asp?stype=1&keyword='+name_gb2312

        try:
            r = requests.get(url, timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return []

        r.encoding = 'gb2312'
        print(r.text)
        sel = Selector(r.text)

        albumList = []
        for c in sel.xpath("//div[@class='pingshu_ysts8']"):
            album = {}
            album['title']=c.xpath(".//a/text()").get()
            album['author']=c.xpath(".//a/span/text()").get()
            album['sound']=c.xpath(".//a/span/text()").get()
            album['url']=urllib.parse.urljoin(r.url, c.xpath(".//a[1]/@href").get())
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

        # print(r.text)

        albumTitle = sel.xpath("//div[@id='ter']//h1/text()").get()
        sounds = []

        for s in sel.xpath("//div[@class='ny_l']//ul//a"):
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
        sounds = ad['sounds']

        # driver = webdriver.Chrome()
        # driver.get(sounds[index]['url'])

        try:
            if index>= len(sounds):
                return {'error':'over'}
            # print(sounds[index]['url'])
            r = s.get(sounds[index]['url'],timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'timeout'}
        r.encoding = 'gb2312'
        # print(r.text)
        iframe = r.text.split('iframe src="')[1].split('"')[0]
        # print(iframe)
        url1 = urllib.parse.urljoin(r.url, iframe)
        
        try:
            r = requests.get(url1, timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return []

        r.encoding = 'gb2312'
        # print(r.text)

        url2 = r.text.split('mp3:\'')[1].split('\'')[0]
        if len(url2)>0 :
            if url2.endswith('.mp3') == False:
                url2 = url2 + '.mp3'
            # print(url2)
        else :
            return self.getUrl(url,index)

        # url = getUrlFromDatas(r.text)

        data = {
            "url":url2,
            'error':''
        }
        return data

if __name__=='__main__':
    # t = Woai()
    # print(t.getUrl("http://www.woaitingshu.com/mp3/4839.html",246))
    # print(t.getAlbumData("http://www.woaitingshu.com/mp3/4839.html"))
    # print(t.search("阳间巡逻人"))
    y = Ysts8()
    # print(y.search("神霄煞仙"))
    print(y.getUrl("https://www.ysts8.net/Yshtml/Ys16188.html",100))
    

