#!/usr/bin/python

import sys

import re

import urllib.request

def parseraw(url):

    s = urllib.request.urlopen(url).read().decode("utf-8")
    source = "N"
    try:
        protid = re.findall("Message ID:</td><td>(.*?)<", s)[-1]
        name = re.findall("Message Name:</td><td>(.*?)<", s)[-1]
        status = re.findall("Message Status:</td><td>(<.*?>)?[A-Z]*<", s)
        if status:
            status = status[-1]
        else:
            status = ""
        source = re.findall("Direction:</td><td>(.*?)\((.*?)\)<", s)[-1][-1]
        arglist = re.findall('font class="keyword">\((.*?)\)</font> *(.*?) *<',s, re.M|re.S)
        remarks = re.findall('Remarks:</td><td> *(.*?) *</td>',s, re.M|re.S)
        if remarks:
            remarks = remarks[-1]
        else:
            remarks = ""
    except IndexError:
        print("error at "+url)
    if source == "Received":
        source = "S"
    elif source == "Sent":
        source = "C"
    f = open(".".join([name, source, "html"]), "w")
    f.write(s)
    f.close()
    return name+"."+source

if __name__ == "__main__":

    u = "http://www.bnetdocs.org"
    findex = "../index.html"
    f = open(findex).read()
    flist = re.findall('<a href="(.*?)"><font size=1>', f)
    for fname in flist:
        print(parseraw(u + fname))
