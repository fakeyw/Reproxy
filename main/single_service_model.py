from main.server_threads import *

class service_piece(object):
	def __init__(self,signal_conn,host='',port=9000):
		this = (host,port)
		local = (host,port+1)
		t = serv_send_t(signal_conn,local,this)
		t.start()