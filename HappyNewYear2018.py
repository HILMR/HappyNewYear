#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LMR
# @Date:   2018-02-15
# 微信贺年卡-2018贺岁大行动

"""导入系统库"""
import os
import time
import string
from collections import namedtuple
import sys

"""导入第三方库
   此库需要另外pip下载
"""
#百度识图API库
from BDST import *
#PIL绘图库
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#worldcloud词云库
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
#jieba分词库
import jieba
import jieba.analyse as analyse
#itchat微信库
import itchat

#解决部分好友昵称含有特殊字符而报错的问题
#（说的就是这些人！！！）
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

"""字符统计函数，统计中文、英文字符，以便更好的确定贴图位置"""
def str_count(s):
    asc=0
    zh=0
    for i in s:
        if i in string.ascii_letters:
            asc=asc+1
        elif i.isalpha():
            zh=zh+1
        else:
            asc=asc+1
    return [zh,asc]

"""绘图函数
   headimg：头像图片文件
   uname：昵称
   nname：备注
   savepath：绘图完成文件储存位置
"""		
def creatpic(headimg,uname,nname,savepath):
    #当字符超过目标后自动以“...”替换以便更美观布局
    if (str_count(nname)[0]>5):
        nname=nname[:5]+"..."
    if (str_count(uname)[0]>=8):
        uname=uname[:8]+"..."
    elif (str_count(uname)[1]>=16):
        uname=uname[:16]+"..."
    
    print("正在识图")
    
    try:
        shitu=BDST(headimg)
    except:
        while(1):
            if(input("识图失败！Enter重试，N退出")=='N'):
                break
            try:
                shitu=BDST(headimg)
                break
            except:
                pass
    
    print("正在分词")
    text=""
    #导入识图文字结果，主要类型是百科词条、关键词、词源图片标题、相关图片关键词，
    #详细可以参考BDST.py对百度识图API的说明
    for i in shitu.get_sourceList():
        text=text+i['fromPageTitle']
    for i in shitu.get_simiList():
        text=text+i['maxword']
    #结巴分词，按默认词库分词
    tags = jieba.analyse.extract_tags(text, topK=100, withWeight=False)
    #“推荐关键词”和“百科词条”取最高优先级
    if (shitu.get_baike()!=None):
        tags.insert(0,shitu.get_baike()['item'])
    if (shitu.get_guessWord()!=None):
        tags.insert(0,shitu.get_guessWord())

    print("正在创建云词图")
    
    fre=[]#词频数组变量
    bg_pic = imread('mask.jpg')#导入词云图的遮罩图片
    if (text!=""):
        
        for i in tags:
            if (i=='...'):
                continue
            fre.append([i,len(tags)-tags.index(i)])
        wordcloud = WordCloud(font_path="C:\Windows\Fonts\郭小语钢笔楷体.ttf",mode="RGBA",mask=bg_pic,background_color=None,scale=1.5).fit_words(dict(fre))
        wordcloud.to_file('wordcloud.png')#导出词云透明图片
    else:
        #如果不含任何搜索结果，则反馈“不知道猜不出”~
        fre=[['不知道',3],['猜不出',2],['啥玩意',1]]
        text="不知道 猜不出 啥玩意 什么呀 不懂 看不出 都是啥呀 系统崩溃 给跪了 我的天 难死了 崩溃"
        wordcloud = WordCloud(font_path="C:\Windows\Fonts\郭小语钢笔楷体.ttf",mode="RGBA",mask=bg_pic,background_color=None,scale=1.5).generate(text)
        wordcloud.to_file('wordcloud.png')
    
    print("正在绘图")
    
    #导入绘图素材文件
    #bg背景图层
    #bk边框图层
    #headimg头像图层
    #wordcloud词云图层
    #tag标签图标
    im = Image.open('bg.jpg')
    imp1 = Image.open('bk.png')
    imp2 = Image.open(headimg)
    imp3 = Image.open('wordcloud.png')
    imp4 = Image.open('tag.png')

    #约束尺寸
    size1=(300,300)
    size2=(240,240)
    size3=(700,700)

    imp1=imp1.resize(size1)
    imp2=imp2.resize(size2)
    imp3=imp3.resize(size3)
    
    #创建画板
    drawObject=ImageDraw.Draw(im)
    Font1=ImageFont.truetype("C:\Windows\Fonts\郭小语钢笔楷体.ttf",100)
    Font2=ImageFont.truetype("C:\Windows\Fonts\郭小语钢笔楷体.ttf",130)
    Font3=ImageFont.truetype("C:\Windows\Fonts\郭小语钢笔楷体.ttf",65)
    #画笔色彩纯黑
    drawObject.ink=0+0*256+0*256*256
    #绘制文字图层
    drawObject.text([700,505],uname,font=Font1)
    if (nname!=""):
        drawObject.text([1060,780],"我经常称呼你",font=Font1)
        drawObject.text([910,900],nname,font=Font2)
    else:
        drawObject.text([1060,780],"好像...还没备注",font=Font1)
        drawObject.text([910,900],"能告诉我么？",font=Font2)
    #绘制标签
    tagx=[710,710+400,710+400*2]
    r,g,b,a = imp4.split()
    for i in tagx:
        im.paste(imp4,(i-100, 2010, i-100+200,2010+200),mask = a)
        if (str_count(fre[tagx.index(i)][0])[0]>6):
            fre[tagx.index(i)][0]=fre[tagx.index(i)][0][:6]+"..."
        drawObject.text([i-str_count(fre[tagx.index(i)][0])[0]*65//2-str_count(fre[tagx.index(i)][0])[1]*10,2000],fre[tagx.index(i)][0],font=Font3)
    #下面代码注意图层顺序
    r,g,b,a = imp3.split()
    im.paste(imp3,(750, 1300, 750+size3[0],1300+size3[0]),mask = a)
    im.paste(imp2,(980, 1530, 980+size2[0],1530+size2[1]))
    r,g,b,a = imp1.split()
    im.paste(imp1,(950, 1500, 950+size1[0],1500+size1[1]),mask = a)
    #裁剪以适应手机屏幕
    im= im.crop((169,0,169+1862,3300))
    
    im.save(savepath, "JPEG")
    print("已保存%s"%(savepath))

#微信扫码登陆并获取好友列表
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
#获取好友过滤列表
#按备注名过滤
with open("E:/L.txt","r") as f:
    filterlist=f.read().split("\n")

input("Enter开始扫描")

print("开始贺岁行动")
for i in friends:

    #过滤列表
    """
    if (i['RemarkName'] in  filterlist):
        continue
    """
    if (i["NickName"]!='LMR'):
        continue
    
    try:
        if (i['RemarkName'][0]=='x'):
            continue
        if (i['RemarkName'][len(i['RemarkName'])-2:]=='老师'):
            continue
    except:
        pass

    
    try:
        if ((i['RemarkName']=='')and((len(i["NickName"])==2)or(len(i["NickName"])==3)or(len(i["NickName"])==4))):
            i['RemarkName']=i["NickName"]  
        print("【好友】%s\n备注：%s"%(i["NickName"].translate(non_bmp_map),i['RemarkName']))
    except:
        print("获取好友名称失败")
        input()
        continue

    try:
        himg = itchat.get_head_img(i["UserName"])
        if (himg!=b''):
            with open("himg.jpg",'wb') as f:
                f.write(himg)
                print("已保存头像")
            tmppath=os.getcwd()+'/himg.jpg'
        else:
            #如果出现头像文件大小为空，则启用默认头像进行绘图
            tmppath=os.getcwd()+'/none.jpg'
    except:
        print("头像保存失败")
        input()
        continue
    
    try:
        creatpic(tmppath,i["NickName"],i['RemarkName'],"E:/final.jpg")
    except:
        print("绘图失败")
        input()
        continue

    """
    #Debug模式
    if(input("发送图片？")=="N"):
        print("图片未发送\n")
        continue
    """
    
    try:
        pass
        #itchat.send_image("E:/final.jpg",'filehelper') Debug模式
        #itchat.send_image("E:/final.jpg",i["UserName"])
        
    except:
        print("发送失败")
        input()
        continue
    
    
    print("已发送\n")
    #休眠10s以屏蔽微信系统检测
    time.sleep(10)
    
