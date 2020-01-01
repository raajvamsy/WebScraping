import os
import json
import re
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, pyqtSignal
import openpyxl
import time

class AliExpress:

    def __init__(self):
        pass

    def so(self, url):
        page_source = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read()
        soup = BeautifulSoup(page_source, "html.parser")
        return soup

    def PageExtract(self,i):
        catid,title,link,id,price,ratings,orders = [],[],[],[],[],[],[]
        s = time.time()
        url = "https://www.aliexpress.com/af/category/100003070.html?catName=men-clothing&CatId=100003070&origin=n&spm" \
              "=2114.search0603.2.3.1f3641d4Fa6YMt&jump=afs&page=" + str(i)
        soup = self.so(url)
        string = re.compile('&CatId=(.*?)&')
        ctid = (str(re.findall(string, url)[0]))
        string = re.compile("/\d+.html")
        page_items = soup.find_all("div", attrs={"class": "item"})
        for item in page_items:
            catid.append(ctid)
            info = item.find("div", attrs={"class": "info"})
            link.append(str(info.find("h3").find("a")["href"]).replace('//', ''))
            title.append(str(info.find("h3").find("a").get_text().encode('utf-8').strip()))
            id.append(str(re.findall(string, str(info.find("h3").find("a")["href"]).replace('//', ''))[0]).strip(
                '/').strip('.html'))
            price.append(str(info.find("span").find("span", attrs={"class": "value"}).get_text()).replace('US', ''))
            try:
                ratings.append(
                    str(info.find("div").find("span")["title"]).replace("Star Rating:", '').replace('out of 5',
                                                                                                    ''))
            except:
                ratings.append('')
            try:
                o = int(
                    str(info.find("span", attrs={'class': "order-num"}).find("a").find("em").get_text()).replace(
                        'Orders', '').strip(' (').strip(')'))
                if o > 10:
                    orders.append(o)
                else:
                    orders.append('')
            except:
                orders.append('')
        df = pd.DataFrame({"CategoryID":catid,"Title":title,"AliID":id,"Price":price,"Ratings":ratings,"Orders":orders})
        with open('Alisample.csv', 'a') as f:
            df.to_csv(f, sep=',')
        print time.time()-s
    def Extract(self):
        s = time.time()
        for i in range(1,100):
            self.PageExtract(i)
        print time.time()-s

if __name__ == "__main__":
    ali = AliExpress()
    ali.Extract()
