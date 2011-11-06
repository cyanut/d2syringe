#!/usr/bin/python

import sys
import os.path
import pprint
import re
import d2protdata

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
    if verbose:
        print("id =", protid)
        print("name =", name)
        print("status =", status)
        print("source =", source)
        print("arglist =", arglist)
        print("remarks =", remarks)
        print("-"*20)
    for t, v in arglist:
        typeset.add(t)
        if v[:2] == "[]":
            templist.append(fname)
    return (protid, "".join([token[x[0]] for x in arglist]))

if __name__ == "__main__":
    f = open("protdata.py", "w")
    prot_dic = {}
    for fname in sys.argv[1:]:
        prot = parseraw(fname)
        if not prot:
            print("died here @ " + fname)
            quit()
        prot_type = os.path.basename(fname).split("_")[0]
        if not prot_type in prot_dic:
            prot_dic[prot_type]={}
        prot_dic[prot_type][prot[0]] = prot[1]
    f.write("prot_dic=\n")
    f.write(pprint.pformat(prot_dic))


    print(typeset)
    print(templist)
