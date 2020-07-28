
# -*- coding: gbk -*-

import os
import glob
from pydub import AudioSegment

wenjianjia = []
path = input('请输入要转码的父文件夹路径：')
for root, dirs, files in os.walk(path):
    wenjianjia.append(root)
wjj = wenjianjia

for dir in wjj:
    video_dir = dir
    extension_list = ('*.mp4', '*.flv')
    i = 1

    os.chdir(video_dir)
    for extension in extension_list:
        for video in glob.glob(extension):
            mp3_filename = os.path.splitext(os.path.basename(video))[0] + '.wav'
            AudioSegment.from_file(video).export(wav_filename, format='wav')
            print('已转码', str(i), '个视频！')
            i += 1
    #
    # for infile in glob.glob(os.path.join(video_dir, '*.mp4')):
    #     os.remove(infile)

