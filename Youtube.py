import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict

class youtube():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(
                                       chrome_options=chrome_options
                                       )

    def data(self, url):
        self.driver.get(url)
        curr_time = time.time() + 5
        while True:
            if (time.time() > curr_time):
                break
            else:
                self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        try:
            data = OrderedDict()
            for k in self.driver.find_elements_by_id("meta")[:-1]:
                title = (str(k.find_element_by_id("video-title").text))
                data[title] = []
                data[title].append(str(k.find_element_by_id("video-title").get_attribute('href')))
                for i in k.find_elements_by_tag_name("span")[1:]:
                    data[title].append(str(i.text))
            self.driver.close()
            return data
        except:
            return None

    def download(self,data):
        pass


if __name__ == "__main__":
    you = youtube()
    username = str(raw_input('Enter the username: '))
    f = open(username+'.txt','w')
    url = "https://www.youtube.com/user/"+username+"/videos?sort=dd"
    data = you.data(url)
    for i in data:
        f.write(str(i)+" Link: "+str(data[i][0])+" Views: "+str(data[i][1])+" Uploaded: "+str(data[i][2])+'\n')
    f.close()

