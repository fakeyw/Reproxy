import socket

main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_sock.bind(('',9000))
main_sock.listen(20)
while True:
	s,a = main_sock.accept()
	c = s.recv(2048)
	s.send(b'1111')
	s.close()