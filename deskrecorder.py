#!python3.6
#
import wave
import pyaudio

import time
import datetime
import random

import sys
import os
import os.path
import subprocess
import schedule
import shutil

import blessed
term = blessed.Terminal()
import re
import base64

MILLISECOND=1000
CHUNK=1024
HZ=44100
COMMANDLINES=7
SCRIPTPATH=''
savepath=''
flg=0
mikein=-1
mp3=False
mes=''

def getobj(obj):
    global mes
    mes=obj
def quoted(words):
    return '\"'+words+'\"'
class mes:
    docs=''
    bar=0
    def __init__(self):
        print(term.enter_fullscreen+term.move_xy(0,0)+term.clear_eol)
        print(term.move_xy(0,0))
    def print(self,*words):
        txt=''
        for i in range(len(words)):
            txt+=str(words[i])+'\r\n'
        self.docs+=txt
        print(term.move_xy(0,1)+term.clear_eol+self.docs)
    def cls(self):
        self.docs=''
        print(term.enter_fullscreen+term.move_xy(0,0)+term.clear)
    def tick(self,val):
        words=''
        for i in range(10):
            if i<=self.bar:
                words+='*'
            else:
                words+='_'
        print(term.move_xy(0,0)+term.clear_eol+str(val)+words)
        self.bar=0 if self.bar==9 else self.bar+1 

def mkchk(cin,ls1,ls2):
    for i in range(len(ls2)):
        if ls2[i]==cin:
            print(ls1[i].decode('sjis'))
            return cin
    return -1
def getmike():
    global mikein
    soundin = pyaudio.PyAudio()
    choices=[]
    canchoices=[]
    mikes=''
    p=pyaudio.PyAudio()
    for i in range(0, soundin.get_device_count()): 
        choices.append(soundin.get_device_info_by_index(i).get('name'))
        try:
            stream=p.open(format=pyaudio.paInt16,channels=1,rate=HZ,input=True,input_device_index = i,frames_per_buffer=CHUNK)
        except OSError:
            pass
        else:
            canchoices.append(i)
            stream.close()
    p.terminate()
    
    for i in range(len(canchoices)):
        mikes+=str(canchoices[i])+' '
    mikes='選択可能：'+mikes+'）＞'

    while mkchk(mikein,choices,canchoices)<0:
        try:
            mikein=int(input('録音マイクを選んでください（'+mikes))
        except:
            mikein=-1

def getstarttime(val):
    global mes
    words=re.sub('[^0123456789\:]','',val).split(':')
    if len(words)!=2:
        print(-1)
        return -1
    for i in range(2):
        try:
            words[i]=int(words[i])
        except:
            print(mes,str(-2)+":"+words[i])
            return -2
    dt=datetime.datetime.now()

    dtf=datetime.datetime(dt.year,dt.month,dt.day,words[0],words[1])
    if dt.hour>=words[0] and dt.minute>=words[1]:
        dtf+=datetime.timedelta(days=1)
    mes.cls()
    mes.print('実行:'+str(dtf))
    return (dtf-dt).seconds,dtf

