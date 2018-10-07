#!/usr/bin/python
# -*- coding: utf-8 -*-
import re,csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


try:
    out = open('guanjianci.csv', 'w', newline='')
except PermissionError:
    print('文件被其他程序占用')
    input('')
csv_writer = csv.writer(out, dialect='excel')
csv_writer.writerow(['原标题','关键词'])
global_txt=['1','2']
global_send_key=['1','2']
driver=['1','2']
url=['1','2']
def EC_located(one_group,value):
    '''
     目的：简化代码长度
    :param presence_of:EC.判断方法
    :选择一个可以使用EC_located(presence_of_element_located,value)
    :选择一组可使用EC_located(presence_of_elements_located,value)
    :param value:要找的值
    :return:选择到的对象
    '''
    wait = WebDriverWait(driver[0], 10)
    if one_group=="one":
        try:
            ecl=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,value)))
            return ecl
        except TimeoutException:
            print(value,'1元素未加载成功，等待超时')
    else:
        try:
            ecl=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,value)))
            return ecl
        except TimeoutException:
            print(value,'1元素---组---未加载成功，等待超时')




def open_chrome():
    driver[0]=webdriver.Chrome()
    driver[0].get('http://www.taobao.com')
    button = EC_located('one', '.btn-search[type=submit]')
    button.click()
    print()


def send_str():
    input=EC_located("one", '[accesskey="s"]')
    input.clear()
    global_send_key[0]=url[0]
    input.send_keys(global_send_key[0])
    button = EC_located('one', '.submit[type=submit]')
    button.click()

def extract():
    send_str()
    '''提取内容'''
    text={}
    items=EC_located('group','.items div.item .H')
    for i in items:
        print(i.text)
        if i.text!='':
            text.update({i.text:i.text})
    global_txt[0]=text.values()


def writer_txt():
    txt=''
    extract()
    for ii in global_txt[0]:
        print(ii)
        txt = txt + '#' + ii + ' '
    print([txt[:-1]])
    csv_writer.writerow([str(global_send_key[0]),txt[:-1]])

def main():
    open_chrome()
    file = 'file.txt'
    with open(file) as f:
        for line in f.readlines():
            url[0]=line
            print(line)
            writer_txt()
        out.close()
        print('已完成')


if __name__ == '__main__':
    main()