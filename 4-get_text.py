## _*_ coding:utf-8 _*_
import os
#抽取-.txt文件
path = r"E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\aResult"
files = os.listdir(path)
files = [path + "\\" + f for f in files if f.endswith('-.txt')]
#print(files)
#读-.txt写入.txt
for i in range(len(files)):
    ###testprint
    #print(files[i])
    FileName="E:\originD\\2019-2020\\2019-2020-2\信存检\作业\小组作业\\"
    f1=open(FileName+"aResult\\"+files[i][53:-4]+".txt","r")
    f2=open(FileName+"aResult\\text\\"+files[i][53:-5]+".txt","a+")
    lines=f1.readlines()
    str1 = "transcript"
    for m in range(len(lines)):
        if str1 in lines[m]:
            f2.write(lines[m][25:-2:])
            # f2.write(lines[6][25:-2:]+lines[15][25:-2:]+lines[24][25:-2:])
        else:
            continue
