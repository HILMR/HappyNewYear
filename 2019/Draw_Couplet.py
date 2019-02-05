#！/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
【2019春联送福】绘图库
本代码仅供学习使用，请务用于其他用途！
"""

__author__='@LMR'

#PIL绘图库
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#对联API库
from Couplet import *

def Draw_Couplet(inp,nick,himgpath,savepath):
    try:
        #获取春联数据
        couplet=get_couplet2(inp)
        #根据返回春联长度选择背景图
        if(len(couplet[0])==7):
            im = Image.open('Elements/BG7.jpg')
        elif(len(couplet[0])==8):
            im = Image.open('Elements/BG8.jpg')
        else:
            #缺省处理
            couplet=get_couplet2("新年")
            im = Image.open('Elements/BG7.jpg')
            
        #导入蒙板及头像
        mask1 = Image.open('Elements/mask.png')
        im1 = Image.open(himgpath)
        #头像预处理
        size1=(500,500)
        im1=im1.resize(size1)
        mask1=mask1.resize(size1)
        #截取alpha通道
        im1mask = mask1.split()[3]
        #粘贴福字
        im1pos=(820,1330)
        im.paste(im1,(im1pos[0], im1pos[1], im1pos[0]+size1[0],im1pos[1]+size1[1]),mask = im1mask )
        #文字预处理
        text_L=""
        text_R=""
        text_U=couplet[2]
        for i in couplet[0]:
            text_L=text_L+i+"\n"
        for i in couplet[1]:
            text_R=text_R+i+"\n"
        #文字坐标设置
        text_L_pos=(270,1090)
        text_R_pos=(1715,1090)
        text_U_pos=(700,690)
        name_pos=(1080,2220)
        #读取字体
        drawObject=ImageDraw.Draw(im)
        Font1=ImageFont.truetype("Elements/STXINGKA.TTF",200)
        Font2=ImageFont.truetype("Elements/STXINGKA.TTF",70)
        #文字绘图
        drawObject.text(text_L_pos,text_L,'black',font=Font1)
        drawObject.text(text_R_pos,text_R,'black',font=Font1)
        drawObject.text(text_U_pos,text_U,'black',font=Font1)
        drawObject.text(name_pos,nick,'#F6E488',font=Font2)
        #保存
        im.save(savepath, "JPEG")
        return True
    except:
        return False
