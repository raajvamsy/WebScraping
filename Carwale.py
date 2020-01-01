from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.common.keys as Key
from selenium.webdriver.chrome.options import Options
import csv
import os.path


class carwaleused():

    def output(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path="chromedriver.exe",
                                  chrome_options=chrome_options
                                  )
        driver.get("https://www.carwale.com/used/cars-for-sale/#pn=1")
        input = driver.find_elements_by_css_selector("input[type='submit']").click()
        input.send_keys(Key.Keys.ESCAPE)
        c = 0
        while True:
            if driver.current_url[44:49] == 'pn=10':
                c += 1
            if c == 11:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = soup.findAll('div', 'card-detail-block__data')
        name,price,km,feul,year,location = [],[],[],[],[],[]
        for i in range(len(data)):
            d = data[i].text.split()
            text = ''
            for j in range(d.index('₹')):
                text = text+" "+str(d[j])
            name.append(text)
            price.append(d[d.index('₹') + 1])
            km.append(d[d.index('km') - 1])
            feul.append(d[d.index('km') + 1])
            year.append(d[d.index('km') + 2])
            text = ''
            for i in range(len(d[d.index('km')+2:])-1):
                text = text + str(d[d.index('km')+3+i])
            location.append(text)
        with open('carwaleused.csv','w') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'price', 'Km', 'Feul', 'Year', 'Location'])
            for i in range(len(name)):
                writer.writerow([name[i], price[i], km[i], feul[i], year[i], location[i]])
        print("Carwale-Used has been obtained")

class carwalenew():

    def run(self):
        for i in range(1, 22):
            self.output(i)


    def output(self, pn):
        url = 'https://www.carwale.com/new/search/#budget=1,2,3,4,5,6,7,8,9&fuel=1,2,3,4,5&make=10,7,16,8,17,9,1,5,2,15,11,20,66,67,25,30,56,36,61,47,49,33,34,50,43,22,51,54,44,21,12,18,4,45,23,19,37&transmission=1,2&ep=5,4,3,2,1&seat=3,2,1&bs=3,10,7,2,1,6,4,8,5&pn=' + str(
            pn)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path="chromedriver.exe",
                                  chrome_options=chrome_options
                                  )
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find_all('a', 'href-title')
        n = soup.find_all('span', 'show')
        price,version,data,emi,name,bhp,feul,transmission,milage = [],[],[],[],[],[],[],[],[]
        for i in soup.find_all('td', 'ver-pdd'):
            version.append(i.find('a').text)
            data.append(i.find('span', 'text-grey').text)
        for i in soup.find_all('td', attrs={'valign': 'top', 'class': None}):
            price.append(i.text.replace('\t', '').replace('\n', '').split()[1])
            emi.append(i.find('span', 'text-bold').text)
        k = 0
        for i in range(len(title)):
            b = int(n[i].text.split()[0])
            for j in range(k, k + b):
                name.append(title[i].text.split()[0]+" "+version[j])
                bhp.append(data[j].split(',')[0])
                feul.append(data[j].split(',')[1])
                transmission.append(data[j].split(',')[2])
                milage.append(data[j].split(',')[3])
            k = k + b
        if pn ==1:
            with open('carwalenew.csv','w') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Bhp', 'Feul', 'Transmission', 'Milage','Price','Emi'])
                for i in range(len(name)):
                    writer.writerow([name[i], bhp[i], feul[i], transmission[i], milage[i], price[i], emi[i]])

        else:
            with open('carwalenew.csv','a') as f:
                writer = csv.writer(f)
                for i in range(len(name)):
                    writer.writerow([name[i],bhp[i],feul[i],transmission[i],milage[i],price[i],emi[i]])
        print("Carwale-New data has been obtained")
if __name__=="__main__":
    carnew = carwalenew()
    carold = carwaleused()
    carnew.run()
    carold.output()
