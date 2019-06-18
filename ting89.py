from parsel import Selector
import requests
import json
class Ting89:
    def getList(self,url):
        r=requests.get(url)

        sel = Selector(r.text)

        dataAll = []

        for s in sel.xpath("//div[@class='numlist border'][2]//a"):
            title = s.xpath("./text()").get()
            url = s.xpath("./@href").get()
            data = {
                "title":title,
                "url":url
            }
            dataAll.append(data)
        return dataAll

    def getUrl(self,url,index):
        dataAll = self.getList(url)
        r = requests.get('http://www.ting89.com'+dataAll[index]['url'])
        sel = Selector(r.text)
        iframe = sel.xpath("//iframe[contains(@src,'mp3')]/@src").get()
        r = requests.get(iframe)
        sel = Selector(r.text)
        return sel.xpath("//a[contains(@href,'mp3')]/@href").get()

if __name__=='__main__':
    t = Ting89()
    print(t.getUrl("http://www.ting89.com/books/13503.html",0))
    # print(t.getList("http://www.ting89.com/books/13503.html"))

