# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 08:51:12 2018

@author: ying.g.sun
"""

import numpy as np
import pandas as pd
import datetime
import time
from datetime import datetime,date,timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
opts = Options()
prefs = {"profile.managed_default_content_settings.images":2} # this will disable image loading in the browser
opts.add_experimental_option("prefs",prefs)  # Added preference into chrome options
opts.add_argument("user-agent="'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
#added chrome option user-agent
# driver = webdriver.Chrome('chromedriver.exe', chrome_options=opts)  # finally add these option
# from bs4 import BeautifulSoup
batchLoadTime = datetime.now()
today = date.today()
print('Current Date: ',today)
print('Load Time: ',batchLoadTime)
import numpy as np

startTime = time.time()
print("start time is: %0.3f"%startTime)

myDirPath = 'C:/Users/ying.g.sun/Documents/work/JUMEI/myscript/'
brandList = ['科颜氏','伊丽莎白雅顿']

# driver = webdriver.Chrome(chrome_options=opts)
driver = webdriver.Chrome()

f = open(myDirPath+"jd_searchResult.txt",encoding='utf-8')
lines = f.readlines()
print('line count: ',len(lines))

urlList = []
for line in lines:
    # print 'line id: ',lines.index(line)
    lineList = line.split(',')
    cat1Name = lineList[5]
    cat2URL = lineList[6]
    # urlList[0].append(cat1Name)
    urlList.append(cat2URL)
    # print ('target url: ', cat1Name,',',cat2URL)

# df = pd.DataFrame(urlList).drop_duplicates()
# print df

uniqURL = np.unique(urlList)
print(len(uniqURL))
# print uniqURL[-1203:]
#
brand = []
for iURL in uniqURL[2904:]:
    driver.get(iURL)
    time.sleep(2)
    print('loop count:', iURL)

    # print 'category info: ',driver.find_element_by_class_name('subpage_menu').text

    if iURL.find('http://item.jd.com/')!=-1:
        try:
            catTxt =  driver.find_element_by_class_name('p-parameter').find_element_by_tag_name('a').text
            print(catTxt)
            brand.append(catTxt)            
        except Exception as e:
            print('no mark info...')

brand = np.unique(brand)            
f = open(myDirPath + str('jd_cosmetic_brand') + '.txt', 'a',encoding='utf-8')

for ibrand in brand:
     f.write(ibrand + '\n')
     # f.write(mainImgText + '\n')
f.close()
print('saved ...')