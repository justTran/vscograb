import requests, progressbar, urllib, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen

class vscoGrab():

    def __init__(self):
        self.dir = None
        self.driver = None
        self.pbar = None
        self.shouldContinue = True
        self.queue = []
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--incognito')
        self.drive()

    def progress(self, block_num, block_size, total_size):
        global pbar
        if self.pbar is None:
            self.pbar = progressbar.ProgressBar(maxval = total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if (downloaded) < total_size:
            self.pbar.update(downloaded)

        else:
            self.pbar.finish()
            self.pbar = None

    def setDirectory(self, newFolder):
        if not os.path.exists(os.getcwd() + '//' + newFolder):
            try:
                print("Making a new path...")
                dir_name = os.makedirs(os.getcwd() + '//' + newFolder)
            except:
                pass

        dir_name = os.getcwd() + '//' + newFolder
        return dir_name

    def getImages(self, image_list):
        count = 0
        for image in image_list:
            print("Downloading " + image.get_attribute('src')[:-6])
            urllib.request.urlretrieve(image.get_attribute('src')[:-6], os.path.join(self.dir, str(count) + ".jpg"), self.progress)
            count += 1

    def startDriver(self, user):
        self.driver.get("https://vsco.co/" + user + "/images")
        self.dir = self.setDirectory(user)
        try:
            button = self.driver.find_element_by_xpath("//html/body/div/div/main/div/div[5]/section/div[2]/button")
            time.sleep(4)
            button.click()
        except:
            pass
        print("Loading the page, this may take a moment....")
        self.loadPage()

    def loadPage(self):
        hasSeen = []
        lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        hasReachedEnd = False
        while(hasReachedEnd == False):
            currentPageIndex = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            image_list = self.driver.find_elements_by_tag_name('img')

            for item in image_list:
                if item not in hasSeen:
                    hasSeen.append(item)

            if currentPageIndex == lenOfPage:
                hasReachedEnd = True
                image_list = self.driver.find_elements_by_tag_name('img')
                
                for item in image_list:
                    if item not in hasSeen:
                        hasSeen.append(item)

                self.getImages(hasSeen)

    def drive(self):
        print ('Enter the vsco.co usernames and type // to end the queue\n')
        while(self.shouldContinue):
            accName = input()

            if accName == '//':
                self.shouldContinue = False
                break

            else:
                self.queue.append(accName)

        if not self.queue:
            pass

        self.queue = sorted(self.queue)
        self.driver = webdriver.Chrome(options = self.chrome_options, executable_path = os.getcwd() + '/chromedriver.exe')
        for n in range(0, len(self.queue)):
            self.startDriver(self.queue[n])

        print("Finished downloading images.")
        self.driver.close()

if __name__ == "__main__":
    vscoGrab()
