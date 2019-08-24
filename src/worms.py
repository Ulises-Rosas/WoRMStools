#!/usr/bin/env python3

# -*- coding: utf-8 -*- #
import re
import urllib.error
import urllib.request
import time
import argparse
import unicodedata

class Worms:
    def __init__(self, taxon):

        self.taxon = taxon.replace(" ", "%20")

        aphiaID_url = "http://www.marinespecies.org/rest/AphiaIDByName/" + \
                      self.taxon + \
                      "?marine_only=false"

        self.aphiaID = None
        # make sure aphiaID will be available for downstream analyses
        while self.aphiaID is None:
            try:
                self.aphiaID = urllib.request.urlopen(aphiaID_url).read().decode('utf-8')
            except urllib.error.HTTPError:
                time.sleep(0.5)
                pass

        ##...variables to fill in...##
        self.taxonomic_ranges = []
        self.classification_page = ""
        self.synonym_list = []
        ##...variables to fill in...##

        ##...urls...##
        self.records_url = "http://www.marinespecies.org/rest/AphiaChildrenByAphiaID/" + \
                           self.aphiaID + \
                           "?marine_only=false&offset=1"
        self.accepted_name = ""
        self.classfication_url = "http://www.marinespecies.org/rest/AphiaClassificationByAphiaID/"
        self.synonym_url = "http://www.marinespecies.org/rest/AphiaSynonymsByAphiaID/"
        ##...urls...##

    def get_children_names(self, till="Species"):

        records_url = 'http://www.marinespecies.org/rest/AphiaChildrenByAphiaID/205965?marine_only=true&offset=1'

        page = urllib.request.urlopen(records_url).read().decode('utf-8')

        names = [names.replace('\"', '').replace('valid_name:', '') for names in
                 re.findall('"valid_name":"[A-Z][a-z]+[ a-z]+"', page)]

        ## in progress
        pass

    def get_accepted_name(self):
        """this function assumes that name is deprecated and tries to find epitopes
        which is more similar with
        """
        # species with unaccepted names for testing:
        # self = Worms("Paratrophon exsculptus")
        # self =  Worms("Manta birostris")
        # self = Worms("Aglaophamus peruana")
        # self = Worms("Euzonus furciferus")
        # self = Worms("Lubbockia squillimana")
        # self = Worms("Doris fontainii")
        # self = Worms("Synarmadillo tristani")
        # self = Worms("Spondylus americanus")
        # self = Worms("Felaniella parilis")

        if len(self.aphiaID) == 0 or self.aphiaID == '-999':

            species_binary = self.taxon.split("%20")

            genus_id_url = "http://www.marinespecies.org/rest/AphiaIDByName/" + \
                           species_binary[0] + \
                           "?marine_only=false"

            genus_id = urllib.request.urlopen(genus_id_url).read().decode('utf-8')

            if genus_id == '-999' or genus_id == '':

                self.accepted_name = ""
                self.aphiaID = ""

                return self.accepted_name

            else:
                complete_url = "http://www.marinespecies.org/aphia.php?p=taxdetails&id=" + genus_id

                page = urllib.request.urlopen(complete_url).read().decode('utf-8')

                # line which contains span
                lines = re.findall("<span.*>" + species_binary[0] + "[\(A-Za-z\) ]{0,} [a-z]+<.*", page)

                # it takes the first species pattern
                epitopes0 = []

                for ep in lines:
                    tmp = re.findall("<i>[A-Z][a-z]+[\(\)A-Za-z ]{0,} [a-z]+</i>", ep)
                    epitopes0.append(tmp)

                epitopes = [i[0].split(" ")[-1].replace("</i>", "") for i in list(filter(None, epitopes0))]

                def get_pieces(string, amplitude):

                    pieces = [string[i:i + amplitude] for i in range(len(list(string)))]

                    trimmed_pieces = [i for i in pieces if len(i) > amplitude - 1]

                    return trimmed_pieces

                for index in range(len(list(species_binary[1])) - 1):
                    # pieces by the length of index, e.g.,
                    # if the string is "abc" and index = 0, then ['a', 'b', 'c']
                    # if the string is "abc" and index = 1, then ['ab', 'bc']

                    # index =0
                    # print(index)

                    a = get_pieces(species_binary[1], index + 1)

                    lengths = []

                    for string in epitopes:

                        matches = [re.findall(i, string) for i in set(a)]
                        # n1 is the number of matches that pieces `a` have with a string
                        # d1 is the number of choices available for matches from a string

                        if len(get_pieces(string, index + 1)) == 0:
                            # if a, which are pieces of `species_binary[1]`, is larger than
                            # the string, you will always have zero matches. That is, `n1` will
                            # be always zero. So, it does not care what value takes d1. In this
                            # case it will take 1 so as to avoid emerging conflicts from division
                            d1 = 1

                        else:
                            d1 = len(get_pieces(string, index + 1))
                        # number of matches. Since inside sum function there is just a list of lists,
                        # sum only counts crowded lists,i.e., number of matches
                        n1 = sum([len(c) for c in matches])

                        # since it can appear a large string with multiple matches from just a part of it,
                        # n1/d1 is the number of matches between "a", pieced `species_binary[1]` and
                        # the epitope (string) (e.i. a --> epitope) divided by the number of
                        # possible substrings (pieces) of an epitope (string) of length "index + 1".
                        # Just a measure of quality in matches. Coverage of "a" over an apitope

                        # d2 is the number of pieces of `a`.
                        # n2 is the number of pieces of "a" that did not have any match with epitope (string)
                        # therefore, 1 - n2/d2 is a measure of coverage of epitope matches over "a"
                        d2 = len(set(a))
                        n2 = len(set(a) - set(
                            ["".join(set(b)) for b in matches if len(b) > 0]))  # len(b) filter just matches

                        # render index
                        lengths.append(n1 / d1 + 1 - n2 / d2)

                    check_max_epitopes = []
                    # check if that max value of `length` just belongs to one single epitopes
                    for d in range(len(lengths)):
                        if lengths[d] == max(lengths):
                            check_max_epitopes.append(epitopes[d])

                    # the loop increase the word size till there is only one single max index
                    if len(set(check_max_epitopes)) == 1:

                        page_line = lines[lengths.index(max(lengths))]
                        try:

                            self.accepted_name = re.findall("<i>[A-Z][a-z]+ [a-z]+</i>", page_line)[-1].replace("<i>","").replace("</i>", "")
                            self.aphiaID = re.findall("aphia.php\?p=taxdetails&id=[0-9]+", page_line)[0].replace("aphia.php?p=taxdetails&id=", "")
                        except IndexError:

                            self.accepted_name = ""
                            self.aphiaID = ""
                        break

            return self.accepted_name

        else:
            complete_url = "http://www.marinespecies.org/aphia.php?p=taxdetails&id=" + self.aphiaID

            page = None
            # make sure aphiaID will be available for downstream analyses
            while page is None:
                try:
                    page = urllib.request.urlopen(complete_url).read().decode('utf-8')
                except urllib.error.HTTPError:
                    pass

            if len(re.findall(">unaccepted<", page)) == 1:

                # get down till species name line:
                line = re.findall('id="AcceptedName".*\n.*\n.*\n.*\n.*', page)[0]

                # previously tested:
                # line = re.findall("p=taxdetails&id=(?!" + self.aphiaID + ").*<i>[A-Z][a-z]+ [a-z]+</i>", page)[0]
                # line = re.findall(">Accepted Name<.*p=taxdetails&id=[0-9]+.*></i><i>[A-Z][a-z]+ [a-z ]{1,}</i>",
                #           page.replace("\n", ""))[0]
                # self.accepted_name = re.sub(".*</i><i>(.*)</i>", "\\1", line)

                self.accepted_name = re.sub(".*</i><i>(.*)</i>.*", "\\1", line.replace("\n", ""))

                aphiaID_url = "http://www.marinespecies.org/rest/AphiaIDByName/" + \
                              re.sub(" ", "%20", self.accepted_name) + "?marine_only=false"

                self.aphiaID = None
                # make sure aphiaID will be available for downstream analyses
                while self.aphiaID is None:
                    try:
                        self.aphiaID = urllib.request.urlopen(aphiaID_url).read().decode('utf-8')
                    except urllib.error.HTTPError:
                        pass

                return self.accepted_name

            else:
                self.accepted_name = self.taxon.replace("%20", " ")

                return self.accepted_name

    def taxamatch(self):
        # self = Worms("Schizodon jacuiensis").taxamatch()
        # self = Worms("Theria rupicapraria")
        # self.accepted_name
        # self = Worms("Lubbockia squillimana")
        # self.taxamatch()
        # self = Worms("Synarmadillo tristani")
        # self = Worms("Aega perualis")

        spps = re.sub("\\(.+\\)", "", self.taxon).lower()
        spps = re.sub("[ ]{2,}", " ", spps)
        # spps = self.taxon

        complete_url = "http://www.marinespecies.org/rest/AphiaRecordsByMatchNames?scientificnames%5B%5D=" + \
                       spps + \
                       "&marine_only=false"

        page = urllib.request.urlopen(complete_url).read().decode('utf-8')

        valid_info = re.sub('.*,"valid_AphiaID":(.*),"valid_name":"(.*)","valid_authority":.*', "\\1,\\2", page)
        # valid_name = "Mobula birostris"

        try:
            aphiaid, valid_name = valid_info.split(',')
            self.accepted_name = valid_name
            self.aphiaID = aphiaid

        except ValueError:
            self.accepted_name = ""

        return self.accepted_name

    def get_taxonomic_ranges(self):
        """Name of all valuable ranks are retrieved and stored at self.taxonomic_ranges and
        also complete string of information used to get it at self.classification_page
        """
        if self.aphiaID == '-999' or self.aphiaID == '':
            self.taxamatch()

        if self.aphiaID == '-999' or self.aphiaID == '':
            self.taxonomic_ranges = None

        else:

            complete_url = self.classfication_url + self.aphiaID
            # This while loop is because of classfication page, or classification string, is needed
            # since self.classification_page is not starting with a value,
            # this while loop may not slow down its request
            while self.classification_page == "":
                try:
                    self.classification_page = urllib.request.urlopen(complete_url).read().decode('utf-8')
                except urllib.error.HTTPError:
                    time.sleep(0.5)
                    pass

            # grant with a white space into the pattern can end up as non-smart search, but it is kept anyways
            self.taxonomic_ranges = [re.sub('"rank":"([A-Za-z ]+)"', "\\1", i) for i in
                                     re.findall('"rank":"[A-Za-z ]+"', self.classification_page)]

    def get_rank(self, rank):

        if self.taxonomic_ranges is None:
            return "check_spell"

        if not self.taxonomic_ranges:
            # if there is not a list of ranks for comparing with the rank variable
            # then, get it with the following and store them
            self.get_taxonomic_ranges()

        # since the prior ensures a list of rank's names, rank variable is looked between them
        spell = [i for i in self.taxonomic_ranges if i == rank]

        # if there was not any match, then a "check_spell" is returned
        if len(spell) == 0:
            return "check_spell"

        rankMatch = re.sub('.*"rank":"' +
                           spell[0] +
                           '","scientificname":"([A-Za-z\[\] ]+)".*',
                           "\\1", self.classification_page)

        if re.findall("\[unassigned\]", rankMatch):
            return 'unassigned'
        else:
            return rankMatch

    def get_synonyms(self):
        """
        wrapper for synonyms method of WoRMS API
        """
        # self = Worms("Anchoa nasus")
        # self = Worms("Schizodon jacuiensis")
        # self = Worms("Dasyatis dipterura").get_synonyms()
        # self = Worms("Lubbockia squillimana")
        # pattern1 = "^[A-Z][a-z]+ [a-z]+$"
        if self.aphiaID == '-999' or self.aphiaID == '':
            self.taxamatch()

        if self.aphiaID == '' or self.aphiaID == '-999':
            return "Check your taxon!"

        else:

            complete_url = self.synonym_url + self.aphiaID
            synonym_page = None

            while synonym_page is None:
                try:
                    synonym_page = urllib.request.urlopen(complete_url).read().decode('utf-8')

                except urllib.error.HTTPError:
                    time.sleep(0.5)
                    pass

            pre_syn = re.findall('"scientificname":"[A-Z][a-z]+ [a-z]+"', synonym_page)

            self.synonym_list = [re.sub('"scientificname":"([A-Za-z ]+)"', "\\1", i) for i in pre_syn]

            return self.synonym_list

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
