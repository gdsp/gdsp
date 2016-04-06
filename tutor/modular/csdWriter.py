#!/usr/bin/python
# -*- coding: latin-1 -*-

""" 
A Csound csd writer, automatic generation of DSP listening tests

@author: Øyvind Brandtsegg, Axel Tidemann
@contact: obrandts@gmail.com
@license: GPL
"""

import random 
import os
import re
import copy
import math
import sys
import time

from collections import OrderedDict

def getEffects(path):
    """
    Get a list of the effects include files in the "effects" directory
    
    @param self: The object pointer.
    @return: A list of files in the directory
    """
    files = os.listdir(os.path.join(path,'effects'))
    incfiles = []
    # check that they are valid include file names
    for f in files:
        if len(re.findall('.inc|.INC', f)) > 0:
            incfiles.append(f) 
    return incfiles

def getWavefileNames(path):
    """
    Get a list of the sound files in the "samples" directory
    
    @param self: The object pointer.
    @return: A list of files in the directory
    """
    files = os.listdir(os.path.join(path, 'samples'))
    wavfiles = []
    # check that they are valid wave file names
    for f in files:
        if len(re.findall('.wav|.WAV', f)) > 0:
            wavfiles.append(f) 
    return wavfiles

def getEffectParameterSet(FX, path):
    # find parameter set for the effects we are going to use
    effectParameterSet = OrderedDict()
    numParameters = 0
    # the following get a more robust implementation (regex?), allowing for extra whitespace and other typo variations
    for effect in FX:
        inc = open(os.path.join(path,'effects',effect), 'r')
        capture = 0
        parameters = OrderedDict()
        for line in inc:
            if '*/' in line:
                capture = 0
            if capture == 1:
                if 'input' in line:# it contains the word 'input' so it is a routing line
                    input, output = line.split('input:')[-1].split(' output:')
                    output = output.rstrip('\n')
                elif 'tags' in line:
                    pass #effectParameterSet['tags'] = line.strip().partition('tags:')[-1].split(',')
                else: # not input or tag: parameter (name range map label) line
                    numParameters += 1
                    l = line.split('range')
                    parameter = l[0].split('"')[1]
                    m = l[1].split('map')
                    r = eval(m[0].strip(' ')) # range as tuple
                    if 'lin' in m[1]: mapping = 'lin'
                    elif 'log' in m[1]: mapping = 'log'
                    elif 'log_1p5' in m[1]: mapping = 'log_1p5'
                    elif 'expon' in m[1]: mapping = 'expon'
                    else: mapping = '*undefined*'
                    if 'int' in m[1]: pType = 'int'
                    elif 'float' in m[1]: pType = 'float'
                    else: pType = '*undefined*'

                    rhs = line.split("label")
                    labelText = ""

                    # Get rid of this try-except-block when all inc files are updated with labels
                    try:
                        labelText = rhs[1].split('"')[1]
                    except Exception, e:
                        pass

                    parameterMap = [r, mapping, pType, labelText]
                    parameters[parameter] = parameterMap # save the range, mapping type and parameter type
            if '/* input parameters for this effect' in line:
                capture = 1
        parameters['input'] = input
        parameters['output'] = output
        print input, output
        effectParameterSet[effect] = parameters#, audioInput, audioOutput]
    return effectParameterSet

def getEffectParameterValues(effectParameterSet):
    # find parameter values for the parameter set (for the effects) we are going to use
    timeNow = int(time.time())
    #log = open('/srv/www/gdsp.hf.ntnu.no/tutor/' + str(timeNow) + '.log', 'w')

    effectParameterValues = copy.copy(effectParameterSet) # copy so we don't write to the dict we iterate over
    for effect in effectParameterSet.keys():
        #log.write(str(effect))
        # generate parameter values
        for key, value in effectParameterSet[effect].items():
            #log.write('key:'+str(key)+ ' value:' + str(value))
            if key == 'input':
                pass
            elif key == 'output':
                pass
            else:
                # parse parameterMap (key:parameterName, value:[range, mapping, parameterType, label])
                r, mapping, pType, label = value
                if mapping == 'lin':
                    v = (random.random()*(r[1]-r[0]))+r[0]
                elif mapping == 'expon':
                    ran = random.random()
                    v = (ran*ran*(r[1]-r[0]))+r[0]
                elif mapping == 'log':
                    logMin = math.log(r[0],2)
                    logMax = math.log(r[1],2)
                    ran = random.random()*(logMax-logMin)
                    v = math.pow(2, ran+logMin)
                else: 
                    print 'WARNING:parameter mapping curve for parameter %s undefined'%key
                    #log.write('WARNING:parameter mapping curve for parameter %s undefined'%key)
                if pType == 'int': v = int(round(v))
                else: pass # assume float
                # save parameter value
                effectParameterValues[effect][key] = v
    #log.close()
    return effectParameterValues

