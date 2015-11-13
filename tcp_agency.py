# -*- coding: utf-8 -*-
import sys
import socket
import threading


# 十六进制导出函数
# 十六进制转储的函数，它仅输出数据包的十六进制和可打印的ASCII码字符。这对了解未知的协议非常有用，还能找到明文协议认证信息


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length * (digits + 1), hexa, text))
    print b'\n'.join(result)

# 接受本地和远程主机的数据，使用socket作为对象作为参数


def receive_from(connection):
    buffer = ""

    # 我们设置了两秒的超时，这取决于目标的情况，可能需要调整
    connection.settimeout(2)

    try:
        # 持续从缓存中读取数据指导没有数据或者超时
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

# 对目标是远程主机的请求进行修改


def request_handler(buffer):
    # 执行包修改
    return buffer

# 对目标是本地主机的响应进行修改


def response_handler(buffer):
    # 执行包修改
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # 连接远程主机 此时作为客户端
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # 如果必要从远程主机接收数据
    # 不向建立连接的远程主机主动发送数据
    if receive_first:
        # 一些作为服务的进程可能会先发送一些数据(比如FTP服务器一般会首先发送旗标)
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)  # 用套接字对象实现数据接收，然后转储数据包的负载，查看里面时候有感兴趣的内容

        # 发送给我们的响应处理
        # response_handler函数，在函数中我们可以修改数据包的内容，进行模糊测试，检测认证问题
        remote_buffer = response_handler(remote_buffer)

        # 如果我们从本地循环读取数据，发送给远程主机和本地主机
        while True:

            # 从本地读取数据
            local_buffer = receive_from(client_socket)

            if len(local_buffer):
                print "[==>] Receive %d bytes from local_host." % len(local_buffer)
                hexdump(local_buffer)

                # 发送给我们的本地请求
                local_buffer = request_handler(local_buffer)  # 将输出的流量进行修改

                # 向远程主机发送数据
                remote_socket.send(local_buffer)
                print "[==>] Sent to remote."

            # 接收响应的数据
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print "[<==] Received %d bytes from remote." % len(remote_buffer)
                hexdump(remote_buffer)

                    # 发送到响应处理函数
                remote_buffer = response_handler(remote_buffer)

                # 将响应发送给本地socket
                client_socket.send(remote_buffer)

                print "[<==] Sent to localhost."

            # 如果两边都没有数据，关闭连接
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] No more data. Closing connections."

                break


def server_loop(local_host, local_port, remote_host, remote_port,
                receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening socket or correct permissions."
        sys.exit(0)
    print "[*] Listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # 打印出本地连接信息
        print "[==>] Receive incoming connection from %s:%d" % (addr[0],
                                                                addr[1])

        # 开启一个线程与远程主机通信
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host,
                                              remote_port, receive_first))
        proxy_thread.start()


def main():
        # 没有华丽的命令行解析
    if len(sys.argv[1:]) != 5:
        print "Usage: python tcp_agency.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]"
        print "Example : python tcp_agency.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    # 设置本地监听参数
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    # 设置远程目标
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # 告诉代理在发送给远程主机之前连接和接受数据
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # 现在设置好我们的监听socket
    server_loop(local_host, local_port, remote_host, remote_port,
                receive_first)
main()
