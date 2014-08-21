#!/usr/bin/python
# -*- coding: latin-1 -*-

import random, copy, subprocess, pdb
import time, inspect, sys, uuid

from tutor.models import Result, History
import modular_path as md
import csdWriter as cs

def find_subclasses(module, clazz):
    return [ cls for name, cls in inspect.getmembers(module)
             if inspect.isclass(cls) and issubclass(cls, clazz) and not cls is clazz]

def find_tests():
    return find_subclasses(sys.modules[__name__], TestCode)

def find(name, level, FX, user):
    for test in find_tests():
        if test.name == name:
            return test(level, FX, user)

def find_tags():
    tags = ''
    for test in find_tests():
        tags += test.tags + ','
    return list(set(tags[:-1].split(',')))

def find_tagged_tests():
    return [ [tag, [ test.name for test in find_tests() if tag in test.tags ]]
             for tag in find_tags() ]

def find_inc_files():
    return sorted(cs.getEffects(md.systemfiles))

class TestCode(object):

    """ The base class for writing tests. All tests must subclass this
    class, since the system searches subclasses of this class and
    loads them dynamically. Every subclass must implement first(), check(),
    easy() and hard(), which describes the initial parameter setting.
    The GuessEffect class is a good starting point."""

    level = None
    FX = None
    user = None

    def __init__(self, level, FX, user):
        if level == 'Hard':
            self.level = self.hard
        if level == 'Easy':
            self.level = self.easy

        if FX == 'ALL FX':
            self.FX = cs.getEffects(md.systemfiles)
        elif FX == 'Effects the student has seen so far':
            self.FX = [ history.effect for history in History.objects.filter(user = user) ]
        else:
            self.FX = FX.split(' ')

        self.user = user

    def first(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def hard(self):
        raise NotImplementedError

    def easy(self):
        raise NotImplementedError

    def process(self, effectParameterValues):
        inputSound = md.systemfiles + '/samples/' + random.choice(cs.getWavefileNames(md.systemfiles))
        csoundFilename = str(uuid.uuid4()) + '.csd'

        # Store which effects are being used
        for effect in effectParameterValues.keys():
            History.objects.get_or_create(user = self.user, effect = effect)
            
        cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound)

        retcode = subprocess.call(['csound', '-d', md.userfiles + '/' + csoundFilename])
        print retcode
        if retcode == 0:
            # Change the normalize CSD file.
            userfile = md.userfiles + '/' + csoundFilename
            subprocess.call('sed s,test,%s, ' % userfile + md.modular + '/normalize.csd >' + md.userfiles + '/normalize.%s' % csoundFilename, shell=True)
            retcode = subprocess.call(['csound', md.userfiles + '/normalize.%s' % csoundFilename ])
            print '******************************'
            print 'source sound:', inputSound
            print effectParameterValues

        else:
            print 'csound error'

        return inputSound.rsplit('/')[-1], csoundFilename

    def diminish_choices(self, request):
        fxs = []
        i = 1 # Because the template iterator starts at 1. Sick.
        while True:
            try:
                # We do not append the previous answer.
                if request.POST['alternative' + str(i)] != request.POST['choice']:
                    fxs.append(request.POST['alternative' + str(i)])
                i += 1
            except:
                break
        return fxs

    def less_choices(self, request):
        return request.POST['answer'], self.diminish_choices(request), request.POST['sound'], request.POST['csd']

    def store_result(self, request):
	correct = request.POST['answer'] == request.POST['choice']
        result = Result(test = self.name, correct = correct, user = request.user, csd = request.POST['csd'],
                        cheated = request.POST['cheated'] == 'True')
        result.save()
        return correct

class GuessEffect(TestCode):

    """ This is the simplest example of a testing class. Use this as a
    template, and implement the first() and check() methods."""

    name = 'Guess the effect'
    tags = 'general'

    def easy(self):
        return 3

    def hard(self):
        return 6

    def first(self):

        random.shuffle(self.FX)
        self.FX = self.FX[0:self.level()]

        effects = [ random.choice(self.FX) ]

        effectParameterSet = cs.getEffectParameterSet(effects, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)

        sound, csd = self.process(effectParameterValues)

        return effects[0], self.FX, sound, csd

    def check(self, request, correct):
        return self.first() if correct else self.less_choices(request)

