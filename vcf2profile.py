

if len(sys.argv) < 3:
    print('''
vcf2profile.py
Turn a VCF file into a profile for use with grapetree.

USAGE: python vcf2profile.py <input.vcf> <output.profile>

''')


import sys
outlist = []
newheader = ["GENOME"]

with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as o:
    for line in f:
        if line.startswith("##"):
            pass
        elif line.startswith("#"):
            header = line.split()
            for i in header[9:]:
                outlist.append(i)
        else:
            splitline = line.split()
            if splitline[6] != "PASS":
                continue
            newheader.append("LOCUS_" + splitline[1])
            for num, i in enumerate(splitline[9:]):
                if i == "0":
                   x = "5"
                else:
                   x = i
                outlist[num].append(x)


    o.write("\t".join(newheader) + "\n")
    for i in outlist:
        o.write("\t".join(i) + "\n")
