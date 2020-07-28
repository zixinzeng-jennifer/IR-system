##检索并且统计检索结果
import jieba
import logging
import pyecharts.options as opts
from pyecharts.charts import Line

jieba.setLogLevel(logging.INFO)

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


## 读取字典
def ReadDict(filename):
    f = open('{}.txt'.format(filename),'r')
    a = f.read()
    dictionary = eval(a)
    f.close()
    return dictionary

def Search():
    stopwords=getStopWord()
    mydict=ReadDict("word_index")
    mystr=input("请输入检索式：")
    mystr=mystr.split(' ')
    myresult={}
    for word in mystr:
        #print(word)
        seg_list=jieba.cut(word,cut_all=False)
        for x in seg_list:
            if x not in stopwords:
                if mydict.get(x)!=None:
                    myresult[x]=mydict[x]
    return myresult

def CountResult(myresult):#分析哪个视频命中结果多
    wholecount={}
    v_index=ReadDict("video_index")
    for x in v_index:#x为视频
        wholecount[x]=0
    for x in myresult:
        for (document,time) in myresult[x]:
            number=wholecount.get(document)
            wholecount[document]=number+1
    return wholecount

def CountEachVideo(myresult):
    details ={}
    v_index = ReadDict("video_index")
    for x in v_index:#x为视频
        for y in range(1,int(v_index[x])+1):#y为时间
            y=str(y)
            sum=0
            for z in myresult:#z为某个词
                lst=myresult[z]
                for (video,time) in lst:
                    if(video==x and time==y):
                        sum=sum+1
            details[(x,y)]=sum
    return details

def SortVideo(wholecount,details):
    average = {}
    partcount = {}
    v_index = ReadDict("video_index")
    for x in v_index: #x为视频
        average[x]=int(wholecount[x])/(int(v_index[x])+1) #计算视频总体信息密度
        partcount[x]=0
        for y in range(1,int(v_index[x])+1): #y为时间，此处计算相关时长
            y = str(y)
            if(int(details[(x,y)])>2): #一分钟出现3次及以上即认为为相关时间
                partcount[x] = partcount[x]+1
    average = dict(sorted(average.items(), key=lambda e: e[1], reverse=True))  #对视频总体信息密度按倒序排序
    partcount = dict(sorted(partcount.items(), key=lambda e: e[1], reverse=True)) #对相关时长按倒序排序
    #print(average)
    #print(partcount)
    num_aver = 0
    num_part = 0
    control = 0
    num=0
    for x in average: #此处判断是否所有视频都不具有较高的信息密度
        if average[x]>0.3:
            control = 1
        break
    if control==1:   #有视频都具有较高的信息密度
        print("以下为检索结果：（按视频总体密度倒序排序）")
        for x in average:
            num = num+1
            if num>3 or average[x]==0:
                break
            print("%d.%s" %(num,x))
            print("\t视频信息密度：%f" %(average[x]))
    elif control==0:    #所有视频都不具有较高的信息密度
        for x in partcount:
            if partcount[x]==0:   #所有视频不仅没有较高的信息密度，同时没有相关时长
                print("无相关结果")
                return 0
            break
        print("以下为检索结果：（按相关时长倒序排序）")
        for x in partcount:
            num = num+1
            if num>3 or partcount[x]==0:
                break
            print("%d.%s" %(num,x))
            print("\t相关时长：%d分钟" %(partcount[x]))
            print("\t视频信息密度：%f" %(average[x]))
    Echartdraw(details)
    return 0

def Echartdraw(details):
    v_index = ReadDict("video_index")
    print()
    print()
    control=input("是否需要展示某个详细密度分布？（Y or N）：")
    if control=="N":
        return 0
    while(True):
        video=input("请选择需要展示详细密度分布的视频（没有请输入0）：")
        if video=="0":
            break
        time=[]
        density=[]
        for x in range(1,int(v_index[video])+1):
            x0=str(x)
            time.append(x)
            density.append(details[(video,x0)])
        #print(time)
        #print(density)
        (   #可视化图形绘制并输出
            Line(
                init_opts=opts.InitOpts(width="1600px", height="600px")
                )
            .add_xaxis(
                xaxis_data=time
                )
            .add_yaxis(
                series_name=video,
                y_axis=density,
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average", name="平均值")]
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=video+"信息密度分布"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(
                    type_="value",
                    min_interval=1,
                    max_interval=5
                    ),
                datazoom_opts=opts.DataZoomOpts(
                    is_show=True,
                    range_start=0,
                    range_end=100
                    )
            )
            .render("%s.html" %video)
        )
        print("%s的详细密度分布在%s.html文件中展示" %(video,video))
        print()
    return 0



myresult=Search()
print()
#print(myresult)
wholecount=CountResult(myresult)
#print(wholecount)
details=CountEachVideo(myresult)
#print(details)
SortVideo(wholecount,details)

