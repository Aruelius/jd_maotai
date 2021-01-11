# jd_maotai
抢京东茅台脚本，定时自动触发，自动预约，自动停止

小白信用 99.6，暂时还没抢到过，朋友 80 多抢到了一瓶，所以我感觉是跟信用分没啥关系，完全是看运气的。

## Python 版本需要 >= 3.6

## 安装依赖
```
pip install requests
```

## 使用方法
1. 浏览器打开：https://order.jd.com/center/list.action
2. 没登录就登录
3. F12 控制台 console 栏输入 console.log(_JdJrTdRiskFpInfo, _JdEid)
4. 参数依次对应：
```
_JdJrTdRiskFpInfo => self._JdJrTdRiskFpInfo
_JdEid => self.eid
```
5. 点击 F12 控制台 network 栏，刷新页面，找到 https://order.jd.com/center/list.action 的请求记录，把 Request Headers 里面 `cookie` 的值填到脚本里的 `self.cookie` 去
6. 将获取的到的值按照上述对应关系，填入脚本中
7. 修改抢购时间`self.buy_time`
8. 运行脚本
```
python main.py
```
9. 不出意外的话，你会收获这些信息，太难了...
```
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90008, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90008, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
{'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 90016, 'skuId': 0, 'success': False}
```

## 写在最后
1. 建议在 9:30 以后运行该脚本，防止期间 Cookie 失效，JD 的 Cookie 失效规则很奇葩
2. 抢茅台完全看运气，这是真的，什么信用分，都是玄学

与 JD 服务器对时参考：https://github.com/huanghyw/jd_seckill
