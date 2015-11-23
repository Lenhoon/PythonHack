# -*- coding: utf-8 -*-
import socket
import paramiko
import threading
import sys
# 使用Paramiko示例文件的密钥
host_key = paramiko.RSAKey(filename='test_rsa.key')


class Server(paramiko.ServerInterface):

    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'Lenhoon') and (password == 'zlhzlh910413'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Listening for connection ...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen failed:' + str(e)
    sys.exit(1)
print '[+] Got a connection!'
# 以上是得到一个socket连接
try:
    bhSession = paramiko.Transport(client)
    # Transport create SSH session over an existing socket,只是创建了一个transport对象，还没开启SSH Session服务 需要用start_client或者start_server开启
    bhSession.add_server_key(host_key) # add a host key to the list of keys used for server mode
    server = Server()
    try:
        bhSession.start_server(server=server) # 将bhSession作为服务器会话开启
        # 其中的参数server是要通信的对象，用于验证和创建通道对象

    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed.'
    chan = bhSession.accept(20)
    print '[+] Authenticated!'
    print chan.recv(1024)
    chan.send('Welcome to bh_ssh')
    while True:
        try:
            command = raw_input("Enter command: ").strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception, e:
    print '[-] Caught exception: ' + str(e)
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)
