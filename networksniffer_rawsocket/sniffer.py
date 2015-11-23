# -*- coding:utf-8 -*-

import socket
import os

# 监听的主机 默认设置为CentOS
host = "222.182.111.19"

# 创建原始套接字，然后绑定在公开接口上
# 混杂模式允许我们嗅探网卡上流经的所有数据包，即使目的地址不是本机
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP  # 通过构建套接字对象对网络接口上的数据包嗅探进行必要的参数设置
    # 这里windows和Linux的区别是Windows允许我们嗅探所有协议的所有数据包，Linux只允许我们嗅探ICMP数据包
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# 设置在捕获的数据包中包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,
                   1)  # 设置套接字选项，设置捕获的数据包中包含IP头

# 在Windows平台上，我们需要设置IOCTL以启用混在模式
if os.name == "nt":  # 判断是否运行在win上，如果是我们发送IOCTL信号到网卡驱动上以启用混杂模式
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# 读取单个的数据包
print sniffer.recvfrom(65565)  # 输出整个数据包没有解码

# 在Windows平台上关闭混杂模式
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
