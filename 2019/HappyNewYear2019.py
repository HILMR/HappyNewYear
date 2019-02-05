#！/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
【春联送福】2019itchat贺岁大行动
本代码仅供学习使用，请务用于其他用途！
"""

__author__='@LMR'

import os,sys,time,shutil
#绘图库
from Draw_Couplet import *

#itchat微信库
import itchat

#解决部分好友昵称含有特殊字符而报错的问题
#（说的就是这些人！！！）
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

#工作目录创建
if(os.path.exists("cache")==False):
    os.mkdir("cache")

#微信扫码登陆并获取好友列表
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)

#读取已发送的好友列表
try:
    with open("inf.log","r") as f:
        rawlist=f.read().split("\n")
    filterlist=[]
    for i in rawlist:
        filterlist.append([i.split(",")[0],i.split(",")[1]])
except:
    filterlist=[]
    

while(1):
    rmname=input("单独发送模式请输入备注名，Enter进行批量发送")
    for i in friends:
        #
        #过滤规则
        #
        
        #单独发送模式
        if((rmname!='')and(i['RemarkName']!=rmname)):
            continue

        #跳过自身
        if (i["NickName"]=='LMR'):
            continue

        #过滤已发送对象
        if(filterlist!=[]):
            if ([i['RemarkName'],i['NickName']] in filterlist):
                print("已跳过%s，%s"%(i['RemarkName'],i['NickName']))
                continue
        #过滤含x的对象
        if(i['RemarkName']!=''):
            if(i['RemarkName'][0]=='x'):
                continue

        #姓名处理(可以自己定义姓名处理的规则）
        if(i['RemarkName']!=''):
            inp=i['RemarkName']
            if(inp.find("老师")!=-1):
                inp=inp[:-2]
                nick=inp[0]+"老师"
            else:
                nick=inp[-2:]
        else:
            inp=i['NickName']
            if(len(inp)>4):
                inp=inp[:4]
            nick=inp

        print("正在创建：",inp)

        #
        #获取头像
        #
        try:
            himg = itchat.get_head_img(i["UserName"])
            if (himg!=b''):
                with open("cache/%d-%shimg.jpg"%(friends.index(i),inp),'wb') as f:
                    f.write(himg)
            else:
                shutil.copy('Elements/none.jpg',"cache/%d-%shimg.jpg"%(friends.index(i),inp))
        except:
            with open("err.log","a")as f:
                f.write("%s,%s,%s,头像获取失败\n"%(i["UserName"],i['RemarkName'],i['NickName']))
            print("头像获取失败！")
            input("下一条继续？")
            continue
        
        #
        #获取春联
        #
        echo=Draw_Couplet(inp,nick,"cache/%d-%shimg.jpg"%(friends.index(i),inp),"cache/%d.jpg"%(friends.index(i)))
        if(echo==False):
            #二次获取
            echo=Draw_Couplet(inp,nick,"cache/%d-%shimg.jpg"%(friends.index(i),inp),"cache/%d.jpg"%(friends.index(i)))
            if(echo==False):
                with open("err.log","a")as f:
                    f.write("%s,%s,%s,春联创建失败\n"%(i["UserName"],i['RemarkName'],i['NickName']))
                print("创建失败！")
                input("下一条继续？")
                continue
        
        #
        #发送
        #
        try:
            #pass #虚拟模式
            itchat.send_image("cache/%d.jpg"%(friends.index(i)),'filehelper') #Debug模式
            #itchat.send_image("cache/%d.jpg"%(friends.index(i)),i["UserName"]) #正式模式（确保无误后开启）
        except:
            with open("err.log","a")as f:
                f.write("%s,%s,%s,发送失败\n"%(i["UserName"],i['RemarkName'],i['NickName']))
            print("发送失败")
            input("下一条继续？")
            continue
        
        print("成功！")
        with open("inf.log","a")as f:
            f.write("%s,%s,拜年成功\n"%(i['RemarkName'],i['NickName']))

        time.sleep(30)

    input("下一条继续？")
