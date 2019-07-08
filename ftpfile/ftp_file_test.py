# ftp_file_test.py
from socket import *
import os,sys
import signal
import time
FILE_PATH = '/home/tarena/FTP/'
class Gongn(object):
    def __init__(self,c):
        self.c = c
        
    def do_list(self):
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            slef.c.send('文件库为空'.encode())
            return
        else:
            self.c.send(b'OK')
            time.sleep(0.1)
        files = '' 
        for file in file_list:
            if file[0] != '.' and \
            os.path.isfile(FILE_PATH + file):
                files = files + file + '#'

        self.c.sendall(files.encode())
    def do_get(self,filename):
        try:
            fd = open(FILE_PATH + filename,'rb')
        except:
            print('没有此文件')
            self.c.send('打开文件失败'.encode())    
            return
        self.c.send(b'ok')
        time.sleep(0.1)
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.c.send(b'##')

            self.c.send(data)
        fd.close()
        print('%s文件发送完毕',filename)
    def do_put(self,filename):
        try:
            fd = open(filename,'wb')
        except:
            print('打开文件失败')
            return

        self.c.send(b'ok')
        while True:
            data = self.c.recv(1024)
            if data == b'##':
                break
            fd.write(data)
        fd.close()
        print('文件上传完成')

          
HOST = ''
PORT = 8848
ADDR = (HOST,PORT)
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('服务端正在等待子进程客户端连接...')
    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        print('已连接客户端',addr)

        pid = os.fork()
       
        if pid == 0:
            s.close()
            Gn = Gongn(c)
            while True:
                data = c.recv(1024).decode()
                
                if not data or data[0] == 'Q':
                    c.close()
                    sys.exit('客户端退出')
                elif data[0] == 'L':
                    Gn.do_list()
                    print(data.encode())
                elif data[0] == 'G':
                    filename = data.split(' ')[-1]
                    Gn.do_get(filename)
                elif data[0] == 'P':
                    filename = data.split(' ')[-1]
                    Gn.do_put(filename)

        else:
            c.close()
            continue

if __name__ == '__main__':
    main()



        