#!/usr/bin/python

import socket, threading
from select import select
import time
import d2prot
import sys
import traceback
from pprint import pprint
SRV_ADDR = "202.104.1.89"
BN_PORT = 6112
BN2_PORT = 6113
GAME_PORT = 4000


def serve(port):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.bind(("", port))
    skt.listen(1)

    print("Server listening @ " + str(port) + " ...")
    while True:
        conn, addr = skt.accept()
        print(repr(addr) + " connected " + str(port) + " !")
        srv_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_skt.connect((SRV_ADDR, port))
        print(repr(srv_skt.getsockname()) + "connected to " + repr((SRV_ADDR, port)))
        conn.setblocking(1)
        srv_skt.setblocking(1)
        work_thread = threading.Thread(target=manage_conn, \
                                        args=(conn, srv_skt))
        work_thread.start()

def manage_conn(cli, srv):
    connpair = set([cli, srv])
    live = True
    while live:
        rl, wl, el = select([cli, srv], [], [])
        for rs in rl:
            msg = rs.recv(4096)
            if rs == cli:
                target = srv
                symbol = str(rs.getsockname()[1])+"==> "
                msg = msg.replace(b"\x7f\x00\x00\x01",b"\xca\x68\x01\x59") 
            elif rs == srv:
                symbol = "<== " + repr(rs.getpeername()) 
                target = cli
                msg = msg.replace(b"\xca\x68\x01\x59", b"\x7f\x00\x00\x01")
            if msg:
                if rs == cli:
                    source = "C"
                else:
                    source = "S"
                print(symbol.encode("utf-8") + msg)
                try:
                    msgdic = d2prot.unpack(msg, source)
                    if msgdic[0][1] != 143 and msgdic[0][1] != 109:
                        pprint(msgdic)
                except BaseException as e:
                    exc_type, exc_val, exc_tb = sys.exc_info()
                    traceback.print_tb(exc_tb)
                    print(repr(e))
                print("-"*10)
            else:
                live = False
                continue
            target.send(msg)




if __name__ == "__main__":
    threading.Thread(target=serve, args=(BN_PORT,)).start()
    threading.Thread(target=serve, args=(BN2_PORT,)).start()
    serve(GAME_PORT)
    

