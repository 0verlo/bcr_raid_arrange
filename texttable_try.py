#!/usr/bin/env python3
# coding=utf-8

from texttable import Texttable
print("hello")

table = Texttable()
table.set_deco(Texttable.HEADER)

s0 = "A1"
s1 = "就发啦可视对讲额我只"
s2 = "e打机啊ifo1"
s3 = "e打机啊ifo11111111111111111"
s4 = "e打机啊ifo2"
s5 = "e打机啊ifo3"
s6 = "e打机啊ifo4"

l1 = [s0,s1,s2,s1,s5]
l2 = ["",s3,s6,s4,s5]
l3 = ["",s1,s3,s2,s5]
l4 = ["",s1,s1,s3,s5]
l5 = ["",s1,s1,s5,s3]
#l1 = [s0,s1]
#l2 = [s0,s1]
cols_dtype = []
cols_align = []
for _str in l1:
    cols_dtype.append('a')
    cols_align.append('l')
table.set_cols_dtype(cols_dtype)
table.set_cols_align(cols_align)
table.set_header_align(cols_align)
table.set_cols_width([5,30,30,30,30])

print([l1,l2])
table.add_rows([l1,l2,l3,l4,l5])

print (table.draw())
