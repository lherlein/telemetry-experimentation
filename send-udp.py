import socket

UDP_IP = "192.168.2.130"
UDP_PORT = 5005
MESSAGE = b"high"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))