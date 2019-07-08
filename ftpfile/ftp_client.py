# ftp_cliebt.py
from socket import *
import os
import sys
import time
FLIE_PATH = '/home/tarena/process/day1/'
class FtpClient(object):
    def __init__(self,so):
        self.so = so
    def do_list(self):
        self.so.send(b'L')#发送请求
        print('已经发送请求...')
        #等待接受消息
        data = self.so.recv(1024).decode()
        if data == 'OK':
            print(data)
            data = self.so.recv(4096).decode()
            files = data.split('#')
            for file in files:
                print(file)
            print('文件展示完毕\n')
        else:
            print(data)
    def do_get(self,filename):
        self.so.send(('G ' + filename).encode())
        print('下载文件请求已发送...')
        data = self.so.recv(1024).decode()
        if data == 'ok':
            fd = open(filename,'wb')
            while True:
                data = self.so.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
            print('%s文件下载完毕'% filename)
        else:
            print('请求失败')
    def do_quit(self):
        self.so.send(b'Q')

    def do_put(self,filename):
        try:
            fd = open(FLIE_PATH + filename,'rb')
        except:
            print('打开文件失败')
            return
        self.so.send(('P ' + filename).encode())
        data = self.so.recv(1024).decode()
        if data == 'ok':
            print('服务端允许上传文件')
            while True:
                data = fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.so.send(b'##')
                    return
                self.so.send(data)
            fd.close()
            print('文件发送完毕')

        else:
            print('糟糕的操作..')
            return

    def do_list_me(self,FLIE_PATH):
        file_list = os.listdir(FLIE_PATH)
        if not file_list:
            print('文件夹为空')
            return
        files = ' '
        for file in file_list:
            if file[0] != '.' and \
            os.path.isfile(FLIE_PATH + file):
                files = files + file + '#'
        print(files.split('#'))
        

        

def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    so = socket()
    try:
        so.connect(ADDR)
    except:
        print('连接服务器失败...')
        return
    FC = FtpClient(so)
    while True:
        print('+--------------------------------+')
        print('|1)查看服务的文件库中的普通文件  |')
        print('|2)从客户端下载文件到本地        |')
        print('|3)将本地文件上传到服务器        |')
        print('|4)退出                          |')
        print('+--------------------------------+')
        cmd = input('请输入>>>')
        if cmd == '查看所有普通文件':
            FC.do_list()
        elif cmd[:3] == 'get':
            
            filename = cmd.split(' ')[-1]
            
            FC.do_get(filename)
        elif cmd == 'quit':
            FC.do_quit()
            so.close()
            sys.exit('谢谢使用')
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            FC.do_put(filename)
        elif cmd == 'list me':

            # FLIE_PATH = input('请输入查询路径')
            FC.do_list_me(FLIE_PATH)
    
        else:
            print('请输入正确命令')
            continue


if __name__ == '__main__':
    main()
