MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_TABLE='product'
KEYWORDS='美食'


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver_list=['1','2']
driver_list[0]=webdriver.Chrome()
wait=WebDriverWait(driver_list[0],10)
d_f_e=driver_list[0].find_element

#容易出错的地方是陈旧的driver session="21e0d1dbb207391e66143672a16fef1f"被加载到文档导致信息不一致，解决办法是函数执行操作时重新拾取最新的session
#自定义方法
def EC_located(value):
    #重新获取最新的session============
    wait = WebDriverWait(driver_list[0], 10)#重点在这==============
    d_f_e = driver_list[0].find_element#重点在这====================
    try:
        ecl=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,value)))
        return ecl
    except TimeoutException:
        print(value,'元素未加载成功，等待超时')


#点击下一页的操作
u_r_l=['1','2']
tb_url=u_r_l[0]
def next_page():
    try:
        #先记录总页数1.先看总页数是否存在 2.记录总页数
        total=EC_located('.total').text
        sub_page=int(re.findall('\d+',total)[0])
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
            return next_page()
    except:
        print(driver_list[0])
        #IP不能用了的处理办法
        print('IP不能用了，正在重启浏览器')
        off_sta()

def off_sta():
    deiver = driver_list[0]
    # 先预先记录本页url地址，以备后面翻页失败后重启调用url
    u_r_l[0] = driver_list[0].current_url
    tb_url = u_r_l[0]
    '''关闭重试'''
    try:
        driver_list[0].close()
    except:
        pass
    driver_list[0] = webdriver.Chrome()
    driver_list[0].get(tb_url)
    next_page()

page=['haha','xixi']
def next_ok(page_num):
    print('执行了next_ok(page_num)函数')
    if int(page_num)==int(EC_located('.item.active span').text):
        print('翻页不成功')
        yes=False
    else:
        print('翻页成功')
        yes=True
    return yes