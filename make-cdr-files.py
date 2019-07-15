# -*- coding: utf-8 -*-

"""

make-cdr-files.py

July 2019, Jamie Heather @ MGH

Goes through FASTA files of the current tag sets, and all CDR1 and CDR2 amino acid files from IMGT
Takes the list and order of genes used and makes a new file combining the CDRs into a fourth output file
That file is used in the generation of the new AIRR seq community format output for the pipeline
    See CDR3translator v 4.0.1

"""

import collections as coll
import os


def read_fa(ff):
    """
    :param ff: opened fasta file
    read_fa(file):Heng Li's Python implementation of his readfq function (tweaked to only bother with fasta)
    https://github.com/lh3/readfq/blob/master/readfq.py
    """

    last = None  # this is a buffer keeping the last unprocessed line
    while True:  # mimic closure; is it a bad idea?
        if not last:  # the first record or a record following a fastq
            for l in ff:  # search for the start of the next record
                if l[0] in '>':  # fasta header line
                    last = l[:-1]  # save this line
                    break
        if not last:
            break
        # name, seqs, last = last[1:].partition(" ")[0], [], None # This version takes everything up to first space
        name, seqs, last = last[1:], [], None  # This version takes the whole line (post '>')
        for l in ff:  # read the sequence
            if l[0] in '>':
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if not last or last[0] != '+':  # this is a fasta record
            yield name, ''.join(seqs), None  # yield a fasta record
            if not last:
                break
        else:
            print "Input file does not appear to be a FASTA file - please check and try again"
            sys.exit()


def nest():
    return coll.defaultdict()


def get_gene(string):
    """
    :param string: a string containing an IMGT gene name - likely a FASTA header, or something derived from it
    :return: the IMGT gene name, bereft of any allele information
    """
    return string.split('|')[1].split('*')[0]


cdrs = coll.defaultdict(nest)

for species in ['human', 'mouse']:
    for chain in ['TRAV', 'TRBV']:
        # First read in the CDR3s
        base = species + '_all_' + chain + '_|s.fasta'
        for cdr in ['cdr1', 'cdr2']:
            file_path = base.replace('|', cdr)
            with open(file_path, 'rU') as in_file:
                for readid, seq, qual in read_fa(in_file):
                    if '*01|' in readid:
                        gene = get_gene(readid)
                        cdrs[cdr][gene] = seq
        # Then read in the tag sets and check which genes are covered
        for tags in ['original', 'extended']:
            file_path = species + '_' + tags + '_' + chain + '.tags'
            if file_path in os.listdir(os.getcwd()):
                print tags, chain
                out_str = []
                out_path = species + '_' + tags + '_' + chain + '.cdrs'
                with open(file_path, 'rU') as in_file, open(out_path, 'w') as out_file:
                    # Find the CDR3s for each gene, in the order they appear in the corresponding tag file
                    for line in in_file:
                        gene = get_gene(line.rstrip().split(' ')[-1]).replace(',', '/')
                        if '/TR' in gene:
                            # If more than two genes present, just take the first one
                            gene = gene.split('/TR')[0]
                        # Ensure there's a value if no listed CDR - accounts for pseudogenes which lack this info
                        for cdr in ['cdr1', 'cdr2']:
                            if gene not in cdrs[cdr]:
                                cdrs[cdr][gene] = 'N/A'
                        out_str.append(' '.join([gene, cdrs['cdr1'][gene], cdrs['cdr2'][gene]]))
                    # Then write those out to a new file
                    out_file.write('\n'.join(out_str))
