'''
should be imported by client.py
'''
from main.conn_handler import inner_pool as ipool
import threading
import socket

class cli_recv_t(threading.Thread):
	#remote,local -> ('ip',port)
	def __init__(self,remote,local,*args,**kw): #首次连接服务器，接收服务器对外端口，触发第二线程，接收信号，运行Rread
		super(cli_recv_t,self).__init__(*args,**kw)
		self.remote = remote
		self.local = local
		self.ipool = None
	
	def run(self):
		signal_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		signal_sock.connect(self.remote)
		outer_port = signal_sock.recv(1024).decode('utf-8')
		print('Get outer port:',outer_port)
		r = (self.remote[0],int(outer_port)+1)
		self.ipool = ipool(signal_sock,r,self.local)
		t2 = cli_send_t(self.ipool)
		t2.start()
		while True:
			self.ipool.Rread()

class cli_send_t(threading.Thread):
	def __init__(self,ipool,*args,**kw): #运行tread
		super(cli_send_t,self).__init__(*args,**kw)
		self.ipool = ipool
		
	def run(self):
		print(1)
		while True:
			self.ipool.Lread()
