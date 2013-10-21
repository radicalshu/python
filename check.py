#!/usr/bin/env python
#encoding: UTF-8
#检查固件版本
#designed by S.W.

import os
import time
import pexpect
import logging
import sys

loginprompt = '[>#$]'

def login(host):
    try:
        telnet = pexpect.spawn("telnet %s" % host)
        telnet.expect('Login: ')
        a = telnet.before
        if "6.3" in a:
            log("%s 软件版本为6.3，开始升级固件" % host)
            print "%s 软件版本为6.3，开始升级固件"  %host
            telnet.sendline('admin')
            telnet.expect('Password: ')
            telnet.sendline('')  #此处隐藏密码
            telnet.expect(loginprompt)
            telnet.sendline('system routerboard upgrade' + '\r\n')
            telnet.expect('[y/n]')
            telnet.sendline('y' +'\r\n')
            time.sleep(2)
            telnet.expect(loginprompt)
            telnet.sendline('system reboot' + '\r\n')
            telnet.expect('[y/n]')
            telnet.sendline('y'+ '\r\n')
            log("%s 固件升级成功" % host)
            print "%s 固件升级成功" % host
        else:
            log("%s 软件版本升级失败，请手动升级" % host)
            print  "%s 固件升级失败" % host
    except pexpect.TIMEOUT:
        print "%s 无法访问，请手动检查" % host
        log("%s 无法访问，请手动检查" % host)

def log(info):     
    #logger=logging.getLogger()
    #handler=logging.FileHandler("check.log")
    #logger.addHandler(handler)
    #logger.setLevel(logging.NOTSET)
    logger.info(info)


if __name__ == '__main__':
    logger=logging.getLogger()
    handler=logging.FileHandler("check.log")
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    global numbers
    global ip
    ips = []
    ip = []
    ips = list(open('/home/shuwei/worktonight/checklist-1','r'))
    numbers = len(ips)
    log("Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>" + time.asctime())
    for i in range(numbers):
        ip.append(ips[i].rstrip('\n'))
        login(ip[i])
    log("End >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + time.asctime())


#
