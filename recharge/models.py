# coding=utf-8
from django.db import models


class Order(models.Model):
    order_id = models.CharField(u'订单号', max_length=50, null=True, blank=True,unique=True)
    product_id = models.CharField(u'商品编号', max_length=50, null=True, blank=True)
    product_name = models.CharField(u'商品名称', max_length=50, null=True, blank=True)
    product_par_value = models.CharField(u'商品面值', max_length=20, null=True, blank=True)
    product_sale_price = models.CharField(u'商品销售单价', max_length=20, null=True, blank=True)
    target_account = models.CharField(u'充值账号', max_length=20, null=True, blank=True)
    target_account_type = models.CharField(u'充值账号类型', max_length=20, null=True, blank=True)
    target_account_type_name = models.CharField(u'充值账号类型名称', max_length=20, null=True, blank=True)
    buy_amount = models.CharField(u'购买数量', max_length=5, null=True, blank=True)
    total_sale_price = models.CharField(u'订单总额', max_length=10, null=True, blank=True)
    game = models.CharField(u'游戏类型', max_length=20, null=True, blank=True)
    game_name = models.CharField(u'游戏类型名称', max_length=20, null=True, blank=True)
    area = models.CharField(u'充值区域', max_length=20, null=True, blank=True)
    area_name = models.CharField(u'充值区域名称', max_length=20, null=True, blank=True)
    server = models.CharField(u'充值服务器', max_length=20, null=True, blank=True)
    server_name = models.CharField(u'充值服务器名称', max_length=20, null=True, blank=True)
    recharge_mode = models.CharField(u'充值方式', max_length=20, null=True, blank=True)
    recharge_mode_name = models.CharField(u'充值方式名称', max_length=20, null=True, blank=True)
    stock_merchant_id = models.CharField(u'进货商家编号', max_length=50, null=True, blank=True)
    stock_merchant_name = models.CharField(u'进货商家名称', max_length=50, null=True, blank=True)
    customer_ip = models.CharField(u'客户IP', max_length=20, null=True, blank=True)
    customer_region = models.CharField(u'客户区域', max_length=20, null=True, blank=True)
    deal_date_time = models.CharField(u'订单交易时间', max_length=30, null=True, blank=True)
    user = models.ForeignKey('User', verbose_name='处理订单经手人', null=True, blank=True)
    create_time = models.DateTimeField(u'获取订单时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(u'最后处理时间', auto_now=True)
    order_state = models.CharField(u'订单状态', max_length=10, null=True, blank=True)
    
    def __unicode__(self):
        return self.order_id

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = u'订单'
        

class User(models.Model):
    username = models.CharField(u'员工账户', max_length=20, unique=True)
    password = models.CharField(u'密码', max_length=30)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(u'最后修改时间', auto_now=True)
    
    def __unicode__(self):
        return self.username
    
    class Meta:
        verbose_name = u'员工'
        verbose_name_plural = u'员工'
        

class FailGetOrder(models.Model):
    state = models.CharField(u'处理状态', max_length=2)
    state_info = models.CharField(u'处理状态说明', max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(u'获取订单时间', auto_now_add=True)
    
    def __unicode__(self):
        return unicode(self.id)
    
    class Meta:
        verbose_name = u'获取订单失败记录'
        verbose_name_plural = u'获取订单失败记录'
    
