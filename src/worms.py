#!/usr/bin/env python3

# -*- coding: utf-8 -*- #
import argparse
from wormstools.processor import wid, wsyn, wval, wrank

def getOpt():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='''WoRMS wrapper''',
                                     epilog="* Warning: Scripts here run as fast as WoRMS server allow us")

    parser.add_argument('spps',
                        metavar='spps_file',
                        default=None,
                        help='Target species in plain text')
    parser.add_argument('-id',
                        action='store_true',
                        help='Get aphiaIDs')
    parser.add_argument('-val',
                        action='store_true',
                        help='Get validated names')
    parser.add_argument('-syn',
                        action='store_true',
                        help='Get species synonyms')
    parser.add_argument('--at',
                        nargs='+',
                        metavar="str",
                        default=None,
                        help='[Optional] Introduce futher taxonomical ranks to species [Default = None]')
    parser.add_argument('--out', metavar="str",
                        action='store',
                        default='input_based',
                        help='Output name [Default = <input_based>.tsv]')
    args = parser.parse_args()

    return args

def main():
    options = vars(getOpt())
    # print(options)
    file = open( options['spps'], 'r' ).read().split("\n")

    if options['id']:

        wid(file,
            options['spps'],
            options['out'])

    if options['val']:

        wval(file,
             options['spps'],
             options['out'],
             options['at'])

    if options['syn']:

        wsyn(file,
             options['spps'],
             options['out'],
             options['at'])

    if not options['val'] and\
       not options['syn'] and\
       options['at'] is not None:

        wrank(file,
              options['spps'],
              options['out'],
              options['at'])

if __name__ == '__main__':
    main()
