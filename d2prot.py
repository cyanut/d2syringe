#!/usr/bin/python

import d2protdata
import struct

def unpack_header(s):
    if s == b"\x01":
        return ("INIT", int(s), "")
    
    if len(s) > 4:
        header_word = struct.unpack("<H", s[:2])[0]
        if header_word == len(s):
            return ("MCP", int(s[2]), s[3:])

    if len(s) > 0:
        header_byte = int(s[0])
    if header_byte == len(s) and len(s) >= 2:
        return ("D2GS", int(s[1]), s[2:])

    elif header_byte == 0xFF and len(s) >= 4:
        if struct.unpack("<H", s[2:4])[0] == len(s):
            return ("SID", int(s[1]), s[4:])


    return False    

def unpack(s, source):
    ptype = unpack_header(s) 
    pformat = d2protdata.protdic[source][ptype[0]][ptype[1]]
    args = pformat["args"]
    print(args)
    #for (argtype, isarray, remarks) in args:

if __name__ == "__main__":
    print(unpack(b"\xff\x25\x08\x00\xf8\xc5\x6f\x79", "C"))

