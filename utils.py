# coding=utf-8
'''
Created on 2015年5月10日
数网接口API封装
@author: Administrator
'''
from xml.etree import ElementTree as ET
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
    print 'send request'
    '获取未处理订单'
    # 构造签名
    print u'getting orders'
    sign = hashlib.md5(MERCHANT_ID + KEY).hexdigest()
    data = {'MerchantID': MERCHANT_ID, 'Sign': sign}
    data = urllib.urlencode(data)
    xmldata = None
    try:
        result = urllib2.urlopen(
            url=WAIT_HANDLE_ORDERS_URL, data=data, timeout=5)
        xmldata = result.read()
    except:
        pass
    # print xmldata
    return xmldata


def handle_orders_data(order_id, handle_state):
    # 构造签名
    sign = hashlib.md5(MERCHANT_ID + order_id + KEY).hexdigest()
    data = {'MerchantID': MERCHANT_ID,
            'OrderID': order_id,
            'State': handle_state,
            'Sign': sign
            }
    data = urllib.urlencode(data)
    result = urllib2.urlopen(HANDLE_ORDER_URL, data)
    # print result
    return result.read()


def xml2db():
    xmldata = get_wait_handle_orders()
    if xmldata:
        xmldata = '<?xml version="1.0" encoding="UTF-8"?>' + xmldata
        root = ET.fromstring(xmldata)
    else:
        return
    print 'state: ', root.find('state').text
    if root.find('state').text == '0':  # 获取订单失败
        state_info = root.find('state-info').text
        print 'state_info'
        fail_get_order = FailGetOrder.objects.create(
            state='0', state_info=state_info)
        fail_get_order.save()

    if root.find('state').text == '1' and root.find('orders').text:
        print u'get orders'
        for order in root.find('orders').findall('order'):
            print 'read an order'
            # print order
            order_id = order.find('order-id').text
            if Order.objects.filter(order_id=order_id).__len__() == 0:
                model_order = Order.objects.create(
                    order_id=order.find('order-id').text,
                    product_id=order.find('product-id').text,
                    product_name=order.find('product-name').text,
                    product_par_value=order.find('product-par-value').text,
                    product_sale_price=order.find('product-sale-price').text,
                    target_account=order.find('target-account').text,
                    target_account_type=order.find('target-account-type').text,
                    target_account_type_name=order.find(
                        'target-account-type-name').text,
                    buy_amount=order.find('buy-amount').text,
                    total_sale_price=order.find('total-sale-price').text,
                    game=order.find('game').text,
                    game_name=order.find('game-name').text,
                    area=order.find('area').text,
                    area_name=order.find('area-name').text,
                    server=order.find('server').text,
                    server_name=order.find('server-name').text,
                    recharge_mode=order.find('recharge-mode').text,
                    recharge_mode_name=order.find('recharge-mode-name').text,
                    stock_merchant_id=order.find('stock-merchant-id').text,
                    stock_merchant_name=order.find('stock-merchant-name').text,
                    customer_ip=order.find('customer-ip').text,
                    customer_region=order.find('customer-region').text,
                    deal_date_time=order.find('deal-date-time').text,
                    order_state='4'
                )
                model_order.save()
                print 'save an order'
