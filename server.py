from main.single_service_model import *
import socket

host = ''
port = 7000
min = 7001
max = 8000

main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_sock.bind((host,port))
main_sock.listen(20)
print('Reproxy server start at',host,port)
port_now = 7001
while True:
	sock,addr = main_sock.accept()
	sock.sendall(str(port_now).encode('utf-8'))
	print('New service at',addr)
	print('--port outer:',port_now,',inner:',port_now+1)
	service_piece(sock,host=host,port=port_now)
	port_now = 7000+(port_now+2)%1000