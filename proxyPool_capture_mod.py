import  requests
from pyquery import PyQuery as pq
from proxy_ip_pool import ProxyAccess
import time



class Capture():
    __url66 = 'http://www.66ip.cn/{}.html'
    __urls = []
    __sum = 0
    __page = 10

    def __init__(self):
        self.redis = ProxyAccess()


    def cap_661p(self):
        print('采集程序开始')
        for i in range(1,self.__page):
            url = self.__url66.format(str(i))
            response = requests.get(url)
            html = response.text
            print('正在解析页面',url)
            doc =pq(html)
            trs = doc('.container table tr:gt(0)').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                yield ':'.join([ip,port])

    def getandstore_proxy(self,page):
        self.__page = int(page)
        for proxy in self.cap_661p():
            print('正在向数据库写入',proxy)
            self.redis.add(proxy)
            print(proxy,'写入完毕')

    def run(self,page):
        self.getandstore_proxy(page)

if __name__ == '__main__':
    page = input('请输入页数：')
    teat = Capture()
    print('proxy采集器主程序开始')
    teat.run(page)
    print('proxy采集器结束，共采集：',str(teat.redis.conut()))

