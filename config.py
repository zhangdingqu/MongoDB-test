import csv
import requests,re
import winsound
MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_TABLE='product'

url_txt= open(input('请输入3-6小时 IP URL.txt文件的路径').replace('\"',''))
url_read=url_txt.read()
KEYWORDS = input('请输入搜索关键词:')

# 保存文件名=input('文件名:')


class writer():
    def __init__(self):
        print('初始化')
        self.dict={
            "标题":"标题",
            "链接":"链接",
            "服务":"服务",
            "dsr":"dsr",
            "店铺名":"店铺名",
            "价格":"价格",
            "付款人数":"付款人数",
            "发货地":"发货地",
            "好评率": "好评率",
            "动态评分": "动态评分",
            "店铺类型": "店铺类型",
            "店铺等级": "店铺等级"
        }
        out = open(KEYWORDS+".csv", 'w', newline='',encoding='utf-8')
        self.csv_writer = csv.writer(out, dialect='excel')
        print('进入到class 自定义类了..........')
        self.csv_writer.writerow(self.dict)

    def writer_to(self,key_value):
        print('进入到class 正在写入..........',key_value)
        self.csv_writer.writerow(key_value)
        self.dict={'标题': '', '链接': '', '服务': '', 'dsr': '', '店铺名': '', '价格': '', '付款人数': '', '发货地': '', '好评率': '', '动态评分': '', '店铺类型': '', '店铺等级': ''}

    def get_url(self):
        self.IP_URL = url_read
        # url_txt.close()
        print(self.IP_URL)
        return self.IP_URL.replace('\n', '')

    print('即将读取本文件夹下的IP_url.txt文件，确保文件中包含IP的获取链接')


    def get_ip(self):
        global url_txt,url_read
        self.IP1 = str(requests.get(self.get_url()).text)
        self.IP = self.IP1.replace('\r\n', '')
        print('当前获取的IP地址为:', self.IP)
        jiaoyan = re.findall('^\d+.\d+.\d+.\d+:\d+', self.IP)
        while jiaoyan==[]:
            winsound.PlaySound("System", winsound.SND_ALIAS)
            url_txt.close()
            url_txt = open('IP_url.txt')
            url_read = url_txt.read()
            self.IP1 = str(requests.get(self.get_url()).text)
            self.IP = self.IP1.replace('\r\n', '')
            print('当前获取的IP地址为:', self.IP)
            jiaoyan = re.findall('^\d+.\d+.\d+.\d+:\d+', self.IP)
        return self.IP



if __name__ == '__main__':
    a=writer()
    new={"链接":"http://www.baidu.com",'标题':'我是标题',}
    a.dict.update(new)
    print(a.dict)
    a.writer_to(a.dict.values())
    print('')
