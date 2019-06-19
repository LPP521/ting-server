from parsel import Selector
import requests
import json
import urllib.parse

class Ting89:
    def getList(self,url):
        r=requests.get(url)
        r.encoding = 'gb2312' # 此网站不规范，只能手写
        
        sel = Selector(r.text)

        dataAll = []

        for s in sel.xpath("//div[@class='numlist border'][2]//a"):
            title = s.xpath("./text()").get()
            url = s.xpath("./@href").get()
            data = {
                "title":title,
                "url":urllib.parse.urljoin(r.url, url)
            }
            dataAll.append(data)
        return dataAll

    def getUrl(self,url,index):
        dataAll = self.getList(url)
        r = requests.get(dataAll[index]['url'])
        r.encoding = 'gb2312'
        sel = Selector(r.text)
        iframe = sel.xpath("//iframe[contains(@src,'mp3')]/@src").get()
        print('iframe:',iframe)
        a = (iframe.split('9090/'))[1]
        url = "http://mp3-f.ting89.com:9090/"+urllib.parse.quote(a)
        # print(url)
        return url

if __name__=='__main__':
    t = Ting89()
    print(t.getUrl("http://www.ting89.com/books/13503.html",0))
    # print(t.getList("http://www.ting89.com/books/13503.html"))

