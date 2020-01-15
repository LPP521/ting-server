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
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class Ysts8:
    def init(self):
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

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
        url2 = ""

        option = webdriver.FirefoxOptions()
        option.add_argument("-headless")
        option.set_preference('permissions.default.image', 2)
        option.set_preference('permissions.default.stylesheet',2)
        print("ss0")
        driver = webdriver.Remote(
            # command_executor="http://selenium-hub:4444/wd/hub",
            options=option,
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        
        try:
            driver.get(sounds[index]['url'])
            print(driver.title)
            iframe = driver.find_element_by_xpath("//iframe[@id='play']")
            time.sleep(1)
            # wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(iframe))
            driver.switch_to.frame(iframe)
            # print("page_source:")
            # print(driver.page_source)
            
            cc = driver.find_element_by_tag_name("audio")
            url2 = cc.get_attribute('src')
        except :
            print("xpath error")
        finally:
            driver.quit()

        if url2 == "":
            data = {
                "url":'',
                'error':'timeout'
            }
            return data
        else:
            # print(url2)        
            data = {
                "url":url2,
                'error':''
            }
            return data

if __name__=='__main__':
    y = Ysts8()
    # print(y.search("神霄煞仙"))
    # print(y.getAlbumData("https://www.ysts8.net/Yshtml/Ys7524.html"))
    print(y.getUrl("https://www.ysts8.net/Yshtml/Ys7524.html",226))
    # y.test()
