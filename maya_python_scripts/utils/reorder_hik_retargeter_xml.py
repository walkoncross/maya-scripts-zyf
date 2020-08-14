#!/usr/bin/env python
from __future__ import print_function
import sys
import re


def reorder(fn):
    fp = open(fn, 'r')
    fp2 = open(fn+'.reoreder_keep_all_lines.xml', 'w')
    fp3 = open(fn+'.reoreder_keep_last_line.xml', 'w')

    lines = fp.readlines()
    fp.close()

    fp2.write(lines[0])
    fp2.write(lines[1])

    fp3.write(lines[0])
    fp3.write(lines[1])

    tmp_dict = dict()

    for line in lines[2:-1]:
        match = re.search('body="(\w+)"', line)
        body = match[1]

        if body not in tmp_dict:
            tmp_dict[body] = [line]
        else:
            tmp_dict[body].append(line)

    keys_list = list(tmp_dict.keys())
    print('===> keys_list', keys_list)

    keys_list.sort()
    print('===> sorted keys_list', keys_list)

    for key in keys_list:
        print('===> write key ', key)
        fp3.write(tmp_dict[key][-1])

        for line in tmp_dict[key]:
            fp2.write(line)

    fp2.write(lines[-1])
    fp2.close()

    fp3.write(lines[-1])
    fp3.close()


if __name__ == '__main__':
    reorder(sys.argv[1])