def writeCsoundFile(filename, effectParameterValues, systemfiles, userfiles, inputsound):
    # create a file object
    outfilename = filename
    print 'outfilename', outfilename
    f = open(os.path.join(userfiles, outfilename), 'w')
    print 'opened file', outfilename
    #options = '-otest.wav -f'#'-odac -b1024 -B2048'
    # This is done so files with unique names can be created.
    options = '-o%s.wav -f' % os.path.join(userfiles, filename).replace('\\','/') #'-odac -b1024 -B2048'
    
    # write top tags and options
    f.write('''<CsoundSynthesizer>\n<CsOptions>\n%s\n</CsOptions>\n<CsInstruments>'''%options)
    
    # write header
    f.write('\n\n')
    inc = open(systemfiles + '/general/header.inc', 'r')
    for line in inc:
        f.write(line)
    inc.close()
    
    ###########################
    # autogenerate DSP code
    ###########################
    
    f.write('\n;*****************************************************\n')
    f.write('instr	1 \n')
    f.write(';*****************************************************\n\n')
    f.write('\tiamp \t\t= ampdbfs(-0) \n\n')

    # sound generator
    print 'inputsound', inputsound
    f.write('\n;****************sound generator***********************\n')
    if inputsound == 'sine':
        freq = effectParameterValues['bandpass.inc']['kCutoff']
        f.write('\ta1 \t\toscili 0.7, %f, giSine \n'%freq)
        f.write('\tilen \t\t= 4 \n')
    elif inputsound == 'noise':
        f.write('\ta1 \t\trnd31 1, 1 \n')
        f.write('\tilen \t\t= 4 \n')
    else:
        f.write('\ta1 \t\tdiskin "%s", 1, 0, 1 \n'%inputsound)
        f.write('\tilen \t\tfilelen "%s" \n'%inputsound)
        f.write('\tp3 \t\t= ilen \n\n')    
    f.write(';*** generate event for the effects processing instr ***\n')
    f.write('\t\t\tevent_i "i", 9, 0, p3+30\n\n')
    currentSignalType = 'mono'
    
    # send signal on chn
    inc = open(os.path.join(systemfiles, 'general','chn_send_mono.inc'), 'r')
    if currentSignalType == 'stereo':
        inc = open(os.path.join(systemfiles, 'general','chn_send_stereo.inc'), 'r')
    for line in inc:
        f.write(line)
    f.write('\n')
    f.write('endin\n')
    
    # effects instrument
    f.write('\n;*****************************************************\n')
    f.write('instr	9 \n')
    f.write(';*****************************************************\n\n')
    f.write('\tiamp \t\t= 1 \n\n')
    
    # read audio on chn channel(s)
    inc = open(os.path.join(systemfiles, 'general','chn_read_mono.inc'), 'r')
    if currentSignalType == 'stereo':
        inc = open(os.path.join(systemfiles, 'general','chn_send_stereo.inc'), 'r')
    for line in inc:
        f.write(line)
    f.write('\n')
        
    # effects
    for effect in effectParameterValues.keys():
        f.write('\n;****************effect: %s ********************************\n'%effect[:-4])
        # read parameter values and audio routing
        for key,value in effectParameterValues[effect].items():
            if key == 'input':
                audioInput = value
            elif key == 'output':
                audioOutput = value
            else:
                s = '\t'+key+'     \t= '+ str(value) + '\n'
                f.write(s)

        # insert effect code
        if 'mono' in currentSignalType:
            if audioInput == 'stereo':
                f.write('\ta2 \t\t= a1\n')  #split mono input into two identical signals
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            currentSignalType = audioOutput

        else: # current signal type is stereo

            # dual mono
            if ('mono' in audioInput) and ('mono' in audioOutput):
                # process first signal channel and write it temporarily to a1out
                inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
                capture = 0 # skip writing the first parts of include files (meta information)
                for line in inc:
                    if capture == 1:
                        f.write(line)
                    if '*/' in line:
                        capture = 1
                inc.close()
                f.write('\n')
                f.write('\ta1out \t\t= a1\n')  #save output to temporary signal a1out
                # process second signal 
                f.write('\ta1 \t\t= a2\n')  #read the second signal
                inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
                capture = 0 # skip writing the first parts of include files (meta information)
                for line in inc:
                    if capture == 1:
                        f.write(line)
                    if '*/' in line:
                        capture = 1
                inc.close()
                f.write('\n')
                f.write('\ta2 \t\t= a1\n')  #save output from second channel to a2
                f.write('\ta1 \t\t= a1out\n')  #restore a1 from temporary storage a1out
    
            # in a stereo signal chain, using a 'mono-input-to-stereo-output' effect
            # we want to preserve the input stereo image so use two separate instances of the effect
            # we will pan the (four) outputs equally across the output stereo image
            if ('mono' in audioInput) and ('stereo' in audioOutput):
                f.write('\ta2in \t\t= a2\n')  #save input on second channel temporarily to a2in
                # process first channel
                inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
                capture = 0 # skip writing the first parts of include files (meta information)
                for line in inc:
                    if capture == 1:
                        f.write(line)
                    if '*/' in line:
                        capture = 1
                inc.close()
                f.write('\n')
                f.write('\ta1_1 \t\t= a1\n')  #save output from first channel to a1_1
                f.write('\ta2_1 \t\t= a2\n')  #save output from second channel to a2_1
                # process second channel
                f.write('\ta1 \t\t= a2in\n')  #restore input on second channel from temporary storage in a2in
                inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
                capture = 0 # skip writing the first parts of include files (meta information)
                for line in inc:
                    if capture == 1:
                        f.write(line)
                    if '*/' in line:
                        capture = 1
                inc.close()
                f.write('\n')
                #pan and output
                f.write('\ta1 \t\t= a1_1+(a1*sqrt(0.33))+(a2_1*sqrt(0.66))\n') 
                f.write('\ta2 \t\t= a2+(a1*sqrt(0.66))+(a2_1*sqrt(0.33))\n')
                
            # normal stereo effect
            if ('stereo' in audioInput) and ('stereo' in audioOutput):
                inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
                capture = 0 # skip writing the first parts of include files (meta information)
                for line in inc:
                    if capture == 1:
                        f.write(line)
                    if '*/' in line:
                        capture = 1
                inc.close()
                f.write('\n')
                        
    #sound output
    f.write('\n;****************output********************************\n')
    incfile = 'out_mono.inc'
    if currentSignalType == 'stereo':
        incfile = 'out_stereo.inc'
    print 'output is', currentSignalType
    inc = open(os.path.join(systemfiles, 'general',incfile), 'r')
    for line in inc:
        f.write(line)
    f.write('\n')
    
    inc.close()
    
    f.write('endin \n\n')
    
    # set score
    score = 'i 1 0 1\ne'
    
    # write closing tags and score
    f.write('</CsInstruments>\n<CsScore>\n%s\n</CsScore>\n</CsoundSynthesizer>' %score)
    
    # close the file
    f.close
    return 0


