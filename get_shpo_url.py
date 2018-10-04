#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv,requests,re,time

save_off=['1','2']
driver_list=['1','2']
IP_url=input('请输入5-25分钟 IP URL.txt文件的路径').replace('\"','')
IP_txt= open(IP_url)
url_read=IP_txt.read()

IP=''
shop_url=input('请输入shop_url.txt文件的路径').replace('\"','')
shop_url_txt=open(shop_url)
KEYWORDS=shop_url.replace('.txt','')
out=open(KEYWORDS+'-otu.txt','a+')
dengdai=int(input('设置等待时间?秒:'))
qiye=input('这一批里面有没有企业店？关系到加载javascript Y加载js N不加载js Y/N:')
def get_ip():
    global IP,url_txt,url_read
    IP1 = str(requests.get(url_read).text)
    IP = IP1.replace('\r\n', '')
    print('当前获取的IP地址为:', IP)
    jiaoyan = re.findall('^\d+.\d+.\d+.\d+:\d+', IP)
    while jiaoyan == []:
        winsound.PlaySound("System", winsound.SND_ALIAS)
        url_txt.close()
        url_txt = open('IP_url.txt')
        url_read = url_txt.read()
        IP1 = str(requests.get(get_url()).text)
        IP = IP1.replace('\r\n', '')
        print('当前获取的IP地址为:', IP)
        jiaoyan = re.findall('^\d+.\d+.\d+.\d+:\d+', IP)

if qiye=='Y' or qiye=='y':
    prefs={'profile.default_content_setting_values': {'images': 2}}
else:
    prefs = {'profile.default_content_setting_values': {'images': 2,'javascript':2}}

def chrome():
    get_ip()
    try:
        driver_list[0].close()
    except:
        pass

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option('prefs', prefs)
    chromeOptions.add_argument("--proxy-server=http://" + IP)
    driver_list[0] = webdriver.Chrome(chrome_options = chromeOptions)
n=0

class get_shop_url():
    def __init__(self):
        out = open(KEYWORDS + ".csv", 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(out, dialect='excel')
        print('进入到class 自定义类了..........')
        self.dict = {
            '商品链接': '商品链接',
            '店铺名': '店铺名',
            '店铺网址':'店铺网址'
        }
        self.csv_writer.writerow(self.dict)
    def EC_located(self,value):
        wait = WebDriverWait(driver_list[0], dengdai)
        try:
            ecl = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            return ecl
        except TimeoutException:
            print(value, '元素未出现，等待超时')

    def get(self,url):
        global n,out
        try:
            driver_list[0].get(url)
        except WebDriverException:
            print('网址有误', url)
            out.write(url)
            print('写入到日志')
            return
        if '访问受限' not in driver_list[0].title or '淘宝'  in driver_list[0].title or '天猫' in driver_list[0].title:
            try:
                if 'detail.tmall.com' in url:
                    try:
                        self.shopname = self.EC_located('.slogo-shopname').text
                        self.shop_url=self.EC_located('.slogo-shopname').get_attribute('href')
                    except:
                        if '天猫超市' in driver_list[0].title:
                            self.shopname = '天猫超市'
                            self.shop_url='https://chaoshi.detail.tmall.com'
                        elif 'tmall.com' not in driver_list[0].title:
                            self.shopname = '店名不知道'
                            self.shop_url = '链接也不知道'
                elif 'item.taobao.com' in url:
                    try:

                        self.shopname = self.EC_located('.shop-name-link').text
                        self.shop_url = self.EC_located('.shop-name-link').get_attribute('href')
                    except AttributeError:
                        self.shopname = self.EC_located('.tb-shop-name').text
                        self.shop_url = self.EC_located('.tb-shop-name a').get_attribute('href')

                self.dict.update({
                    '商品链接':url,
                    '店铺名':self.shopname,
                    '店铺网址':str(self.shop_url)+'search.htm?'
                                })


            except AttributeError:
                print('1重试...')
                if driver_list[0].current_url == url.replace('\n', '') and 'detail.tmall.com' not in driver_list[0].title and 'item.taobao.com' not in driver_list[0].title:

                    if n < 5:

                        n += 1
                        # chrome()
                        return self.get(url)
                    else:
                        n = 0

                        print('放弃', url)
                        out.write(url)
                        print('写入到日志')
                        return
                elif '淘宝' not in driver_list[0].title and '天猫' not in driver_list[0].title:

                    chrome()
                    return self.get(url)

        elif '访问受限' in driver_list[0].title:
            print('访问受限，等待5秒再重新get网址...')
            time.sleep(5)
            if n<5:
                n += 1
                return self.get(url)
            else:
                print('2重试...')
                n=0

                print('放弃',url)
                out.write(url)
                print('写入到日志')
                return
        elif '淘宝' not in driver_list[0].title and '天猫' not in driver_list[0].title:

            chrome()
            return self.get(url)


    def save(self):
        print('正在写入文件\n',self.dict)
        self.csv_writer.writerow(self.dict.values())
        print(self.shopname,'保存成功！')

def main():
    chrome()
    a=get_shop_url()
    shop_url_read='ha'
    while shop_url_read !='':

        shop_url_read = shop_url_txt.readline()
        if 'http' in shop_url_read:
            a.get(shop_url_read)
            if a.dict['店铺名'] !='':
                a.save()
                a.dict.update({
                    '商品链接':'',
                    '店铺名':'',
                    '店铺网址':''})

    print('采集完成...')



if __name__ == '__main__':
    input('IP_url.txt请使用3-5分钟有效IP，否则会很费钱哦！...')
    main()
    out.close()
    driver_list[0].close()