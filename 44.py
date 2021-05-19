from tkinter.constants import LEFT, RIDGE, RIGHT
import mitmproxy.http
import re
import json
import csv
from tkinter import Label,StringVar,Tk,Text
import threading
import os
import time
tktext='答案：暂未获取'
tktitle='题目：正在等待答题'
def tkmain():
    def refreshText():
        global tktext,tktitle,tk_view
        text1.set(tktitle)
        text2.set(tktext)
        top.after(1000,refreshText)
    def closeWindow():
        os.system('切换开启和关闭.bat"')
    top = Tk()
    top.geometry('500x200')
    top.resizable(0,0) #防止用户调整尺寸
    top.protocol('WM_DELETE_WINDOW', closeWindow)
    text1=StringVar()
    text1.set(tktitle)
    text2=StringVar()
    text2.set(tktext)

    # 进入消息循环
    w0= Label(top, textvariable=text1,wraplength=400,height=5,font=('microsoft yahei', 8))
    w1 = Label(top, textvariable=text2,font=('microsoft yahei', 20))
    w2=Text
    w0.pack()
    w1.pack()
    top.after(1000,refreshText)
    top.mainloop()
time.sleep(2)
tk_view=1
thread = threading.Thread(target=tkmain)
thread.start()
def ReadFile():
    with open("题库.csv", "r",encoding='UTF-8') as f:
        reader = csv.reader(f)
        db = []
        for row in list(reader):
            db.append(row)
    return db
#写入题库
def IntoFile(FileNmae = '题库.csv',Data=[]):
    with open("题库.csv", "a",encoding='UTF-8',newline='') as file:
        f = csv.writer(file)
        f.writerow(Data)
        print('已写入%s文件:'%(FileNmae),Data)

class Counter:
    def __init__(self):
        self.titleid=''
        self.no_result={}
        self.titletext=''



    def response(self, flow: mitmproxy.http.HTTPFlow):
        global tktext,tktitle
        #print(titleid,no_result)
        if flow.request.host=='ssxx.univs.cn' :
            if  "/cgi-bin/race/question/" in flow.request.path:
                teee=json.loads(flow.response.get_text())
                #此处获取到题目
                title = teee['data']['title']
                replace1 = re.findall('<.*?>',title)
                for i in range(len(replace1)):
                    if 'display:none;' in replace1[i] or 'display: none;' in replace1[i]:
                        replace2 = re.findall('%s.*?%s'%(replace1[i],replace1[i+1]),title)
                        title = str(title).replace(replace2[0],'')
                for i in replace1:
                    title = str(title).replace(i,'')
                print(title)
                options = teee['data']['options']
                #此处获取到选项，并击落ABCD位置。  
                result = {}
                result1 = {}
                for i,choice in zip(options,'ABCD'):
                    rtitle = i['title']
                    replace1 = re.findall('<.*?>', rtitle)
                    for j in range(len(replace1)):
                        if 'display:none;' in replace1[j] or 'display: none;' in replace1[j]:
                            replace2 = re.findall('%s.*?%s' % (replace1[j], replace1[j + 1]), rtitle)
                            rtitle = str(rtitle).replace(replace2[0], '')
                    for j in replace1:
                        rtitle = str(rtitle).replace(j, '')
                    
                    result[rtitle] = choice
                    result1[i['id']] = rtitle
                
                '''判断题目是否已在题库中'''
                db = ReadFile()
                for i in db:
                    if not i:
                        continue
                    if title in i[0]:
                        answer = []
                        for j,k in result.items():
                            if j in eval(i[1]):
                                answer.append(k)
                        break
                    
                else:
                    self.titleid=teee['data']['id']
                    self.titletext=title
                    answer='未找到答案'
                    self.no_result=result1

                print(answer)
                tktitle='题目：'+title
                tktext='答案：'+''.join(answer)
            elif  "/cgi-bin/race/answer/" in flow.request.path:
                no_answer=json.loads(flow.request.get_text())
                yes_id=json.loads(flow.response.get_text())["data"]["correct_ids"]
                yes_answer=[]
                if no_answer['question_id']==self.titleid:
                    for i in yes_id:
                        if i in self.no_result.keys():
                            yes_answer.append(self.no_result[i])
                    print(self.titletext,yes_answer)
                    IntoFile(FileNmae = '题库.csv',Data=[self.titletext,yes_answer])
                    self.titleid=''
                    self.no_result={}
                    self.titletext=''
            elif  "/cgi-bin/race/finish/" in flow.request.path:
                print('本轮答题完成！')
                tktext='答案：'
                tktitle='题目：'
            


addons = [
    Counter()
]

