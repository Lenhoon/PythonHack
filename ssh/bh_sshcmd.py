# -*- coding:utf-8 -*-
import threading
import paramiko
import subprocess
import sys

# 我们创建一个名为ssh_command的函数
# 该函数连接到ssh服务器并运行一条命令
# 可以命令行输入我们想要连接的主机

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # Paramiko支持用密钥认证来代替密码验证
    # client.load_host_keys('/home/justin/.ssh/known_hosts')
    # 设置策略自动添加和保存目标SSH服务器的SSH密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        # 通过调用ssh_command 函数运行命令
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    ssh_session.close()
    return


remote_ip = sys.argv[1]
remote_user = sys.argv[2]
remote_pass = sys.argv[3]
while True:
    cmd = ""
    cmd = raw_input(remote_user + ">>")
    ssh_command(remote_ip, remote_user, remote_pass, cmd)
