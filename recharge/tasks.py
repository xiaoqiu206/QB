# coding=utf-8
'''
Created on 2015年7月24日
celery的task
@author: Administrator
'''
from celery import task


@task()
def add(x, y):
    return x * y
