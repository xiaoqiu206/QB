# coding=utf-8
'''
Created on 2015年5月11日
定时任务,定时获取订单
@author: Administrator
'''
import time
import utils
import thread


while 1:
    thread.start_new_thread(utils.xml2db, ())
    time.sleep(5)
