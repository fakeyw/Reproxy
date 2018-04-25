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

如果接收到外部报文，则在recv后在内容前加上固定长度uuid，发送 （连接选择协议）怎么找到uuid呢？继承socket类加个uuid项

接收到内网报文时截取uuid从保存的conn中取出选择conn，发送

---

首次服务连接：

client			  server

cli-work-sock bind local port with select&LOCK (out first)

cli-conn           -->      Handler Main sock 

​				   Accpet  a  conn 

​			           Creat a SERVICE instance, a socket bind a free port

​						with two threads (one work one wait)

​					        the working one wait for conn

close conn	 <--     distribute the free port

cli-send-conn   -->    connect, save as serv-recv-conn

cli-recv-conn    -->    connect, save as serv-send-conn

​				   thread-1 change its work as recv thread

​				   start thread-2 as send thread

main thread change work as send thread

start thread-2 as recv thread



About threads

cli

t1 start local socket, connect serv- > recv from local send to serv

t2 			recv from serv send to local

​				serv

​				t1 connect cli -> recv from cli send to remote

​				t2           (accept conn) recv from remote, send to cli

conn_pool created by the first thread of a service, and then pass 



About sockets

cli - local connect() static

cli - serv connect() static

serv - remote bind() active

serv - cli bind() active --(after two acceptions)-> static 



关于socket select protocol（已经没用了）

是为了分辨外部访问多个socket，避免经过反代转发后丢失返回目标，类似路由器的路由表

(反代貌似就是干了比路由器相反的活)

---

> 这个协议意义不大，ssh之类的持续连接本来就是直接开conn

现在的问题是，在异步传输模式下，怎样分辨协议包？

设置本地conn的recv buffer为N，读到raw(可能是原包的一部分)

uuid+rawlen+raw 

rawlen为raw长度，rawlen的长度(bin)为2^rawlen = N

发送端：如果传入packer的数据长度超过N，则会被自动分割到list中，分别发送

接收端：将接收到的报文传入parser会拿到下次要接收的报文长度，长度为0时重置为len(uuid)+len(rawlen)+rawlen，那么就会有几种情况出现：

- 读入太多，包含一个报文以上 -- parser会将完整报文内容+uuid放入队列中等待调用，需读长度由最后一个未读完的报文决定
- 实际读入比需读偏少，直接传入，parser会将上次记录的减去
- socket的buffer限制，在实例化协议的时候加入参数，将需读内容分割
- 读入过少，未读到完整报文头，记录，以最大值读取，拼接后再次分析

---

流程修改：

client			  server

cli-work-sock bind local port with select&LOCK (out first)

cli-conn           -->      Handler Main sock 

​				   Accpet  a  conn 

​			           Creat a SERVICE instance, a socket bind a free port

​						with two threads (one work one wait)

​					        the working one wait for conn

close conn	 <--     distribute the free port

cli-listener bind port  

​				   thread-1 change its work as recv thread

​				   start thread-2 as send thread

main thread change work as send thread

start thread-2 as recv thread

对外socket被select(由send thread扫描)时 服务端connect本地，新建的conn由recv thread扫描

本地接收到的conn由recv select，并向服务所在端口作connect



About threads

cli

t1 start local socket, connect serv- > recv from local send to serv

t2 			recv from serv send to local

​				serv

​				t1 connect cli -> recv from cli send to remote

​				t2           (accept conn) recv from remote, send to cli

conn_pool created by the first thread of a service, and then pass 



About sockets

cli - local connect() active

cli - serv connect() active

serv - remote bind() active

serv - cli bind() active

---

那么下一个问题，解决端内conn对应的问题

两个conn共用一个uuid 双向可查

给类添加id貌似失败了

借用了一下对象锁的实现方法，成功给socket对象套了一个id

{ uuid : [conn1,conn2], ... }

conn1 - uuid - dict -conn2



已测试python的一个socket conn可同时读写（实际上有队列等待）

