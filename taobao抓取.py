#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from config import writer,KEYWORDS
import time

a=writer()
IP=a.get_ip()

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--proxy-server=http://"+IP)

'''先判断元素是否存在[EC.presence_of_element_located]
   判断元素是否是可点击[EC.element_to_be_clickable]
   
   '''


driver_list = ['1', '2']
driver_list[0] = webdriver.Chrome(chrome_options = chromeOptions)
d_f_e = driver_list[0].find_element

#是否存在方法
def EC_located(value):
    wait = WebDriverWait(driver_list[0], 10)
    d_f_e = driver_list[0].find_element
    try:
        ecl=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,value)))
        return ecl
    except TimeoutException:
        print(value,'元素未加载成功，等待超时')

#是否存在方法
def values(driver,value):
    wait = WebDriverWait(driver_list[0], 10)
    try:
        ecl=driver.find_elements(By.CSS_SELECTOR,value)
        return ecl
    except TimeoutException:
        print(value,'元素未加载成功，等待超时')


# 根据关键字查询初始化
def search():
    wait = WebDriverWait(driver_list[0], 10)
    d_f_e = driver_list[0].find_element

    driver_list[0].get('http://www.taobao.com')
    #检查搜索框是不是已经加载出来
    input_search=EC_located('#q')
    while input_search==None:
        print('网页打开异常,重试..')
        off_sta()
        input_search = EC_located('#q')

    input_search.send_keys(KEYWORDS)#输入美食
    #检查按钮是否是可点击的
    submit_button=EC_located('.btn-search.tb-bg')
    submit_button.click()
    time.sleep(2)
    #准备工作就绪，检查商品页面加载出来
    EC_located('.grid.g-clearfix')
    #商品页面加载已就绪


#点击下一页的操作
u_r_l=['1','2']
sub_page=['1','2']
def next_page():
    try:

        #先记录当前高亮页码
        page[0]=(int(EC_located('.item.active span').text))
        # 检查激活页码下一个是不是已经加载出来
        next = EC_located('.item.active+li>a')
        next.click()
        #检查高亮的页码选项是不是比刚才的+1
        time.sleep(1)
        if next_ok(page[0]) ==True:
            print('ok')
        else:
            print('翻页失败，正在重试...')
            off_sta()
    except:
        print(driver_list[0])
        #IP不能用了的处理办法
        print('IP不能用了，正在重启浏览器')
        off_sta()

def off_sta():
    # 先预先记录本页url地址，以备后面翻页失败后重启调用url
    global IP
    IP = a.get_ip()
    u_r_l[0] = driver_list[0].current_url
    '''关闭重试'''
    try:
        driver_list[0].close()
    except:
        pass
    print('正在重启浏览器')
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--proxy-server=http://" + IP)
    driver_list[0] = webdriver.Chrome(chrome_options = chromeOptions)
    driver_list[0].get(u_r_l[0])
    if EC_located('.submit') !=None:
        return
        # next_page()
    elif EC_located('.btn-search') !=None:
        return
    else:
        off_sta()


page=['haha','xixi']
def next_ok(page_num):
    print('执行了next_ok(page_num)函数')
    if int(page_num)==int(EC_located('.item.active span').text):
        print('翻页不成功')
        #如果翻到了末页，就提示一下input
        if int(EC_located('.item.active span').text)==int(sub_page[0]):
            print('采集完了...')
            input('请回车继续关闭程序...')
            driver_list[0].quit()
        yes=False
    else:
        print('翻页成功')
        yes=True
    return yes

#定义一个鼠标放到上面的自定义函数
style_map=['1','2']
def Action(items,value):
    '''
    鼠标放上去
    '''
    above=items.find_element(By.CSS_SELECTOR,value)
    ActionChains(driver_list[0]).move_to_element(above).perform()


def by_css(items,value):
    css_value=items.find_element(By.CSS_SELECTOR,value)
    return css_value
