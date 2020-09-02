import aiohttp
import asyncio
from proxy_ip_pool import ProxyAccess
import time




Test_url = 'http://www.deepsc.cn'
VALID_STATUS_CODS = [200]
BATCH_TEST_SIZE = 100


class Check_ip:
    def __init__(self):
        self.redis = ProxyAccess()
    async def single_check(self,proxy):
        purl = 'http://' + proxy
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy=proxy.decode('utf-8')
                print('正在测试',proxy)
                async with session.get(url = Test_url,timeout = 10,proxy = purl) as response:
                    if response.status in VALID_STATUS_CODS:
                        self.redis.setmax(proxy)
                        print('代理有效', purl)
                    else:
                        self.redis.decrease(proxy)
                        print('代理请求码不合法',purl)
            except (aiohttp.ClientError,aiohttp.ClientConnectorError,TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败',proxy)
            except :
                self.redis.decrease(proxy)
                print(proxy,'出现未知错误，执行decrease')


    def run(self):
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            print(len(proxies))
            loop = asyncio.get_event_loop()
            #批量测试
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.single_check(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                print('当前测试第',i,'个')
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e)


if __name__ == '__main__':
    test = Check_ip()
    test.run()
    print('检测程序执行完毕')
