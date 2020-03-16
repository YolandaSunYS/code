# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:57:50 2018

@author: ying.g.sun
"""

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import datetime
from datetime import datetime,date,timedelta

opts = Options()
prefs = {"profile.managed_default_content_settings.images":2} # this will disable image loading in the browser
opts.add_experimental_option("prefs",prefs)  # Added preference into chrome options
opts.add_argument("user-agent="'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')

batchLoadTime = datetime.now()
myDirPath = 'C:/Users/ying.g.sun/Documents/work/JUMEI/myscript'
brandList = ['资生堂']
driver = webdriver.Chrome()

totalLoopCount = 1#000

for iLoop in range(totalLoopCount):
    for iBrand in brandList:
        brandURL = 'http://search.jd.com/Search?keyword='+str(iBrand)+'&enc=utf-8&wq='+str(iBrand)
        driver.get(brandURL)

        print('loop count:',iLoop,brandURL)
        # driver.implicitly_wait(30)
        pages = driver.find_element_by_class_name('p-skip').find_elements_by_tag_name('b')
        totalPage = pages[len(pages)-2].text
        # print 'page count: ',driver.find_element_by_class_name('search_list_head').find_element_by_class_name('head_pagecount').text.replace('共','').replace('个商品','')
        # totalPage = np.ceil(float(driver.find_element_by_class_name('head_pagecount').text.replace('共','').replace('个商品',''))/float(36))
        print('total page count: ',totalPage)

        for i in range(1,(int(totalPage)-1)*2+1,2):
            print('page: ',(i-1)/2+1)
            baseURL = 'http://search.jd.com/Search?keyword='+str(iBrand)+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+str(iBrand)+'&stock=1&page='+str(i)+'&s=1&click=0'
            driver.get(baseURL)
            print(baseURL)

            try:
                js = 'var q=document.documentElement.scrollTop = ' + str(6000)
                driver.execute_script(js)
                time.sleep(3)
                print('scrolling down...')
            except Exception as e:
                print(e)
            # driver.get('http://search.jumei.com/?brand='+str(iBrand)+'&filter=0-11-2')
            time.sleep(2)

            # driver.implicitly_wait(30)
            items = driver.find_element_by_css_selector('ul.gl-warp.clearfix').find_elements_by_tag_name('li')
            print(len(items))

            for item in items:
                itemInsertTime = datetime.now()
                sku = item.get_attribute('data-sku')
                itemURL = item.find_element_by_css_selector('div.p-name.p-name-type-2').find_element_by_tag_name('a').get_attribute('href')
                
                # recomPrice = item.find_element_by_class_name('search_list_price').find_element_by_tag_name('del').text
                print(1,iLoop+1,'brand: ',iBrand,(i-1)/2+1,items.index(item)+1,sku,batchLoadTime,itemInsertTime)
                newLine = str(1)+','+str(iBrand)+','+str(iLoop+1) +','+ str((i-1)/2+1) +','+ str(items.index(item)+1)+','+ str(sku)+','+ str(itemURL)+','+ str(batchLoadTime)+','+ str(itemInsertTime)

                f = open(myDirPath + str('jd_searchResult1') + '.txt', 'a',encoding='utf-8')
                # f.read()
                f.write(newLine+'\n')
                # f.write(mainImgText + '\n')
                f.close()

    #time.sleep(60*30)
