'''
should be imported by single-service-model.py
'''
from main.conn_handler import outer_pool as opool
import threading
import socket

class serv_send_t(threading.Thread):
	#local由主连接线程获取
	def __init__(self,signal_conn,local,this,*args,**kw):
		super(serv_send_t,self).__init__(*args,**kw)
		self.this = this
		self.local = local
		self.signal_conn = signal_conn
		self.opool = None
		
	def run(self):
		recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		recv_sock.bind(self.this)
		recv_sock.listen(20)	#to outer
		
		send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		send_sock.bind(self.local)
		send_sock.listen(20)	#to inner
		
		self.opool = opool(recv_sock,send_sock,self.signal_conn)
		t2 = serv_recv_t(self.opool)
		t2.start()
		print('start work')
		while True:
			self.opool.Oread()
	
class serv_recv_t(threading.Thread):
	def __init__(self,opool,*args,**kw):
		super(serv_recv_t,self).__init__(*args,**kw)
		self.opool = opool
		
	def run(self):
		while True:
			print(1)
			self.opool.Iread()
			
			
			
			