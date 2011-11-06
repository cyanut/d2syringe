#!/usr/bin/python

import re
import sys
import pprint

labels = ["source","id","type","name","args","remark"]

def init_prot(raw):
    prot_dic = {}
    prot_re = re.compile("([CS]) > [CS] \[(0x[0-9A-F]{2})\] ([A-Z0-9]+)_([A-Z0-9]+).*?Used By:.*?Diablo\ II.*?Format:\n(.*?)Remarks:(.*?)~~", re.M|re.S)

    results = [list(x) for x in prot_re.findall(raw, re.M|re.S)]
    for p in results:
        temp = []
        p[1] = int(p[1], 16)
        p[4] = p[4].split("\n")
        for argline in p[4][:-1]:
            arg = re.findall(" *\(([A-Z0-9_]*)\) ?(\[[-9]*\])? *(.*?)\.?\*{0,2}\ *$", argline)

            if arg:
                temp.append(arg[0])
        p[4] = temp
        p = dict(zip(labels, p))
        if not p["source"] in prot_dic:
            prot_dic[p["source"]] = {}
        if not p["type"] in prot_dic[p["source"]]:
            prot_dic[p["source"]][p["type"]] = {}
        prot_dic[p["source"]][p["type"]][p["id"]] = p
    return prot_dic


if __name__ == "__main__":
    results = init_prot(open(sys.argv[1]).read())
    open("protdata.py", "w").write(pprint.pformat(results))
    print(len(results))
