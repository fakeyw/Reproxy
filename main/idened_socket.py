import socket
import uuid

class idsock(socket.socket):
	def __init__(self,*args,**kw):
		super(self,idsock).__init__(*args,**kw)
		self.uuid = uuid.uuid4()