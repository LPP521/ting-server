#coding=utf-8
import os
from parsel import Selector
import requests
import json
import urllib.parse
from requests.adapters import HTTPAdapter
import pickle as pk

class Baidu:
    def search(self,name):
        lsStr = os.popen("python baidu2.py ls -c off /ting|awk '{print $3}'").read()
        albumList = []
        for n in lsStr.split('\n'):
            if len(n)>0:
                if n.find(name)>=0:
                    album = {}
                    album['title']=n
                    # album['author']=c.xpath(".//p[3]/text()").get()
                    # album['sound']=c.xpath(".//p[4]/text()").get()
                    album['url']=n
                    albumList.append(album)
        
        return albumList

    def getAlbumData(self,url):
        albumTitle = url
        lsStr = os.popen("python baidu2.py ls -c off /ting/"+url+"|awk '{print $3}'").read()
        sounds = []
        for s in lsStr.split('\n'):
            if len(s)>0 and (s.find('.mp3')>0 or s.find('.m4a')>0):
                title = albumTitle
                url = s
                data = {
                    "title":s,
                    "url":albumTitle+'/'+url
                }
                sounds.append(data)
        # sort
        sounds.sort(key=lambda n: n['url'])
        data = {
            'title':albumTitle,
            'sounds':sounds,
            'error':''
        }
        return data

    def getUrl(self,url,index):
        
        ad = self.getAlbumData(url)
        sounds = ad['sounds']
        url = os.popen("python baidu2.py d /ting/"+sounds[index]['url']).read()
        url = url[:-1]#去掉结尾的\n
        print(url)
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        
        j = pk.load(open(".bp.cookies","br"))
        try:
            header = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
            r = s.get(url,timeout=3,allow_redirects=False,cookies=j['u03013112']['cookies'],headers=header)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'timeout'}
        print(r.status_code)
        url = r.headers['Location']
        data = {
            "url":url,
            'error':''
        }
        return data

if __name__=='__main__':
    t = Baidu()
    print(t.getUrl("超级惊悚直播",0))
    # print(t.getAlbumData("超级惊悚直播"))
    # print(t.search("超级"))
    

    # url = os.popen("python ding.py d /ting/超级惊悚直播/001.mp3").read()
    # print(url)