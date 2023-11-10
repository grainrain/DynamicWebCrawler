import os

if __name__ == '__main__':
    urlstr = 'http://jshrss.jiangsu.gov.cn/module/download/'

    file = os.path.splitext(urlstr)
    filename, type = file
    print(filename)
    print(type)
