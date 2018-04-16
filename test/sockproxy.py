import socket
import threading
import re
import logging
from datetime import datetime

#配置

#实际端口
protect_ip = '127.0.0.1'
protect_port = 30000
#暴露端口
exposed_ip = '0.0.0.0'
exposed_port = 80
TIME_OUT=3

#数据包大小
PKT_BUFF_SIZE = 2048

#日志


url_pattern = re.compile(r'^(GET|POST).*')
post_pattern = re.compile(r'^\\r\\n\\r\\n.*')

def send_log(content,request_ip):
	time_now_string='['+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+']'
	print(time_now_string+content)
	
	#-----------------------------IP Classfied log-------------------------------------------------#
	log_file=open("%s%s" % (request_ip,"log.txt"),"a")
	log_file.write('%s' % time_now_string +'\n')
	log_file.write(content+'\n-----------------------------------------------------------\n')
	log_file.close()
	
	#-----------------------------Summary log----------------------------------------------#
	if not request_ip == '':
		log_file2=open("log.txt","a")
		log_file2.write('%s' % time_now_string +'\n')
		log_file2.write(content+'\n-----------------------------------------------------------\n')
		log_file2.close()
	
	return

#数据交换
def switcher(from_conn,to_conn,request_ip):
	while True:
		try:
			data = from_conn.recv(PKT_BUFF_SIZE)
		except Exception as e:
			send_log('Event: Connection closed.',request_ip)
			logging.exception(e)
			break
		
		if not data:
			print("no data")
			break
		#-----------------------------------Construct log content----------------------------------#
		#maybe a decorator or just content.add(str) is better
		
		log_content=''
		url_log=url_pattern.match(data.decode('utf-8')).group()
		post_log=str(data).partition("\\r\\n\\r\\n")[2]
		log_content=log_content+'Url:'+url_log+'\n'
		
		if not post_log == "'":
			log_content=log_content+'Post params:'+post_log
		send_log(log_content,request_ip)
		
		to_conn.send(data)
		while True:
			try:
				resp=to_conn.recv(PKT_BUFF_SIZE)
			except Exception as e:
				send_log('Event: Connection closed.',request_ip)
				logging.exception(e)
				break
		
			if not resp:
				print("no data")
				break
			from_conn.send(resp)
			#send_log('Info: Mapping data > %s ' % repr(data))
			#send_log('Info: Mapping > %s -> %s > %d bytes.' % (conn_receiver.getpeername(), conn_sender.getpeername(), len(data)))

	from_conn.close()
	to_conn.close()

	return

#并发请求处理
def deal_request(exposed_conn, protect_ip, protect_port, request_ip):
	global TIME_OUT
	#对每个请求都单独建立socket
	protect_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	protect_conn.setblocking(1)
	protect_conn.settimeout(TIME_OUT)
	try:
		protect_conn.connect((protect_ip, protect_port))
	except Exception:
		exposed_conn.close()
		send_log('Error: Unable to connect to the remote server.',request_ip)
		return

	threading.Thread(target=switcher, args=(exposed_conn,protect_conn,request_ip)).start()
	return

# 端口映射函数
def tcp_mapping(protect_ip, protect_port, exposed_ip, exposed_port):
	#对暴露端口建立socket连接
	exposed_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	exposed_server.bind((exposed_ip, exposed_port))
	exposed_server.listen(5)

	send_log('Event: Starting mapping service on ' + exposed_ip + ':' + str(exposed_port) + ' ...','')

	while True:
		try:
			#暴露端口获取到一个请求就建立一个连接，之后的交换就只用这个conn就行了
			(exposed_conn, request_addr) = exposed_server.accept()
		except KeyboardInterrupt as e:
			exposed_server.close()
			send_log('Event: Stop mapping service.','')
			break
		#新开线程处理
		request_ip=request_addr[0]
		threading.Thread(target=deal_request, args=(exposed_conn, protect_ip, protect_port,request_ip)).start()
		
		send_log('Event: Receive mapping request from %s:%d.' % request_addr,'')

	return

if __name__ == '__main__':
	tcp_mapping(protect_ip, protect_port, exposed_ip, exposed_port)