# 获取一页上所有的商品
def get_products():
    style_ads = ''
    shop_lis = ''
    wait = WebDriverWait(driver_list[0], 10)
    d_f_e = driver_list[0].find_element
    items=values(driver_list[0],'.grid.g-clearfix .item')
    for i in items:
        # 提取标题
        title=by_css(i, '.ctx-box a.J_ClickStat').text
        a.dict.update({'标题':title})#@@@@@@@@@@@@@@@@@@@
        # 提取链接
        ctx_box_url = by_css(i, '.ctx-box a.J_ClickStat').get_attribute('href')
        a.dict.update({'链接': ctx_box_url})#@@@@@@@@@@@@@@@@@@@
        print(title,ctx_box_url)
        icons=values(i,'.icons span')
        #提取服务项目
        try:
            for span_class in icons:
                sls=str(span_class.get_attribute('class')\
                      .replace('icon-fest-gongyibaobei','公益宝贝')
                      .replace('icon-service-jinpaimaijia', '金牌卖家')
                      .replace('icon-service-fuwu', '15天退换')
                      .replace('icon-service-tianmao', '天猫')
                      .replace('icon-fest-tmallzhisongonly', '天猫直送')
                      .replace('icon-fest-quanqiugou', '全球购')
                      .replace('icon-service-xinpin', '新品')
                      .replace('icon-service-remai', '掌柜热卖')
                      .replace('icon-service-tianmao', '天猫'))

                shop_lis=shop_lis+sls+','
            print(shop_lis)#@@@@@@@@@
            a.dict.update({'服务': shop_lis})
        except:
            pass
        #提取DSR状态
        dsr_w1=''
        dsrs=values(i,'.dsrs .dsr')
        for dsr in dsrs:
            dsr_w=str(dsr.get_attribute('class')).replace('dsr morethan','红').replace('dsr lessthan','蓝').replace('dsr equalthan','黄')#@@@@@@@@@
            dsr_w1=dsr_w1+dsr_w
        print(dsr_w1)
        a.dict.update({'dsr':dsr_w1})#@@@@@@@@@@@@
        # 提取店铺名
        shopname = by_css(i, '.dsrs+span').text#@@@@@@@@@
        a.dict.update({'店铺名': shopname})
        # 提取价格
        price=by_css(i, '.price strong').text#@@@@@@@@@
        a.dict.update({'价格': price})
        # 提取付款人数
        deal = by_css(i, ' .deal-cnt').text#@@@@@@@@@
        a.dict.update({'付款人数': deal})
        #发货地
        location=by_css(i, ' .location').text#@@@@@@@@@
        a.dict.update({'发货地': location})
        #盒子DIV展开部分提取
        #1.鼠标放到上面
        EC_located('.shopname')
        Action(i, '.shopname')
        #获取div style的位置
        map_style=EC_located('.srp-popup.srp-overlay').get_attribute('style')
        #获取div盒子的class属性
        div_class=EC_located('.srp-popup.srp-overlay').get_attribute('class')
        div_class = EC_located('.srp-popup.srp-overlay').get_attribute('class')
        #判断盒子正常
        hz=0
        while 'hidden' in div_class or style_ads==map_style:
            Action(i, '.shopname')
            time.sleep(0.5)
            map_style = EC_located('.srp-popup.srp-overlay').get_attribute('style')
            div_class = EC_located('.srp-popup.srp-overlay').get_attribute('class')
            hz+=1
            if hz>30:
                hz=0
                off_sta()

        #获取店铺div盒子里面的店铺信息集合
        EC_located('.shop-main .rank-box span')
        value = True
        shop_widgets = ''
        level=1
        while value == True:
            try:
                shop_mains = values(driver_list[0], '.shop-main .rank-box span')
                for shop_widget in shop_mains:
                    shop_widgets1=shop_widget.get_attribute('class')
                    shop_widgets=shop_widgets+shop_widgets1+','
                print(shop_widgets)
                #店铺等级解析
                shop_widgets_list=shop_widgets.split(',')
                for widget_for in shop_widgets_list:
                    print(widget_for)
                    if widget_for=='icon-service-qiye-large':
                        a.dict.update({'店铺类型':'企业店铺'})
                    # elif widget_for=='icon-service-tianmao-large':
                    elif 'detail.tmall.com' in ctx_box_url:
                        a.dict.update({'店铺类型':'天猫店'})
                    elif widget_for=='icon icon-supple-level-xin':
                        a.dict.update({'店铺等级':str(level)+'心'})
                        level+=1
                    elif widget_for=='icon icon-supple-level-zuan':
                        a.dict.update({'店铺等级':str(level)+'钻'})
                        level+=1
                    elif widget_for=='icon icon-supple-level-guan':
                        a.dict.update({'店铺等级':str(level)+'冠'})
                        level+=1
                    elif widget_for=='icon icon-supple-level-jinguan':
                        a.dict.update({'店铺等级':str(level)+'金冠'})
                        level+=1
                    elif a.dict['店铺类型']=='' and 'detail.tmall.com' not in ctx_box_url:
                        a.dict.update({'店铺类型':'淘宝c店'})

                value = False

            except:
                time.sleep(0.8)
                print('调试信息1...')
                value == True
#=============================================
        if '天猫' in shop_lis:
            a.dict.update({'店铺等级':'','好评率': ''})
        else:
            try:#好评率
                Action(i, '.shopname')
                good=EC_located('.rate').text
                print(good)#@@@@@@@@@
                a.dict.update({'好评率': good})
            except:
                pass
        #获取具体评分
        EC_located('.scores li .percent')
        value = True
        while value==True:
            try:
                dsrs = values(driver_list[0], '.scores li .percent')
                dsr_lis = ''
                for dsr in dsrs:
                    dsr_lis=dsr_lis+dsr.text+','
                print(dsr_lis)#@@@@@@@@@
                a.dict.update({'动态评分': dsr_lis})
                value = False
            except:
                time.sleep(0.8)
                print('调试信息2...')
                value == True
        #再次初始化list
        shop_lis=''
        style_ads = map_style

        print(a.dict)
        print('=====================================')
        print('正在写入')

        a.dict.update(a.dict)
        a.writer_to(a.dict.values())
        shop_widgets = None




def main():

    '''
    控制器_抓取内容+翻页
    '''
    # 先记录总页数1.先看总页数是否存在 2.记录总页数
    while EC_located('.total') ==None:
        search()
        total = EC_located('.total').text
        sub_page[0] = int(re.findall('\d+', total)[0])
    #排序方式
    try:
        print('1、综合排序 2、销量排序 3、信用排序')
        zonghe=values(driver_list[0],'.sort-inner .sorts .sort')
        clik=int(input('请选择排序方式:'))
        zonghe[clik-1].click()
        time.sleep(2)
    except:
        pass

    for i in range(0,  sub_page[0]+ 1):
        get1=False
        print('当前循环i值是', i)
        while get1 == False:
            try:
                get_products()
                get1=True
            except:
                get1 = False
                off_sta()
        next_ajax=EC_located('.item.next a').get_attribute('class')
        if next_ajax=='J_Ajax num icon-tag':
            next_page()
        else:
            break

    input('采集结束，按回车键结束:')

if __name__ == '__main__':
    main()