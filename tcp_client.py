from socket import *

#创建套接字
so = socket(AF_INET,SOCK_STREAM)

#发起连接
server_addr = ('127.0.0.1',8888)
so.connect(server_addr)

while True:
    #消息发送接受
    data = input('请输入>>>')
    so.send(data.encode())
    if data == '##':
        break
    data = so.recv(1024)
    print('接受到:',data.decode())

so.close()