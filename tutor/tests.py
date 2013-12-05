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

class Filter(TestCode):

    name = 'General filter'
    tags = 'filter'

    # Easy and hard returns a random starting frequency, the scaling factor (in each direction) and Q.
    def easy(self):
        return random.randrange(1000, 2000), .75, .609

    def hard(self):
        return random.randrange(500, 8000), .25, .609

    def shuffle_fxs(self, freq, scaling):
        fxs = [ int(freq*(1-scaling)), freq, int(freq*(1+scaling)) ]
        return fxs, fxs[random.randrange(3)]

    def first(self):
        freq, scaling, Q = self.level()
        fxs, answer = self.shuffle_fxs(freq, scaling)
        sound, csd = self.filter_effect(answer, Q)
        return answer, fxs, sound, csd

    def check(self, request, correct):
        if correct:
            # Simple solution: walk 50% in each direction, randomly.
            freq = int(int(request.POST['answer'])*random.choice([0.5, 1.5]))
            _, scaling, Q = self.level()
            fxs, answer = self.shuffle_fxs(freq, scaling)
            sound, csd = self.filter_effect(answer, Q)
        
            return answer, fxs, sound, csd
        else:
            return self.less_choices(request)
    
    def filter_effect(self, freq, Q):
        effectParameterSet = cs.getEffectParameterSet(self.FX, md.systemfiles)
        effectParameterValues = cs.getEffectParameterValues(effectParameterSet)

        effectParameterValues[self.FX[0]]['kCutoff'] = freq
        effectParameterValues[self.FX[0]]['kBW'] = Q

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

