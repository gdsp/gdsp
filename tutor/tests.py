#!/usr/bin/python
# -*- coding: latin-1 -*-

import random, copy, subprocess, pdb
import time, inspect, sys, uuid, copy

from tutor.models import Result, History
from os import path
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
    easy(), medium(), hard() and adaptive(), which describes the initial 
    parameter setting. The GuessEffect class is a good starting point."""

    level = None
    FX = None
    user = None

    def __init__(self, level, FX, user):
        print("FX: ", FX)
        if level == 'Hard':
            self.level = self.hard
        if level == 'Medium':
            self.level = self.medium
        if level == 'Easy':
            self.level = self.easy
        if level == 'Adaptive':
            self.level = self.adaptive

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

    def medium(self):
        raise NotImplementedError

    def easy(self):
        raise NotImplementedError

    def adaptive(self):
        raise NotImplementedError

    def _history(self):
        return [ result.correct for result in Result.objects.filter(test = self.name).filter(user = self.user).order_by('pk') ]

    def _consecutive(self, n):
        """ Returns a list, e.g. [-1, 1, 0, 1], which says whether the difficulty should increase or decrease, depending on the n consecutive 
        correct/wrong answers. """
        grouped = zip(*[iter(self._history())]*n)
        results = [0]*len(grouped)
        for i, group in enumerate(grouped):
            if list(group) == [1]*n:
                results[i] = 1
            if list(group) == [0]*n:
                results[i] = -1
        return results

    def _calculate_integer_level(self, n_consecutive, lowest, highest):
        trend = self._consecutive(n_consecutive)
        level = lowest
        for t in trend:
            level = max(lowest, min(highest, level+t))
        return level

    def process(self, effectParameterValues, isInteractive):
        if isInteractive:
            inputSound = path.join(md.systemfiles, 'samples', random.choice(cs.getWavefileNames(md.systemfiles)))
            
            csoundFilename = str(uuid.uuid4()) + '.csd'    
            csoundFilepath = path.join(md.userfiles, csoundFilename)

            # # Store which effects are being used
            # for effect in effectParameterValues.keys():
            #     History.objects.get_or_create(user = self.user, effect = effect)

            #csoundFilename = 'target_effect.inc'

            cs.writeCsoundFileInteractiveParameters(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles)   
            #retcode = subprocess.call(['csound', '-d', csoundFilepath])

        else:
            inputSound = path.join(md.systemfiles, 'samples', random.choice(cs.getWavefileNames(md.systemfiles)))
            csoundFilename = str(uuid.uuid4()) + '.csd'
            csoundNormFilename = 'normalize.' + csoundFilename
    
            csoundFilepath = path.join(md.userfiles, csoundFilename)
            csoundNormFilepath = path.join(md.userfiles, csoundNormFilename)
    
            # Store which effects are being used
            for effect in effectParameterValues.keys():
                History.objects.get_or_create(user = self.user, effect = effect)
                
            cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound.replace('\\','/'))       
            retcode = subprocess.call(['csound', '-d', csoundFilepath])
            if retcode == 0:
                # Change the normalize CSD file.
                normalizeFile = path.join(md.modular, 'normalize.csd')
                subprocess.call('sed s,test,%s, ' % csoundFilepath.replace('\\','/') + normalizeFile + ' > ' + csoundNormFilepath, shell=True)
                retcode = subprocess.call(['csound', csoundNormFilepath])    
            else:
                print 'csound error'
        return path.basename(inputSound), csoundFilename

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
        print '\n\n STORE RESULT LESSON_ID {} \n\n'.format(request.COOKIES['lesson_id'])
        correct = request.POST['answer'] == request.POST['choice']
        result = Result(lesson = request.COOKIES['lesson_id'], test = self.name, correct = correct, user = request.user, csd = request.POST['csd'],
                        cheated = request.POST['cheated'] == 'True')
        result.save()
        return correct

class GuessEffect(TestCode):

    """ This is the simplest example of a testing class. Use this as a
    template, and implement the first() and check() methods."""

    name = 'Guess the effect'
    tags = 'general'

    def easy(self):
        return 2

    def medium(self):
        return 4

    def hard(self):
        return 6

    def adaptive(self):
        """ We examine the entire history of this effect, and look at the trend of corrects. Two corrects in a row yields and increase, 
        two wrongs a decrease. A mix is no change. In the worst case, a student will have done this a couple of thousand times, which 
        should pose no problem to the Django engine. """
        return self._calculate_integer_level(2, self.easy(), self.hard())

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

class InteractiveTest(TestCode):

    name = 'Interactive test'
    tags = 'general'

    def easy(self):
        return 1

    def medium(self):
        return 2

    def hard(self):
        return 3

    def adaptive(self):
        """ We examine the entire history of this effect, and look at the trend of corrects. Two corrects in a row yields and increase, 
        two wrongs a decrease. A mix is no change. In the worst case, a student will have done this a couple of thousand times, which 
        should pose no problem to the Django engine. """
        return self._calculate_integer_level(2, self.easy(), self.hard())

    def first(self):
        random.shuffle(self.FX)
        self.FX = self.FX[0:self.level()]
        effects = [ random.choice(self.FX) ]
        effects = self.FX

        print("level", self.level())
        print("self.FX", self.FX)
        print("effects", effects)

        effectParameterSet = cs.getEffectParameterSet(effects, md.systemfiles)

        # Making a deep copy of the dictionary, because getEffectParameterValues() for some reason is changing it
        effectParameterSetCopy = copy.deepcopy(effectParameterSet)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSetCopy)
        sound, csd = self.process(effectParameterValues, isInteractive = True)

        # Return the csd-file as well as the dry sound file
        return effectParameterSet, effectParameterValues, sound, csd

    def check(self, request, correct):
        return self.first() if correct else self.less_choices(request)

class BandpassMusic(TestCode):

    name = 'Bandpass music'
    tags = 'frequency, filter'

    # Easy and hard returns a random starting frequency, the scaling factor (in each direction) and Q.
    def easy(self):
        return random.randrange(1000, 2000), .75, .609

    def medium(self):
        return random.randrange(800, 3000), .5, .609

    def hard(self):
        return random.randrange(500, 8000), .25, .609

    def adaptive(self):
        trend = self._consecutive(2)
        level = [1000, 2000, .75, .609]
        for t in trend:
            level[0] = min(1000, max(500, level[0]-t*50)) # 10 steps
            level[1] = max(2000, min(8000, level[1]+t*600))
            level[2] = min(.75, max(.25, level[2]-t*.05))
        return random.randrange(level[0], level[1]), level[2], level[3]

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
        csoundNormFilename = 'normalize.' + csoundFilename
        csoundFilepath = path.join(md.userfiles, csoundFilename)
        csoundNormFilepath = path.join(md.userfiles, csoundNormFilename)

        # Store which effects are being used
        for effect in effectParameterValues.keys():
            History.objects.get_or_create(user = self.user, effect = effect)

        cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound)

        retcode = subprocess.call(['csound', '-d', csoundFilepath])
        print retcode
        if retcode == 0:
            # Change the normalize CSD file.
            normalizeFile = path.join(md.modular, 'normalize.csd')
            subprocess.call('sed s,test,%s, ' % csoundFilepath.replace('\\','/') + normalizeFile + ' > ' + csoundNormFilepath, shell=True)
            retcode = subprocess.call(['csound', csoundNormFilepath])
            print '******************************'
            print 'source sound:', inputSound
            print effectParameterValues

        else:
            print 'csound error'

        return path.basename(inputSound), csoundFilename


class SineFrequency(BandpassMusic):

    name = 'Sine'
    tags = 'frequency'

    def process(self, effectParameterValues):
        print 'effectParameterValues', effectParameterValues
        inputSound = 'sine'

        csoundFilename = str(uuid.uuid4()) + '.csd'
        csoundNormFilename = 'normalize.' + csoundFilename
        csoundFilepath = path.join(md.userfiles, csoundFilename)
        csoundNormFilepath = path.join(md.userfiles, csoundNormFilename)

        # Store which effects are being used
        for effect in effectParameterValues.keys():
            History.objects.get_or_create(user = self.user, effect = effect)

        cs.writeCsoundFile(csoundFilename, effectParameterValues, md.systemfiles, md.userfiles, inputSound)

        retcode = subprocess.call(['csound', '-d', csoundFilepath])
        print retcode
        if retcode == 0:
            # Change the normalize CSD file.
            normalizeFile = path.join(md.modular, 'normalize.csd')
            subprocess.call('sed s,test,%s, ' % csoundFilepath.replace('\\','/') + normalizeFile + ' > ' + csoundNormFilepath, shell=True)
            retcode = subprocess.call(['csound', csoundNormFilepath])
            print '******************************'
            print 'source sound:', inputSound
            print effectParameterValues

        else:
            print 'csound error'

        return path.basename(inputSound), csoundFilename

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

    def medium(self):
        return 3

    def hard(self):
        return 4

    def adaptive(self):
        return self._calculate_integer_level(3, self.easy(), self.hard())
    
    def fx(self, num_fx):
        random.shuffle(self.FX)

        exclude = {}
        execfile(path.join(md.systemfiles, 'effects_combination_rules.txt'), exclude)
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

