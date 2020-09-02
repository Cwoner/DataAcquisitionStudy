from redis import StrictRedis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
INITAL_SCORE = 10
HOST_RIDES = '127.0.0.1'
PORT_RIDES = 6379
PASSWORD_RIDES = None
KEY_RIDES = 'proxy'

class ProxyAccess:
    def __init__(self):
        self.db = StrictRedis(host=HOST_RIDES, port=PORT_RIDES, password=PASSWORD_RIDES, decode_responses=True)

    def add(self,ip,score=INITAL_SCORE):
        self.db.zadd(KEY_RIDES, {ip:score})

    def randomget(self):
        result = self.db.zrangebyscore(KEY_RIDES, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrangebyscore(KEY_RIDES, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                return PoolEmptyError

    def decrease(self, ip):
        score = self.db.zscore(KEY_RIDES, ip)
        if score and score > MIN_SCORE:
            print('代理' + ip + '分数' + str(score) + '执行减1，最终得分' + str(score-1))
            try:
                self.db.zincrby(KEY_RIDES, -1, ip)
                print('减分操作执行完毕（-1）')
            except:
                print('数据库减分操作出现问题')
        else:
            print('代理' + ip + '分数' + score + '执行移除操作')
            return self.db.zrem(KEY_RIDES, ip)

    def exists(self, ip):
        return not self.db.zscore(KEY_RIDES, ip) == None

    def setmax(self, ip):
        print('正在设置ip' +' ' + ip + ' ' + '的分数为100')
        self.db.zadd(KEY_RIDES, {ip: MAX_SCORE})
        print(ip,'设置100分，完毕！')

    def conut(self):
        return self.db.zcard(KEY_RIDES)

    def all(self):
        return self.db.zrangebyscore(KEY_RIDES, MIN_SCORE, MAX_SCORE)

if __name__ == '__main__':
    test = ProxyAccess()
    test.add('admin')
    print(test.conut())
    print(test.randomget())
    test.setmax('admin')
    test.decrease('admin')
