
import socket
import sys

target_host = "192.168.2.6"
target_prot = 9999

buff = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_prot))

client.send(buff)

response = client.recv(4096)

print response
