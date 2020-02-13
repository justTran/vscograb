#This code is depreciated and no longer working.


from bs4 import BeautifulSoup
import requests, progressbar
import urllib, urllib2, os, time

pbar = None
queue = []
done = []
shouldContinue = True

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

print ('Enter the vsco.co usernames and type stop to end the queue\n')

while(shouldContinue):
    accName = raw_input()

    if accName == 'stop':
        shouldContinue = False
        break

    else:
        queue.append(accName)

if not queue:
    pass

else:
    for n in range(0, len(queue)):
        count = 1
        index = 1
        if not os.path.exists(queue[n]):
            try:
                print("making a new path")
                dir_name = os.makedirs(os.getcwd() + '//' + queue[n])
            except:
                pass

        dir_name = os.getcwd() + '//' + queue[n]

        while(True):
            if (len(done) > 0):
                del done[:]

            url = "https://vsco.co/" + queue[n] + "/images/" + str(index)
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            if soup.title.string == "VSCO - Create, discover, and connect":
                break

            print ("page" + str(index))
            index += 1
            source = soup.find_all('script')[2]

            for line in source.prettify().split("responsiveUrl")[1:-1]:
                img = line.split(',"showLocation"')[0]
                if img.find("im.vsco.co"):
                    if img[3:img.rfind('"')] not in done:
                        done.append(img[3:img.rfind('"')])
                        print("Downloading https://" + str(img[3:img.rfind('"')]))
                        urllib.urlretrieve("https://" + img[3:img.rfind('"')], os.path.join(dir_name, str(count) + ".jpg"), progress)
                        count += 1
                    else:
                        pass

print ('downloads complete')