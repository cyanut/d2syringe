#!/usr/bin/python

import sys
import os.path
import pprint
import re
from d2protdata import protdic

typeset = set()
templist = []
verbose = False

token={"WORD":"W",\
        "STRING":"S",\
        "VOID":"V",\
        "FILETIME":"F",\
        "BOOLEAN":"O",\
        "DWORD":"D",\
        "BYTE":"B"}

def parseraw(fname):

    s = open(fname).read()
    source = "N"
    try:
        protid = re.findall("Message ID:</td><td>(.*?)<", s)[-1]
        name = re.findall("Message Name:</td><td>(.*?)<", s)[-1]
        status = re.findall("Message Status:</td><td>(<.*?>)?(.*?)<", s)
        if not status:
            status = ""
        else:
            status = status[-1][-1]
        source = re.findall("Direction:</td><td>(.*?)\((.*?)\)<", s)[-1][-1]
        arglist = re.findall('font class="keyword">\((.*?)\)</font> *(.*?) *<',s, re.M|re.S)
        remarks = re.findall('Remarks:</td><td> *(.*?) *</td>',s, re.M|re.S)
        if not remarks:
            remarks = ""
        else:
            remarks = remarks[-1]
    except IndexError:
        return False
    if source == "Received":
        source = "S"
    elif source == "Sent":
        source = "C"
    remarks = re.sub("<.*?>", "", remarks, re.M|re.S)
    try:
        protid = int(protid, 16)
    except ValueError:
        return False
    if verbose:
        print("id =", protid)
        print("name =", name)
        print("status =", status)
        print("source =", source)
        print("arglist =", arglist)
        print("remarks =", remarks)
        print("-"*20)
    temparg = []
    for t, v in arglist:
        typeset.add(t)
        if v[:2] == "[]":
            templist.append(fname)
            temparg.append([t+"[]", v[2:]])
        else:
            temparg.append([t,v])
    arglist = temparg
    
    prottype = name.split("_")[0]
    if source in protdic and \
            prottype in protdic[source] and \
            not protid in protdic[source][prottype]:
        protdic[source][prottype][protid] = {\
                "id":       protid,\
                "name":     name.split("_")[1],\
                "remark":   remarks,\
                "source":   source,\
                "type":     prottype,\
                "args":     arglist
                }

                

if __name__ == "__main__":
    
    for fname in sys.argv[1:]:
        prot = parseraw(fname)
     
    open("d2protdata2.py", "w").write("protdic="+pprint.pformat(protdic))


    print(typeset)
    print(templist)
