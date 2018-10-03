#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv,requests,re

driver_list=['1','2']
IP_url=input('请输入5-25分钟 IP URL.txt文件的路径').replace('\"','')
IP_txt= open(IP_url)
url_read=IP_txt.read()
IP=''
shop_url=input('请输入shop_url.txt文件的路径').replace('\"','')
shop_url_txt=open(shop_url)
KEYWORDS=shop_url.replace('.txt','')

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


prefs={'profile.default_content_setting_values': {'images': 2}}

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
        wait = WebDriverWait(driver_list[0], 10)
        try:
            ecl = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            return ecl
        except TimeoutException:
            print(value, '元素未出现，等待超时')

    def get(self,url):
        driver_list[0].get(url)
        if '访问受限' not in driver_list[0].title:
            try:
                if 'detail.tmall.com' in url:
                    self.shopname = self.EC_located('.slogo-shopname').text
                    self.shop_url=self.EC_located('.slogo-shopname').get_attribute('href')
                elif 'item.taobao.com' in url:
                    try:
                        self.shopname = self.EC_located('.tb-shop-name').text
                        self.shop_url = self.EC_located('.tb-shop-name a').get_attribute('href')
                    except AttributeError:
                        self.shopname = self.EC_located('.shop-name-link').text
                        self.shop_url = self.EC_located('.shop-name-link').get_attribute('href')
                self.dict.update({
                    '商品链接':url,
                    '店铺名':self.shopname,
                    '店铺网址':self.shop_url
                                })
            except AttributeError:
                print('换3分钟IP后重试...')
                chrome()
                return self.get(url)
        else:
            print('换3分钟IP后重试...')
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
        if shop_url_read!='':
            a.get(shop_url_read)
            a.save()
    print('采集完成...')



if __name__ == '__main__':
    input('IP_url.txt请使用3-5分钟有效IP，否则会很费钱哦！...')
    main()
    driver_list[0].close()