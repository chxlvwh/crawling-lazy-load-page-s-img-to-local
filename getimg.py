from selenium import webdriver
import time
import urllib
import re

#返回代码片段数据
def getPageSource(url):

    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080) #设置窗口宽高
    driver.get(url) #打开这个网址
    time.sleep(1)
    lastHeight = driver.execute_script("return document.documentElement.scrollHeight") #执行这个js语句，获取滚动高度
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") #执行这个JS语句，把页面滚动到底部
        time.sleep(1) #等待1秒钟
        newHeight = driver.execute_script("return document.documentElement.scrollHeight") #执行这个JS语句，获取新的滚动高度
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    clientHeight = driver.execute_script(
        "return document.documentElement.clientHeight")

    heightLen = lastHeight // clientHeight + 1

    for index in range(heightLen*2):
        driver.execute_script("window.scrollTo(0, " + str(clientHeight * index//2) + ");")
        time.sleep(0.1)

    element = driver.find_element_by_tag_name('body') #找到body这个元素
    outerhtml = element.get_attribute("outerHTML") #获取这个元素的代码片段


    # driver.quit()

    return outerhtml

#返回一个存放src数据的数组
def getImageUrlList(html):

    url = [] #获取所有src中的数据
    for v in html.split(" "):
        if v.startswith('src="'):
            url.append(v.split('"')[1])

    urls = [] #去重
    for i in url:
        if i not in urls:
            urls.append(i)

    for i in urls:
        if ('html' in i):
            urls.remove(i)
    for i in urls:
        if ('.js' in i):
            urls.remove(i)
    for i in urls:
        if 'http' not in i:
            v = urls.index(i)
            urls[v] = 'https:' + i
    for i in urls:
        if i.count('http')>1:
            urls.remove(i)
    return urls
#下载列表中的内容
def downloadImg(urls, pre='/img'):
    sfn = 11
    for url in urls:
        file_name = 'd:{}/{}.{}'.format(pre, sfn, url.split('.')[-1])

        if '?' in file_name:
            file_name = file_name[:file_name.index('?')]

        with urllib.request.urlopen(url) as response, open(file_name,
                                                           'wb') as out_file:
            data = response.read()
            out_file.write(data)
        sfn += 1


html = getPageSource("https://www.meishichina.com")
urls = getImageUrlList(html)
print(urls)
downloadImg(urls)
