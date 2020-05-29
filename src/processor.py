#!/usr/bin/env python3

# -*- coding: utf-8 -*- #
import re
import time
from wormstools.utils import *
from wormstools.worms_core import Worms

def wid(file, win, wout):

    fo = wout + '_worms_aphiaID.tsv' if wout != 'input_based' else cname(win, 'aphiaID')
    pf = wformat(file, 'general')

    msg, firstLine = msgFirstL('aphiaIDs', None)
    print(msg)

    f = open(fo, "w")
    f.write(firstLine)
    # file = open(options['spps']).read().split("\n")
    for i in range(0, file.__len__()):

        spps0 = file[i].replace("\n", "")
        spps = modName(spps0)

        if not spps:
            continue

        if re.findall(" sp[p\\.]{0,2}$", spps):
            id = ''

        else:
            wObj = Worms(spps.lower())
            id = wObj.aphiaID
            time.sleep(0.5)

        print(pf % (i + 1, spps0))

        if not id:
            f.write('%s\t%s\t%s\n' % (spps0, '', 'Record not found in WoRMS'))
        else:
            f.write('%s\t%s\t%s\n' % (spps0, id, ''))
    f.close()

def wval(file, win, wout, wat):

    fo = wout + '_worms_val.tsv' if wout != 'input_based' else cname(win, 'val')

    pf1, pf2 = wformat(file, 'validation')

    msg, firstLine = msgFirstL('validated names', wat)
    print(msg)

    f = open(fo, "w")
    f.write(firstLine)
    # file = open(options['spps']).read().split("\n")
    for i in range(0, file.__len__()):
        # i = 1
        spps0 = file[i].replace("\n", "")
        spps = modName(spps0)

        if not spps:
            continue

        if re.findall(" sp[p\\.]{0,2}$", spps):
            spps_v = ''

        else:
            wObj = Worms(spps.lower())
            spps_v = wObj.taxamatch()
            time.sleep(0.5)

        OutStr = ''
        if not spps_v:

            OutStr += '%s\t%s\t%s' % (spps0, '', 'Record not found in WoRMS')
            print(pf2 % (i + 1, spps0))
        else:

            OutStr += '%s\t%s\t%s' % (spps0, spps_v, '')
            print(pf1 % (i + 1, spps0, spps_v))

        if wat is not None:
            OutStr = rankStr(spps_v, wObj, wat, OutStr)

        f.write(OutStr + '\n')

    f.close()

def wsyn(file, win, wout, wat):

    fo = wout + '_worms_syn.tsv' if wout != 'input_based' else cname(win, 'syn')
    pf = wformat(file, 'general')

    msg, firstLine = msgFirstL('synonyms', wat)
    print(msg)

    f = open(fo, "w")
    f.write(firstLine)

    for i in range(0, file.__len__()):
        # i = 4
        spps0 = file[i].replace("\n", "")
        # spps0 = "Alopias pelgicus"
        spps = modName(spps0)

        if not spps:
            continue

        if re.findall(" sp[p\\.]{0,2}$", spps):
            syns = ''
        else:

            wObj = Worms(spps)
            syns = wObj.get_synonyms()
            time.sleep(0.5)

        cc = '' if isinstance(syns, str) else 'in WoRMS'
        print(pf % (i + 1, spps0))

        OutStr = ''
        if not cc:

            OutStr += '%s\t%s\t%s' % (spps0, '', 'Record not found in WoRMS')
        else:

            jsyns = ", ".join(syns)

            if wObj.accepted_name:
                obs = "Deprecated name: %s" % spps0
                spps0 = wObj.accepted_name

            else:
                obs = ''

            OutStr += '%s\t%s\t%s' % (spps0, jsyns, obs)

        if wat is not None:
            OutStr = rankStr(cc, wObj, wat, OutStr)

        f.write(OutStr + '\n')

    f.close()

def wrank(file, win, wout, wat):

    print("\nAdding taxonomical ranks:\n")

    fo = wout + '_worms_ranks.tsv' if wout != 'input_based' else cname(win, 'ranks')
    pf = wformat(file, 'general')

    firstLine = "%s\tSpecies\tObs\n" % "\t".join(wat)

    f = open(fo, "w")
    f.write(firstLine)

    for i in range(0, file.__len__()):

        spps0 = file[i].replace("\n", "")
        # spps0 = "Alopias pelgicus"
        spps = modName(spps0)

        if not spps:
            continue

        if re.findall(" sp[p\\.]{0,2}$", spps):
            tax_ranks = []

        else:
            wObj = Worms(spps)
            wObj.get_taxonomic_ranges()
            tax_ranks = wObj.taxonomic_ranges

        print(pf % (i + 1, spps0))

        if not tax_ranks:
            so = "%s\t%s" % (spps0, 'Record not found in WoRMS')

        else:
            if wObj.accepted_name:
                obs = "deprecated name: %s" % spps0
                spps0 = wObj.accepted_name

            else:
                obs = ''
            so = "%s\t%s" % (spps0, obs)

        f.write(rankStr(tax_ranks, wObj, wat, so) + "\n")
    f.close()
