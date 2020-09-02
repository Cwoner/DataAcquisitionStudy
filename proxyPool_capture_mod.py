import  requests
from pyquery import PyQuery as pq
from proxy_ip_pool import ProxyAccess
import time



class Capture:
     __url66 = 'http://www.66ip.cn/{}.html'
    __urls = []
    __sum = 0
    __page = 10

    def __init__(self,page):
        self.redis = ProxyAccess()
        self.__page = page

    def cap_661p(self):
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'
...         }
...         for n in range(1,self.__page):
...             url = self.__url66.format(n)
...             self.__urls.append(url)
...         for urlq in self.__urls:
...             print('正在采集页面：' + urlq)
...             # time.sleep(2)
...             response = requests.get(url=urlq,headers=head)
...             htmldoc = pq(response.text)
...             trs = htmldoc('.containerbox tr:gt(0)').items()
...             for tr in trs:
...                 ip = tr.find('td:nth-child(1)').text()
...                 port = tr.find('td:nth-child(2)').text()
...                 yield ':'.join([ip, port])
... 
...     def getproxy(self):
...         for proxy in self.cap_661p():
...             print('获取代理' + proxy + '，并存入数据库.当前第' + str(self.__sum+1) )
...             self.redis.add(proxy)
...             self.__sum = self.__sum + 1
... 
... 
... 
... 
... if __name__ == '__main__':
...     npage = int(input('请输入要爬取的页数：'))
...     test = Capture(npage)
...     test.getproxy()
...     print('采集工作执行完毕,共采集',str(test.redis.conut()),'个')