'''配合油猴批量找图脚本的批量下载python脚本,没有调用第三方库和外部程序'''

from urllib import request
from threading import Thread,Lock
import os
import re

# 以下是设定部分,自设参数在这里修改
download_path=r'f:\download\pythonTestDir' #需要下载到的目录
links_file=r'f:\download\pythonTestDir\links5.txt' #需要读取的文本文件
thread_num=5 #下载线程数
# 设定部分结束,后面与参数设定无关请不要随便修改

# 数据字典,记录下载任务过程中需要的数据.
# links:下载链接表.dirs:下载目录表.current_dir:当前下载目录.lock:线程锁
data_dict={'links':[],'dirs':[],'current_dir':'','lock':Lock()}

# 下载线程方法
def download(data_dict):
    while True:
        with data_dict['lock']:
            if len(data_dict['links'])==0:
                return
            link=data_dict['links'].pop()
            if link=='next_path':
                data_dict['current_dir']=data_dict['dirs'].pop()
                continue
        filename=data_dict['current_dir']+'\\'+re.findall(r'([^\/]*)\s',link)[0]
        request.urlretrieve(link,filename)
        print(filename+'下载成功')
    return

# 读取下载链接文件
# 下载链接放入data_dict['links'],下载目录放入data_dict['dirs']
# 不同文件夹的链接用'next_path'分隔,线程读取到next_path自然会改变current_path
with open(links_file,'r') as f:
    for line in f:
        if (re.match(r'^\[.*\][\s\S]*',line)):
            line=line[1:-2]
            temp_path=(download_path+'\\'+line).replace(' ', '')
            try:
                os.mkdir(temp_path)
            except:
                pass
            data_dict['dirs'].append(temp_path)
            data_dict['links'].append('next_path')
        else:
            if line[-1]!='\n':
                line+='\n'  #结尾行如果缺换行的,加一个,方便正则查找
            data_dict['links'].append(line)
data_dict['links'].reverse()
data_dict['dirs'].reverse()

# 多线程开始任务
threadList=[]
for i in range(thread_num):
    t=Thread(target=download,args=(data_dict,))
    threadList.append(t)
    t.start()
for i in range(thread_num):
    threadList[i].join()
input('下载全部完成!按回车中止脚本')