class BandpassMusic(TestCode):

    name = 'Bandpass music'
    tags = 'frequency, filter'

    # Easy and hard returns a random starting frequency, the scaling factor (in each direction) and Q.
    def easy(self):
        return random.randrange(1000, 2000), .75, .609

    def hard(self):
        return random.randrange(500, 8000), .25, .609

    def shuffle_fxs(self, freq, scaling):
        fxs = [ int(freq*(1/(1+scaling))), freq, int(freq*(1+scaling)) ]
        return fxs, fxs[random.randrange(3)]

    def first(self):
        freq, scaling, Q = self.level()
        fxs, answer = self.shuffle_fxs(freq, scaling)
        sound, csd = self.filter_effect(answer, Q)
	print 'first', answer, fxs, sound, csd
        return answer, fxs, sound, csd

    def check(self, request, correct):
        if correct:
            # Simple solution: walk up to 50% in each direction, randomly.
            freq = int(int(request.POST['answer'])*random.choice([0.67, 0.71, 0.77, 1.3, 1.4, 1.5]))
            x, scaling, Q = self.level()
            if (freq > 12000) or (freq < 50):
                freq = x # reset to randrange if out of range
            fxs, answer = self.shuffle_fxs(freq, scaling)
            sound, csd = self.filter_effect(answer, Q)
        
            return answer, fxs, sound, csd
        else:
            return self.less_choices(request)
    
    def filter_effect(self, freq, Q):
        self.FX = ['bandpass.inc']
        effectParameterSet = cs.getEffectParameterSet(self.FX, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)

        effectParameterValues[self.FX[0]]['kCutoff'] = freq
        effectParameterValues[self.FX[0]]['kBW'] = Q

        return self.process(effectParameterValues)

class BandpassNoise(BandpassMusic):

    name = 'Bandpass Noise'
    tags = 'frequency, filter'

    def process(self, effectParameterValues):
        print 'effectParameterValues', effectParameterValues
        inputSound = 'noise'
        csoundFilename = str(uuid.uuid4()) + '.csd'

        # Store which effects are being used
        for effect in effectParameterValues.keys():
            History.objects.get_or_create(user = self.user, effect = effect)

        cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound)

        retcode = subprocess.call(['csound', '-d', md.userfiles + '/' + csoundFilename])
        print retcode
        if retcode == 0:
            # Change the normalize CSD file.
            userfile = md.userfiles + '/' + csoundFilename
            subprocess.call('sed s,test,%s, ' % userfile + md.modular + '/normalize.csd >' + md.userfiles + '/normalize.%s' % csoundFilename, shell=True)
            retcode = subprocess.call(['csound', md.userfiles + '/normalize.%s' % csoundFilename ])
            print '******************************'
            print 'source sound:', inputSound
            print effectParameterValues

        else:
            print 'csound error'

        return inputSound.rsplit('/')[-1], csoundFilename


class SineFrequency(BandpassMusic):

    name = 'Sine'
    tags = 'frequency'

    def process(self, effectParameterValues):
        print 'effectParameterValues', effectParameterValues
        inputSound = 'sine'
        csoundFilename = str(uuid.uuid4()) + '.csd'

        # Store which effects are being used
        for effect in effectParameterValues.keys():
            History.objects.get_or_create(user = self.user, effect = effect)

        cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound)

        retcode = subprocess.call(['csound', '-d', md.userfiles + '/' + csoundFilename])
        print retcode
        if retcode == 0:
            # Change the normalize CSD file.
            userfile = md.userfiles + '/' + csoundFilename
            subprocess.call('sed s,test,%s, ' % userfile + md.modular + '/normalize.csd >' + md.userfiles + '/normalize.%s' % csoundFilename, shell=True)
            retcode = subprocess.call(['csound', md.userfiles + '/normalize.%s' % csoundFilename ])
            print '******************************'
            print 'source sound:', inputSound
            print effectParameterValues

        else:
            print 'csound error'

        return inputSound.rsplit('/')[-1], csoundFilename

class ReverbTimeAndMix(TestCode):

    name = 'Reverb Time and Mix'
    tags = 'reverb'

    def __init__(self, level, FX, user):
        if level == 'Hard':
            self.level = self.hard
        if level == 'Easy':
            self.level = self.easy

        self.FX = ['freeverb_time.inc']
	self.parameters = [(2.5, 0.7)] # alternatives for time and mix
        self.user = user

    # Easy and hard returns a [time, mixrando] parameter set, and the scaling factor (in each direction).
    def easy(self):
	self.parameters = [(0.9, 0.8), (1.8, 0.5), (2.5, 0.4), (4.0, 0.3)]
	scaling = 0.5
        return scaling

    def hard(self):	
	self.parameters = [(0.7, 0.9), (0.9, 0.8), (1.2, 0.5), 
                           (1.3, 0.45), (1.6, 0.4), (1.9, 0.4), 
                           (2.2, 0.4), (2.5, 0.4), (3.0, 0.35), 
                           (3.5, 0.2), (4.0, 0.15)]        
	scaling = 0.2
	return scaling

    def shuffle_fxs(self, parms, scaling):
	time1 = round(parms[0]*(1-scaling),1)
	if time1 < 0.6: time1 = 0.6
	mix1 = round(parms[1]*(1-scaling),1)
	if mix1 < 0.1: mix1 = 0.1
	time3 = round(parms[0]*(1+scaling),1)
	if time3 > 8.0: time3 = 8.0
	mix3 =round(parms[1]*(1+scaling),1)
	if mix3 > 1.0: mix3 = 1.0
        fxs = [ (time1, mix1), 
                parms, 
                (time3,mix3) ]
        return fxs, fxs[random.randrange(3)]

    def first(self):
        scaling = self.level()
	parms = random.choice(self.parameters)
        fxs, answer = self.shuffle_fxs(parms, scaling)
        sound, csd = self.reverb_effect(answer)
	print 'reverb_first', answer, fxs, sound, csd
        return answer, fxs, sound, csd

    def check(self, request, correct):
        if correct:
	    parms = random.choice(self.parameters)
            scaling = self.level()
            fxs, answer = self.shuffle_fxs(parms, scaling)
            sound, csd = self.reverb_effect(answer)
        
            return answer, fxs, sound, csd
        else:
            return self.less_choices(request)
    
    def reverb_effect(self, answer):        
	effectParameterSet = cs.getEffectParameterSet(self.FX, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)
	print 'effectParameterValues', effectParameterValues
        effectParameterValues[self.FX[0]]['kRevTime'] = answer[0]
        effectParameterValues[self.FX[0]]['kmix'] = answer[1]
        effectParameterValues[self.FX[0]]['kHFDamp'] = 0.5
	print 'effectParameterValues', effectParameterValues

        return self.process(effectParameterValues)

