# script for typing Varicella Zoster Virus
# USAGE: python VZV_typing.py query.fna NC_001348.1.fna
# Where query.fna is a multi-fasta of sequences for which you want to determine the genotype, one fasta entry per sequence allowed
# and NC_001348.1.fna is the reference genome NC_001348.1 in FASTA format


import sys
import subprocess


position_list = [33725, 37902, 38055, 52365, 69424, 98437, 114639]


mafftout = subprocess.check_output("mafft --6merpair --keeplength --addfragments {} {}".format(sys.argv[1], sys.argv[2]), shell=True, stderr=subprocess.PIPE).decode()


clade_dict = {('T', 'A', 'T', 'C', 'G', 'T', 'T'): "Clade 1",
        ('C', 'G', 'C', 'C', 'G', 'C', 'T'): "Clade 2",
        ('C', 'A', 'T', 'C', 'A', 'T', 'T'): "Clade 3",
        ('C', 'A', 'C', 'T', 'G', 'C', 'T'): "Clade 4",
        ('C', 'A', 'T', 'T', 'G', 'T', 'T'): "Clade 5",
        ('C', 'A', 'T', 'C', 'A', 'C', 'C'): "Clade 6",
        ('C', 'A', 'T', 'C', 'G', 'C', 'T'): "Clade VIII",
        ('C', 'A', 'C', 'C', 'A', 'C', 'T'): "Clade 9"}



seqdict = {}
for line in mafftout.split("\n"):
    if line.startswith(">"):
        name = line.split()[0][1:]
        seqdict[name] = ""
    else:
        seqdict[name] += line.rstrip()


sys.stdout.write("\t".join(["Sequence"] + list(map(str, position_list))) + "\tclade\n")
for i in seqdict:
    outlist = [i]
    for num in position_list:
        outlist.append(seqdict[i][num-1].upper())
    profile = tuple(outlist[1:])
    if profile in clade_dict:
        outlist.append(clade_dict[profile])
    else:
        outlist.append("unknown")
    sys.stdout.write("\t".join(outlist) + "\n")
