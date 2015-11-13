# -*- coding:utf-8 -*-
import socket

target_host = "127.0.0.1"
target_port = 8080

#建立一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#发送一些数据
client.sendto("AAABBBCCC",("127.0.0.1",8080))
#接受一些数据
data, addr = client.recvfrom(1024)
print "receive data:%s  from %s" %(data,str(addr))