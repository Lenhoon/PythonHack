import socket
import sys

target_host = sys.argv[1]
targe_port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, targe_port))

client.send("GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n")

response = client.recv(4096)

print response
