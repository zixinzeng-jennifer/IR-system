import os
import wave
import numpy as np
import pylab as plt


#抽取wav文件列表
path=r"E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\alist"
files=os.listdir(path)
files=[path+"\\"+f for f in files if f.endswith('.wav')]
#确认列表
def SetFileName(WavFileName):
    for i in range(len(files)):
        FileName=files[i]
        print('SetFileName File Name is',FileName)
        FileName=WavFileName
#以60s截断文件
CutTimeDef = 60
#音频切割
def CutFile():
    for i in range (len(files)):
        FileName=files[i]
        print('CutFile File Name is',FileName)
        f=wave.open(r""+FileName,"rb")
        params=f.getparams()
        print(params)
        nchannels,sampwidth,framerate,nframes=params[:4]
        CutFrameNum=framerate*CutTimeDef
        #读取参数
        print("CutFrameNum=%d" %(CutFrameNum))
        print("nchannels=%d" %(nchannels))
        print("framerate=%d" %(framerate))
        print("nframes=%d" %(nframes))
        str_data=f.readframes(nframes)
        f.close()
        #二进制数据转换为数组
        wave_data=np.fromstring(str_data, dtype=np.short)
        wave_data.shape=-1,2
        wave_data=wave_data.T
        temp_data=wave_data.T
        StepNum = int(CutFrameNum)
        StepTotalNum=0
        m=0
        while StepTotalNum<int(nframes):
            print("Stemp=%d"%(m))
            FileName="E:\originD/2019-2020/2019-2020-2\信存检\作业\小组作业/aResult/"+files[i][-9:-4]+"-"+str(m+1)+".wav"
            print(FileName)
            temp_dataTemp=temp_data[StepNum*(m):StepNum*(m+1)]
            m=m+1
            StepTotalNum=m*StepNum
            temp_dataTemp.shape = 1, -1
            temp_dataTemp = temp_dataTemp.astype(np.short)
            # 打开WAV文档
            f=wave.open(FileName,"wb")
            #配置声道数，量化位数和取样频率
            f.setnchannels(nchannels)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            #将wave_data转换为二进制数据写入文件
            f.writeframes(temp_dataTemp.tostring())
            f.close()

if __name__=='__main__':
    CutFile()

    print("音频切分结束")






