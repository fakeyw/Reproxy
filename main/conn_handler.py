import uuid
import select
import socket
from base.Dynamic_attr import DA

# HOSTS -conn1(l)-> OUTER_SERVER -conn2(c)->-conn3(l)- INNER_SERVER -conn4(c)-> SERVICE
# A > B is 'B listening, A connect B'

class switching_pool(object):
	def __init__(self,listener,target):
		self.conn_dict = dict()					#'uuid':[listening,binding]
		self.target = target 					#('ip',port)
		self.listener = listener				
		self.listen_conns = [self.listener]		#save listening
		self.touch_conns = [self.listener]					#save touching
		
	#For listener thread
	def lread(self):
		inp,outp,err = select.select(self.listen_conns,[],[])
		for c in inp:
			if c is self.listener:
				new_uuid = str(uuid.uuid4())
				A,addr = c.accept()
				new_lis_conn = DA(A,{'uuid':new_uuid})
				B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				print(self.target)
				B.connect(self.target)
				new_tou_conn = DA(B,{'uuid':new_uuid})
				
				self.conn_dict[new_uuid] = [new_lis_conn,new_tou_conn]
				self.listen_conns.append(new_lis_conn)
				self.touch_conns.append(new_tou_conn)
			else:
				try:
					recv_data = c.recv(2048)
					if recv_data:
						id = c.uuid
						self.conn_dict[id][1].sendall(recv_data)
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.listen_conns.remove(l)
					self.touch_conns.remove(t)
					del self.conn_dict[id]

	#for toucher thread
	def tread(self):
		inp,outp,err = select.select(self.touch_conns,[],[])
		for c in inp:
			if c is self.listener:
				pass
			else:
				try:
					recv_data = c.recv(2048)
					print(recv_data)
					if recv_data:
						id = c.uuid
						self.conn_dict[id][0].sendall(recv_data)
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.listen_conns.remove(l)
					self.touch_conns.remove(t)
					del message_queue[id]
			
# HOSTS -conn1(l)-> OUTER_SERVER -conn2(c)-<-conn3(l)- INNER_SERVER -conn4(c)-> SERVICE
# A > B is 'B listening, A connect B'	
class outer_pool(object):
	def __init__(self,L_outer,L_inner,signal_conn):#bind two direction,need two ports
		self.conn_dict = dict()				#'uuid':[listening,binding]
		self.L_outer = L_outer
		self.outer_conns = [L_outer]		#save listening
		self.L_inner = L_inner
		self.inner_conns = [L_inner]
		self.signal_conn = signal_conn		#making signal, ask cli to touch serv
		
	def Oread(self):
		inp,outp,err = select.select(self.outer_conns,[],[])
		#print(inp)
		for c in inp:
			if c is self.L_outer:
				new_uuid = str(uuid.uuid4())
				A,addr = c.accept()
				new_outer_conn = DA(A,{'uuid':new_uuid})
				self.signal_conn.sendall(b'1')
				B,addr = self.L_inner.accept()
				new_inner_conn = DA(B,{'uuid':new_uuid})
				self.conn_dict[new_uuid] = [new_outer_conn,new_inner_conn]
				self.outer_conns.append(new_outer_conn)
				self.inner_conns.append(new_inner_conn)
				print('NEW LINK READY')
			else:
				try:
					recv_data = c.recv(2048)
					#print('Oread data:',recv_data)
					if recv_data:
						id = c.uuid
						self.conn_dict[id][1].sendall(recv_data)
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.outer_conns.remove(l)
					self.inner_conns.remove(t)
					del self.conn_dict[id]
					
	def Iread(self):
		print(2)
		inp,outp,err = select.select(self.inner_conns,[],[])
		#print(inp)
		for c in inp:
			print(3)
			if c is self.L_inner:
				pass
			else:
				try:
					recv_data = c.recv(2048)
					print('Iread data:',recv_data)
					if recv_data:
						id = c.uuid
						self.conn_dict[id][0].sendall(recv_data)
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.outer_conns.remove(l)
					self.inner_conns.remove(t)
					del self.conn_dict[id]
					
class inner_pool(object):
	def __init__(self,signal_conn,remote,local):
		self.conn_dict =  dict()
		self.signal_conn = signal_conn
		self.remote = remote
		self.remote_conns = [signal_conn]
		self.local = local
		self.local_conns = [signal_conn]
		
	def Rread(self):
		inp,outp,err = select.select(self.remote_conns,[],[])
		#print(inp)
		for c in inp:
			if c is self.signal_conn:
				r = c.recv(1024) #clean signal
				new_uuid = str(uuid.uuid4())
				A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				A.connect(self.remote)
				new_remote_conn = DA(A,{'uuid':new_uuid})
				B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				B.connect(self.local)
				new_local_conn = DA(B,{'uuid':new_uuid})
				self.conn_dict[new_uuid] = [new_remote_conn,new_local_conn]
				self.remote_conns.append(new_remote_conn)
				self.local_conns.append(new_local_conn)
				print('NEW LINK READY')
			else:
				try:
					recv_data = c.recv(2048)
					#print('Rread data:',recv_data)
					if recv_data:
						id = c.uuid
						self.conn_dict[id][1].sendall(recv_data)
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.remote_conns.remove(l)
					self.local_conns.remove(t)
					del self.conn_dict[id]
					
	def Lread(self):
		print(2)
		inp,outp,err = select.select(self.local_conns,[],[])
		#print(inp)
		for c in inp:
			if c is self.signal_conn:
				print(3)
			else:
				print(4)
				try:
					recv_data = c.recv(2048)
					print('Lread data:',recv_data)
					if recv_data:
						print(5)
						id = c.uuid
						self.conn_dict[id][0].sendall(recv_data)
						print(self.conn_dict[id][0])
				except ConnectionResetError:
					id = c.uuid
					l,t = self.conn_dict[id]
					self.remote_conns.remove(l)
					self.local_conns.remove(t)
					del self.conn_dict[id]
			
			
			
			
		