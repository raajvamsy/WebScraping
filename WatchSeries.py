from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib2 import Request,urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict


class WatchSeries:
    def __init__(self,url=None):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe",
                                       chrome_options=chrome_options
                                       )
        self.url = url
        self.getthelinks()

    def soupobj(self,link):
        page_source = urlopen(Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read()
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    def getthelinks(self):

        soup = self.soupobj(self.url)
        title = soup.find('a',attrs={'itemprop':'url'}).find('span',attrs={'itemprop':'name'}).get_text()
        file = open(str(title)+'.html','w')
        file.write('<html><head><title>The Mentalist</title><style>table{margin:20 0 20 20px;}td{padding:0 0 0 10px;}</style></head><body>')
        seasons = OrderedDict()
        list = soup.find_all('div',attrs={'itemprop':'season'})
        for i in list:
            seasons[str(i.find('span',attrs={'itemprop':'name'}).get_text())]=OrderedDict()
        for i in list:
            s = str(i.find('span',attrs={'itemprop':'name'}).get_text())
            for j in i.find_all('li'):
                seasons[s][str(j.find('a').find('span').get_text().replace(u'\xa0',u' '))]=str(j.find('a')['href'])
        for i in seasons:
            for j in seasons[i]:
                link = seasons[i][j]
                l = link
                soup = self.soupobj(link)
                try:
                    link = str(soup.find('a', attrs={'title': 'powvideo.net'})['href'])
                    self.driver.get(link)
                    link = str(self.driver.find_element_by_xpath('//a[@class="push_button blue"]').get_attribute('href'))
                except:
                    link = l
                seasons[i][j]=link
        self.driver.close()
        for i in seasons:
            file.write('<table><thead><th>'+str(i)+'</th></thead><tbody>')
            for j in seasons[i]:
                file.write('<tr><th>'+str(j)+'</th><td><a href="'+seasons[i][j]+'">'+seasons[i][j]+'</a></td></tr>')
            file.write('</tbody>')
        file.write('</table></body></html>')
        file.close()
if __name__=="__main__":
    url = str(raw_input("Enter the url: ").strip(' '))
    watch = WatchSeries(url)
