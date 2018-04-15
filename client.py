import threading
import socket

class client_t(threading.Thread):
	def __init__(self,bind,forward,*args,**kw):
		self.bind = bind
		self.forward = forward
		
	def run():
		