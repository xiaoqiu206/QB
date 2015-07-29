# coding=utf-8
from django.shortcuts import render_to_response, HttpResponseRedirect
from models import User, Order
from django.http import HttpResponse
from recharge import utils
from recharge.tasks import add


def index(request):
    add.delay(15, 20)
    return render_to_response('index.html', {'username': '', 'msg': ''})


def login(request):
    data = request.GET
    username = data['username']
    password = data['password']
    users = User.objects.filter(username=username, password=password)
    if len(users) > 0:  # 登录成功
        request.session['username'] = users[0].username
        return HttpResponseRedirect('/list')
    else:
        return render_to_response('index.html', {'username': username, 'msg': u'用户名或密码错误'})


def rechargeList(request):
    if 'username' not in request.session:
        return HttpResponseRedirect('/')
    else:
        username = request.session['username']  # 当前登录的用户名
        user = User.objects.get(username=username)

        handling_orders = Order.objects.filter(
            order_state='2', user=user)  # 当前用户的处理中订单
        unhandle_orders = Order.objects.filter(order_state='4')  # 未处理订单
        orders = handling_orders | unhandle_orders
        return render_to_response('list.html', {'orders': orders})


def handle_order(request):
    if 'username' not in request.session:  # 如果没有登录,就返回登录界面
        return HttpResponseRedirect('/')
    order_id = request.GET['order_id']  # 获取订单号
    state = request.GET['state']  # 获取订单状态
    username = request.session['username']  # 获取员工账号
    user = User.objects.get(username=username)
    order = Order.objects.get(order_id=order_id)
    if state == '2':  # 发送 处理中 的请求
        if order.user:  # 已经有人处理
            return HttpResponse('fail')
        else:
            order.user = user
            order.save()

    result = utils.handle_orders_data(order_id, state)
    print result
    # 如果有返回而且表示处理成功
    if not result and xmltodict.parse(result)['result']['state'] == 1:
        order.order_state = state
        order.save()
        return HttpResponse('success')
    # 如果有返回而且表示失败
    elif not result and xmltodict.parse(result)['result']['state'] == 0:
        return HttpResponse('fail')
    else:
        order.order_state = state
        order.save()
        return HttpResponse('success')
