#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LMR
# @Date:   2018-02-11
#update 2019-01-30
# 百度识图API

import requests
import os
import json
import re

class BDST(object):
    def __init__(self,picfile):
        try:
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                }
            source='http://image.baidu.com'
            
            if(picfile[:4]=='http'):
                self.queryImageUrl=picfile
                url2="http://image.baidu.com/n/pc_search?queryImageUrl=%s"%(self.queryImageUrl)
            else:
                #得到vs
                vs_url=source+'/?fr=shitu'
                vs_page=requests.get(vs_url,headers=headers).text
                vs_id=re.findall('window.vsid = "(.*?)"',vs_page)[0]
                #post上传图片至百度相册服务器a.hiphotos.baidu.com
                url='/pcdutu/a_upload?fr=html5&target=pcSearchImage&needJson=true'
                filepath=os.path.split(picfile)[0]
                pic=os.path.split(picfile)[1]
                files={'file':(pic,open(filepath+'/'+pic,'rb'),'image/jpeg'),'pos':(None,'upload'),
                       'uptype':(None,'upload_pc'),'fm':(None,'home')}
                r=requests.post(source+url,headers=headers,files=files)
                tmp=r.text
                tmp_json=json.loads(tmp)
                #获取图片url
                self.queryImageUrl=tmp_json['url']
                querySign=tmp_json['querySign']
                simid=tmp_json['simid']
                #get百度识图
                url2=source+'/pcdutu?queryImageUrl='+self.queryImageUrl+'&querySign='+querySign+'fm=index&uptype=upload_pc&result=result_camera&vs='+vs_id
            self.resdata=requests.get(url2,headers=headers).content.decode('utf-8')
        except:
            print("识图失败！")
            
    """获取百度识图页面的原始数据"""
    def get_rawData(self):
        return {'ImageUrl':self.queryImageUrl,'ResData':self.resdata}
    
    """获取猜测词义，无返回None"""    
    def get_guessWord(self):
        try:
            #return re.findall("('guessWord': ')(\S+)(',)",self.resdata)[0][1]
            tmp=self.resdata[self.resdata.find("'guessWord'")+14:self.resdata.find("'",self.resdata.find("'guessWord'")+14)]
            if (tmp==""):
                return None
            return tmp
        except:
            return None
    """获取百科词义，
       返回值为字典，item：百科词条 baikeUrl：百度百科词条地址 abstract：百科摘要
       无返回None"""    
    def get_baike(self):
        try:
            tmp={}
            tmp['item']=re.findall('("ne":")([^",]+)(",)?',self.resdata[self.resdata.find("newBaike"):])[0][1]
            tmp['baikeUrl']=re.findall("('baikeUrl': ')(\S+)(',)",self.resdata)[0][1]
            tmp['abstract']=re.findall('("abstract":")([^",]+)(",)?',self.resdata[self.resdata.find("newBaike"):])[0][1]
            return tmp
        except:
            return None
    """获取图片来源，
       返回值为字典列表，fromURL：来源网址 fromPageTitle：来源网站标题 textHost：来源网站摘要
       无返回None"""            
    def get_sourceList(self):
        try:
            tmp1=re.findall('("fromURL":")([^",]+)(",)?',self.resdata)
            tmp2=re.findall('("fromPageTitle":")([^",]+)(",)?',self.resdata)
            tmp3=re.findall('("textHost":")([^",]+)(",)?',self.resdata)
            sourceList=[]
            for i in range(0,max(len(tmp1),len(tmp2),len(tmp3))):
                tmp={}
                try:
                    if(tmp1[i][1].find("\\")!=-1):
                        tmp['fromURL']=tmp1[i][1].replace("\\","")
                    else:
                        tmp['fromURL']=tmp1[i][1]
                except:
                    tmp['fromURL']=''
                try:
                    if(tmp2[i][1].find("\\u")!=-1):
                        tmp['fromPageTitle']=tmp2[i][1].encode("UTF-8").decode('unicode_escape')
                    else:
                        tmp['fromPageTitle']=tmp2[i][1]
                except:
                    tmp['fromPageTitle']=''
                try:
                    if(tmp3[i][1].find("\\u")!=-1):
                        tmp['textHost']=tmp3[i][1].encode("UTF-8").decode('unicode_escape')
                    else:
                        tmp['textHost']=tmp3[i][1]
                except:
                    tmp['textHost']=''
                sourceList.append(tmp)
            return sourceList
        except:
            return None

    """获取相关图片，
       返回值为字典列表，ObjURL：相关图片下载地址 maxword：相关图片关键词
       cont：相关图片网站标题 gpg：相关图片网址
       无返回None""" 
    def get_simiList(self):
        try:
            tmp1=re.findall('("ObjURL":")([^"]+)(",)?',self.resdata)
            tmp2=re.findall('("cont":")([^"]+)(",)?',self.resdata)
            tmp3=re.findall('("maxword":")([^"]+)(",)?',self.resdata)
            tmp4=re.findall('("gpg":")([^"]+)(",)?',self.resdata)
            simiList=[]
            for i in range(0,max(len(tmp1),len(tmp2),len(tmp3),len(tmp4))):
                tmp={}
                try:
                    if(tmp1[i][1].find("\\")!=-1):
                        tmp['ObjURL']=tmp1[i][1].replace("\\","")
                    else:
                        tmp['ObjURL']=tmp1[i][1]
                except:
                    tmp['ObjURL']=''
                try:
                    if(tmp2[i][1].find("\\u")!=-1):
                        tmp['cont']=tmp2[i][1].encode("UTF-8").decode('unicode_escape')
                    else:
                        tmp['cont']=tmp2[i][1]
                except:
                    tmp['cont']=''
                try:
                    if(tmp3[i][1].find("\\u")!=-1):
                        tmp['maxword']=tmp3[i][1].encode("UTF-8").decode('unicode_escape')
                    else:
                        tmp['maxword']=tmp3[i][1]
                except:
                    tmp['maxword']=''
                try:
                    if(tmp4[i][1].find("\\")!=-1):
                        tmp['gpg']=tmp4[i][1].replace("\\","")
                    else:
                        tmp['gpg']=tmp4[i][1]
                except:
                    tmp['gpg']=''
                simiList.append(tmp)
            return simiList
        except:
            return None

