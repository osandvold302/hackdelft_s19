import socket

UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

while True:
    file = open('raw.txt','a')
    packet = sock.recvfrom(65535)
    raw_request = str(packet[0])[2:-1]
    file.write(raw_request+"\n")
    print(raw_request)
    file.close()