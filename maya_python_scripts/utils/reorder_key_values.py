#!/usr/bin/env python
import sys


def reorder(fn):
    fp=open(fn, 'r')
    fp2=open(fn+'.reoreder.xml', 'w')

    for line in fp:
        spl_0=line.split('<')
        if spl_0[1].startswith('item'):
            spl_1=spl_0[1].split(' ')
            if spl_1[1].startswith('value'):
                spl_2=spl_1[-1].split('/')
                fp2.write(spl_0[0] + '<' + (' '.join([spl_1[0], spl_2[0], spl_1[1]]))+'/>\n')
            else:
                fp2.write(line)
        else:
            fp2.write(line)

    fp.close()
    fp2.close()


if __name__=='__main__':
    reorder(sys.argv[1])
