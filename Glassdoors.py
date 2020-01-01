from urllib2 import Request,urlopen
from bs4 import BeautifulSoup
import os,time,json,csv

class GlassDoors:

    def __init__(self,site=""):
        self.site = site
        self.jsondata = {"Reviews":[]}
    def soupobj(self,link):
        page_source = urlopen(Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read()
        soup = BeautifulSoup(page_source, "html.parser")
        return soup

    def Extraction(self):
        pgno=1
        temp = ["Recommend Job","Outlook of Firm","Approval of CEO"]
        reviews = 0
        while True:
            soup = self.soupobj(self.site+"_P"+str(pgno)+".htm")
            total_reviews = int(soup.find('a',attrs={"data-label":"Reviews"}).find('span').get_text())
            size = len(soup.find("div",attrs={"id":"ReviewsRef"}).find('ol').find_all('li',attrs={"class":"empReview cf"}))
            if(size>0):
                for i in soup.find_all('div',attrs={"class":"hreview"}):
                    js = {}
                    js["title"]= i.find('span',attrs={"class":"summary"}).get_text()
                    js["Overall Rating"]=i.find('span',attrs={"class":"value-title"})["title"]
                    for j in i.find('ul',attrs={"class":"undecorated"}).find_all('li'):
                        js[j.find('div').get_text()]=j.find('span')["title"]
                    no = 0
                    for j in i.find_all('div',attrs={"class":"col-sm-4"}):
                        js[temp[no]]= j.find("span").get_text()
                        no=no+1
                    s = ""
                    for j in i.find_all("p"):
                        s = s + j.get_text()
                    js["Qualitative review"]= s.replace("\n","")
                    self.jsondata["Reviews"].append(js)
                    reviews = reviews+1
                    print str(reviews)+"/"+str(total_reviews)
                pgno=pgno+1
            else:
                break
if __name__ == "__main__":
    site = raw_input("Site address:")
    site = site.replace(".htm","").replace(" ","")
    filename = site[site.rfind("/")+1:len(site)]
    obj = GlassDoors(site)
    obj.Extraction()
    print "Saving to "+filename+".csv .."
    headers = []
    data = []
    for i in obj.jsondata["Reviews"][0]:
        headers.append(i)
    for i in obj.jsondata["Reviews"]:
        d = []
        for j in headers:
            try:
                d.append(i[j])
            except:
                d.append("NONE")
        data.append(d)
    with open(filename+'.csv', mode='wb') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for i in data:
            writer.writerow([unicode(s).encode("utf-8") for s in i])

    # print "Saving to "+filename+".json .."
    # with open(filename+'.json', 'w') as f:
    #     json.dump(obj.jsondata, f, indent=4)
