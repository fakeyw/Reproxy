udp暂时不管



服务端



要考虑双侧主动发送问题

与客户端交互需要带上addr信息

被动接收不难，循环或select就可以



每个反代服务需要两个select

对外select的内容包括 主socket与外部connection

对内select内容为



双侧选择性发送：

外部连接保存 uuid:conn

与客户端有两个conn，一个用于发送一个用于接收

如果接收到外部报文，则在recv后在内容前加上固定长度uuid，发送 （连接选择协议）怎么找到uuid呢？继承socket类加个uuid项就好了嘛

接收到内网报文时截取uuid从保存的conn中取出选择conn，发送

---

首次服务连接：

client			  server

cli-work-sock bind local port with select&LOCK (out first)

cli-sock           -->      Handler Main sock 

​				   Accpet  a  conn 

​			           Creat a SERVICE instance, a socket bind a free port

​						with two threads (one work one wait)

​					        the working one wait for conn

close sock	 <--     distribute the free port

cli-send-sock   -->    connect, save as serv-recv-sock

cli-recv-sock    -->    connect, save as serv-send-sock

​				   thread-1 change work as recv thread

​				   start thread-2 as send thread

main thread change work as send thread

start thread-2 as recv thread



t1 start local socket, connect serv- > recv from local send to serv

t2 			recv from serv send to local

​				t1 connect cli -> recv from cli send to remote

​				t2           (accept conn) recv from remote, send to cli





conn_pool created by the first thread of a service, and then pass 