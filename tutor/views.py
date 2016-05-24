import sys, pdb, random, inspect, urllib
import cPickle as pickle

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url

from tutor.models import Result
import tests
import modular_path as md
from core.models import TestElement

def test(request, test_name, level, FX):
    path = request.META.get('HTTP_REFERER', '') # No elegant way to extract Lesson ID, we must find it by regexing this.
    key = 'lessons/' # If the URLs themselves change, this is where to correct it. Hairy.
    
    if key in path:
        path = path[path.find(key) + len(key):]
        lesson_id = path[:path.find('/')]
        request.COOKIES['lesson_id'] = lesson_id

    print("request.COOKIES['lesson_id']: ", request.COOKIES['lesson_id'])
    context = {}
    context['test_name'] = test_name
    context['level'] = level
    context['FX'] = FX

    test = tests.find(test_name, level, FX, request.user)

    correct = test.store_result(request) if request.method == 'POST' else False    
    answer, fxs, sound, csd = test.check(request, correct) if request.method == 'POST' else test.first()

    context['choices'] = fxs
    context['answer'] = answer 
    context['sound'] = sound
    context['csd'] = csd
    try:
        context['last_csd'] = Result.objects.filter(user = request.user).filter(correct = 1).latest('timestamp').csd
    except:
        context['last_csd'] = 'Not a single correct answer yet!?'
    context['msg'] = ''
    if request.method == 'POST':
        context['msg'] = 'Correct. Good job!' if correct else 'Oops, try again :)'
    config = {}
    execfile(md.systemfiles + '/effectsDict_edit.txt', config)
    context['effectsDict'] = config['effectsDict']
    response = render_to_response('tutor/test.html', { 'context': context }, context_instance=RequestContext(request))

    if key in request.META['HTTP_REFERER']:
        response.set_cookie('lesson_id', lesson_id)
    return response

