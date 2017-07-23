#-*_coding:utf8-*-
import sys
import json
import os
import itchat, time
import traceback
import pandas as pd 


szExcel = "test1.xlsx"
szExcelPath = os.path.join(os.path.abspath('.') ,szExcel)
print(szExcelPath)
data = pd.read_excel(szExcelPath)
print(">>>>>>>>>>>>>>>>>")
print(data['分享地址'])

def readTransFile(fileDir):
    if fileDir == None:
        return {}
    load_dict = {}
    try:
        with open(fileDir,'r',encoding= 'utf8') as load_f:
            load_dict = json.load(load_f)
    except Exception:
        traceback.print_exc()

    return load_dict
szDicFileName = "CCText.json"
fileDir = os.path.join(os.path.abspath('.'),szDicFileName)
sourceDic = readTransFile(fileDir)




@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    for x in msg:
        print("key: {key} value:{value}".format(key = x,value = msg[x]))

    szMsgText = msg['Text']
    if szMsgText in sourceDic.keys():
        szMsgText = sourceDic[szMsgText]
    itchat.send('%s'%(szMsgText), msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    fileDir = '%s%s'%(msg['Type'], int(time.time()))
    msg['Text'](fileDir)
    itchat.send('%s received'%msg['Type'], msg['FromUserName'])
    itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), msg['FromUserName'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.get_contract()
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register('Text', isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s'%(msg['ActualNickName'], msg['Content']), msg['FromUserName'])



def use_logging(level):
    def decorator(func):
        def wrapper(*args,**kwargs):
            print(args)
            print(kwargs)
            if level == "warn":
                print("{} {} is running",format(func.__name__))
            return func(*args,**kwargs)
        return wrapper

    return decorator

@use_logging(level="warn")
def foo(name='foo',addr = "bingjing"):
    print("i am %s"%name)

foo()




# itchat.auto_login()
# itchat.run()