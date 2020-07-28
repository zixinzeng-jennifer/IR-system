##jieba精确模式
##建立倒排档索引
##索引结构为：key为与此，value为一个list,标识出现的课程文件和分钟，升序排列
import jieba
import string
import numpy as np
import re
##读取停用词表
def getStopWord_init():
    stopword_list=[]
    f=open("baidu_stopwords.txt","rb")
    line=f.read().decode('utf-8','ignore')
    line=line.split('\n')
    for x in line:
        stopword_list.append(x)
    f = open("hit_stopwords.txt", "rb")
    line = f.read().decode('utf-8', 'ignore')
    line = line.split('\n')
    for x in line:
        stopword_list.append(x)
    f = open("cn_stopwords.txt", "rb")
    line = f.read().decode('utf-8', 'ignore')
    line = line.split('\n')
    for x in line:
        stopword_list.append(x)
    f = open("scu_stopwords.txt", "rb")
    line = f.read().decode('utf-8', 'ignore')
    line = line.split('\n')
    for x in line:
        stopword_list.append(x)
    stopword_list=list(set(stopword_list))#去重
    f=open("my_stopwords.txt","w")
    for x in stopword_list:
        try:
            f.write(x+'\n')
        except:
            continue
    return stopword_list

def getStopWord():
    stopword_list=[]
    f=open("my_stopwords.txt","r")
    line=f.readline()
    line=line[:-1]  ##去掉换行符
    while(len(line)):
        stopword_list.append(line)
        line=f.readline()
        line=line[:-1]
    f.close()
    return stopword_list

## 读取和保存字典
def SaveDict(dictionary,filename):
    f = open('{}.txt'.format(filename),'w')
    f.write(str(dictionary))
    f.close()
def ReadDict(filename):
    f = open('{}.txt'.format(filename),'r')
    a = f.read()
    dictionary = eval(a)
    f.close()
    return dictionary


##分词
##输入的参数分别为文件名前缀和文件综述
def BuildIndex(file_name,segment_number,stopword_list):
    mydict=ReadDict("word_index")
    for i in range(1,int(segment_number)+1):
        time='%d'%i
        segment_name="video\\"+file_name+"\\"+file_name+"_"+time+".txt"
        #segment_name=file_name+"_"+time+".txt"
        print(segment_name)
        f=open(segment_name,"rb")
        mystr=f.read().decode('utf-8','ignore')
        mystr=mystr.replace(' ','')#去除空格
    #print(mystr)
        seg_list=jieba.cut(mystr,cut_all=False)##精确模式
        for word in seg_list:
        #print(word)
            if (word not in stopword_list):
                if (word in mydict):
                    mydict[word].append((file_name,time))
                else:
                    mydict[word]=[(file_name,time)]
    #print(mydict)
        f.close()
#print(mydict.keys())
    SaveDict(mydict,"word_index")

def Init():
    mydict={}
    SaveDict(mydict,"word_index")
    myvideo={}
    SaveDict(myvideo,"video_index")

#stopword_list=getStopWord_init()
stopword_list=getStopWord()
Init()
flag=True
while(flag):
    file_name = input("请输入课程文件名称:(输入0结束)")
    if(file_name=="0"):
        flag=False
        break
    segment_number = input("请输入文件总数:")
    video_index=ReadDict("video_index")
    video_index[file_name]=segment_number
    SaveDict(video_index,"video_index")
    BuildIndex(file_name,segment_number,stopword_list)
