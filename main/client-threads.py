'''
should be imported by client.py
'''


import threading

'''
First connect to proxy server as main thread, get port
then, work as a sender
'''
class cli_send_t(threading.Thread):
	pass
	

class cli_recv_t(threading.Thread):
	def __init__(self,recv_conn):
		pass

