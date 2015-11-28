# -*- coding:utf-8 -*-
import socket
import os
import struct
import sys
from ctypes import *

# 监听的主机
host = "192.168.2.1"

# IP头定义


class IP(Structure):  # Structure是ctype中的一个类
    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_uint32),
        ("dst",           c_uint32)
    ]

    # 类里面的构造方法 __init__() 负责将类的实例化
    # 而在 __init__() 启动之前，__new__() 决定是否要使用该 __init__() 方法
    # 因为__new__() 可以调用其他类的构造方法或者直接返回别的对象来作为本类的实例。

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
#  __new__()方法将原始缓冲区中的数据（本例中是我们从网络接收到的数据）填充到结构中，当调用
#  __init__()方法时，new已经完成了对缓冲区中数据的处理
# from_buffer_copy 这个方法创建一个ctype的实例，从原可读对象buffer中复制buffer

    def __init__(self, socket_buffer=None):
        # 协议字段与协议名称对应
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        # 可读性更强的IP地址
        # socket.inet_ntoa 将网络32位地址转换为点分十进制
        # struct.pack用于将Python的值根据格式符，转换为字符串（因为Python中没有字节(Byte)类型，可以把这里的字符串理解为字节流，或字节数组
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))
        #  "<L" little-endian ordered unsigned long value 小端无符号整形

        # 协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unuset", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


# 下面的代码类似于之前的例子
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # 读取数据包
        raw_buffer = sniffer.recvfrom(65565)[0]

        # 将缓冲区的前20个字节按IP头进行解析
        #ip_header = IP(raw_buffer)
        ip_header = IP(raw_buffer[0:20])

        # 输出协议和通信双方IP地址
        print "Protocol : %s %s -> %s" % (ip_header.protocol,
                                          ip_header.src_address, ip_header.dst_address)

        # 判断接受的数据包是不是ICMP,如果为ICMP,进行处理
        if ip_header.protocol == "ICMP":

            # 计算ICMP包的起始位置
            offset = ip_header.ihl * 4 # 计算ICMP数据在原始数据包中的偏移
            # ip_header.ihl字段，代表IP头中32bit(4字节的块)长的分片的片数
            buf = raw_buffer[offset:offset + sizeof(ICMP)]

            # 解析ICMP数据包
            icmp_header = ICMP(buf)

            print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)


# 处理 CTRL-C
except KeyboardInterrupt:

        # 如果在Windows上运行，关闭混杂模式
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
