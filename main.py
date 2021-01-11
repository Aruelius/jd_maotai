# coding="utf-8"
import time
from datetime import datetime, timedelta
from threading import Thread

import requests


class Maotai(object):
    def __init__(self):
        self.session = requests.session()
        self.skuId = "100012043978" # 茅台
        self.buy_time = "2021-01-11 09:59:59.500"
        self.run_time = 5 # 分钟
        # 打开 https://order.jd.com/center/list.action
        # F12 控制台输入 console.log(_JdJrTdRiskFpInfo, _JdEid)
        self.cookie = ""
        self.eid = ""
        self._JdJrTdRiskFpInfo = ""

        self.session.headers.update({
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        })

        self.diff_time = self.time_diff()
        self.run_task = True

    def init_action(self):
        r = self.session.post(
            url="https://marathon.jd.com/seckillnew/orderService/pc/init.action",
            data={
                'sku': self.skuId,
                'num': '1',
                'isModifyAddress': 'false'
            }
        )
        return r.json()

    def reserve_order(self):
        r = self.session.get(f"https://item-soa.jd.com/getWareBusiness?skuId={self.skuId}").json()
        self.session.get(url="https:" + r["yuyueInfo"]["url"])
        if "贵州茅台酒" in self.session.get("https://yushou.jd.com/member/qualificationList.action").text:
            print("预约成功")

    def submit_order(self, resp):
        addressList = resp["addressList"][0]
        data = {
            'skuId': self.skuId,
            'num': resp["seckillSkuVO"]["num"],
            'addressId': addressList["id"],
            'yuShou': 'true',
            'isModifyAddress': 'true',
            'name': addressList["name"],
            'provinceId': addressList["provinceId"],
            'cityId': addressList["cityId"],
            'countyId': addressList["countyId"],
            'townId': addressList["townId"],
            'addressDetail': addressList["addressDetail"],
            'mobile': addressList["mobile"],
            'mobileKey': addressList["mobileKey"],
            'email': addressList["email"],
            'postCode': addressList["postCode"],
            'invoiceTitle': resp["invoiceInfo"]["invoiceTitle"],
            'invoiceCompanyName': '',
            'invoiceContent': resp["invoiceInfo"]["invoiceContentType"],
            'invoiceTaxpayerNO': '',
            'invoiceEmail': resp["invoiceInfo"]["invoiceEmail"],
            'invoicePhone': resp["invoiceInfo"]["invoicePhone"],
            'invoicePhoneKey': resp["invoiceInfo"]["invoicePhoneKey"],
            'invoice': 'true',
            'password': '',
            'codTimeType': '3',
            'paymentType': '4', # 在线支付
            'areaCode': addressList["areaCode"],
            'overseas': addressList["overseas"],
            'phone': addressList["phone"],
            'eid': self.eid,
            'fp': self._JdJrTdRiskFpInfo,
            'token': resp["token"],
            'pru': '',
            'provinceName': addressList["provinceName"],
            'cityName': addressList["cityName"],
            'countyName': addressList["countyName"],
            'townName': addressList["townName"]
        }
        while self.run_task:
            try:
                r = self.session.post(
                    url=f"https://marathon.jd.com/seckillnew/orderService/pc/submitOrder.action?skuId={self.skuId}",
                    data=data
                ).json()
                print(r)
                if r.get("success"):
                    print("="*39)
                    print("抢购成功！！！")
                    self.run_task = False
                    return
            except KeyboardInterrupt:
                self.run_task = False
                break
            except:
                pass
            # time.sleep(0.05)

    def main(self):
        print(f"和京东服务器时差为：{self.diff_time}")
        address_info = self.init_action()
        if address_info.get("islogin") == "-1":
            print("需要登录")
            return
        self.reserve_order()
        t = Thread(target=self.timer)
        t.setDaemon(True)
        t.start()
        time.sleep(1)
        while self.run_task:
            buy_time = datetime.strptime(self.buy_time, "%Y-%m-%d %H:%M:%S.%f")
            buy_time_ms = int(time.mktime(buy_time.timetuple()) * 1000 + buy_time.microsecond / 1000)
            if self.get_localtime() - self.diff_time >= buy_time_ms:
                print("开始抢购...")
                self.submit_order(address_info)
            else:
                time.sleep(0.5)
        
    def get_jd_time(self):
        r = requests.get("https://a.jd.com//ajax/queryServerData.html").json()
        return r["serverTime"]

    def get_localtime(self):
        return int(time.time() * 1000)

    def time_diff(self):
        return self.get_localtime() - self.get_jd_time()

    def timer(self):
        while self.run_task:
            start_time = datetime.strptime(self.buy_time, "%Y-%m-%d %H:%M:%S.%f")
            end_time = start_time + timedelta(minutes=self.run_time)
            if end_time < datetime.now():
                print("时间到，抢购结束...")
                self.run_task = False


if __name__ == "__main__":
    mt = Maotai()
    mt.main()