def writeCsoundFileInteractiveParameters(filename, effectParameterValues, systemfiles, userfiles):
    
    # Create file object
    outfilename = filename
    f = open(os.path.join(userfiles, outfilename), 'w')
    print 'opened file', outfilename

    # Top tags and options
    f.write("<CsoundSynthesizer>\n<CsOptions>\n-odac -W -d -b1024 -B2048\n</CsOptions>\n<CsInstruments>")

    # Header
    f.write('\n\n')
    inc = open(systemfiles + '/general/interactive_header.inc', 'r')
    for line in inc:
        f.write(line)
    inc.close()
    
    # Input channel, target (instr 1)
    inc = open(systemfiles + '/general/interactive_input_target.inc', 'r')
    for line in inc:
        f.write(line)
    inc.close()

    # Input channel, user (instr 2)
    f.write('\n\n')
    inc = open(systemfiles + '/general/interactive_input_user.inc', 'r')
    for line in inc:
        f.write(line)
    inc.close()


    # Start at instrument 100 and increase number programmatically based on number of effects
    # Corresponding user_instr will always be target_instr + 100 
    instrumentNumber = 100

    # Initialize an empty string which will start all appended instruments in CsScore
    csScore = ""

    # Generate target effect code
    for effect in effectParameterValues.keys():
        
        f.write("\n;******************************** Effect: %s ********************************\n"%effect[:-4])
        f.write("instr {}\n\n".format(instrumentNumber))

        # read parameter values and audio routing
        for key, value in effectParameterValues[effect].items():
            if key == 'input':
                audioInput = value
            elif key == 'output':
                audioOutput = value
            else:
                s = '\t'+key+'     \t= '+ str(value) + '\n'
                f.write(s)

        f.write("a1 chnget \"target_audio_left\"\n")
        f.write("a2 chnget \"target_audio_right\"\n")

        # dual mono
        if ('mono' in audioInput) and ('mono' in audioOutput):
            # process first signal channel and write it temporarily to a1out
            inc = open(os.path.join(systemfiles, 'effects', effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta1out \t\t= a1\n')  #save output to temporary signal a1out
            # process second signal 
            f.write('\ta1 \t\t= a2\n')  #read the second signal
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta2 \t\t= a1\n')  #save output from second channel to a2
            f.write('\ta1 \t\t= a1out\n')  #restore a1 from temporary storage a1out
    
        # in a stereo signal chain, using a 'mono-input-to-stereo-output' effect
        # we want to preserve the input stereo image so use two separate instances of the effect
        # we will pan the (four) outputs equally across the output stereo image
        if ('mono' in audioInput) and ('stereo' in audioOutput):
            f.write('\ta2in \t\t= a2\n')  #save input on second channel temporarily to a2in
            # process first channel
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta1_1 \t\t= a1\n')  #save output from first channel to a1_1
            f.write('\ta2_1 \t\t= a2\n')  #save output from second channel to a2_1
            # process second channel
            f.write('\ta1 \t\t= a2in\n')  #restore input on second channel from temporary storage in a2in
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            #pan and output
            f.write('\ta1 \t\t= a1_1+(a1*sqrt(0.33))+(a2_1*sqrt(0.66))\n') 
            f.write('\ta2 \t\t= a2+(a1*sqrt(0.66))+(a2_1*sqrt(0.33))\n')
            
        # normal stereo effect
        if ('stereo' in audioInput) and ('stereo' in audioOutput):
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')

        f.write("chnset a1, \"target_audio_left\"\n")
        f.write("chnset a2, \"target_audio_right\"\n")

        f.write("\nendin\n")
        csScore += "i{} 0 999999999\n".format(instrumentNumber)
        instrumentNumber += 10


    instrumentNumber = 200

    # Generate user effect code
    for effect in effectParameterValues.keys():
        
        effect_name = effect[:-4]

        f.write("\n;******************************** Effect: %s ********************************\n"%effect_name)
        f.write("instr {}\n\n".format(instrumentNumber))

        # read parameter values and audio routing
        for key, value in effectParameterValues[effect].items():
            if key == 'input':
                audioInput = value
            elif key == 'output':
                audioOutput = value
            else:
                #s = '\t'+key+'     \t= '+ str(value) + '\n'
                s = "{} \tchnget \"{}\"\n".format(key, effect_name + "_" + key)
                f.write(s)

        f.write("\na1 chnget \"user_audio_left\"\n")
        f.write("a2 chnget \"user_audio_right\"\n")

        # dual mono
        if ('mono' in audioInput) and ('mono' in audioOutput):
            # process first signal channel and write it temporarily to a1out
            inc = open(os.path.join(systemfiles, 'effects', effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta1out \t\t= a1\n')  #save output to temporary signal a1out
            # process second signal 
            f.write('\ta1 \t\t= a2\n')  #read the second signal
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta2 \t\t= a1\n')  #save output from second channel to a2
            f.write('\ta1 \t\t= a1out\n')  #restore a1 from temporary storage a1out
    
        # in a stereo signal chain, using a 'mono-input-to-stereo-output' effect
        # we want to preserve the input stereo image so use two separate instances of the effect
        # we will pan the (four) outputs equally across the output stereo image
        if ('mono' in audioInput) and ('stereo' in audioOutput):
            f.write('\ta2in \t\t= a2\n')  #save input on second channel temporarily to a2in
            # process first channel
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            f.write('\ta1_1 \t\t= a1\n')  #save output from first channel to a1_1
            f.write('\ta2_1 \t\t= a2\n')  #save output from second channel to a2_1
            # process second channel
            f.write('\ta1 \t\t= a2in\n')  #restore input on second channel from temporary storage in a2in
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')
            #pan and output
            f.write('\ta1 \t\t= a1_1+(a1*sqrt(0.33))+(a2_1*sqrt(0.66))\n') 
            f.write('\ta2 \t\t= a2+(a1*sqrt(0.66))+(a2_1*sqrt(0.33))\n')
            
        # normal stereo effect
        if ('stereo' in audioInput) and ('stereo' in audioOutput):
            inc = open(os.path.join(systemfiles, 'effects',effect), 'r')
            capture = 0 # skip writing the first parts of include files (meta information)
            for line in inc:
                if capture == 1:
                    f.write(line)
                if '*/' in line:
                    capture = 1
            inc.close()
            f.write('\n')

        f.write("chnset a1, \"user_audio_left\"\n")
        f.write("chnset a2, \"user_audio_right\"\n")

        f.write("\nendin\n")
        csScore += "i{} 0 999999999\n".format(instrumentNumber)
        instrumentNumber += 10

    # Master channel (instr 999)
    f.write('\n\n')
    inc = open(systemfiles + '/general/interactive_master.inc', 'r')
    for line in inc:
        f.write(line)
    inc.close()
    
    # Closing tags and score
    f.write("</CsInstruments>\n<CsScore>\n{}i999 0 999999999\n</CsScore>\n</CsoundSynthesizer>".format(csScore))
    
    f.close
    return 0


if __name__ == '__main__':
    path = sys.argv[1]
    print path
    csoundFilename = 'target_effect.inc'
    effectprocessors = getEffects(path) # list of available effects    
    #effectprocessors = ['reverbsc.inc', 'freeverb.inc'] # Temporarily only using reverbsc

    numEffects = 2 # adjust difficulty: number of simultaneous effects (only used for random selection, not used if we specify a list of effects)
    effects = [] # list to hold the effects we will use in this test (empty list will be filled with randomly chosen effects)
    try: 
        effectArg = sys.argv[2] # try to get effects list (or number of random effects) from command line input
        effectArg = eval(effectArg) # convert from string input to python list or int
        if type(effectArg) is int: # but if the argument is an int, use it to set the number of (random) effects to use
            numEffects = effectArg
        elif type(effectArg) is list:
            effects = effectArg # please note that effect names must 
                                #   - must refer to effects include file names e.g. 'downsample.inc'
                                #   - a list can not contain spaces in this context, e.g. 
                                #       ['downsample.inc','pvsblur.inc'] will work 
                                #       ['downsample.inc', 'pvsblur.inc'] will not work
        else: pass
    except: 
        pass
    if effects == []:
        i = 0
        while i < numEffects:
            newEffect = random.choice(effectprocessors)
            effects.append(newEffect)
            effectprocessors.remove(newEffect) # prevent more than one instance of the same effect
            i += 1

    effectParameterSet = getEffectParameterSet(effects, path) # get list of effect parameters for the chosen effects
    effectParameterValues = getEffectParameterValues(effectParameterSet) #get values for the effect parameters
    inputsound = os.path.join(path,'samples',random.choice(getWavefileNames(path)))
    retCode = writeCsoundFileInteractiveParameters(csoundFilename, effectParameterValues, path, path)
    
    '''
    print '*******************'
    print effectParameterSet
    print '*******************'
    print effectParameterValues
    print '*******************'
    
    print "RETCODE:"
    print retCode
    
    import subprocess
    retcode = subprocess.call(['csound', csoundFilename])
    print "RETCODE:"
    print retcode
    if retcode == 0:
        retcode = subprocess.call(['csound', 'normalize.csd'])
        print retcode
        print '******************************'
        print 'source sound:', inputsound
        print 'effects used:', effects
    else:
        print 'csound error'
    '''

