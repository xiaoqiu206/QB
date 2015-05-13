# coding=utf-8
'''
Created on 2015年5月10日
数网接口API封装
@author: Administrator
'''
import xmltodict
import hashlib
import urllib2
import urllib
from django.core.management import setup_environ
import QB.settings
setup_environ(QB.settings)
from recharge.models import Order, FailGetOrder

# 商家编号
MERCHANT_ID = '12078'  
# 开通供货API的商家得到的KEY值
KEY = 'u05v7c6h9g2r3sn'  
# 查询待处理订单接口的url
WAIT_HANDLE_ORDERS_URL = 'http://api.maxshu.com/api/GetUnhandleOrders'
# 通知订单处理结果接口的url
HANDLE_ORDER_URL = 'http://api.maxshu.com/api/HandleOrder'


def get_wait_handle_orders():
    '获取未处理订单'
    # 构造签名
    sign = hashlib.md5(MERCHANT_ID + KEY).hexdigest()
    data = {'MerchantID':MERCHANT_ID, 'Sign':sign}
    data = urllib.urlencode(data)
    result = urllib2.urlopen(WAIT_HANDLE_ORDERS_URL, data)
    xmldata = result.read()
    # print xmldata
    return xmldata


def handle_orders_data(order_id, handle_state):
    # 构造签名
    sign = hashlib.md5(MERCHANT_ID + order_id + KEY).hexdigest()
    data = {'MerchantID':MERCHANT_ID,
            'OrderID':order_id,
            'State':handle_state,
            'Sign':sign
            }
    data = urllib.urlencode(data)
    result = urllib2.urlopen(HANDLE_ORDER_URL, data)
    return result.read()


def xml2db():
    order_dict = xmltodict.parse(get_wait_handle_orders())
    if order_dict['result']['state'] == '0':  # 获取订单失败
        state_info = order_dict['result']['state-info']
        fail_get_order = FailGetOrder.objects.create(state='0', state_info=state_info)
        fail_get_order.save()

    if order_dict['result']['state'] == '1' and order_dict['result']['orders']:
        for _, order in order_dict['result']['orders'].items():
            order_id = order['order-id']
            if Order.objects.filter(order_id=order_id).__len__() == 0:
                model_order = Order.objects.create(
                                order_id=order['order-id'],
                                product_id=order['product-id'],
                                product_name=order['product-name'],
                                product_par_value=order['product-par-value'],
                                product_sale_price=order['product-sale-price'],
                                target_account=order['target-account'],
                                target_account_type=order['target-account-type'],
                                target_account_type_name=order['target-account-type-name'],
                                buy_amount=order['buy-amount'],
                                total_sale_price=order['total-sale-price'],
                                game=order['game'],
                                game_name=order['game-name'],
                                area=order['area'],
                                area_name=order['area-name'],
                                server=order['server'],
                                server_name=order['server-name'],
                                recharge_mode=order['recharge-mode'],
                                recharge_mode_name=order['recharge-mode-name'],
                                stock_merchant_id=order['stock-merchant-id'],
                                stock_merchant_name=order['stock-merchant-name'],
                                customer_ip=order['customer-ip'],
                                customer_region=order['customer-region'],
                                deal_date_time=order['deal-date-time'],
                                order_state='4'
                            )
                model_order.save()
