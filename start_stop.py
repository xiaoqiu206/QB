# coding=utf-8
'''
Created on 2015年5月17日
停止或开启远程linux上的进程
@author: Administrator
'''
import paramiko
import re
import time


def get_sshcon():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('123.56.42.5', 22, 'root', 'Blackcatstudio206')
    # ssh.connect('192.168.199.128', 22, 'qiu', '123321')
    print 'get connect'
    return ssh


def stop_ps():
    ssh = get_sshcon()
    stdin, stdout, stderr = ssh.exec_command('ps -ef|grep python\ cron.py')
    if not stderr.read():
        out = stdout.read()
        print out
        pids = re.findall(r'root\s+\d+', out)
        for each in pids:
            pid = re.search(r'\d+', each).group()
            ssh.exec_command('kill ' + str(pid))
            print u'成功关闭!'.encode('GBK'), pid
    else:
        print stderr.read()


def start_ps():
    ssh = get_sshcon()
    command = 'cd /home/qiu/QB/;nohup python cron.py &'
#     command = 'cd /home/qiu/QB/;nohup python cron.py &'
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.write('\n')
    stdin.flush()
    ssh.close()
    print u'成功开启!'.encode('GBK')


if __name__ == '__main__':
    cammand = raw_input(u'输入1开始,输入0停止,按回车结束:'.encode('GBK'))
    if cammand == '1':
        start_ps()
    if cammand == '0':
        stop_ps()
    print u'10秒后自动关闭'.encode('GBK')
    time.sleep(10)