#!/usr/bin/python

import d2protdata
import struct
from pprint import pprint as print

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
    p = 0
    pstr = ptype[2]
    values = []
    for argtype in [x[0] for x in args]:
        if argtype == "BYTE":
            values.append(pstr[p])
            p += 1
        elif argtype == "WORD":
            values.append(struct.unpack("<H", pstr[p:p+2])[0])
            p += 2
        elif argtype == "DWORD":
            values.append(struct.unpack("<I", pstr[p:p+4])[0])
            p += 4
        elif argtype == "STRING":
            str_end = pstr.index(b"\x00", p)
            values.append(pstr[p:str_end])
            p = str_end + 1
        else:
            break
    newarg = [[x[0][0], x[1], x[0][1]] for x in zip(args, values)]
    

    return (ptype, pformat, newarg)
    #for (argtype, isarray, remarks) in args:

if __name__ == "__main__":

    print(unpack(b"\xff>%\x00\x15\x00\x00\x00\xf0M\xb5t\xe7\xf7\x87kX\xbb\xee\xf8\xbc\xdf\xc3\x8bY\xa3\xb2sStage1st\x00", "C"))
    print(unpack(b"\x0b\x00\x07lettace\x00", "C"))
