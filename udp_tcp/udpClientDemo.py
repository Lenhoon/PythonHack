#coding=utf-8
#客户端，基于UDP协议
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto("hello",("127.0.0.1",8080))
data,addr=s.recvfrom(1024)
print "receive data:%s  from %s" %(data,str(addr))