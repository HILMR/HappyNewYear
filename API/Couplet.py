#！/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
智能春联API
本代码仅供学习使用，请务用于其他用途！
"""

__author__='@LMR'

import requests
import base64
import hashlib
import re

def get_couplet(inp,filepath):
    """腾讯春联AI：http://couplet.ronghuiad.com/
inp：输入
filepath：输出春联PNG图片
"""
    url="http://couplet.ronghuiad.com/api/index.php/api/imageText"
    try:
        r=requests.post(url,data={'word':inp,'sort':1,'type':2})
        pngUrl=r.json()["data"]["pngUrl"]
        load=requests.get(pngUrl,stream=True)
        with open('%s'%(filepath), "wb") as f:
            for chunk in load.iter_content(chunk_size=1024):
                f.write(chunk)
        return True
    except:
        return False

def get_couplet2(inp):
    """百度春联AI：https://chunlian.news.cntv.cn/
inp：输入
输出为春联的json，分别为上联、下联和横批
"""
    url="https://couplet.3g.163.com/couplet2019/api/generate"
    try:
        #通过改变index的值可以获得多个候选春联
        data={'type':2,'query':inp,'index':1}
        r=requests.post(url,data=data)
        res=r.json()['data']
        return [res['upper'],res['lower'],res['streamer']]
    except:
        return False

def analysis_pic(picpath):
    """百度人脸AI：https://chunlian.news.cntv.cn/
用于提取关键词进行春联创作
picpath：图片路径
输出为人脸信息的json，gender为性别，age为年龄，glasses为是否佩戴眼镜，expression为微笑指数，beauty为美丽指数
keyword为人脸关键词
"""
    url="https://couplet.3g.163.com/couplet2019/api/photo/upload"
    try:
        #base64编码
        with open(picpath, 'rb') as f:
            base64_data = 'data:image/jpeg;base64,'+base64.b64encode(f.read()).decode()
        #md5获取
        md5 = hashlib.md5()
        md5.update(base64_data.encode())
        #数据包装
        data={'base64Data':base64_data,'k':md5.hexdigest()}
        #返回数据有点问题，对全文编码会出错（因为含图片的base64）因此需要取前一部分再进行编码
        r=requests.post(url,data=data).content[:500].decode("utf-8")
        #正则表达式提取信息
        gender=re.findall(r'"gender":([^,]+),',r)[0]
        age=re.findall(r'"age":([^,]+),',r)[0]
        glasses=re.findall(r'"glasses":([^,]+),',r)[0]
        expression=re.findall(r'"expression":([^,]+),',r)[0]
        beauty=re.findall(r'"beauty":([^,]+),',r)[0]
        keyword=re.findall(r'"keyword":"([^"]+)"',r)[0]
        return {'gender':gender,'age':age,'glasses':glasses,'expression':expression,'beauty':beauty,'keyword':keyword}
    except:
        return False
