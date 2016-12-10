# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 18:26:10 2016

@author: weir
"""

import requests
from bs4 import BeautifulSoup
import os

class mzitu():
    
    def all_url(self,url):
        html=self.request(url)
        #使用BeautifulSoup解析网页，lxml为指定解析器，先查找所有class为all的div标签，再查找所有的<a>标签
        all_list=BeautifulSoup(html.text,'lxml').find('div',class_='all').find_all('a')
        for a in all_list:
            #取出a标签的文本
            title=a.get_text()            
            print(u"开始保存",title)
            path=str(title).replace("?","_")    #去除问号，防止文件命名时出错
            self.mkdir('D:\meizitu\\'+path)
            os.chdir('D:\meizitu\\'+path)       #切换到目录          
            href=a['href']                      #取出a标签的href属性，就是html
            self.html(href)
                
    #处理套图地址获得图片页面地址       
    def html(self,href):
        html = self.request(href)
        max_span=BeautifulSoup(html.text,'lxml').find_all('span')[10].get_text()#查找所有的<span>标签发现第十一对<span>标签的中的内容是最后一个照片的编号
        for page in range(1,int(max_span)+1):
            page_url = href+'/'+str(page)
            self.img(page_url)
            
    #处理图片页面地址获得图片实际地址
    def img(self,page_url):
        img_html=self.request(page_url)
        #获得图片实际地址
        img_url=BeautifulSoup(img_html.text,'lxml').find('div',class_='main-image').find('img')['src']
        self.save(img_url)
        
    #保存照片
    def save(self,img_url):
        #根据url名给照片编号取名
        name = img_url[-9:-4]
        img = self.request(img_url)
        f=open(name+'.jpg','ab')
        f.write(img.content)
        f.close()
        
    #创建文件夹
    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\\meizitu\\",path))
        if not isExists:
            print(u"建立新文件夹，名字:",path)
            os.makedirs(os.path.join("D:\\meizitu\\",path))
            return True
        else:
            print(u"名字叫做",path,u"已经存在")
            return False

    def request(self,url):
        headers = {'User-Agent':"Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.1(KHTML,like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content=requests.get(url,headers=headers)
        return content


Mzitu=mzitu()
Mzitu.all_url('http://www.mzitu.com/all')   #传入地址
