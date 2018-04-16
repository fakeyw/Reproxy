import socket
import threading
import time

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('',9000))
ss.listen(10)
print(1)



def read(conn):
	while True:
		print('read')
		conn.recv(30)
		
def send():
	sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sc.connect(('127.0.0.1',9000))
	
	tr = threading.Thread(target=read,args=(sc,))
	tr.start()
	tr2 = threading.Thread(target=read,args=(sc,))
	tr2.start()
	tr3 = threading.Thread(target=read,args=(sc,))
	tr3.start()
	for i in range(3):
		print('send')
		sc.send(b'aaaaa')
		c[0].sendall(b'111111111')
		time.sleep(0)
		
		
tr = threading.Thread(target=send)
tr.start()
c = ss.accept()
tr.join()

'''
测试说明socket并不能同时读和写，而是类似队列的形式进行交替读写
所以read的buffer可能需要大一些，否则一次读得太少会导致read内容少send内容多的情况
但还好不会报错
'''