def test_interactive(request, test_name, level, FX):

    test = tests.find(test_name, level, FX, request.user)
    #correct = test.store_result(request) if request.method == 'POST' else False  

    context = {}

    if request.method == 'GET':
        effect_set, effect_values, sound, csd = test.first()
        
        # Remove input and output keys from the dictionary. 
        # TODO: Do this in csdWriter.py instead
        for key, val in effect_set.iteritems():
            del val['input']
            del val['output']

        for key, val in effect_values.iteritems():
            del val['input']
            del val['output']

        # Get all effect names
        config = {}
        execfile(md.systemfiles + '/effectsDict_edit.txt', config)
        humanReadableEffectNames = config['effectsDict']

        # Remove ".inc" from both the keys of both effect dictionaries
        effect_keys = list(effect_set.keys())
        for effect_key in effect_keys:
            effect_set[effect_key[:-4]] = dict(effect_set.pop(effect_key))
            effect_values[effect_key[:-4]] = dict(effect_values.pop(effect_key))

        queryset = TestElement.objects.all()
        queryset.default_factory = None

        # Add a default answer value (0.0) in a touple along with the generated value 
        for effect, parameters in effect_values.iteritems():
            for parameter_name, parameter_value in parameters.iteritems():
                min_value = effect_set[effect][parameter_name][0][0]
                max_value = effect_set[effect][parameter_name][0][1]
                shape = effect_set[effect][parameter_name][1]

                effect_set[effect][parameter_name].append([parameter_value, test.getValueFromFunctionShape((max_value+min_value)*0.5, min_value, max_value, shape)])
                effect_set[effect][parameter_name].append("unevaluated")
                # Appending the effect title to each parameter. Not good...
                effect_set[effect][parameter_name].append(humanReadableEffectNames[effect + ".inc"])

        input_level = 1.0 # Default input level

        context = {
            'test_elements': queryset,
            'test_name': test_name,
            'level': level,
            'effect_set': dict(effect_set),
            'sound': sound,
            'csd': csd,
            'FX': FX,
            'input_level': input_level,
        }
    elif request.method == 'POST':
        correct, effect_set = test.store_result(request)

        if correct:
            effect_set, effect_values, sound, csd = test.first()
        
            # Remove input and output keys from the dictionary. 
            # TODO: Do this in csdWriter.py instead
            for key, val in effect_set.iteritems():
                del val['input']
                del val['output']

            for key, val in effect_values.iteritems():
                del val['input']
                del val['output']

            # Get all effect names
            config = {}
            execfile(md.systemfiles + '/effectsDict_edit.txt', config)
            humanReadableEffectNames = config['effectsDict']

            # Remove ".inc" from both the keys of both effect dictionaries
            effect_keys = list(effect_set.keys())
            for effect_key in effect_keys:
                effect_set[effect_key[:-4]] = dict(effect_set.pop(effect_key))
                effect_values[effect_key[:-4]] = dict(effect_values.pop(effect_key))

            queryset = TestElement.objects.all()
            queryset.default_factory = None

            # Add a default answer value (0.0) in a touple along with the generated value 
            for effect, parameters in effect_values.iteritems():
                for parameter_name, parameter_value in parameters.iteritems():     
                    min_value = effect_set[effect][parameter_name][0][0]
                    max_value = effect_set[effect][parameter_name][0][1]
                    shape = effect_set[effect][parameter_name][1]
    
                    effect_set[effect][parameter_name].append([parameter_value, test.getValueFromFunctionShape((max_value+min_value)*0.5, min_value, max_value, shape)])
                    effect_set[effect][parameter_name].append("unevaluated")
                    # Appending the effect title to each parameter. Not good...
                    effect_set[effect][parameter_name].append(humanReadableEffectNames[effect + ".inc"])

            msg = 'Good work!'
            input_level = 1.0 # Default input level

            context = {
                'test_elements': queryset,
                'test_name': test_name,
                'level': level,
                'effect_set': dict(effect_set),
                'sound': sound,
                'csd': csd,
                'FX': FX,
                'msg': msg,
                'input_level': input_level,
            }
            #context['last_csd'] = Result.objects.filter(user = request.user).filter(correct = 1).latest('timestamp').csd
        else:

            msg = 'One or more parameters was too far off, please try again.'

            context = {
                'test_name': test_name,
                'level': level,
                'effect_set': effect_set,
                'sound': request.POST.get("sound"),
                'csd': request.POST.get("csd"),
                'FX': FX,
                'msg': msg,
                'input_level': request.POST.get("input_level_hidden"),
            }

            print("input_level_hidden:")
            print(request.POST.get("input_level_hidden"))

            #context['last_csd'] = 'Not a single correct answer yet!?'
        
        #effect_values = validate_effect_parameters(effect_set, effect_values)

    response = render_to_response('tutor/test_interactive.html', { 'context': context }, context_instance=RequestContext(request))
    return response

def lesson_results(request):
    print '\n\n LESSON RESULTS FOR LESSON ID {} \n\n'.format(request.COOKIES['lesson_id'])
    context = {}
    results_with_feedback = []
    for task, correct, total, ratio, day_groups, everything, time_spent in Result.objects.aggregated_results(request.user, request.COOKIES['lesson_id']):
        test_element = TestElement.objects.filter(test = task).latest('pk')
        feedback = test_element.feedback_bad
        if ratio > 40:
            feedback = test_element.feecback_ok
        if ratio > 80:
            feedback = test_element.feecback_good
        results_with_feedback.append((task, correct, total, ratio, day_groups, everything, time_spent, feedback))

    context['results'] = results_with_feedback
    return render_to_response('tutor/results.html', { 'context': context }, context_instance=RequestContext(request))

def results(request):
    context = {}
    context['results'] = Result.objects.aggregated_results(request.user)
    return render_to_response('tutor/results.html', { 'context': context }, context_instance=RequestContext(request))
