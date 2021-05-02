#!python3.6
import os
import sys
import subprocess
import pyaudio
import codecs

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# import deskrecorder as dk

import re

MILLISECOND=1000
CHUNK=1024
HZ=44100
SCRIPTPATH=sys.argv[0]
SCRIPTPATH=SCRIPTPATH[0:SCRIPTPATH.rfind('\\')]
MYSUFF='.exe'

class mikeset:
    def __init__(self, id, name):
        self.id = id
        self.name = name
def test(root):
    root.print(root,'test')

def quoted(words):
    return '\"'+words+'\"'

def getmike(mikes):
    soundin = pyaudio.PyAudio()
    p=pyaudio.PyAudio()
    for i in range(0, soundin.get_device_count()): 
        try:
            thisname=soundin.get_device_info_by_index(i).get('name').decode('shift-jis')
        except:
            thisname=soundin.get_device_info_by_index(i).get('name')
        try:
            stream=p.open(format=pyaudio.paInt16,channels=1,rate=HZ,input=True,input_device_index = i,frames_per_buffer=CHUNK)
        except OSError:
            pass
        else:
            mikes.append(mikeset(i,thisname))
            mikes[i].name=mikes[i].name
            stream.close()
    p.terminate()


def getcom(args):
    var=[]
    for i in range(0,len(args)):
        var.append(str(args[i].get()))
    var[2]=int(var[2])
    var[7]=int(var[7])
    var[2]+=var[7]*60
    var[2]=str(var[2])
    if len(var[6])==1:
        var[6]='0'+var[6]
    if len(var[5])==1:
        var[5]='0'+var[5]
    var[5]+='_'+var[6]

    del var[7]
    del var[6]

    for i in range(1,len(var)):
        var[i]=str(var[i])

    var[0]=SCRIPTPATH+'\\deskrecorder'+MYSUFF
    return var
def showcom(args,e):
    var=[]
    var=getcom(args)

    var[0]=var[0].replace('\\\\','\\')
    var[0]=quoted(var[0])
    var[6]="\""+var[6]+"\""

    for i in range(1,len(var)):
        var[0]+=' '+var[i]
    e.set('')
    e.set(str(var[0]))

    return 

def execution(var,root):
    # m=''
    if var[2]=='0':
        tk.messagebox.showinfo('エラー','録音時間を入力してください')
        return
    root.destroy()

    subprocess.run(var,shell=True)
    sys.exit()



def fm1():
    root=tk.Tk()
    root.title('deskrecorder')
    root.geometry('400x400')
    root.resizable(width=False,height=False)
    options=[]
    fr=[0]*4
    mikes=[]
    mikename=[]
    mikerb=[]
    getmike(mikes)
    for i in range(len(mikes)):
        mikename.append(str(mikes[i].id)+': '+str(mikes[i].name))
        mikerb.append('')

    # 0:絶対パス
    # 1:選択マイク
    # 2:収録分数　(7:収録時間数)
    # 5:開始時間数　6:開始分数
    # 3:ファイル形式
    # 4:終了方法

    for i in range(9):
        options.append('')
        options[i]=tk.StringVar()
        options[i].set('0')
    options[i].set(SCRIPTPATH)
    frm = tk.Frame(root)

    tk.Label(frm,text='タスクスケジューラ用',width=8,justify=tk.LEFT,anchor=tk.W).pack(fill=tk.X)
    mbf=tk.StringVar()
    monitor= tk.Entry(frm,justify=tk.LEFT,textvariable=mbf).pack(fill=tk.X)
    tk.Label(frm,text='保存先パス',width=10,justify=tk.LEFT,anchor=tk.W).pack(fill=tk.X)
    spath= tk.Entry(frm,justify=tk.LEFT,textvariable=options[8]).pack(fill=tk.X)
    frm.pack(fill=tk.X,pady=5,padx=5)

    fr[0] = tk.Frame(root)
    tk.Label(fr[0],text='開始時刻',width=8,justify=tk.LEFT).grid(row=2,column=0)
    hspin=tk.Spinbox(fr[0],
    from_=0,
    to=23,
    increment=1,
    textvariable=options[5],
    command=lambda :showcom(options,mbf),
    width=2,
    state='readonly',
    wrap=True).grid(row=2,column=1)
    tk.Label(fr[0],text=':',width=1).grid(row=2,column=2)
    mspin=tk.Spinbox(fr[0],
    from_=0,
    to=59,
    increment=1,
    textvariable=options[6],
    command=lambda :showcom(options,mbf),
    width=2,
    state='readonly',
    wrap=True).grid(row=2,column=3)
    tk.Label(fr[0],text='録音時間',width=8,justify=tk.LEFT).grid(row=2,column=4)
    rhspin=tk.Spinbox(fr[0],
    from_=0,
    to=24,
    increment=1,
    textvariable=options[7],
    command=lambda :showcom(options,mbf),
    width=2,
    state='readonly',
    wrap=True).grid(row=2,column=5)
    tk.Label(fr[0],text='：',width=1,justify=tk.LEFT).grid(row=2,column=6)
    rmspin=tk.Spinbox(fr[0],
    from_=0,
    to=59,
    increment=1,
    textvariable=options[2],
    command=lambda :showcom(options,mbf),
    width=2,
    state='readonly',
    wrap=True).grid(row=2,column=7)
    fr[0].pack(fill=tk.X,pady=5,padx=5)
    
    fr[1] = tk.Frame(root)
    pcshut=tk.Checkbutton(fr[1],
    text='録音後にPC終了',
    onvalue='2',
    offvalue='1',
    variable=options[4],
    command=lambda :showcom(options,mbf)).grid(row=0,column=0)
    options[4].set('1')
    options[3].set('1')
    if os.path.exists(SCRIPTPATH+'\\ffmpeg.exe'):
        mp3switch=tk.Checkbutton(fr[1],
        text='mp3変換',
        onvalue='2',
        offvalue='1',
        variable=options[3],
        command=lambda :showcom(options,mbf)).grid(row=0,column=1)
    fr[1].pack(fill=tk.X,pady=5,padx=5)

    fr[2] = tk.Frame(root)
    exe=tk.Button(fr[2],text='deskrecorderを実行',command=lambda :execution(getcom(options),root)).grid(row=0,column=1)
    fr[2].pack(fill=tk.X,pady=5,padx=5)
    
    fr[3] = tk.Frame(root)
    tk.Label(fr[3],text='マイク',width=12).pack()
    for i in range(len(mikerb)):
        mikerb[i]=ttk.Radiobutton(fr[3],
        text=mikename[i],
        value=str(mikes[i].id),
        variable=options[1],
        command=lambda :showcom(options,mbf)).pack()
    options[1].set(str(mikes[0].id))
    fr[3].pack(pady=5,padx=5)

    tk.mainloop()

def main():
    global MYSUFF
    MYSUFF=os.path.splitext(sys.argv[0])[1]
    if MYSUFF=='.pyw':
        MYSUFF='.py'
    fm1()


if __name__ == '__main__':
    main()