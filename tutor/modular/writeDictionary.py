#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import re
f = open('effectsDict.txt', 'w')
f.write('effectsDict={')

def getEffects():
    files = os.listdir('effects')
    incfiles = []
    # check that they are valid include file names
    for f in files:
        if len(re.findall('.inc|.INC', f)) > 0:
            incfiles.append(f) 
    return incfiles

for file in getEffects():
    f.write(file+': ,\n')
f.write('}')
f.close()    