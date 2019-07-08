from socket import *
import os,sys
import signal

#创建套接字
HOST = ''
PORT = 8888
ADDR = (HOST,PORT)
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

def server_handler(c):
    print('开始处理子进程客户端连接',c.getpeername())
    try:
        while True:    
            data = c.recv(1024)
            if not data:
                break
            print('收到消息: ',data.decode())
            c.send('收到你的消息...'.encode())
    except (KeyboardInterrupt,SystemError):
        sys.exit('退出')
    except Exception as e:
        print(e)
    c.close()
    sys.exit(0)
print('进程%d正在等待客户端连接' % os.getpid())
#在父进程中忽略子进程状态的改变,子进程结束由系统处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        sys.exit('服务器退出')
    except Exception as e:
        print('Error',e)
        continue


    pid = os.fork()
    if pid == 0:
        s.close()
        server_handler(c)

    else:
        c.close()
        continue