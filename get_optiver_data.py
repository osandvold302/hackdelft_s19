import socket

'''
s = socket.socket()

addr = ('127.0.0.1',7001)

s.connect(addr)
'''

UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST!"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('',7001))

#m=sock.recvfrom(1024)

while True:
    msg = sock.recv(4096)
    print(msg)
