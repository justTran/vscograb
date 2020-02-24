import requests, progressbar, urllib, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen

pbar = None
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

def progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval = total_size)
        pbar.start()

    downloaded = block_num * block_size
    if (downloaded) < total_size:
        pbar.update(downloaded)

    else:
        pbar.finish()
        pbar = None

def setDirectory(newFolder):
    if not os.path.exists(os.getcwd() + '//' + newFolder):
        try:
            print("Making a new path...")
            dir_name = os.makedirs(os.getcwd() + '//' + newFolder)
        except:
            pass

    dir_name = os.getcwd() + '//' + newFolder
    return dir_name

def getImages(image_list, dir_name):
    count = 0
    for image in image_list:
        print("Downloading " + image.get_attribute('src')[:-6])
        urllib.request.urlretrieve(image.get_attribute('src')[:-6], os.path.join(dir_name, str(count) + ".jpg"), progress)
        count += 1

def startDriver(user):
    hasSeen = []
    driver = webdriver.Chrome(options = chrome_options, executable_path = os.getcwd() + '/chromedriver.exe')
    driver.get("https://vsco.co/" + user + "/images")
    dir = setDirectory(user)
    try:
        button = driver.find_element_by_xpath("//html/body/div/div/main/div/div[5]/section/div[2]/button")
        time.sleep(4)
        button.click()
    except:
        pass

    print("Loading the page, this may take a moment....")

    try:
        if (len(hasSeen) > 0):
            del hasSeen[:]
    except:
        pass

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    hasReachedEnd = False
    while(hasReachedEnd == False):
        currentPageIndex = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        image_list = driver.find_elements_by_tag_name('img')

        for item in image_list:
            if item not in hasSeen:
                hasSeen.append(item)

        if currentPageIndex == lenOfPage:
            hasReachedEnd = True
            image_list = driver.find_elements_by_tag_name('img')
            
            for item in image_list:
                if item not in hasSeen:
                    hasSeen.append(item)

            getImages(hasSeen, dir)
            driver.quit()

def main():
    dir_name = None
    shouldContinue = True
    queue = []
    print ('Enter the vsco.co usernames and type // to end the queue\n')
    while(shouldContinue):
        accName = input()

        if accName == '//':
            shouldContinue = False
            break

        else:
            queue.append(accName)

    if not queue:
        pass

    queue = sorted(queue)
    for n in range(0, len(queue)):
        startDriver(queue[n])

main()
print("Finished downloading images.")
