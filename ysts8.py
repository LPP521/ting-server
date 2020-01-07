#coding=utf-8
from parsel import Selector
import requests
import json
import urllib.parse
from requests.adapters import HTTPAdapter
from getUrlFromDatas import getUrlFromDatas
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        driver.set_page_load_timeout(5)
        url2 = ""
        try:
            driver.get(sounds[index]['url'])
            print(driver.title)
            iframe = driver.find_element_by_xpath("//iframe[@id='play']")
            driver.switch_to_frame(iframe) 
            cc = driver.find_element_by_tag_name("audio")
            url2 = cc.get_attribute('src')
        except:
            print("xpath error")
        finally:
            driver.quit()

        print(url2)
        if url2 != "":
            data = {
                "url":url2,
                'error':''
            }
            # print(data)
            return data

        return self.getUrl(url,index)

    def test(self):
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        driver.set_page_load_timeout(5)
        try:
            driver.get("https://www.ysts8.net/play_16188_55_1_1.html")
            print(driver.title)
            iframe = driver.find_element_by_xpath("//iframe[@id='play']")
            driver.switch_to_frame(iframe) 
            cc = driver.find_element_by_tag_name("audio")
            print(cc.get_attribute('src'))
        except:
            print("xpath error")
        finally:
            driver.quit()
        
        
if __name__=='__main__':
    # t = Woai()
    # print(t.getUrl("http://www.woaitingshu.com/mp3/4839.html",246))
    # print(t.getAlbumData("http://www.woaitingshu.com/mp3/4839.html"))
    # print(t.search("阳间巡逻人"))
    y = Ysts8()
    # print(y.search("神霄煞仙"))
    print(y.getUrl("https://www.ysts8.net/Yshtml/Ys16188.html",100))
    # y.test()
