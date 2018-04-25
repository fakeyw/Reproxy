from main.client_threads import *

remote = ('127.0.0.1',7000) #reproxy service
local = ('127.0.0.1',9000) #local service
t1 = cli_recv_t(remote,local)
t1.start()