def rec(sec,dts):

    global flg
    global mikein
    global mes
    global savepath
    
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=HZ,input=True,input_device_index = mikein,frames_per_buffer=CHUNK)
    mulength=sec/MILLISECOND
    dt=datetime.datetime.now()
    dt+=datetime.timedelta(milliseconds=sec)

    dts=str(dts)
    dts=dts[0:dts.rfind('\:')]
    dts=dts[:dts.find('.')]
    dts=re.sub('\:|\.','',dts)
    dts=re.sub(' ','_',dts)
    dt=str(dt)
    dt=dt[:dt.find('.')]

    mes.print('録音中です。終了時刻：'+dt)
    music=[]
    mes.bar=0
    for i in range(0, int(HZ / CHUNK * mulength)):
        if i%43==0:
            mes.tick('録音中：')
        data = stream.read(CHUNK)
        music.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    while 1:
        workdir=str(random.randint(10000000000,99999999999))[1:]
        if os.path.exists('c:\\'+workdir)==False:
            workdir='c:\\'+workdir
            break
    os.mkdir(workdir)
    os.chdir(workdir)

    song=wave.open(dts+'.wav','wb')
    song.setnchannels(1)
    song.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    song.setframerate(HZ)
    song.writeframes(b"".join(music))
    song.close()
    
    savesuff='.wav'
    if mp3==True and os.path.exists(SCRIPTPATH+'\\ffmpeg.exe'):
        subprocess.run(SCRIPTPATH+'\\ffmpeg.exe -i '+dts+'.wav '+dts+'.mp3',shell=True)
        os.remove(dts+'.wav')
        savesuff='.mp3'
    flg+=1
    title=dts
    overlapped=1
    while os.path.exists(savepath+'\\'+title+savesuff)==True:
        title=dts+' ('+str(overlapped)+')'
        overlapped+=1
    
    shutil.move(workdir+'\\'+dts+savesuff,savepath+'\\'+title+savesuff)
    os.chdir(quoted(savepath))
    shutil.rmtree(quoted(workdir))

    

    return schedule.CancelJob

def main():
    global mes
    global SCRIPTPATH
    val=[]
    SCRIPTPATH=sys.argv[0]
    SCRIPTPATH=SCRIPTPATH[0:SCRIPTPATH.rfind('\\')]
    os.chdir(SCRIPTPATH)
    print(SCRIPTPATH)
    if len(sys.argv)==COMMANDLINES:
        for i in range(COMMANDLINES):
            val.append(str(sys.argv[i]))
        val[0]=SCRIPTPATH
    else:
        val.append(SCRIPTPATH)
    mes=mes()
    menu(val)


def menu(argv):
    global mes
    global mp3
    global mikein
    global savepath
    dts=''
    if mes=='':
        mes=mes()
    
    ready=-100
    sfdt=''
    words=''
    rec_on=0
    ending=0    
    mporwav=0
    dts=''
    

    if len(argv)==COMMANDLINES:
        mikein=int(argv[1])
        rec_on=int(argv[2])
        mporwav=int(argv[3])
        ending=int(argv[4])
        ready,dts=getstarttime(argv[5].replace('_',':'))
        savepath=argv[6] if re.sub('\r\n ','',argv[6])!='' else str(random.randint(10000000000,99999999999))[1:]

    if os.path.exists(savepath)==False:
        savepath=os.getcwd()
    
    getmike()

    while rec_on==0:
        try:
            rec_on=int(input('何分間収録するか決めてください(単位・分)＞'))
        except:
            rec_on=0
        if rec_on<0:
            rec_on=0
    
    while mporwav<=0 and os.path.exists(argv[0]+'\\ffmpeg.exe'):
        try:
            mporwav=int(input('ファイル形式を決めてください（1:wav　2:mp3)＞'))
        except:
            mporwav=0
        if mporwav>2:
            mporwav=0
    if mporwav==2:
    	mp3=True
    
    while ending<=0:
        try:
            ending=int(input('終了方法を決めてください（1:アプリを終了　2:パソコンを終了）＞'))
        except:
            ending=0
        if ending>2:
            ending=0
    while ready<0:
        words=input('開始時間を指定してください。※現在時刻以前は翌日となります（Hour:Minute）＞')
        ready,dts=getstarttime(words)

    rec_on=rec_on*60*MILLISECOND
    mes.print('保存先：'+savepath)
    schedule.every(ready).seconds.do(rec,rec_on,dts)
    while flg==0:
        mes.tick('待機中：')
        schedule.run_pending()
        time.sleep(1)
        # recstandby-=1
    if ending==2:
        cmd=['shutdown','-s','-t','0']
        subprocess.run(cmd,shell=True)
        # print(cmd)
        # input('shutdownを設定しました\r\nテストなので実行しません。')
    return 0

if __name__ == '__main__':
    main()