class Pan(TestCode):

    name = 'Stereo pan'
    tags = 'pan'

    def __init__(self, level, FX, user):
        if level == 'Hard':
            self.level = self.hard
        if level == 'Easy':
            self.level = self.easy

        self.FX = ['pan.inc']
	self.parameters = [0.5] # init
        self.user = user

    # Easy and hard returns a set of possible parameter values, and the scaling factor (in each direction).
    def easy(self):
	self.parameters = [0.25, 0.5, 0.75] #not including the extremes, because an offset alternative is added
	offset = 0.25 # ...so e.g. the alternative is 0.75 +/- 0.25 = [0.5, 0.75, 1.0]
        return offset

    def hard(self):	
	self.parameters = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # not including the extremes (see easy())
	offset = 0.1
	return offset

    def shuffle_fxs(self, parms, offset):
	fxs = [ parms-offset, parms, parms+offset]
        return fxs, fxs[random.randrange(3)]

    def first(self):
        offset = self.level()
	parms = random.choice(self.parameters)
        fxs, answer = self.shuffle_fxs(parms, offset)
        sound, csd = self.pan_effect(answer)
        return answer, fxs, sound, csd

    def check(self, request, correct):
        if correct:
	    parms = random.choice(self.parameters)
            offset = self.level()
            fxs, answer = self.shuffle_fxs(parms, offset)
            sound, csd = self.pan_effect(answer)
            return answer, fxs, sound, csd
        else:
            return self.less_choices(request)
    
    def pan_effect(self, answer):        
	effectParameterSet = cs.getEffectParameterSet(self.FX, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)
	print 'effectParameterValues', effectParameterValues
	print 'one', self.FX, answer
        effectParameterValues[self.FX[0]]['kPan'] = answer
	print 'effectParameterValues', effectParameterValues
	print 'two'
        return self.process(effectParameterValues)

class Combinations(TestCode):

    name = 'Combination of effects'
    tags = 'combination,general'

    def easy(self):
        return 2

    def hard(self):
        return 4
    
    def fx(self, num_fx):
        random.shuffle(self.FX)

        exclude = {}
        execfile(md.systemfiles + '/effects_combination_rules.txt', exclude)
        for e in exclude:
            if '__' not in e: # We exclude __builtins__ and __doc__
                try:
                    indexes = [ self.FX.index(effect) for effect in exclude[e] ]
                except:
                    continue
                exclude[e].pop(indexes.index(min(indexes)))
                for remove_effect in exclude[e]:
                    self.FX.remove(remove_effect)

        effects = self.FX[0:num_fx]
        effectParameterSet = cs.getEffectParameterSet(effects, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)

        return effects, self.FX, self.process(effectParameterValues)

    def multiple_fx(self, num_fx):
        answer, all_fx, (sound, csd) = self.fx(num_fx)
        answer = '+'.join(answer)

        fxs = [ answer ]
        # We want there to be 4 alternatives (remember answer is included)
        for i in range(4):
            random.shuffle(all_fx)
            fxs.append('+'.join(all_fx[0:num_fx]))

        # Shuffle the list again, so the correct answer won't be the first element
        random.shuffle(fxs)

        return answer, fxs, sound, csd

    def first(self):
        return self.multiple_fx(self.level())

    def check(self, request, correct):
        if correct:
            # Increase the number of effects. This number you will know from the length of the answer list.
            num_fx = len( request.POST['answer'].split('+') )

            # Also, the number of tries is known from the alternative entries in the request.POST. So we diminish choices.
            remainders = len(self.diminish_choices(request))
            if remainders == 4:
                num_fx += 1
            elif remainders == 0:
                num_fx -= 1

            return self.multiple_fx(num_fx)
        else:
            return self.less_choices(request)

