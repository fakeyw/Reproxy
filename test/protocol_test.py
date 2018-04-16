import socket
import threading
import time
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../main')))
print(sys.path)

from socket_select_protocol import *

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('',9000))
ss.listen(10)
print(1)
'''
Need to test portocol
Send - recv with different buffer
XD

'''
parser1 = SSP_parser(send_buffer=2048,recv_buffer=20)
parser2 = SSP_parser(send_buffer=10,recv_buffer=50)

def read(conn): #use p1 recv
	while True:
		recv =conn.recv(parser1.recvlen)
		print(recv)
		parser1.consume(recv) 
		
def send(): #use p2 send
	sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sc.connect(('127.0.0.1',9000))
	
	tr = threading.Thread(target=read,args=(sc,))
	tr.start()
	for i in range(3):
		msg = input('Msg:')
		list = parser2.pack(uuid,msg) #uuid is of static length
		print(list)
		for i in list:
			c[0].send(i)
		
		
ts = threading.Thread(target=send)
ts.start()
c = ss.accept()
tr.join()

'''
测试说明socket并不能同时读和写，而是类似队列的形式进行交替读写
所以read的buffer可能需要大一些，否则一次读得太少会导致read内容少send内容多的情况
但还好不会报错
'''



