'''
should be imported by client.py
'''
from main.client-works import *
import threading

class cli_send_t(threading.Thread):
	def __init__(self,host,port,reg_conn): #首次连接服务器，监控本地-服务conn 发送至反代服务器对应conn
		self.server_host = host
		self.server_port = port
		self
	
	def run(self):
		

class cli_recv_t(threading.Thread):
	def __init__(self,reg_conn): #监控本地-反代服务conn  发送至本地服务对应conn/创建新连接（双侧，注册到reg中）
		pass

