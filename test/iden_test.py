import socket
import threading
import time
import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../base')))
print(sys.path)
from Dynamic_attr import da




ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('',9000))
ss.listen(10)
print(1)
'''
Need to test portocol
Send - recv with different buffer
XD
'''

def read(conn): #use p1 recv
	while True:
		recv =conn.recv(1024)
		print(recv)
		
def send(): #use p2 send
	sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sc.connect(('127.0.0.1',9000))
	sc = da(sc,{'uuid':1})
	
	tr = threading.Thread(target=read,args=(sc,))
	tr.start()
	c[0].send(b'aaaaaa')
		
		
ts = threading.Thread(target=send)
ts.start()
c = ss.accept()
ts.join()

'''
测试说明socket并不能同时读和写，而是类似队列的形式进行交替读写
所以read的buffer可能需要大一些，否则一次读得太少会导致read内容少send内容多的情况
但还好不会报错
'''


