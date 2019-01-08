# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 19:25:59 2019

@author: hfutzf
"""

import requests
import re,time
    

'''获取网页HTML文本'''
def get_text(url,sleep=0,timeout=5):
    try:
        time.sleep(float(sleep))
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Content-Type': 'application/json',
        }
        r=requests.get(url,headers=header,timeout=float(timeout))
        r.encoding=r.apparent_encoding
        return r.text.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
    except:
        return ''

class Notice():
    def __init__(self):
        self.header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Content-Type': 'application/json',
        }
        
    '''图书馆馆藏查询
    书名、isbn、图书状态、描述、网址，输入参数为图书名称，返回参数为列表'''
    def find_books(self,name):
        url='http://210.45.242.51:8080/search?kw='+str(name)+'&searchtype=title&page=1&xc=3'
        book_list=re.compile('<li><ahref="(.*?)"class="result"><divclass="title"><span>\d+\.(.*?)</span></div><divclass="detail"><p>书名信息：(.*?)</p><p>馆藏信息：馆藏复本：(.*?)可借复本：(.*?)</p><p>索书号：(.*?)</p></div></a></li>').findall(get_text(url))
        book_info=[]
        for i in book_list:
            burl='http://210.45.242.51:8080'+i[0]
            book_html=get_text(burl)
            isbn=re.compile('<p>ISBN及定价:(.*?)CNY(.*?)</p>').findall(book_html)
            describe=re.compile('<p>提要文摘附注:(.*?)</p>').findall(book_html)
            state=re.compile('<divclass="tableCon"style=""><tablecellpadding="0"cellspacing="0"><tr><thwidth="80">索书号</th><td>(.*?)</td></tr><tr><th>条码号</th><td>.*?</td></tr><tr><th>年卷期</th><td>.*?</td></tr><tr><th>馆藏地</th><td>(.*?)</td></tr><tr><th>书刊状态</th><td>(.*?)</td></tr></table></div>').findall(book_html)
            book_info.append([i[1].replace('<fontcolor="#0099CC">','').replace('</font>',''),isbn,state,describe,burl])
        return book_info
   
lib=['学校所有图书馆','屯溪路校区图书馆','合肥校区图书馆','宣城校区图书馆','翡翠湖校区图书馆']
def find():
    mail_text=str(input('请输入图书查询指令！（查阅图书名称#数字。例如指令“微积分#1”是指查找屯溪路校区可借的名为“微积分”的书） 【0、学校所有图书馆。1、屯溪路校区。2、合肥校区。3、宣城校区。4、翡翠湖校区。程序默认为0】\n\n请输入图书查询指令\n>>'))
    try:
        if 1:
            if 1:
                print('正在执行【图书查询】指令！')
                try:
                    info_=mail_text.split('#')
                    name=info_[0]
                    try:
                        mode=info_[1]
                    except:
                        mode=u'0'
                    print('正在查找图书 《'+name+'》 ')
                    print('搜索范围>>>> '+lib[int(mode)])
                    book=[]
                    book_list=Notice().find_books(name)
                    #print(book_list)
                    if len(book_list)>0:
                        for i in book_list:
                            for j in i[2]:
                                if j[2]==u'可借':
                                    if mode==u'0':
                                        book.append([i[0],j[0],j[1]])
                                    elif mode==u'1':
                                        if  j[1][:2]==u'宣城' or j[1][:3]==u'翡翠湖' or j[1][:2]==u'共达':
                                            pass
                                        else:
                                            book.append([i[0],j[0],j[1]])
                                    elif mode==u'2':
                                        if  j[1][:2]==u'宣城' or j[1][:2]==u'共达':
                                            pass
                                        else:
                                            book.append([i[0],j[0],j[1]])
                                    elif mode==u'3':
                                        if  j[1][:2]==u'屯溪路' or j[1][:3]==u'翡翠湖' or j[1][:2]==u'共达':
                                            pass
                                        else:
                                            book.append([i[0],j[0],j[1]])
                                    elif mode==u'4':
                                        if  j[1][:2]==u'屯溪路' or j[1][:2]==u'宣城' or j[1][:2]==u'共达':
                                            pass
                                        else:
                                            book.append([i[0],j[0],j[1]])
                    book1 = []
                    n=1
                    for i in book:
                        if i not in book1:
                            book1.append(i)
                    if len(book1)==0:
                        text=u'很抱歉，在'+str(mode)+'图书馆中没有找到可借的该条目的书。（备注：结果仅供参考，如果急需该条目的书请去图书馆找）\n'
                    else:
                        text=u'同学您好：\n    【下面所示的图书都是可以借的，已屏蔽掉借出的书的数据以及重复的数据。】\n\n\n'
                    for i in book1:
                        text=text+'   '+str(n)+'、['+str(i[0])+u']   ['+str(i[1])+u']   ['+str(i[2])+u']\n\n'
                        n=n+1
                    #text=text+'\n\n\n   【备注】：该邮件由程序自动编写和发送，请不要回复。多谢您使用图书查询功能，希望能够帮到你(:(: ！！'
                    print(text)
                   # send('codetest@126.com','hfutzf083415','1379875051@qq.com',"smtp.126.com",str(name)+'查询结果',text)  
                except:
                    print('很抱歉，【图书查询】指令出现错误！')
                   # send('codetest@126.com','hfutzf083415','1379875051@qq.com',"smtp.126.com",'图书查询结果','很抱歉，程序出现错误！')   
            
    except:
        print('很抱歉，指令出现错误！')
        pass
num=1
while 1:
    print('这是第 '+str(num)+' 次查询！\n')
    find()
    print('\n\n')
    print('程序运行完毕！！查找结果如上所示！！（备注：结果仅供参考，如果急需该条目的书请去图书馆找，因为程序仅读取了前20页的数据）')
    goon=str(input('输入1并回车继续查询，输入其他任意字符退出程序！！\n请输入\n>>')) 
    if goon =='1':
        pass
    else:
        break
    print('\n\n\n')
    print('\n\n\n')
    num=num+1
