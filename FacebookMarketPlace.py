from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from joblib import Parallel, delayed
import json,time,csv
import multiprocessing
import functools
from PIL import Image
from StringIO import StringIO

proxy = ""
path = ""
def with_timeout(timeout):
    def decorator(decorated):
        @functools.wraps(decorated)
        def inner(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(1)
            async_result = pool.apply_async(decorated, args, kwargs)
            try:
                return async_result.get(timeout)
            except multiprocessing.TimeoutError:
                return
        return inner
    return decorator

@with_timeout(50)
def getdata(item):
    global proxy,path,city,country
    data = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--hide-scrollbars")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path="chromedriver.exe",
                              chrome_options=chrome_options)
    try:
        driver.get(item)
        time.sleep(2)
        WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@itemprop="offers"]')))
        element = driver.find_element_by_xpath('//div[@data-testid="marketplace_pdp_component"]')
        element_png = element.screenshot_as_png
        path = path+str(item).replace('https://www.facebook.com/marketplace/item/','').strip('/')+'.png'
        with open(path, "wb") as file:
            file.write(element_png)
        price = driver.find_element_by_xpath('//div[@itemprop="offers"]').text
        description = driver.find_element_by_xpath('//span[@itemprop="description"]').text
        title = driver.find_element_by_xpath('//span[@data-testid="marketplace_pdp_title"]').text
        data = [item,title, price, description]
        print data
        driver.close()
        driver.quit()
        return data

    except:
        driver.close()
        driver.quit()
        getdata(item)
class webscraping:
    def __init__(self):
        global proxy
        self.chrome_options = Options()
        print proxy
        if proxy != 'None':
            self.chrome_options.add_argument('--proxy-server=%s' % proxy)
        else:
            self.chrome_options.add_argument('--no-proxy-server')
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("disable-infobars")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument('--load-images=no')
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe",
                                       chrome_options=self.chrome_options)
    def extract(self,city,query=None):
        #extract is used to get items from a market place
        links = []
        city1 = city+'search/?query='+str(query)
        print city1
        try:
            self.driver.get(city1)
            #checks if any items are there or not
            try:
                if str(self.driver.find_element_by_xpath('//span[@class=" _50f7 _2iel"]').text) == 'No listings found for "'+query+'" within 60 kilometres.':
                    self.driver.close()
                    self.driver.quit()
                    return links
            # if present scrolls bottom to get more items and returns links.
            except:
                ttime = time.time()
                while time.time()<ttime + 20:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    for i in self.driver.find_element_by_xpath('//div[@class="_65db _7ere"]').find_elements_by_xpath('//div[@class="_7yc _3ogd"]'):
                        links.append(i.find_element_by_tag_name('a').get_attribute('href'))
                except:
                    pass
                self.driver.close()
                self.driver.quit()
                return links
        except:
            self.driver.close()
            self.driver.quit()
            return []
if __name__== "__main__":
    # path to store screenshot
    path = 'C:/Users/'
    # gets proxy
    f1 = open('proxy.txt','r')
    temp = [i.strip('\n') for i in f1.readlines()]
    proxy1 = {}
    items = []
    for i in temp:
        proxy1[i.split()[0]]= i.split()[1]

    #get countries and cities
    f = open('cc.json','r')
    cc = json.load(f)
    cities = []
    for i in cc:
        for j in cc[i]:
            proxy = proxy1[i]
            web = webscraping()
            it = web.extract(cc[i][j],'nivea')
            if it!= None:
                items = items+it
    if items == None:
        pass
    else:
        d = (Parallel(n_jobs=-1)(delayed(getdata)(item) for item in items))
        print d
        #save data to csv
        f1 = open("data.csv", "w")
        cw = csv.writer(f1)
        cw.writerow(d)
        f1.close()
