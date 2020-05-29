#!/usr/bin/env python3

# -*- coding: utf-8 -*- #
import unicodedata

def wformat(f, k):
    # f = file
    f = list(filter(None, f))

    if not f:
        print("\nEmpty file\n")
        exit()

    maxL = sorted([list(i).__len__() for i in f])[-1]
    we   = "%{}s".format(maxL)
    ne   = "%{}s".format(str(len(f)).__len__())

    if k == "general":
        return "%s. %s" % (ne, we)

    elif k == "validation":
        nwe = "%-{}s".format(maxL)

        notval = "%s. not validated: %s" % (ne, we)
        val = "%s. validated:     %s -> %s" % (ne, we, nwe )

        return val, notval

def cname(s, ty):

    tail = "_worms_%s.tsv" % ty
    try:
        return s.split(".")[-2].split("/")[-1] + tail
    except IndexError:
        return s.split("/")[-1] + tail

def modName(s):
    rmAcc = lambda s: unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')

    spps0 = " ".join(filter(None, s.split(' ')))
    spps0 = rmAcc(spps0)
    return spps0

def msgFirstL(s, a):

    if a is None:
        msg = "\nGetting %s:\n" % s
        firstL = "species\t%s\tObs\n" % s
    else:
        msg = "\nGetting %s and adding taxonomical ranks:\n" % s
        firstL = "%s\tspecies\t%s\tObs\n" % ("\t".join(a), s)

    return msg, firstL

def rankStr(c, o, a, i=None):
    # c, o, a, i = (spps_v, wObj, ['Class'], OutStr)
    if not c:
        rs = "\t".join([''] * len(a))
    else:
        rs = "\t".join([o.get_rank(ii) for ii in a])

    if i is None:
        return rs

    else:
        if isinstance(i, str):
            i = [i]

        rs = [rs] + i

        return "\t".join(rs)

