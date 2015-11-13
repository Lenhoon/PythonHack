
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("127.0.0.1",8080))  
print "Begin to listen ..."
while True:
    data,client=s.recvfrom(1024)
    print "receive a connection from %s,data is: %s"  %(str(client),str(data))    
    data = "Hello !!!"
    s.sendto("echo:"+data,client)