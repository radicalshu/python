#!/usr/bin/env python
#encoding: UTF-8
#design for city's routerboards upgrade
#除了升级固件，顺便配置一下ntp和timezone


import sys
import os
import pexpect 
import time
import logging

loginprompt = '[>#$]'

#global numbers   #ip地址数et synatx on set synatx on 

def col():                    #处理一下文本文件，去掉换行符号存进列表 
    global numbers
    global ip
    ips = []
    ip = []
    ips = list(open('/home/shuwei/worktonight/justupdate','r'))
    numbers = len(ips)
    log("Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>" + time.asctime())
    for i in range(numbers):
        ip.append(ips[i].rstrip('\n'))
    action()
    log("Ending >>>>>>>>>>>>>>>>>>>>>>>>>>>>" + time.asctime())

def action():           
    for i in range(numbers):                   #逐个IP地址登陆设置
        try:
            telnet = pexpect.spawn("telnet %s" % ip[i])
            telnet.expect('Login: ')
            telnet.sendline('admin')
            telnet.expect('Password: ')
            telnet.sendline('') #此行隐藏掉密码
            telnet.expect(loginprompt)
            if telnet:
                print "Connect %s sucessfully" % ip[i]
                log("Connect %s successfully" % ip[i])
                telnet.sendline('system ntp client set primary-ntp=202.120.2.101 mode=unicast enabled=yes' + '\r\n')  #加上NTP服务器
                telnet.sendline('system clock set time-zone-name=Asia/Shanghai' + '\r\n')                             #时区改为上海的时区
                telnet.sendline('system upgrade upgrade-package-source add address=172.16.0.1 user=shuwei' + '\r\n')
                telnet.expect('password: ')
                telnet.sendline('13998580315a' + '\r\n')
                time.sleep(5)
                telnet.sendline('system upgrade refresh' + '\r\n')
                time.sleep(5)
                #telnet.sendline('system upgrade print' + '\r\n')
               # #print telnet.after
                telnet.sendline('system upgrade download numbers=0' + '\r\n')
               # telnet.sendline('system upgrade download-all reboot-after-download=yes' + '\r\n')           ########下载完自动重启
                time.sleep(5)
                telnet.close()
                #telnet.sendline('system reboot' + '\r\n')
                #telnet.expect('[y/n]')
                #telnet.sendline('y' +'\r\n')
                #print telnet.before
                #b = telnet.expect(['downloading',''],timeout=5)
                #if b == 0:
                #    print "beginning to download the fireware,please wait 100s..."
                #    time.sleep(100)
                #    telnet.sendline('system upgrade print' + '\r\n')
                #    c = telnet.expect(['downloaded','downloading'],timeout=5)
                #    if c == 0:
                #        print "Done!"
                #        log("%s done" % ip[i])
                #    else:
                #        print "it costs too much time to downloading,juse let it go"
                #        log("%s is still downloading when we log out" % ip[i])
                #else:
                #    print "someting got wrong,system will jump to next one" 
                #    log("<WRONG>%s doesn't work" % ip[i]) 
            else:
                print "Can't connect to %s"  % ip[i]
                log("<WRONG>cant's connect to %s" % ip[i])
                
        except pexpect.TIMEOUT:
            print "Can't connect to %s" % ip[i]
            log("<WRONG>cant's connect to %s,catch by except" % ip[i])
        #else:
        #    print "Can't connect to %s" % ip[i]
        #    log("<WRONG>can't connect to %s" %ip[i])






def log(infor):     #涉及设备数量较多，周期较长，记录日至为了方便检查结果
    #logger=logging.getLogger()
   # handler=logging.FileHandler("result.log")
    #logger.addHandler(handler)
    #logger.setLevel(logging.NOTSET)
    logger.info(infor)

if __name__ == '__main__':
    logger=logging.getLogger()
    handler=logging.FileHandler("justupdate.log")
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    col()    

