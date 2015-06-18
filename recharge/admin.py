# coding=utf-8
from django.contrib import admin
from models import User, Order, FailGetOrder


# 批量修改为充值成功
def change_to_success(modeladmin, request, queryset):
    queryset.Update(order_state='1')

change_to_success.short_description = u'修改为充值成功'

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password')
    ording = ('-id',)
    list_per_page = 50
    list_filter = ('create_time', 'last_modify_time')
    search_fields = ['username']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'product_id', 'product_name', 'target_account', 'buy_amount', 'total_sale_price', 'deal_date_time', 'recharge_mode', 'stock_merchant_name', 'order_state', 'user')
    ording = ('-id',)
    list_per_page = 50
    list_filter = ('create_time', 'user')
    actions = (change_to_success,)
    
    
class FailGetOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'state_info', 'create_time')
    ording = ('-id',)
    list_per_page = 50
    list_filter = ('create_time',)
    
    
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FailGetOrder, FailGetOrderAdmin)
