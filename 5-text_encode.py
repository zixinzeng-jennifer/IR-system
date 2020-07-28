import os
import codecs
import chardet

def list_folders_files(path): #返回文件夹和文件夹中文件
    list_folders = []
    list_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_folders.append(file)
        else:
            list_files.append(file)
    return (list_folders, list_files)

def convert(file, in_enc="GBK", out_enc="UTF-8"): #将GBK格式文件转为UTF-8
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    try:
        print("convert [ " + file.split('\\')[-1] + " ].....From " + in_enc + " --> " + out_enc)
        f = codecs.open(file, 'r', in_enc, "ignore")
        new_content = f.read()
        codecs.open(file, 'w', out_enc).write(new_content)
    except IOError as err:
        print("I/O error: {0}".format(err))

# 将路径下面的所有文件，完成格式转换
if __name__ == "__main__":
    path = r'C:\Users\顾伟业\Desktop\信存检代码\video\test4'         #需要转换的文件夹的路径
    (list_folders, list_files) = list_folders_files(path)

    print("Path: " + path)
    for fileName in list_files:
        filePath = path + '\\' + fileName
        with open(filePath, "rb") as f:
            data = f.read()
            codeType = chardet.detect(data)['encoding']
            convert(filePath, codeType, 'UTF-8')
